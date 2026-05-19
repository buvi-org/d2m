"""AI Agentic CadQuery -> subCAD Translator.

Uses an LLM (DeepSeek, Anthropic, or OpenAI) in an agentic loop with the
subCAD REPL to translate CadQuery constructive programs into subCAD
subtractive programs. The loop:

1. Prompts the LLM with CadQuery code + ops trace + STEP bbox + subCAD API docs
2. Executes generated subCAD code in the REPL
3. Compares output volume to reference STEP
4. Feeds results back to LLM for refinement (up to N attempts)
5. Saves validated translation pairs for training
"""

from __future__ import annotations

import json
import os
import re
import sys
import textwrap
import time
from pathlib import Path
from typing import Optional

import trimesh

from .subcad_repl import run_subcad, compare_to_reference, format_feedback
from .cadquery_to_subcad import (
    reconstruct_chains,
    classify_chain,
    step_to_stock_dims,
    _extract_measures,
)

# Optional imports for richer mesh comparison (requires trimesh + scipy)
try:
    from ..simulation.mesh_compare import compare_meshes, generate_error_feedback
    _HAS_MESH_COMPARE = True
except ImportError:
    compare_meshes = None
    generate_error_feedback = None
    _HAS_MESH_COMPARE = False

try:
    from ..simulation.feature_compare import compare_with_features, generate_feature_feedback
    _HAS_FEATURE_COMPARE = True
except ImportError:
    compare_with_features = None
    generate_feature_feedback = None
    _HAS_FEATURE_COMPARE = False


# =========================================================================
#  SubCAD API reference (embedded in the system prompt)
# =========================================================================

SUBCAD_API_REFERENCE = textwrap.dedent("""\
## SubCAD API Reference

SubCAD is a subtractive CAD library. You start with a rectangular stock block
and cut material away using machining operations. Each method returns a new
Stock instance (immutable/fluent pattern).

### Factory Constructors

- `Stock.rectangular(length, width, height, material="aluminum_6061")`
  Creates rectangular prismatic stock. length=X, width=Y, height=Z.

### Machining Operations (each returns new Stock)

- `.face_mill(depth=1.0)` — Face mill the top surface, removing *depth* mm.

- `.pocket(width, length, depth, *, corner_radius=0.0, cx=0.0, cy=0.0)`
  Cut a rectangular pocket. (cx, cy) is center on the top face.

- `.circular_pocket(diameter, depth, *, cx=0.0, cy=0.0)`
  Cut a circular pocket/bore.

- `.drill(diameter, depth=0.0, *, cx=0.0, cy=0.0, through=False)`
  Drill a hole at (cx, cy). Set through=True to drill through entire part.

- `.chamfer(width=0.5)` — Chamfer top edges by *width* mm.

- `.slot(length, width, depth=5.0, *, angle=0.0, cx=0.0, cy=0.0, through=False)`
  Cut a straight slot (obround).

- `.contour(depth, *, stepdown=None)` — Profile/contour milling around outer boundary.

- `.tap(diameter, thread_pitch=0.0, *, depth=10.0, cx=0.0, cy=0.0)`
  Tap a pre-drilled hole. Geometry unchanged (thread form too fine for B-Rep).

- `.threaded_hole(diameter, depth=0.0, *, cx=0.0, cy=0.0, through=False)`
  Convenience: spot-drill + drill + tap in one call.

### Export / Inspection

- `part.to_step(path)` — Export STEP file.
- `part.to_mesh()` — Get trimesh mesh (for volume, faces).
- `part.process_plan()` — Get manufacturing process plan dict.

### Translation Rules

1. CadQuery builds UP (extrude, union) — SubCAD cuts DOWN from stock.
2. Use stock dimensions = final part XY dimensions (length, width). Do NOT add
   margin — the stock should match the outer XY envelope of the final part.
   Only add margin to Z (height): use the measures height + 2-3 mm.
3. face_mill first to achieve the final Z-height from the stock.
4. Pockets replace CadQuery cut/cutBlind operations.
5. Holes (cboreHole, cskHole) become drill operations with cx, cy from the
   CadQuery source.  Drill through=True for through-holes.
6. Chamfers map to .chamfer(width).  Fillet has no subCAD equivalent — skip it.
7. CadQuery "union" (adding a boss) is achieved by NOT cutting that volume away
   from the stock.
8. DO NOT use .contour() — it is unreliable.
9. Coordinate system: (cx=0, cy=0) is the FACE CENTER (CadQuery convention).
   Positive cx = right (+X), positive cy = up (+Y).  Negative values go
   left/down from center.  For a 70 x 40 mm face, the bottom-left corner
   is at (cx=-35, cy=-20), the top-right at (cx=35, cy=20).
   For example: to center a pocket on a 70x40 face, use cx=0, cy=0.
   To put a hole at the face center, use cx=0, cy=0.
10. The code MUST assign the final Stock to a variable named `part`.
11. Do NOT write any import statements. `Stock` is already imported.
12. Do NOT call .face_mill(depth=0) — if the stock is already at the right
    height, just skip face_mill entirely.
""")

# Shorter reference for iteration prompts (the LLM already saw the full one)
SUBCAD_API_SHORT = textwrap.dedent("""\
## SubCAD API (abbreviated)

Stock.rectangular(L, W, H, material="aluminum_6061")
.face_mill(depth)           # mill top face
.pocket(W, L, depth, cx, cy)  # rectangular pocket
.circular_pocket(dia, depth, cx, cy)
.drill(dia, depth, cx, cy, through=False)
.chamfer(width)
.slot(L, W, depth, angle, cx, cy, through=False)
.contour(depth)
.tap(dia, pitch, depth, cx, cy)
.threaded_hole(dia, depth, cx, cy, through)

Assign final Stock to variable named `part`.
""")


# =========================================================================
#  Prompt builders
# =========================================================================

def _extract_measures_block(cq_code: str) -> str:
    """Extract the Measures class/code from CadQuery source for reuse in subCAD.

    Looks for a block starting with `m = Measures(` or `m = SimpleNamespace(`.
    Returns the block as a Python code string, or a minimal measures dict.
    """
    import re

    # Try to find the CadQuery measures pattern: m = Measures(...)
    # Match from 'm = Measures(' or similar to the closing ')' that starts a line
    patterns = [
        r"(m\s*=\s*(?:Measures|type\([^)]+\)\([^)]*\))\s*\(.*?^\s*\))",
        r"(m\s*=\s*SimpleNamespace\s*\(.*?^\s*\))",
    ]

    # Also extract the import: from types import SimpleNamespace as Measures
    import_line = ""
    import_match = re.search(
        r"from\s+types\s+import\s+SimpleNamespace\s+as\s+Measures",
        cq_code,
    )
    if import_match:
        import_line = import_match.group(0)

    for pat in patterns:
        match = re.search(pat, cq_code, re.MULTILINE | re.DOTALL)
        if match:
            block = match.group(1).strip()
            if import_line:
                block = import_line + "\n" + block
            return block

    # Fallback: return just the first few lines that define measures
    lines = cq_code.split("\n")
    measure_lines = []
    in_measures = False
    for line in lines:
        if "Measures(" in line or "SimpleNamespace" in line or "= Measures" in line:
            in_measures = True
        if in_measures:
            measure_lines.append(line)
            if line.rstrip().endswith(")") and not line.rstrip().endswith("()"):
                break
    if measure_lines:
        return "\n".join(measure_lines)

    # Last resort
    return "# No measures found in source — define your own parameters"


def build_system_prompt() -> str:
    """Build the system prompt with subCAD API reference."""
    return f"""You are an expert CAD/CAM translator. Your job is to convert CadQuery
(constructive CAD) programs into equivalent subCAD (subtractive CAD) programs.

{SUBCAD_API_REFERENCE}

Always respond with valid Python code inside a markdown code fence.
The code must assign the final Stock to a variable named `part`.
IMPORTANT: `Stock` is already imported in the execution environment — do NOT
write `from subcad import Stock` or `from src.subcad import Stock`.
Just use `Stock.rectangular(...)` directly."""


def build_user_prompt(
    cq_code: str,
    ops_trace: list[dict],
    step_path: str,
    stock_dims: dict,
) -> str:
    """Build the user prompt with CadQuery sample data.

    Args:
        cq_code: Original CadQuery Python source code.
        ops_trace: The CadQuery ops trace (list of flattened call records).
        step_path: Path to the reference STEP file.
        stock_dims: dict with length, width, height from STEP bbox.
    """
    # Reconstruct chains for readable summary
    chains = reconstruct_chains(ops_trace)
    chain_summary = []
    for c in chains:
        cls = classify_chain(c)
        chain_summary.append(
            f"  line {c['lineno']}: [{cls}] {c['function_path']}"
        )

    # Load reference mesh for volume info
    try:
        ref_mesh = trimesh.load(step_path)
        ref_vol = round(float(ref_mesh.volume), 1) if ref_mesh else 0.0
    except Exception:
        ref_vol = 0.0

    # Extract measures for the LLM to reference
    measures = _extract_measures(ops_trace)

    # Extract the Measures block from the CadQuery source for reuse
    measures_block = _extract_measures_block(cq_code)

    prompt = f"""## Task

Translate the following CadQuery program into a subCAD subtractive program.

## Reference Geometry
- STEP volume: {ref_vol} mm^3
- Stock dimensions (final part XY + small Z margin): {stock_dims['length']:.0f} x {stock_dims['width']:.0f} x {stock_dims['height']:.0f} mm

## Measures (named parameters — COPY-PASTE into subCAD code)
```python
{measures_block}
```

Use `m.width`, `m.depth`, `m.height`, `m.wall_thickness`, etc. in your
subCAD code instead of hardcoding values.

## CadQuery Source Code
```python
{cq_code}
```

## Operations Trace (reconstructed chains)
{chr(10).join(chain_summary)}

## Instructions

Translate this constructive CadQuery program into an equivalent subCAD
subtractive program. Remember:
- Stock XY = final part XY (use {stock_dims['length']:.0f} x {stock_dims['width']:.0f}).
  Only add extra Z height for face_mill.
- Cut AWAY material to reveal the final shape.
- The target volume is approximately {ref_vol} mm^3.
- Assign the final Stock to a variable named `part`.
- Copy the Measures block above and use m.width, m.depth, etc.

Respond with ONLY the subCAD Python code inside a markdown code fence."""
    return prompt


def build_iteration_prompt(
    previous_code: str,
    exec_result: dict,
    comparison: dict,
    target_volume: float,
    mesh_comparison: dict | None = None,
    feature_comparison: dict | None = None,
) -> str:
    """Build a feedback prompt for iterative refinement.

    Args:
        previous_code: The subCAD code that was just executed.
        exec_result: Result dict from run_subcad().
        comparison: Result dict from compare_to_reference().
        target_volume: The reference STEP volume to match.
        mesh_comparison: Optional result from compare_meshes() with SDF and/or
            Z-slice analysis. Includes localized deviation feedback.
        feature_comparison: Optional result from compare_with_features() with
            per-feature comparison data. Requires ops trace.
    """
    feedback = format_feedback(previous_code, exec_result, comparison)

    vol_ratio = comparison.get("volume_ratio", 0)
    direction = "too small" if vol_ratio < 1.0 else "too large"

    # Build the base prompt
    parts = [f"""## Previous Attempt Feedback

{feedback}

The subCAD volume is {direction} (volume ratio: {vol_ratio:.3f}).
Target volume: {target_volume:.1f} mm^3."""]

    # --- Include localized mesh deviation feedback ---
    if mesh_comparison and mesh_comparison.get("feedback"):
        parts.append("")
        parts.append("## Localized Shape Deviation")
        parts.append("The following analysis identifies *where* the candidate "
                     "shape deviates from the reference. Use this to fix "
                     "specific dimensions (depths, widths, positions).")
        score = mesh_comparison.get("score")
        if score is not None:
            parts.append(f"Mesh quality score: {score:.0f}/100")
        parts.append("")
        parts.append(mesh_comparison["feedback"])

    # --- Include per-feature comparison feedback ---
    if feature_comparison and feature_comparison.get("feedback"):
        parts.append("")
        parts.append("## Per-Feature Comparison")
        parts.append("The following compares individual features (pockets, holes, "
                     "chamfers) between the reference and candidate. Features "
                     "listed as MISSING, WRONG SIZE, or SHIFTED should be fixed.")
        fscore = feature_comparison.get("score")
        if fscore is not None:
            parts.append(f"Feature quality score: {fscore:.0f}/100")
        parts.append("")
        parts.append(feature_comparison["feedback"])

    # --- API reference and previous code ---
    parts.append(f"""
{SUBCAD_API_SHORT}

## Previous Code
```python
{previous_code}
```

## Instructions

Fix the subCAD code so the output volume better matches the target of
{target_volume:.1f} mm^3. Adjust stock dimensions, operation depths, or
operation parameters as needed.

Respond with ONLY the corrected subCAD Python code inside a markdown code fence.""")

    return "\n".join(parts)


# =========================================================================
#  Code extraction
# =========================================================================

def extract_code(response: str) -> Optional[str]:
    """Extract Python code from an LLM response.

    Handles:
      - ```python ... ``` fences
      - ``` ... ``` fences (no language tag)
      - Bare code (no fences)
    """
    # Try fenced code first
    fence_pat = re.compile(r"```(?:python)?\s*\n(.*?)\n\s*```", re.DOTALL)
    match = fence_pat.search(response)
    if match:
        return match.group(1).strip()

    # Try any code fence
    any_fence = re.compile(r"```\s*\n(.*?)\n\s*```", re.DOTALL)
    match = any_fence.search(response)
    if match:
        return match.group(1).strip()

    # Fallback: look for code patterns
    if "Stock.rectangular" in response or "from src.subcad" in response:
        # Try to extract everything between import and part assignment
        lines = response.split("\n")
        code_lines = []
        in_code = False
        for line in lines:
            if "from src.subcad" in line or "Stock.rectangular" in line:
                in_code = True
            if in_code:
                code_lines.append(line)
            if in_code and ")" == line.strip() and len(code_lines) > 3:
                # Heuristic: standalone ) on its own line = end of chain
                break
        if code_lines:
            return "\n".join(code_lines)

    return None


# =========================================================================
#  LLM client abstraction
# =========================================================================

class LLMClient:
    """Unified LLM client supporting DeepSeek, Anthropic, and OpenAI."""

    def __init__(
        self,
        provider: str = "deepseek",
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ):
        self.provider = provider.lower()

        if self.provider == "deepseek":
            self.model = model or "deepseek-v4-flash"
            resolved_key = api_key or os.environ.get("DEEPSEEK_API_KEY")
            if not resolved_key:
                raise ValueError(
                    "DeepSeek API key not found. Set DEEPSEEK_API_KEY env var."
                )
            from openai import OpenAI
            self._client = OpenAI(
                api_key=resolved_key,
                base_url=base_url or "https://api.deepseek.com",
            )
            self._is_anthropic = False
            self._is_openai_compat = True

        elif self.provider == "openai":
            self.model = model or "gpt-4o"
            resolved_key = api_key or os.environ.get("OPENAI_API_KEY")
            if not resolved_key:
                raise ValueError(
                    "OpenAI API key not found. Set OPENAI_API_KEY env var."
                )
            from openai import OpenAI
            self._client = OpenAI(api_key=resolved_key)
            self._is_anthropic = False
            self._is_openai_compat = True

        elif self.provider == "anthropic":
            self.model = model or "claude-sonnet-4-6"
            resolved_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
            if not resolved_key:
                raise ValueError(
                    "Anthropic API key not found. Set ANTHROPIC_API_KEY env var."
                )
            import anthropic
            self._client = anthropic.Anthropic(api_key=resolved_key)
            self._is_anthropic = True
            self._is_openai_compat = False

        else:
            raise ValueError(f"Unknown provider: {provider}. "
                             "Use 'deepseek', 'openai', or 'anthropic'.")

    def chat(
        self,
        messages: list[dict],
        temperature: float = 0.2,
        max_tokens: int = 4096,
    ) -> str:
        """Send a chat completion request and return the response text."""
        if self._is_anthropic:
            system = None
            user_messages = []
            for m in messages:
                if m["role"] == "system":
                    system = m["content"]
                else:
                    user_messages.append(m)
            resp = self._client.messages.create(
                model=self.model,
                system=system or "",
                messages=user_messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return resp.content[0].text
        else:
            resp = self._client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return resp.choices[0].message.content


# =========================================================================
#  Convergence controller
# =========================================================================

class ConvergenceController:
    """Decides whether to continue iterating based on convergence toward target.

    Instead of a fixed attempt cap, this tracks the volume ratio across
    attempts and stops when:

    - **Success**: |ratio - 1.0| < tolerance (e.g., within 5%)
    - **Converging**: error is shrinking over the recent window -> continue
    - **Stagnant**: no improvement for *stagnation_limit* attempts -> stop
    - **Diverging**: error is growing away from target -> stop
    - **Execution failing**: too many consecutive execution errors -> stop
    - **Safety cap**: absolute maximum reached -> stop

    Attributes:
        tolerance: Relative volume error that counts as "success" (default 0.05 = 5%).
        window: Number of recent attempts to check for convergence (default 3).
        stagnation_limit: Consecutive non-improving attempts before stopping (default 3).
        divergence_limit: Consecutive worsening attempts before stopping (default 2).
        max_consecutive_errors: Stop if this many attempts fail to execute (default 3).
        safety_cap: Absolute maximum attempts regardless of trend (default 20).
    """

    def __init__(
        self,
        tolerance: float = 0.05,
        window: int = 3,
        stagnation_limit: int = 3,
        divergence_limit: int = 2,
        max_consecutive_errors: int = 3,
        safety_cap: int = 20,
    ):
        self.tolerance = tolerance
        self.window = window
        self.stagnation_limit = stagnation_limit
        self.divergence_limit = divergence_limit
        self.max_consecutive_errors = max_consecutive_errors
        self.safety_cap = safety_cap

        self._ratios: list[float] = []
        self._errors_required: list[float] = []  # |ratio - 1.0|
        self._consecutive_errors = 0
        self._best_error = float("inf")
        self._best_ratio = 0.0
        self._non_improving = 0
        self._diverging = 0

    def record(self, volume_ratio: float, exec_success: bool) -> str:
        """Record an attempt result. Returns the decision as a string.

        Returns one of: "continue", "success", "stagnant", "diverging",
        "execution_failing", "safety_cap".
        """
        self._ratios.append(volume_ratio)

        if not exec_success:
            self._consecutive_errors += 1
        else:
            self._consecutive_errors = 0

        # Compute error = distance from perfect 1.0 ratio
        error = abs(volume_ratio - 1.0) if volume_ratio > 0 else float("inf")
        self._errors_required.append(error)

        # --- Success check ---
        if error < self.tolerance and volume_ratio > 0:
            return "success"

        # --- Execution failure check ---
        if self._consecutive_errors >= self.max_consecutive_errors:
            return "execution_failing"

        # --- Safety cap ---
        if len(self._ratios) >= self.safety_cap:
            return "safety_cap"

        # --- Not enough data yet, keep going ---
        if len(self._ratios) < 2:
            return "continue"

        # --- Track improvement ---
        if error < self._best_error - 0.001:  # small threshold to avoid float noise
            self._best_error = error
            self._best_ratio = volume_ratio
            self._non_improving = 0
            self._diverging = 0
        else:
            self._non_improving += 1

        # --- Track divergence (error getting worse) ---
        if len(self._errors_required) >= 2:
            prev = self._errors_required[-2]
            if error > prev + 0.001:
                self._diverging += 1
            else:
                self._diverging = 0

        # --- Stagnation check ---
        if self._non_improving >= self.stagnation_limit:
            return "stagnant"

        # --- Divergence check ---
        if self._diverging >= self.divergence_limit:
            return "diverging"

        return "continue"

    @property
    def summary(self) -> str:
        n = len(self._ratios)
        if n == 0:
            return "no attempts"
        last = self._ratios[-1]
        best = self._best_ratio if self._best_error < float("inf") else last
        return (f"{n} attempts, last_ratio={last:.4f}, best_ratio={best:.4f}, "
                f"best_error={self._best_error:.4f}")

    @property
    def attempt_count(self) -> int:
        return len(self._ratios)


# =========================================================================
#  Agentic Translator
# =========================================================================

class AgenticTranslator:
    """Translates CadQuery programs to subCAD using an LLM + REPL feedback loop.

    Uses convergence-based stopping: keeps iterating as long as the volume
    ratio is improving toward 1.0, stops when progress stagnates or diverges.

    Usage::

        translator = AgenticTranslator(provider="deepseek")
        result = translator.translate(sample, step_path="model.step")
        if result["success"]:
            print(result["subcad_code"])
    """

    def __init__(
        self,
        provider: str = "deepseek",
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        tolerance: float = 0.05,
        stagnation_limit: int = 3,
        divergence_limit: int = 2,
        safety_cap: int = 20,
        verbose: bool = True,
        comparison_methods: Optional[list[str]] = None,  # sentinel, default set below
        feature_aware: bool = False,
    ):
        """Initialize the translator.

        Args:
            provider: LLM provider - "deepseek", "anthropic", or "openai".
            model: Model name. Uses provider default if None.
            api_key: API key. Reads from env var if None.
            base_url: API base URL override.
            tolerance: Volume ratio error that counts as success (0.05 = 5%).
            stagnation_limit: Non-improving attempts before giving up.
            divergence_limit: Worsening attempts before giving up.
            safety_cap: Absolute max attempts regardless of trend.
            verbose: Print progress to stdout.
            comparison_methods: Mesh comparison methods (default ["sdf", "slice"]).
                Pass None to disable. Requires trimesh + scipy.
            feature_aware: If True, run per-feature comparison (requires ops trace,
                slower). Default False.
        """
        self.llm = LLMClient(
            provider=provider,
            model=model,
            api_key=api_key,
            base_url=base_url,
        )
        self.tolerance = tolerance
        self.stagnation_limit = stagnation_limit
        self.divergence_limit = divergence_limit
        self.safety_cap = safety_cap
        self.verbose = verbose
        self.comparison_methods = comparison_methods if comparison_methods is not None else ["sdf", "slice"]
        self.feature_aware = feature_aware
        self._system_prompt = build_system_prompt()

    def translate(
        self,
        sample: dict,
        step_path: Optional[str] = None,
        tolerance: Optional[float] = None,
    ) -> dict:
        """Translate a single CadQuery sample to subCAD.

        Uses convergence-based iteration: keeps going while the volume ratio
        improves toward 1.0, stops when progress stagnates or diverges.

        Args:
            sample: Dict with keys:
                - cadquery_file (str): CadQuery source code
                - cadquery_ops_json (str): JSON-serialized ops trace
                - step_file (bytes): Reference STEP file bytes
            step_path: Path to a local STEP file (used instead of step_file if set).
            tolerance: Per-translation tolerance override.

        Returns:
            dict with keys:
                success: bool
                subcad_code: str (final generated code)
                attempts: int (number of LLM calls made)
                exec_result: dict (from final run_subcad)
                comparison: dict (from final compare_to_reference)
                history: list[dict] (all attempt results)
                stop_reason: str (why iteration stopped)
                error: str (if fatal error)
        """
        conv = ConvergenceController(
            tolerance=tolerance or self.tolerance,
            stagnation_limit=self.stagnation_limit,
            divergence_limit=self.divergence_limit,
            safety_cap=self.safety_cap,
        )

        # --- Unpack sample ---
        cq_code = sample.get("cadquery_file", "")
        if isinstance(cq_code, bytes):
            cq_code = cq_code.decode("utf-8")

        ops_json = sample.get("cadquery_ops_json", "[]")
        if isinstance(ops_json, str):
            ops_trace = json.loads(ops_json)
        else:
            ops_trace = ops_json

        # --- Get reference STEP path ---
        if step_path is None:
            import tempfile
            step_bytes = sample.get("step_file", b"")
            if isinstance(step_bytes, str):
                step_bytes = step_bytes.encode("utf-8")
            with tempfile.NamedTemporaryFile(suffix=".step", delete=False) as tf:
                tf.write(step_bytes)
            step_path = tf.name

        # --- Determine stock dimensions from STEP ---
        with open(step_path, "rb") as f:
            step_bytes = f.read()
        stock_dims = step_to_stock_dims(step_bytes)

        # --- Load reference volume (try CadQuery first, fallback to trimesh) ---
        target_volume = 0.0
        try:
            from src.subcad.geometry import import_step
            ref_shape = import_step(step_path)
            target_volume = round(float(ref_shape.val().Volume()), 1)
        except Exception:
            try:
                ref_mesh = trimesh.load(step_path)
                target_volume = round(float(ref_mesh.volume), 1) if ref_mesh else 0.0
            except Exception:
                target_volume = 0.0

        # --- Build initial user prompt ---
        user_prompt = build_user_prompt(cq_code, ops_trace, step_path, stock_dims)

        messages = [
            {"role": "system", "content": self._system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        history = []
        final_code = None
        final_exec = None
        final_comparison = None
        final_mesh_comparison = None
        final_feature_comparison = None
        stop_reason = "not_started"

        attempt = 0
        while True:
            attempt += 1

            # --- Check convergence before calling LLM ---
            if attempt > 1:
                vol_ratio = final_comparison.get("volume_ratio", 0) if final_comparison else 0
                exec_ok = final_exec.get("success", False) if final_exec else False
                decision = conv.record(vol_ratio, exec_ok)

                if decision != "continue":
                    stop_reason = decision
                    if self.verbose:
                        print(f"\n  Stop: {decision} ({conv.summary})")
                    break

            if self.verbose:
                print(f"  [attempt {attempt}] Calling LLM...", end=" ", flush=True)

            # --- Call LLM ---
            try:
                response = self.llm.chat(messages)
            except Exception as e:
                if self.verbose:
                    print(f"LLM error: {e}")
                return {
                    "success": False,
                    "subcad_code": None,
                    "attempts": attempt,
                    "exec_result": None,
                    "comparison": None,
                    "mesh_comparison": None,
                    "feature_comparison": None,
                    "history": history,
                    "stop_reason": f"LLM API error: {e}",
                    "error": f"LLM API error: {e}",
                }

            # --- Extract code ---
            code = extract_code(response)
            if code is None:
                if self.verbose:
                    print("no code extracted from response")
                messages.append({"role": "assistant", "content": response})
                messages.append({
                    "role": "user",
                    "content": "No code found in your response. "
                    "Please output ONLY the subCAD Python code inside a "
                    "```python ... ``` code fence."
                })
                history.append({
                    "attempt": attempt,
                    "code": None,
                    "exec_result": None,
                    "comparison": None,
                    "mesh_comparison": None,
                    "feature_comparison": None,
                    "error": "No code extracted from LLM response",
                })
                # Record a failed attempt for convergence tracking
                conv.record(0.0, False)
                continue

            if self.verbose:
                print(f"{len(code)} chars", end=" ", flush=True)

            # --- Execute in REPL ---
            exec_result = run_subcad(code)

            if self.verbose:
                if exec_result["success"]:
                    print(f"vol={exec_result['volume']:.1f}", end=" ", flush=True)
                else:
                    print(f"ERROR: {exec_result.get('error', '?')[:80]}", end=" ", flush=True)

            # --- Compare to reference ---
            if exec_result["success"] and exec_result.get("step_path"):
                comparison = compare_to_reference(
                    exec_result["step_path"], step_path
                )
            else:
                comparison = {"match": False, "volume_ratio": 0.0,
                              "error": "Execution failed"}

            if self.verbose:
                if comparison.get("match"):
                    print("MATCH!")
                else:
                    print(f"ratio={comparison.get('volume_ratio', 0):.3f}")

            # --- Richer mesh comparison (SDF + Z-slice) ---
            mesh_comparison = None
            feature_comparison = None

            if (exec_result["success"]
                    and self.comparison_methods
                    and _HAS_MESH_COMPARE):
                # Get candidate mesh (prefer STL for trimesh compatibility)
                cand_mesh = None
                cand_mesh_path = (exec_result.get("stl_path")
                                  or exec_result.get("step_path"))
                if cand_mesh_path:
                    try:
                        cand_mesh = trimesh.load(cand_mesh_path)
                    except Exception:
                        cand_mesh = None

                # Load reference mesh (use CadQuery for STEP, cascadio unavailable)
                ref_mesh = None
                try:
                    ref_mesh = trimesh.load(step_path)
                except Exception:
                    try:
                        import cadquery as cq
                        shape = cq.importers.importStep(step_path).val()
                        verts, faces = shape.tessellate(0.1)
                        ref_mesh = trimesh.Trimesh(
                            vertices=[(v.x, v.y, v.z) for v in verts],
                            faces=faces,
                        )
                    except Exception:
                        ref_mesh = None

                # Run mesh comparison (SDF + slice)
                if ref_mesh is not None and cand_mesh is not None:
                    try:
                        mesh_comparison = compare_meshes(
                            ref_mesh, cand_mesh,
                            methods=self.comparison_methods,
                        )
                        if self.verbose and mesh_comparison.get("score") is not None:
                            print(f"mesh_qual={mesh_comparison['score']:.0f}",
                                  end=" ", flush=True)
                    except Exception:
                        mesh_comparison = None

                # Run feature-aware comparison (expensive, opt-in)
                if (self.feature_aware and _HAS_FEATURE_COMPARE
                        and cand_mesh is not None):
                    try:
                        feature_comparison = compare_with_features(
                            step_path, cand_mesh, ops_trace,
                        )
                        if (self.verbose
                                and feature_comparison.get("score") is not None):
                            print(f"feat_qual={feature_comparison['score']:.0f}",
                                  end=" ", flush=True)
                    except Exception:
                        feature_comparison = None

            # --- Record history ---
            history.append({
                "attempt": attempt,
                "code": code,
                "exec_result": exec_result,
                "comparison": comparison,
                "mesh_comparison": mesh_comparison,
                "feature_comparison": feature_comparison,
            })

            final_code = code
            final_exec = exec_result
            final_comparison = comparison
            final_mesh_comparison = mesh_comparison
            final_feature_comparison = feature_comparison

            # --- Convergence check (triggers at top of next iteration) ---
            vol_ratio = comparison.get("volume_ratio", 0)
            exec_ok = exec_result.get("success", False)
            decision = conv.record(vol_ratio, exec_ok)

            if decision != "continue":
                stop_reason = decision
                if self.verbose:
                    print(f"  Stop: {decision} ({conv.summary})")
                break

            # --- Build iteration prompt for refinement ---
            iteration_prompt = build_iteration_prompt(
                code, exec_result, comparison, target_volume,
                mesh_comparison=mesh_comparison,
                feature_comparison=feature_comparison,
            )
            messages.append({"role": "assistant", "content": response})
            messages.append({"role": "user", "content": iteration_prompt})

        return {
            "success": final_comparison.get("match", False) if final_comparison else False,
            "subcad_code": final_code,
            "attempts": len(history),
            "exec_result": final_exec,
            "comparison": final_comparison,
            "mesh_comparison": final_mesh_comparison,
            "feature_comparison": final_feature_comparison,
            "history": history,
            "stop_reason": stop_reason,
            "error": None,
        }


# =========================================================================
#  Batch translation
# =========================================================================

def translate_batch(
    samples: list[dict],
    step_dir: Optional[str] = None,
    provider: str = "deepseek",
    model: Optional[str] = None,
    tolerance: float = 0.05,
    stagnation_limit: int = 3,
    safety_cap: int = 20,
    output_dir: Optional[str] = None,
    verbose: bool = True,
) -> list[dict]:
    """Translate a batch of samples.

    Args:
        samples: List of sample dicts, each with cadquery_file, cadquery_ops_json,
                 and optionally step_file. If step_file is absent, step_dir is used.
        step_dir: Directory containing model.step files (keyed by uuid or index).
        provider: LLM provider.
        model: Model override.
        tolerance: Volume ratio error that counts as success (0.05 = 5%).
        stagnation_limit: Non-improving attempts before giving up.
        safety_cap: Absolute max attempts per sample.
        output_dir: If set, save subCAD code and result JSON per sample.
        verbose: Print progress.

    Returns:
        List of result dicts (one per sample).
    """
    translator = AgenticTranslator(
        provider=provider,
        model=model,
        tolerance=tolerance,
        stagnation_limit=stagnation_limit,
        safety_cap=safety_cap,
        verbose=verbose,
    )

    results = []
    for i, sample in enumerate(samples):
        uid = sample.get("uuid", f"sample_{i}")
        if isinstance(uid, bytes):
            uid = uid.decode("utf-8")
        uid_short = uid[:16] if isinstance(uid, str) else str(uid)[:16]

        if verbose:
            print(f"\n[{i+1}/{len(samples)}] Translating {uid_short}...")

        # Resolve STEP path
        step_path = None
        if step_dir:
            candidate = os.path.join(step_dir, f"{uid_short}", "model.step")
            if os.path.exists(candidate):
                step_path = candidate
            else:
                candidate = os.path.join(step_dir, f"{i:04d}", "model.step")
                if os.path.exists(candidate):
                    step_path = candidate
            if step_path is None:
                # Try direct model.step in step_dir
                direct = os.path.join(step_dir, "model.step")
                if os.path.exists(direct):
                    step_path = direct

        try:
            result = translator.translate(
                sample,
                step_path=step_path,
            )
            result["uuid"] = uid_short
            results.append(result)

            status = "MATCH" if result["success"] else "MISMATCH"
            if result.get("error"):
                status = f"ERROR: {result['error'][:60]}"
            if verbose:
                print(f"  {status} ({result['attempts']} attempts)")

        except Exception as e:
            if verbose:
                print(f"  FATAL: {e}")
            results.append({
                "uuid": uid_short,
                "success": False,
                "subcad_code": None,
                "attempts": 0,
                "exec_result": None,
                "comparison": None,
                "history": [],
                "error": str(e),
            })

        # Save if requested
        if output_dir and results[-1].get("subcad_code"):
            os.makedirs(output_dir, exist_ok=True)
            code_path = os.path.join(
                output_dir, f"{i:04d}_{uid_short}_subcad.py"
            )
            with open(code_path, "w", encoding="utf-8") as f:
                f.write(results[-1]["subcad_code"])
            result_path = os.path.join(
                output_dir, f"{i:04d}_{uid_short}_result.json"
            )
            with open(result_path, "w", encoding="utf-8") as f:
                json.dump({
                    "uuid": uid_short,
                    "subcad_code": results[-1]["subcad_code"],
                    "attempts": results[-1]["attempts"],
                    "success": results[-1]["success"],
                    "comparison": results[-1].get("comparison"),
                }, f, indent=2, default=str)

    return results


# =========================================================================
#  Convenience: translate from exploration directory
# =========================================================================

def translate_exploration_sample(
    sample_dir: str,
    provider: str = "deepseek",
    model: Optional[str] = None,
    tolerance: float = 0.05,
    stagnation_limit: int = 3,
    safety_cap: int = 20,
    verbose: bool = True,
) -> dict:
    """Translate a single exploration sample directory.

    Uses convergence-based iteration — keeps going while the volume ratio
    is improving, stops when progress stagnates or diverges.

    Args:
        sample_dir: Path to directory containing cadquery_code.py,
                    ops_trace.json, and model.step.
        provider: LLM provider.
        model: Model override.
        tolerance: Volume ratio error that counts as success (0.05 = 5%).
        stagnation_limit: Non-improving attempts before giving up.
        safety_cap: Absolute max attempts.
        verbose: Print progress.

    Returns:
        Result dict from AgenticTranslator.translate().
    """
    cq_path = os.path.join(sample_dir, "cadquery_code.py")
    ops_path = os.path.join(sample_dir, "ops_trace.json")
    step_path = os.path.join(sample_dir, "model.step")

    if not os.path.exists(cq_path):
        raise FileNotFoundError(f"Missing cadquery_code.py in {sample_dir}")
    if not os.path.exists(ops_path):
        raise FileNotFoundError(f"Missing ops_trace.json in {sample_dir}")
    if not os.path.exists(step_path):
        raise FileNotFoundError(f"Missing model.step in {sample_dir}")

    with open(cq_path, "r", encoding="utf-8") as f:
        cq_code = f.read()
    with open(ops_path, "r", encoding="utf-8") as f:
        ops_trace = json.load(f)

    sample = {
        "cadquery_file": cq_code,
        "cadquery_ops_json": json.dumps(ops_trace),
        "uuid": os.path.basename(sample_dir.rstrip("/\\")),
    }

    translator = AgenticTranslator(
        provider=provider,
        model=model,
        tolerance=tolerance,
        stagnation_limit=stagnation_limit,
        safety_cap=safety_cap,
        verbose=verbose,
    )
    return translator.translate(sample, step_path=step_path)
