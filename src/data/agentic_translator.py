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
import math
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
from .pure_subcad_planner import plan_pure_subcad_features

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
- `Stock.cylindrical(diameter, height, material="aluminum_6061")`
  Creates round-bar/cylindrical stock. Use this when the final outer envelope
  is made from CadQuery `.cylinder(...)`, circle extrusion, round disk, washer,
  sleeve, flange, or other axisymmetric blank.

### Machining Operations (each returns new Stock)

- `.face_mill(depth=1.0)` — Face mill the top surface, removing *depth* mm.

- `.pocket(width, length, depth, *, corner_radius=0.0, cx=0.0, cy=0.0, base_height=None, face_selector=">Z")`
  Cut a rectangular pocket. IMPORTANT: width is the Y dimension and length
  is the X dimension. (cx, cy) is center on the selected setup face.

- `.circular_pocket(diameter, depth, *, cx=0.0, cy=0.0, face_selector=">Z")`
  Cut a circular pocket/bore.

- `.drill(diameter, depth=0.0, *, cx=0.0, cy=0.0, through=False, face_selector=">Z")`
  Drill a hole at (cx, cy). Set through=True to drill through entire part.

- `.chamfer(width=0.5)` — Chamfer top edges by *width* mm.
- `.edge_chamfer(selector, width, *, angle=45.0)` — Chamfer selected edges.
  Use selector `"all_edges"` for unqualified CadQuery `.edges().chamfer(...)`.
  Use selector `">Z"` only when CadQuery explicitly selects top-face edges.
  Preserve directional CadQuery selectors such as `"|Z"` for vertical edges.
- `.edge_fillet(selector, radius)` — Machine selected edge radii with ball/bull-nose finishing.

- `.slot(length, width, depth=5.0, *, angle=0.0, cx=0.0, cy=0.0, through=False, face_selector=">Z")`
  Cut a straight slot (obround).

- `.contour(depth, *, stepdown=None)` — Profile/contour milling around outer boundary.
- `.profile_pocket(profile, depth, *, face_selector=">Z", islands=None)` —
  Machine arbitrary closed profile pockets. Profiles may be dicts with
  points/width/length/diameter. For rectangular profiles, use
  {"length": x_size, "width": y_size}.
- `.profile_cutout(profile, *, depth=None, through=False, face_selector=">Z")`
  Cut through or blind arbitrary profiles.
- `.profile_contour(profile, depth, *, side="outside", face_selector=">Z")` — Contour arbitrary profiles.
- `.machine_around_profile(profile, height, *, stock_envelope=None, base_height=None, face_selector=">Z")` —
  Machine around retained bosses, pads, ribs, and joined profiles.
- `.machine_around_profiles([profile, ...], height, *, stock_envelope=None, base_height=None, face_selector=">Z")` —
  Machine around multiple retained islands in one operation. Use this for
  patterned ribs/bosses from `rarray`, `polarArray`, loops, or repeated
  constructive unions so earlier retained islands are not erased by later cuts.
- `.machine_around_cylinder(diameter, height, *, cx=0.0, cy=0.0, base_height=None, face_selector=">Z")` —
  Machine around retained cylindrical bosses.
- `.rib(width, length, height, *, cx=0.0, cy=0.0, angle=0.0, face_selector=">Z")` and
  `.pad(profile, height)` — Retained material features. For ribs/pads,
  width is Y and length is X.

- `.spot_drill(diameter, *, cx=0.0, cy=0.0)` — Spot a hole before drilling.

- `.counterbore(hole_diameter, counterbore_diameter, counterbore_depth, *,
  cx=0.0, cy=0.0, through=False)` — Counterbore a hole. Use positional
  arguments in that exact order.

- `.countersink(diameter, countersink_diameter, *, depth=0.0,
  countersink_angle=82.0, cx=0.0, cy=0.0)` — Countersink a drilled hole.

- `.tap(diameter, thread_pitch=0.0, *, depth=10.0, cx=0.0, cy=0.0)`
  Tap a pre-drilled hole. Geometry unchanged (thread form too fine for B-Rep).

- `.threaded_hole(diameter, depth=0.0, *, cx=0.0, cy=0.0, through=False)`
  Convenience: spot-drill + drill + tap in one call.

- Turning / mill-turn: `.turn_profile(profile, axis="Z", stock_diameter=None)`,
  `.turn_face(z)`, `.turn_od(diameter, length)`, `.turn_id(diameter, depth)`,
  `.turn_groove(width, depth, z)`, `.turn_thread(diameter, pitch, length,
  internal=False)`, `.mill_turn_setup(axis="Z", work_offset="G54")`.
  For tapered round extrudes, use `.turn_profile({"type":
  "tapered_cylinder", "bottom_diameter": ..., "top_diameter": ...,
  "height": ...}, stock_diameter=...)`. Use `"type": "tapered_ring"` only
  when the source actually creates a through bore.

- Thin wall / shell: `.thin_wall_pocket(profile, wall_thickness, depth,
  open_faces=None)`, `.hollow_bore(inner_profile, outer_profile, depth)`,
  `.tube_profile(outer_profile, inner_profile, length, process="turn|mill_turn")`.

- Tolerance-machined 3D CNC: `.surface_mill(surface_ref, tolerance_mm=0.10,
  strategy="parallel")`, `.sweep_mill(profile, path, tolerance_mm=0.10)`,
  `.loft_mill(profiles, tolerance_mm=0.10)`, `.dome_mill(radius, height,
  cx=0.0, cy=0.0, tolerance_mm=0.10)`.

- Wire/profile cutting: `.wire_cut_profile(profile, thickness, taper=0,
  tolerance_mm=0.05)`, `.wire_cut_internal(profile, thickness, start_hole=None,
  tolerance_mm=0.05)`.

### Export / Inspection

- `part.to_step(path)` — Export STEP file.
- `part.to_mesh()` — Get trimesh mesh (for volume, faces).
- `part.process_plan()` — Get manufacturing process plan dict.

### Translation Rules

1. CadQuery builds UP (extrude, union) — SubCAD cuts DOWN from stock.
2. Use stock dimensions = final part XY dimensions (length, width). Do NOT add
   margin — the stock should match the outer XY envelope of the final part.
   Only add margin to Z (height): use the measures height + 2-3 mm.
   For round/cylindrical CadQuery source geometry, use
   `Stock.cylindrical(diameter, height)` instead of approximating with a
   rectangular block.
3. face_mill first to achieve the final Z-height from the stock.
4. Pockets/profile operations replace CadQuery cut/cutBlind operations.
   Dimension convention is critical:
   - CadQuery `.rect(x_size, y_size)` maps to SubCAD
     `.pocket(width=y_size, length=x_size, ...)`.
   - CadQuery `.box(x_size, y_size, z_size)` maps to
     `Stock.rectangular(length=x_size, width=y_size, height=z_size)`.
   - SubCAD `width` always means Y span for rectangular pockets, ribs, pads,
     and profile dicts; SubCAD `length` always means X span.
   - Example: a CadQuery `.rect(34, 12).cutBlind(-6)` centered on the top face
     becomes `.pocket(width=12, length=34, depth=6, cx=0, cy=0)`, never
     `.pocket(width=34, length=12, ...)`.
5. Preserve CadQuery workplane face selectors when the SubCAD operation has
   `face_selector`. `.faces(">Z").workplane()` uses `face_selector=">Z"`,
   `.faces("<Z").workplane()` uses `face_selector="<Z"`, and similarly for
   `">X"`, `"<X"`, `">Y"`, `"<Y"`. Do not translate an underside or side
   operation as a default top-face operation.
6. Holes (cboreHole, cskHole) become drill operations with cx, cy from the
   CadQuery source.  Drill through=True for through-holes.
7. Selected chamfers map to .edge_chamfer(...). Selected fillets map to
   .edge_fillet(...). Do not skip edge treatments. If CadQuery says
   `model.edges().chamfer(...)` without a face selector, use
   `.edge_chamfer("all_edges", width=...)` because it chamfers top, bottom,
   vertical, and feature edges. Use `.edge_chamfer(">Z", ...)` only for
   source code like `.faces(">Z").edges().chamfer(...)`. If CadQuery uses
   `.edges("|Z").chamfer(...)`, preserve that as `.edge_chamfer("|Z", ...)`.
8. CadQuery "union" / constructive bosses must become retained-material
   operations: machine_around_profile, machine_around_cylinder, rib, or pad.
   Preserve boss/rib/pad location with `cx` and `cy`, either inside the profile
   dict or as `.machine_around_profile(profile, height, cx=..., cy=...)`.
   For multiple retained ribs/bosses from a loop, `rarray`, or `polarArray`,
   prefer `.machine_around_profiles([...], height=...)` with one profile per
   island instead of repeated single-island `.rib(...)` calls. Retained top
   features require stock height equal to base thickness plus feature height;
   do not face_mill away the material that forms the rib/boss before machining
   around it.
   Never call `.face_mill(...)` after `.machine_around_profile(...)`,
   `.machine_around_profiles(...)`, `.machine_around_cylinder(...)`, `.rib(...)`,
   or `.pad(...)` unless the CadQuery source explicitly removes those retained
   features. A later face mill will erase the boss/rib geometry and produce an
   invalid low-volume part.
   For mixed-height retained features, use `base_height=<height from stock
   bottom to feature base>`. Example: a 12 mm boss and 4 mm ribs starting on an
   8 mm base can be represented as an upper boss-only retained band and a lower
   boss+ribs retained band. Prefer `suggested_subcad` from the planner when it
   is present.
   If a CadQuery base cut affects only the lower/base thickness while taller
   retained boss/rib stock remains above it, use `.pocket(...,
   base_height=0.0)` or the appropriate Z-band instead of cutting from the
   current top face.
   Only machine around a unioned feature when it actually protrudes beyond the
   existing stock/base envelope or rises above the surrounding surface. If a
   unioned box lies fully inside existing solid stock at the same height, it may
   be construction-only evidence and should not remove surrounding material.
   Use the CadQuery `translate((x, y, z))` coordinates literally; do not infer
   that a feature is on the left/right edge unless the source coordinates put it
   there. If a unioned feature protrudes beyond the final outer envelope, the
   initial SubCAD stock dimensions must include that envelope.
9. Use profile_pocket/profile_cutout/profile_contour for polygon, polyline,
   arc-chain, slot-like, and non-rectangular profiles.
   CadQuery `.polygon(n, diameter)` maps to a profile dict like
   `{"type": "polygon", "n_sides": n, "circumdiameter": diameter}`; the
   second CadQuery argument is the polygon diameter, not the radius. This is
   still true when the CadQuery variable is named `hex_radius` or similar.
   Copy the exact second argument expression into `circumdiameter`; do not
   multiply it by 2, divide it by 2, or recompute it from flat-to-flat formulas.
10. Coordinate system: (cx=0, cy=0) is the FACE CENTER (CadQuery convention).
   Positive cx = right (+X), positive cy = up (+Y).  Negative values go
   left/down from center.  For a 70 x 40 mm face, the bottom-left corner
   is at (cx=-35, cy=-20), the top-right at (cx=35, cy=20).
   For example: to center a pocket on a 70x40 face, use cx=0, cy=0.
   To put a hole at the face center, use cx=0, cy=0.
11. The code MUST assign the final Stock to a variable named `part`.
12. Do NOT import CadQuery or SubCAD. `Stock` is already imported by the REPL.
    Allowed imports are `from types import SimpleNamespace as Measures` and
    `import math` when needed for source measures.
13. Keep the code as a small executable SubCAD program. Do not include markdown,
    explanation text, print statements, file writes, or plotting.
14. Do NOT call .face_mill(depth=0) — if the stock is already at the right
    height, just skip face_mill entirely.
15. Use pure SubCAD operations only. Never import CadQuery, never reconstruct
    the original model directly with cq.Workplane/CadQuery syntax, never import
    or reuse opaque STEP/B-Rep/mesh geometry, and never emit a hybrid_feature
    placeholder.
16. For `cboreHole`, drill the pilot hole and then call
    `counterbore(hole_diameter, counterbore_diameter, counterbore_depth, cx=..., cy=...)`.
    Never use keyword names `diameter`, `depth`, or `pilot_diameter` with
    `counterbore`.
17. If CadQuery uses shell/revolve/sweep/loft/freeform surfaces, use the pure
    CNC operation family: thin_wall_pocket/hollow_bore/tube_profile,
    turn_profile, sweep_mill, loft_mill, surface_mill, or dome_mill.
18. Prefer the pure SubCAD operation families supplied by the planner. If the
    CadQuery trace and STEP evidence are ambiguous, choose among the planned
    operation candidates only; do not invent a hybrid/imported/direct-rebuild
    fallback.
19. If CadQuery uses `.extrude(height, taper=angle)` or
    `.extrude(height, taper=-angle)` on a circular/profile sketch, do not use a
    straight `Stock.cylindrical(...)` approximation by itself. Add a
    `turn_profile` tapered-frustum operation. For CadQuery positive-Z
    extrusion, `taper=-angle` means the top outer diameter is LARGER by
    `2 * height * tan(abs(angle))`; `taper=+angle` means the top outer diameter
    is SMALLER by `2 * height * tan(angle)`. Do not add a center
    `circular_pocket` merely because a CadQuery Sketch contains a second
    `.circle(...)` or an `inner_radius` variable; add a bore only when the
    source/STEP evidence shows an actual through hole/cut or the planner lists
    a circular_pocket/bore candidate.
""")

# Shorter reference for iteration prompts (the LLM already saw the full one)
SUBCAD_API_SHORT = textwrap.dedent("""\
## SubCAD API (abbreviated)

Stock.rectangular(L, W, H, material="aluminum_6061")
Stock.cylindrical(D, H, material="aluminum_6061")
.face_mill(depth)           # mill top face
.pocket(W_y, L_x, depth, cx=cx, cy=cy, face_selector=">Z")  # rectangular pocket: W_y=Y, L_x=X
.circular_pocket(dia, depth, cx=cx, cy=cy, face_selector=">Z")
.drill(dia, depth, cx=cx, cy=cy, through=False, face_selector=">Z")
.chamfer(width)
.edge_chamfer(selector, width, angle=45)
.edge_fillet(selector, radius)
.slot(L, W, depth, angle=0, cx=cx, cy=cy, through=False, face_selector=">Z")
.contour(depth)
.profile_pocket(profile, depth)
.profile_cutout(profile, depth=None, through=False)
.profile_contour(profile, depth, side="outside", face_selector=">Z")
.machine_around_profile(profile, height, face_selector=">Z")
.machine_around_profiles([profile1, profile2], height, face_selector=">Z")
.machine_around_cylinder(dia, height, cx=cx, cy=cy, face_selector=">Z")
.rib(width, length, height, cx=cx, cy=cy, angle=0, face_selector=">Z")
.pad(profile, height)
.turn_profile(profile, axis="Z", stock_diameter=None)  # supports {"type":"tapered_cylinder", ...}
.thin_wall_pocket(profile, wall_thickness, depth)
.surface_mill(surface_ref, tolerance_mm=0.10)
.sweep_mill(profile, path, tolerance_mm=0.10)
.loft_mill(profiles, tolerance_mm=0.10)
.dome_mill(radius, height, cx, cy, tolerance_mm=0.10)
.wire_cut_profile(profile, thickness)
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

    # Also extract the import: from types import SimpleNamespace as Measures
    import_line = ""
    import_match = re.search(
        r"from\s+types\s+import\s+SimpleNamespace\s+as\s+Measures",
        cq_code,
    )
    if import_match:
        import_line = import_match.group(0)

    block = _extract_balanced_assignment(
        cq_code,
        r"\bm\s*=\s*(?:Measures|SimpleNamespace)\s*\(",
    )
    if block:
        if import_line and "SimpleNamespace" in block and import_line not in block:
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


def _extract_balanced_assignment(source: str, start_pattern: str) -> str:
    """Extract an assignment with nested parentheses by balancing parens."""
    match = re.search(start_pattern, source)
    if not match:
        return ""

    line_start = source.rfind("\n", 0, match.start()) + 1
    idx = match.end() - 1
    depth = 0
    in_string: str | None = None
    escaped = False

    for pos in range(idx, len(source)):
        ch = source[pos]
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == in_string:
                in_string = None
            continue

        if ch in {"'", '"'}:
            in_string = ch
            continue
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return source[line_start:pos + 1].strip()

    return source[line_start:].strip()


def _cadquery_variable_volume_evidence(cq_code: str, *, max_items: int = 16) -> str:
    """Execute trusted CadQuery source and summarize Workplane variable volumes.

    Zero-to-CAD rows are local benchmark programs.  This evidence is used only
    to tell the translator which named CadQuery intermediates changed geometry;
    generated SubCAD is still compared against the original STEP target.
    """
    try:
        import cadquery as cq  # type: ignore
    except Exception:
        return "CadQuery unavailable; no variable volume evidence."

    namespace: dict[str, object] = {"cq": cq, "math": math}
    try:
        exec(cq_code, namespace)
    except Exception as exc:
        return f"CadQuery source execution failed; no variable volume evidence: {exc}"

    rows: list[str] = []
    previous_volume: float | None = None
    for name, value in namespace.items():
        if name.startswith("__") or name in {"cq", "math"}:
            continue
        volume = _object_volume(value)
        if volume is None:
            continue
        if previous_volume is None:
            delta = ""
        else:
            change = volume - previous_volume
            if abs(change) < 1e-6:
                delta = " (no volume change vs previous solid)"
            else:
                delta = f" (delta {change:+.3f} mm^3)"
        rows.append(f"- `{name}`: {volume:.3f} mm^3{delta}")
        previous_volume = volume
        if len(rows) >= max_items:
            break

    if not rows:
        return "No CadQuery Workplane/Solid variable volumes found."
    return "\n".join(rows)


def _object_volume(value: object) -> float | None:
    try:
        if hasattr(value, "val"):
            solid = value.val()  # type: ignore[attr-defined]
            if hasattr(solid, "Volume"):
                return float(solid.Volume())
        if hasattr(value, "Volume"):
            return float(value.Volume())  # type: ignore[attr-defined]
    except Exception:
        return None
    return None


def build_system_prompt() -> str:
    """Build the system prompt with subCAD API reference."""
    return f"""CRITICAL: You are a tool-using code generator.
Your job is to translate CadQuery constructive CAD into executable SubCAD.
You MUST call the `execute_subcad` tool with raw Python code in its `code`
argument. Do not put markdown fences, explanations, comments about your
reasoning, JSON outside the tool call, or prose in the code string.

{SUBCAD_API_REFERENCE}

`Stock` is pre-imported. Do not import CadQuery or SubCAD. Avoid `.contour()`
unless the source clearly requires outer profiling that cannot be represented
with pockets, holes, slots, or face milling."""


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

    ref_vol = _load_reference_volume(step_path)

    # Extract measures for the LLM to reference
    measures = _extract_measures(ops_trace)
    measures_json = json.dumps(measures, indent=2, default=str)

    # Extract the Measures block from the CadQuery source for reuse
    measures_block = _extract_measures_block(cq_code)
    planner_plan = plan_pure_subcad_features(ops_trace, cq_code)
    planner_summary = _format_planner_candidates(planner_plan.to_dict())
    volume_evidence = _cadquery_variable_volume_evidence(cq_code)

    prompt = f"""## Task

Translate the following CadQuery program into a subCAD subtractive program.

## Reference Geometry
- STEP volume: {ref_vol} mm^3
- Stock dimensions (final part XY + small Z margin): {stock_dims['length']:.0f} x {stock_dims['width']:.0f} x {stock_dims['height']:.0f} mm

## Measures (named parameters — COPY-PASTE into subCAD code)
```python
{measures_block}
```

## Extracted Numeric Measures
```json
{measures_json}
```

Use `m.width`, `m.depth`, `m.height`, `m.wall_thickness`, etc. in your
subCAD code instead of hardcoding values when the names are relevant. If a
measure is a final part dimension, use it directly; do not add arbitrary stock
margin in X/Y. Never use bare measure names like `flange_thickness` or
`hole_diameter` unless you first assign them as local variables; use
`m.flange_thickness`, `m.hole_diameter`, etc.

## CadQuery Source Code
```python
{cq_code}
```

## Operations Trace (reconstructed chains)
{chr(10).join(chain_summary)}

## CadQuery Variable Volume Evidence
{volume_evidence}

## Pure SubCAD Operation Plan (planner candidates)
{planner_summary}

## Instructions

Translate this constructive CadQuery program into an equivalent subCAD
subtractive program. Remember:
- Stock XY = final part XY (use {stock_dims['length']:.0f} x {stock_dims['width']:.0f}).
  Only add extra Z height for face_mill.
- If the CadQuery source uses `.cylinder(...)`, round-bar stock, or a circular
  outer envelope, start from `Stock.cylindrical(diameter, height)` instead of
  rectangular stock.
- If the CadQuery source uses `.extrude(..., taper=...)`, represent the taper
  with `turn_profile({{"type": "tapered_cylinder", ...}})` or a real tapered
  profile operation. Do not approximate it as a straight cylinder, and do not
  add a center bore solely because a Sketch has a second `.circle(...)`.
  CadQuery `taper=-angle` on a positive-Z extrusion makes the TOP diameter
  larger; `taper=+angle` makes the TOP diameter smaller.
- Cut AWAY material to reveal the final shape.
- Use the CadQuery Variable Volume Evidence above to avoid machining no-op
  source operations. If two consecutive named CadQuery solids have the same
  volume, the later source operation did not affect the final target for this
  benchmark row. Do not translate the operations that produced that no-change
  variable. Example: if `recess` has "no volume change", omit the corresponding
  pocket/cut; if `peripheral` has "no volume change", omit those hole operations.
- The target is the original STEP reference geometry. Match that original STEP;
  do not import, read, reuse, or wrap the STEP/B-Rep/mesh inside generated code.
- The target volume from the original STEP is approximately {ref_vol} mm^3.
- Assign the final Stock to a variable named `part`.
- Copy the Measures block above when useful and use m.width, m.depth, etc.
  Never reference copied measure fields as bare variables; always use `m.<name>`
  unless you explicitly assign a local helper variable in the generated code.
- Call the `execute_subcad` tool with raw Python code. Do not include markdown
  fences or explanation text in the tool argument.
- Prefer the pure SubCAD operation families in the planner candidates above.
  If evidence is ambiguous, choose among those planned operation candidates only.
- Do not add major feature operations absent from the planner candidates. For
  example, do not add a center `circular_pocket`/bore unless the planner/source
  shows a circular cut, hole, bore, or other real opening.
- Use simple SubCAD operations first: face_mill, pocket, circular_pocket,
  drill, slot, and chamfer. Use counterbore/countersink only when visible in
  the CadQuery source.
- Keep rectangular dimensions in the correct axes. CadQuery `.rect(x_size,
  y_size)` maps to SubCAD `.pocket(width=y_size, length=x_size, ...)`.
  SubCAD `width` always means Y span, and SubCAD `length` always means X span.
  The same convention applies to rectangular profile dicts, ribs, and pads.
- For CadQuery `.polygon(n, diameter)`, use
  `{{"type": "polygon", "n_sides": n, "circumdiameter": diameter}}`.
  The CadQuery polygon value is a diameter, not a radius, even when the source
  variable is named `hex_radius` or similar. Copy the exact second argument
  expression from `.polygon(...)` into `circumdiameter`; do not multiply it by
  2, divide it by 2, or infer a new value from volume feedback.
  For an outer outline cut through the full stock thickness, call
  `.profile_cutout(profile, through=True)` or pass a depth equal to the current
  stock height.
- Preserve retained-feature locations. For a CadQuery union/boss/pad translated
  to a nonzero X/Y location, pass `cx=...` and `cy=...` or include them in the
  profile dict. Do not machine around a translated box that is fully inside the
  existing base stock and does not add material. Use the source
  `translate((x, y, z))` values literally; do not move the feature to a stock
  edge unless the source coordinate is actually at that edge.
- Preserve CadQuery edge scope. Unqualified `.edges().chamfer(...)` means all
  model edges, so use `.edge_chamfer("all_edges", width=...)`; do not narrow it
  to only the top face unless the CadQuery source explicitly used `.faces(">Z")`.
  Directional CadQuery selectors should also be preserved, for example
  `.edges("|Z").chamfer(...)` becomes `.edge_chamfer("|Z", width=...)`.
- Forbidden fallbacks: hybrid_feature placeholders, direct CadQuery reconstruction
  with cq.Workplane or CadQuery imports, import_step, opaque B-Rep/mesh reuse,
  or any hybrid/imported geometry that hides the manufacturing operations.

CALL `execute_subcad` NOW with your best first SubCAD translation."""
    return prompt


def _format_planner_candidates(plan: dict) -> str:
    """Return a compact pure-operation planner summary for the prompt."""
    lines = [
        f"- coverage_mode: {plan.get('coverage_mode', 'pure_subcad_operations')}",
        f"- compatible: {bool(plan.get('compatible'))}",
    ]
    features = plan.get("features") or []
    if not features:
        lines.append("- candidates: none detected; use conservative basic SubCAD operations only")
        return "\n".join(lines)

    lines.append("- candidates:")
    for feature in features:
        operation = feature.get("operation", "unknown")
        status = feature.get("planner_status", "unknown")
        family = feature.get("family", "unknown")
        source = feature.get("source", "unknown")
        reason = feature.get("reason", "")
        lines.append(
            f"  - {operation} ({status}, {family}) from {source}: {reason}"
        )
        evidence = feature.get("evidence") or {}
        suggested = evidence.get("suggested_subcad")
        if suggested:
            lines.append(f"    suggested_subcad: {suggested}")
        profiles = evidence.get("profiles") or []
        if profiles:
            lines.append(f"    retained_profiles: {json.dumps(profiles, sort_keys=True)[:900]}")
        if evidence.get("height") is not None:
            lines.append(f"    retained_height: {evidence.get('height')}")
        if evidence.get("base_height") is not None:
            lines.append(f"    retained_base_height: {evidence.get('base_height')}")
    return "\n".join(lines)


def _load_reference_volume(step_path: str) -> float:
    """Load a reference STEP volume using CadQuery first, then mesh fallback."""
    try:
        from src.subcad.geometry import import_step
        ref_shape = import_step(step_path)
        return round(float(ref_shape.val().Volume()), 1)
    except Exception:
        pass

    try:
        ref_mesh = trimesh.load(step_path)
        return round(float(ref_mesh.volume), 1) if ref_mesh else 0.0
    except Exception:
        return 0.0


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
Target volume from the original STEP reference: {target_volume:.1f} mm^3.
Repair against the original STEP comparison, not the previous candidate. Keep
the fix as pure SubCAD operations; do not switch to CadQuery reconstruction,
import_step, hybrid_feature, or opaque STEP/B-Rep/mesh reuse."""]

    # --- Include localized mesh deviation feedback ---
    if mesh_comparison and mesh_comparison.get("feedback"):
        parts.append("")
        parts.append("## Localized Shape Deviation")
        parts.append("The following original-STEP comparison identifies *where* "
                     "the candidate shape deviates from the reference. Use this "
                     "to fix specific dimensions (depths, widths, positions).")
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
                     "chamfers) between the original STEP reference and candidate. "
                     "Features listed as MISSING, WRONG SIZE, or SHIFTED should "
                     "be fixed with pure SubCAD operations.")
        fscore = feature_comparison.get("score")
        if fscore is not None:
            parts.append(f"Feature quality score: {fscore:.0f}/100")
        parts.append("")
        parts.append(feature_comparison["feedback"])

    # --- Previous code and terse instructions (no API ref — LLM knows it) ---
    parts.append(f"""
## Previous Code
```python
{previous_code}
```

## Instructions

Call the `execute_subcad` tool again with corrected raw SubCAD Python code.
No markdown fences, no explanation, no analysis, no file writes. The code must
assign the final Stock to `part` and should start with the Measures block if
needed, followed by `part = Stock.rectangular(...`. Preserve the planner-backed
pure operation policy; do not repair by importing or reconstructing the original
CadQuery/STEP geometry directly.""")

    return "\n".join(parts)


# =========================================================================
#  Optional rich comparison helpers
# =========================================================================

_OMIT_JSON_KEYS = {
    "per_vertex_deviation",
    "submesh",
    "mesh",
    "reference_mesh",
    "candidate_mesh",
    "part",
}


def _compact_for_history(value):
    """Return a JSON-friendly copy of comparison data for results/history."""
    if value is None or isinstance(value, (str, int, float, bool)):
        return value

    if isinstance(value, dict):
        compact = {}
        for key, item in value.items():
            if key in _OMIT_JSON_KEYS:
                compact[key] = _describe_omitted_value(item)
            elif key == "face_indices" and hasattr(item, "__len__"):
                compact[key] = f"<{len(item)} face indices omitted>"
            else:
                compact[key] = _compact_for_history(item)
        return compact

    if isinstance(value, (list, tuple)):
        return [_compact_for_history(item) for item in value]

    if hasattr(value, "shape"):
        shape = getattr(value, "shape", None)
        size = getattr(value, "size", None)
        if size is not None and size <= 20 and hasattr(value, "tolist"):
            return value.tolist()
        return f"<array shape={shape} omitted>"

    if hasattr(value, "vertices") and hasattr(value, "faces"):
        try:
            return (
                f"<mesh vertices={len(value.vertices)} "
                f"faces={len(value.faces)} omitted>"
            )
        except Exception:
            return "<mesh omitted>"

    return str(value)


def _describe_omitted_value(value) -> str:
    if hasattr(value, "shape"):
        return f"<array shape={getattr(value, 'shape', '?')} omitted>"
    if hasattr(value, "vertices") and hasattr(value, "faces"):
        try:
            return (
                f"<mesh vertices={len(value.vertices)} "
                f"faces={len(value.faces)} omitted>"
            )
        except Exception:
            return "<mesh omitted>"
    if hasattr(value, "__len__") and not isinstance(value, (str, bytes, dict)):
        return f"<{len(value)} values omitted>"
    return "<omitted>"


def _mesh_from_execution(exec_result: dict):
    """Best-effort conversion of a successful REPL result into a Trimesh."""
    part = exec_result.get("part")
    if part is not None:
        to_mesh = getattr(part, "to_mesh", None)
        if callable(to_mesh):
            mesh = to_mesh()
            if mesh is not None:
                return _coerce_trimesh(mesh)

        try:
            from src.subcad.geometry import to_mesh as geometry_to_mesh
            mesh = geometry_to_mesh(part)
            if mesh is not None:
                return _coerce_trimesh(mesh)
        except Exception:
            pass

    stl_path = exec_result.get("stl_path")
    if stl_path and os.path.exists(stl_path):
        mesh = trimesh.load(stl_path)
        if mesh is not None:
            return _coerce_trimesh(mesh)

    raise RuntimeError("candidate mesh unavailable")


def _load_step_mesh(step_path: str):
    """Load a STEP reference as a Trimesh using CadQuery first, then trimesh."""
    try:
        from src.subcad.geometry import import_step, to_mesh
        mesh = to_mesh(import_step(step_path))
        if mesh is not None:
            return _coerce_trimesh(mesh)
    except Exception:
        pass

    mesh = trimesh.load(step_path)
    if mesh is None:
        raise RuntimeError("reference mesh unavailable")
    return _coerce_trimesh(mesh)


def _coerce_trimesh(mesh):
    """Convert Trimesh scenes into a single mesh; pass meshes through."""
    if hasattr(mesh, "geometry"):
        geometries = list(mesh.geometry.values())
        if not geometries:
            raise RuntimeError("mesh scene has no geometry")
        return trimesh.util.concatenate(geometries)
    return mesh


def _align_candidate_mesh_to_reference(candidate_mesh, reference_mesh):
    """Return a translated candidate mesh aligned by bounding-box minimum.

    Zero-to-CAD STEP files commonly use a bottom-at-Z-zero convention, while
    SubCAD stock meshes are centered around their local frame. For translation
    quality we care about shape and feature placement, not this arbitrary origin
    offset, so rich comparison applies translation-only alignment. Orientation
    and scale are intentionally left unchanged.
    """
    if not hasattr(candidate_mesh, "bounds") or not hasattr(reference_mesh, "bounds"):
        return candidate_mesh, [0.0, 0.0, 0.0]

    aligned = candidate_mesh.copy()
    ref_min = reference_mesh.bounds[0]
    cand_min = candidate_mesh.bounds[0]
    translation = ref_min - cand_min
    aligned.apply_translation(translation)
    return aligned, [float(v) for v in translation]


def _comparison_feedback_payload(
    code: str,
    exec_result: dict,
    comparison: dict,
    target_volume: float,
    mesh_comparison: dict | None,
    feature_comparison: dict | None,
) -> dict:
    """Build compact tool feedback for the next LLM turn."""
    payload = {
        "volume_ratio": round(comparison.get("volume_ratio", 0), 4),
        "candidate_volume": round(exec_result.get("volume", 0), 1),
        "target_volume": round(
            comparison.get("target_volume", target_volume), 1
        ),
        "success": exec_result.get("success", False),
        "error": exec_result.get("error")
        if not exec_result.get("success", False) else None,
        "feedback": format_feedback(code, exec_result, comparison),
        "repair_policy": (
            "Repair against the original STEP reference target using pure SubCAD "
            "operations only; do not use hybrid_feature, direct CadQuery "
            "reconstruction, import_step, or opaque STEP/B-Rep/mesh reuse."
        ),
    }

    if mesh_comparison and mesh_comparison.get("feedback"):
        payload["mesh_feedback"] = mesh_comparison["feedback"]
        if mesh_comparison.get("score") is not None:
            payload["mesh_score"] = mesh_comparison["score"]

    if feature_comparison and feature_comparison.get("feedback"):
        payload["feature_feedback"] = feature_comparison["feedback"]
        if feature_comparison.get("score") is not None:
            payload["feature_score"] = feature_comparison["score"]

    return payload


# =========================================================================
#  Code extraction
# =========================================================================

def extract_code(response: str) -> Optional[str]:
    """Extract Python code from an LLM response.

    Handles:
      - ```python ... ``` fences
      - ``` ... ``` fences (no language tag)
      - Bare code starting with Stock.rectangular or part =
      - Code buried in explanatory text
    """
    # Try fenced code first
    fence_pat = re.compile(r"```(?:python)?\s*\n(.*?)\n\s*```", re.DOTALL)
    match = fence_pat.search(response)
    if match:
        code = match.group(1).strip()
        if "Stock.rectangular" in code:
            return code

    # Try any code fence
    any_fence = re.compile(r"```[a-z]*\s*\n(.*?)\n\s*```", re.DOTALL)
    for match in any_fence.finditer(response):
        code = match.group(1).strip()
        if "Stock.rectangular" in code:
            return code

    # Look for lines starting with "part = Stock.rectangular" or similar
    # even if they're embedded in markdown or explanatory text
    lines = response.split("\n")
    code_start = None
    for i, line in enumerate(lines):
        stripped = line.strip()
        if re.match(r"^(part|stock)\s*=\s*(Stock\.rectangular|\()", stripped):
            code_start = i
            break
        if stripped.startswith("Stock.rectangular"):
            code_start = i
            break

    if code_start is not None:
        code_lines = []
        paren_depth = 0
        for line in lines[code_start:]:
            code_lines.append(line)
            paren_depth += line.count("(") - line.count(")")
            if paren_depth <= 0 and len(code_lines) > 1:
                break
        code = "\n".join(code_lines).strip()
        if "Stock.rectangular" in code:
            return code

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
        _load_local_env_if_present()

        if self.provider == "deepseek":
            self.model = model or "deepseek-chat"
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

    def tool_chat(
        self,
        messages: list[dict],
        tools: list[dict],
        temperature: float = 0.2,
        max_tokens: int = 4096,
    ) -> dict | None:
        """Send a chat request with tool calling. Returns tool call dict or None.

        DeepSeek and OpenAI use the same function-calling API.
        Anthropic uses native tool_use.
        """
        if self._is_anthropic:
            # Convert OpenAI-style tools to Anthropic format
            anthropic_tools = []
            for t in tools:
                fn = t["function"]
                anthropic_tools.append({
                    "name": fn["name"],
                    "description": fn["description"],
                    "input_schema": {
                        "type": "object",
                        "properties": fn["parameters"]["properties"],
                        "required": fn["parameters"].get("required", []),
                    },
                })

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
                tools=anthropic_tools,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            # Extract tool_use block
            for block in resp.content:
                if block.type == "tool_use":
                    return {
                        "id": block.id,
                        "name": block.name,
                        "arguments": block.input,
                    }
            return None  # no tool call

        else:
            # OpenAI-compatible (DeepSeek, OpenAI)
            resp = self._client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools,
                tool_choice="required",
                temperature=temperature,
                max_tokens=max_tokens,
            )
            msg = resp.choices[0].message
            if msg.tool_calls:
                tc = msg.tool_calls[0]
                try:
                    args = json.loads(tc.function.arguments)
                except json.JSONDecodeError:
                    # LLM may produce malformed JSON (unescaped code strings).
                    # Extract code from raw arguments by finding the code value.
                    raw = tc.function.arguments
                    code = _extract_code_from_json(raw)
                    if code:
                        args = {"code": code}
                    else:
                        return None
                return {"id": tc.id, "name": tc.function.name, "arguments": args}
            return None


def _load_local_env_if_present(path: str = ".env") -> None:
    """Load simple KEY=VALUE lines from .env without printing secrets."""
    env_path = Path(path)
    if not env_path.exists():
        return
    try:
        lines = env_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        return
    for line in lines:
        text = line.strip()
        if not text or text.startswith("#") or "=" not in text:
            continue
        key, value = text.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


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


def _mesh_comparison_is_trusted(
    mesh_comparison: dict | None,
    *,
    min_mesh_score: float,
    tolerance_mm: float,
) -> tuple[bool, str]:
    """Return whether a rich mesh comparison is good enough to stop iterating."""
    if not mesh_comparison:
        return False, "missing"
    if mesh_comparison.get("error"):
        return False, "error"

    score = float(mesh_comparison.get("score", 0.0) or 0.0)
    sdf = mesh_comparison.get("sdf") or {}
    rms = abs(float(sdf.get("rms_error", 0.0) or 0.0))
    max_overcut = abs(float(sdf.get("max_overcut", 0.0) or 0.0))
    max_undercut = abs(float(sdf.get("max_undercut", 0.0) or 0.0))
    slice_result = mesh_comparison.get("slice") or {}
    problem_slices = slice_result.get("problem_slices") or []

    if score < min_mesh_score:
        return False, f"score_{score:.1f}"
    if max(rms, max_overcut, max_undercut) > tolerance_mm:
        return False, f"deviation_{max(rms, max_overcut, max_undercut):.3f}"
    if problem_slices:
        return False, f"slices_{len(problem_slices)}"
    return True, "trusted"


def _extract_code_from_json(raw_json: str) -> Optional[str]:
    """Extract code value from malformed JSON with unescaped code strings.

    Handles the case where the LLM puts raw Python code (with newlines and
    quotes) directly into the JSON string value without proper escaping.
    """
    # Pattern: "code": "...code..."
    # Try to find the code value between "code": " and the closing "}
    match = re.search(r'"code"\s*:\s*"(.*?)"\s*\}?\s*$', raw_json, re.DOTALL)
    if match:
        code = match.group(1)
        # Unescape JSON escapes
        code = code.replace("\\n", "\n").replace("\\t", "\t").replace("\\\"", "\"")
        code = code.replace("\\\\", "\\")
        if "Stock.rectangular" in code:
            return code

    # Try to extract everything after "code": "
    idx = raw_json.find('"code"')
    if idx >= 0:
        # Find the value start after the colon+quote
        colon = raw_json.find(":", idx)
        if colon >= 0:
            value = raw_json[colon + 1:].strip().strip('"')
            # Remove trailing "} if present
            if value.endswith('"}'):
                value = value[:-2]
            elif value.endswith('}'):
                value = value[:-1].rstrip().rstrip('"')
            value = value.replace("\\n", "\n").replace("\\t", "\t").replace("\\\"", "\"")
            value = value.replace("\\\\", "\\")
            if "Stock.rectangular" in value or "part" in value:
                return value

    return None


# =========================================================================
#  Tool schema for function calling
# =========================================================================

EXECUTE_SUBCAD_TOOL = {
    "type": "function",
    "function": {
        "name": "execute_subcad",
        "description": (
            "Execute subCAD subtractive code and return geometry results. "
            "Call this with your translated subCAD code to check the output."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": (
                        "Complete subCAD Python code. Stock is pre-imported — "
                        "use Stock.rectangular(...) directly. Copy the Measures "
                        "block from the prompt. Assign final part to 'part'."
                    ),
                }
            },
            "required": ["code"],
        },
    },
}


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
        strict_mesh_convergence: bool = False,
        min_mesh_score: float = 95.0,
        mesh_tolerance_mm: float = 0.25,
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
            strict_mesh_convergence: If True, do not stop on volume-only success
                when rich mesh comparison reports a shape mismatch.
            min_mesh_score: Minimum rich comparison score for strict convergence.
            mesh_tolerance_mm: Maximum SDF deviation for strict convergence.
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
        self.strict_mesh_convergence = strict_mesh_convergence
        self.min_mesh_score = min_mesh_score
        self.mesh_tolerance_mm = mesh_tolerance_mm
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
        target_volume = _load_reference_volume(step_path)

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
        best_code = None
        best_exec = None
        best_comparison = None
        best_mesh_comparison = None
        best_feature_comparison = None
        best_attempt = None
        best_attempt_score = None
        reference_mesh = None
        reference_mesh_error = None
        stop_reason = "not_started"

        attempt = 0
        while True:
            attempt += 1

            if self.verbose:
                if attempt == 1:
                    print(f"  [attempt {attempt}] tool-calling LLM...",
                          end=" ", flush=True)
                else:
                    print(f"  [attempt {attempt}] calling LLM...",
                          end=" ", flush=True)

            # --- Call LLM with tool ---
            try:
                if attempt == 1:
                    # First attempt: force tool call
                    tool_result = self.llm.tool_chat(
                        messages,
                        tools=[EXECUTE_SUBCAD_TOOL],
                    )
                else:
                    # Subsequent: LLM sees previous tool results and decides
                    tool_result = self.llm.tool_chat(
                        messages,
                        tools=[EXECUTE_SUBCAD_TOOL],
                    )
            except Exception as e:
                if self.verbose:
                    print(f"LLM error: {str(e).encode('ascii', errors='replace').decode('ascii')}")
                return {
                    "success": False, "subcad_code": None, "attempts": attempt,
                    "exec_result": None, "comparison": None,
                    "mesh_comparison": None, "feature_comparison": None,
                    "history": history, "stop_reason": f"LLM API error: {e}",
                    "error": f"LLM API error: {e}",
                }

            # --- Handle LLM response ---
            if tool_result is None or "code" not in tool_result.get("arguments", {}):
                # LLM returned no tool call — try text fallback
                if self.verbose:
                    print("(no tool call)", end=" ", flush=True)
                conv.record(0.0, False)
                history.append({
                    "attempt": attempt, "code": None, "exec_result": None,
                    "comparison": None, "error": "LLM did not call tool",
                })
                continue

            code = tool_result["arguments"]["code"]
            if self.verbose:
                print(f"{len(code)} chars", end=" ", flush=True)

            # --- Execute code ---
            exec_result = run_subcad(code)

            if self.verbose:
                if exec_result["success"]:
                    print(f"vol={exec_result['volume']:.1f}", end=" ", flush=True)
                else:
                    err_msg = str(exec_result.get('error', '?'))[:80]
                    err_msg = err_msg.encode('ascii', errors='replace').decode('ascii')
                    print(f"ERR: {err_msg}", end=" ", flush=True)

            # --- Compare to reference ---
            if exec_result["success"] and exec_result.get("step_path"):
                comparison = compare_to_reference(
                    exec_result["step_path"], step_path
                )
            else:
                comparison = {"match": False, "volume_ratio": 0.0,
                              "error": exec_result.get("error", "Execution failed")}

            # --- Optional richer mesh / feature comparison ---
            mesh_comparison = None
            feature_comparison = None
            candidate_mesh = None
            candidate_compare_mesh = None
            mesh_alignment = None
            reference_comparison_ok = (
                exec_result["success"]
                and exec_result.get("step_path")
                and not comparison.get("error")
            )
            needs_candidate_mesh = (
                reference_comparison_ok
                and (
                    (self.comparison_methods and _HAS_MESH_COMPARE)
                    or (self.feature_aware and _HAS_FEATURE_COMPARE)
                )
            )
            if needs_candidate_mesh:
                try:
                    candidate_mesh = _mesh_from_execution(exec_result)
                except Exception as e:
                    if self.verbose:
                        msg = str(e).encode("ascii", errors="replace").decode("ascii")
                        print(f"mesh-skip={msg[:50]}", end=" ", flush=True)

            if (
                candidate_mesh is not None
                and self.comparison_methods
                and _HAS_MESH_COMPARE
            ):
                try:
                    if reference_mesh is None and reference_mesh_error is None:
                        try:
                            reference_mesh = _load_step_mesh(step_path)
                        except Exception as e:
                            reference_mesh_error = str(e)
                    if reference_mesh is not None:
                        candidate_compare_mesh, translation = _align_candidate_mesh_to_reference(
                            candidate_mesh,
                            reference_mesh,
                        )
                        mesh_alignment = {
                            "method": "bounds_min_translation",
                            "translation": translation,
                        }
                        mesh_comparison = compare_meshes(
                            reference_mesh,
                            candidate_compare_mesh,
                            methods=self.comparison_methods,
                        )
                        mesh_comparison["alignment"] = mesh_alignment
                    elif reference_mesh_error:
                        mesh_comparison = {"error": reference_mesh_error}
                except Exception as e:
                    mesh_comparison = {"error": str(e)}

            if (
                candidate_mesh is not None
                and self.feature_aware
                and _HAS_FEATURE_COMPARE
            ):
                try:
                    feature_comparison = compare_with_features(
                        step_path,
                        candidate_compare_mesh if candidate_compare_mesh is not None else candidate_mesh,
                        ops_trace=ops_trace,
                    )
                    if mesh_alignment:
                        feature_comparison["alignment"] = mesh_alignment
                except Exception as e:
                    feature_comparison = {"error": str(e)}

            vol_ratio = comparison.get("volume_ratio", 0)
            if self.verbose:
                if comparison.get("match"):
                    print("MATCH!", end=" ", flush=True)
                else:
                    print(f"ratio={vol_ratio:.3f}", end=" ", flush=True)

            # --- Record ---
            history.append({
                "attempt": attempt, "code": code,
                "exec_result": exec_result, "comparison": comparison,
                "mesh_comparison": _compact_for_history(mesh_comparison),
                "feature_comparison": _compact_for_history(feature_comparison),
            })
            final_code = code
            final_exec = exec_result
            final_comparison = comparison
            final_mesh_comparison = _compact_for_history(mesh_comparison)
            final_feature_comparison = _compact_for_history(feature_comparison)
            if exec_result.get("success"):
                mesh_score = 0.0
                if isinstance(mesh_comparison, dict):
                    mesh_score = float(mesh_comparison.get("score") or 0.0)
                volume_error = abs(1.0 - float(comparison.get("volume_ratio") or 0.0))
                attempt_score = (
                    1 if comparison.get("match") else 0,
                    mesh_score,
                    -volume_error,
                )
                if best_attempt_score is None or attempt_score > best_attempt_score:
                    best_code = code
                    best_exec = exec_result
                    best_comparison = comparison
                    best_mesh_comparison = _compact_for_history(mesh_comparison)
                    best_feature_comparison = _compact_for_history(feature_comparison)
                    best_attempt = attempt
                    best_attempt_score = attempt_score

            # --- Add tool result to messages ---
            feedback_prompt = build_iteration_prompt(
                code,
                exec_result,
                comparison,
                target_volume,
                mesh_comparison=mesh_comparison,
                feature_comparison=feature_comparison,
            )
            tool_result_content = json.dumps(
                _comparison_feedback_payload(
                    code,
                    exec_result,
                    comparison,
                    target_volume,
                    mesh_comparison,
                    feature_comparison,
                ),
                default=str,
            )

            # OpenAI-compatible tool result format
            messages.append({
                "role": "assistant",
                "content": None,
                "tool_calls": [{
                    "id": tool_result["id"],
                    "type": "function",
                    "function": {
                        "name": "execute_subcad",
                        "arguments": json.dumps({"code": code}),
                    },
                }],
            })
            messages.append({
                "role": "tool",
                "tool_call_id": tool_result["id"],
                "content": tool_result_content,
            })

            # --- Convergence check ---
            exec_ok = exec_result.get("success", False)
            decision = conv.record(vol_ratio, exec_ok)
            if (
                decision == "success"
                and self.strict_mesh_convergence
                and self.comparison_methods
            ):
                mesh_ok, mesh_reason = _mesh_comparison_is_trusted(
                    mesh_comparison,
                    min_mesh_score=self.min_mesh_score,
                    tolerance_mm=self.mesh_tolerance_mm,
                )
                if not mesh_ok:
                    if attempt >= conv.safety_cap:
                        decision = "mesh_mismatch_safety_cap"
                    else:
                        decision = "continue"
                        if self.verbose:
                            print(f"mesh-mismatch={mesh_reason}", end=" ", flush=True)
            if decision != "continue":
                stop_reason = decision
                if self.verbose:
                    print(f"\n  Stop: {decision} ({conv.summary})")
                break

            messages.append({
                "role": "user",
                "content": feedback_prompt,
            })

        returned_best_attempt = False
        if (not (final_exec or {}).get("success")) and best_exec is not None:
            final_code = best_code
            final_exec = best_exec
            final_comparison = best_comparison
            final_mesh_comparison = best_mesh_comparison
            final_feature_comparison = best_feature_comparison
            returned_best_attempt = True

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
            "returned_best_attempt": returned_best_attempt,
            "best_attempt": best_attempt,
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
