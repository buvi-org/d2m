"""SubCAD REPL: execute generated subCAD code and compare to reference geometry.

Provides the execution and comparison backend for the agentic translator's
REPL feedback loop. Executes subCAD code in a controlled environment,
compares output geometry to reference STEP files, and formats human-readable
feedback for the LLM.

Key design notes:
  - STEP files are loaded via CadQuery's built-in importer (cascadio is unavailable).
  - trimesh is used only as a fallback for non-STEP formats.
  - Both Stock objects (subCAD) and CadQuery Workplane objects are supported.
"""

from __future__ import annotations

import os
import re
import sys
import tempfile
import traceback
from typing import Optional


# ---------------------------------------------------------------------------
#  Guard: check what is available
# ---------------------------------------------------------------------------

_HAS_CADQUERY = False
try:
    import cadquery as cq
    _HAS_CADQUERY = True
except ImportError:
    pass

_HAS_TRIMESH = False
try:
    import trimesh
    _HAS_TRIMESH = True
except ImportError:
    pass


# =============================================================================
#  Code execution
# =============================================================================

def run_subcad(code: str) -> dict:
    """Execute a subCAD code string in a controlled environment.

    Executes the code with the subCAD ``Stock`` class pre-imported, captures
    the ``part`` variable (or any Stock / Workplane result), and extracts
    geometry data including volume, face count, and optional STEP/STL exports.

    Args:
        code: Python source code that creates a subCAD part.  Must assign the
              final Stock instance to a variable named ``part``, or return a
              value through the last expression.

    Returns:
        On success:
          ``{"success": True, "volume": float, "faces": int,
             "part": object, "step_path": str|None, "stl_path": str|None,
             "process_plan": dict|None}``

        On failure:
          ``{"success": False, "error": str}``
    """
    guard_error = _generated_code_guard(code)
    if guard_error:
        return {"success": False, "error": guard_error}

    # Build a namespace with key pre-imports available to the executed code.
    # We import Stock explicitly so that generated code using
    # ``from src.subcad import Stock`` or bare ``Stock.rectangular(...)``
    # works when executed via exec().
    try:
        from src.subcad import Stock
        from src.subcad.geometry import (
            compute_volume,
            compute_bounding_box,
            export_step,
            export_stl,
        )
    except ImportError as e:
        return {
            "success": False,
            "error": f"SubCAD import failed: {e}",
        }

    namespace: dict = {
        "__builtins__": __builtins__,
        "Stock": Stock,
        # Prevent destructive operations
        "exec": None,
        "eval": None,
        "compile": None,
        "__import__": __import__,
    }

    # Also add CadQuery to the namespace (some generated code may import it)
    if _HAS_CADQUERY:
        namespace["cadquery"] = cq
        namespace["cq"] = cq

    # Execute the code
    try:
        exec(code, namespace)
    except Exception as e:
        tb = traceback.format_exc()
        return {
            "success": False,
            "error": f"Execution error: {e}\n{tb}",
        }

    # Find the result object — prefer ``part``, fall back to the last
    # non-dunder, non-module variable assigned.
    part = namespace.get("part")

    if part is None:
        # Try to find any Stock or Workplane in the namespace
        for name in reversed(list(namespace.keys())):
            if name.startswith("_"):
                continue
            val = namespace[name]
            if _is_stock(val) or _is_workplane(val):
                part = val
                break

    if part is None:
        # Last resort: scan for any CadQuery/Stock object
        for name, val in namespace.items():
            if name.startswith("_"):
                continue
            if _is_stock(val) or _is_workplane(val):
                part = val
                break

    if part is None:
        return {
            "success": False,
            "error": (
                "No 'part' variable found in executed code. "
                "Make sure the subCAD code assigns the final Stock "
                "to a variable named 'part'."
            ),
        }

    # --- Extract geometry data ---
    volume = 0.0
    faces = 0
    process_plan = None

    try:
        if _is_stock(part):
            volume = part.volume
            process_plan = part.process_plan()
        elif _is_workplane(part):
            volume = compute_volume(part)
        else:
            return {
                "success": False,
                "error": f"Variable 'part' is not a Stock or CadQuery Workplane: {type(part)}",
            }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to extract volume: {e}",
        }

    # Face count from the B-Rep shape
    try:
        shape = _get_shape(part)
        if shape is not None:
            faces = len(shape.Faces())
    except Exception:
        faces = 0

    # --- Export STEP and STL to temp files ---
    step_path: Optional[str] = None
    stl_path: Optional[str] = None

    try:
        if _is_stock(part):
            # Stock has its own export methods
            fd, step_path = tempfile.mkstemp(suffix=".step")
            os.close(fd)
            part.to_step(step_path)
        elif _is_workplane(part):
            fd, step_path = tempfile.mkstemp(suffix=".step")
            os.close(fd)
            export_step(part, step_path)
    except Exception:
        step_path = None

    try:
        if _is_stock(part):
            fd, stl_path = tempfile.mkstemp(suffix=".stl")
            os.close(fd)
            part.to_stl(stl_path)
        elif _is_workplane(part):
            fd, stl_path = tempfile.mkstemp(suffix=".stl")
            os.close(fd)
            export_stl(part, stl_path)
    except Exception:
        stl_path = None

    return {
        "success": True,
        "volume": volume,
        "faces": faces,
        "part": part,
        "step_path": step_path,
        "stl_path": stl_path,
        "process_plan": process_plan,
    }


# =============================================================================
#  Comparison to reference
# =============================================================================

def compare_to_reference(part_or_path, reference_path: str) -> dict:
    """Compare an executed part (or its STEP export) to a reference STEP file.

    Computes volume ratio, absolute volume difference, and a boolean match
    indicator.  Uses CadQuery for STEP import (cascadio is unavailable) and
    falls back to trimesh for non-STEP formats.

    Args:
        part_or_path: Either a path to a STEP/STL file, a ``Stock`` instance,
                      or a CadQuery ``Workplane`` object.
        reference_path: Absolute path to the reference STEP file.

    Returns:
        ``{"volume_ratio": float, "volume_diff": float,
           "target_volume": float, "candidate_volume": float,
           "ok": bool, "match": bool}``

        ``match`` and ``ok`` are True when ``volume_ratio`` is within 10%
        of 1.0 (``0.9 <= ratio <= 1.1``).  ``ok`` is provided for backwards
        compatibility; ``match`` is the canonical key used by the translator.
    """
    # Resolve candidate volume
    candidate_volume: float = 0.0
    candidate_ok = False

    try:
        if isinstance(part_or_path, str):
            # Path to a file
            candidate_volume = _load_volume_from_file(part_or_path)
            candidate_ok = True
        elif _is_stock(part_or_path):
            candidate_volume = part_or_path.volume
            candidate_ok = True
        elif _is_workplane(part_or_path):
            from src.subcad.geometry import compute_volume
            candidate_volume = compute_volume(part_or_path)
            candidate_ok = True
        else:
            return {
                "volume_ratio": 0.0,
                "volume_diff": 0.0,
                "target_volume": 0.0,
                "candidate_volume": 0.0,
                "ok": False,
                "match": False,
                "error": f"Unsupported type for part_or_path: {type(part_or_path)}",
            }
    except Exception as e:
        return {
            "volume_ratio": 0.0,
            "volume_diff": 0.0,
            "target_volume": 0.0,
            "candidate_volume": 0.0,
            "ok": False,
            "match": False,
            "error": f"Failed to load candidate volume: {e}",
        }

    # Resolve reference volume
    target_volume: float = 0.0
    try:
        target_volume = _load_volume_from_file(reference_path)
    except Exception as e:
        return {
            "volume_ratio": 0.0,
            "volume_diff": 0.0,
            "target_volume": 0.0,
            "candidate_volume": candidate_volume,
            "ok": False,
            "match": False,
            "error": f"Failed to load reference volume: {e}",
        }

    # Compute ratio and difference
    if target_volume <= 0.0:
        volume_ratio = 0.0
        volume_diff = abs(candidate_volume - target_volume)
    else:
        volume_ratio = candidate_volume / target_volume
        volume_diff = abs(candidate_volume - target_volume)

    # A part is considered a match when volume is within 10% of reference.
    # The ConvergenceController uses a tighter tolerance (default 5%), so
    # this is a loose gate.
    match = 0.9 <= volume_ratio <= 1.1

    return {
        "volume_ratio": round(volume_ratio, 6),
        "volume_diff": round(volume_diff, 2),
        "target_volume": round(target_volume, 1),
        "candidate_volume": round(candidate_volume, 1),
        "ok": match,
        "match": match,
    }


# =============================================================================
#  Feedback formatting
# =============================================================================

def format_feedback(code: str, exec_result: dict, comparison: dict) -> str:
    """Format execution and comparison results as human-readable LLM feedback.

    The returned string is injected into the iteration prompt so the LLM
    can understand what went wrong and how to improve.

    Args:
        code: The subCAD source code that was executed (may be truncated if long).
        exec_result: Return value from :func:`run_subcad`.
        comparison: Return value from :func:`compare_to_reference`.

    Returns:
        A formatted feedback string.
    """
    lines: list[str] = []

    # --- Execution status ---
    if exec_result.get("success"):
        lines.append("[EXECUTION] OK")
        lines.append(f"  Volume: {exec_result.get('volume', 0):.1f} mm^3")
        lines.append(f"  Faces: {exec_result.get('faces', 0)}")

        plan = exec_result.get("process_plan")
        if plan and isinstance(plan, dict):
            ops = plan.get("operations", [])
            if ops:
                lines.append(f"  Operations recorded: {len(ops)}")
                for op in ops[:5]:  # show at most 5
                    if isinstance(op, dict):
                        op_name = op.get("operation", "?")
                        op_depth = op.get("depth_mm", "")
                    else:
                        op_name = str(op)
                        op_depth = ""
                    lines.append(f"    - {op_name}" +
                                 (f" (depth={op_depth}mm)" if op_depth else ""))
                if len(ops) > 5:
                    lines.append(f"    ... and {len(ops) - 5} more")
    else:
        lines.append("[EXECUTION] FAILED")
        err = exec_result.get("error", "Unknown error")
        # Truncate very long tracebacks
        if len(err) > 800:
            err = err[:800] + "\n... (truncated)"
        lines.append(f"  Error: {err}")

    # --- Volume comparison ---
    lines.append("")
    lines.append("[COMPARISON]")
    if comparison.get("error"):
        lines.append(f"  Error: {comparison['error']}")
    else:
        vol_ratio = comparison.get("volume_ratio", 0)
        vol_diff = comparison.get("volume_diff", 0)
        target_vol = comparison.get("target_volume", 0)
        candidate_vol = comparison.get("candidate_volume", 0)

        lines.append(f"  Reference volume:  {target_vol:.1f} mm^3")
        lines.append(f"  SubCAD volume:     {candidate_vol:.1f} mm^3")
        lines.append(f"  Volume ratio:      {vol_ratio:.4f}")
        lines.append(f"  Volume difference: {vol_diff:.1f} mm^3")

        if vol_ratio > 0:
            pct = abs(vol_ratio - 1.0) * 100
            if vol_ratio < 1.0:
                lines.append(f"  SubCAD is {pct:.1f}% SMALLER than reference.")
            else:
                lines.append(f"  SubCAD is {pct:.1f}% LARGER than reference.")

        if comparison.get("match"):
            lines.append("  Status: MATCH (within 10%)")
        else:
            lines.append("  Status: MISMATCH (outside 10% tolerance)")

    return "\n".join(lines)


# =============================================================================
#  Internal helpers
# =============================================================================

def _generated_code_guard(code: str) -> str | None:
    """Reject generated SubCAD patterns known to erase retained geometry."""
    code_no_comments = re.sub(r"#.*", "", code)
    lowered = code_no_comments.lower()
    retained_tokens = [
        ".machine_around_profile(",
        ".machine_around_profiles(",
        ".machine_around_cylinder(",
        ".rib(",
        ".pad(",
    ]
    retained_positions = [lowered.find(token) for token in retained_tokens if token in lowered]
    if not retained_positions:
        return None
    first_retained = min(position for position in retained_positions if position >= 0)
    later_face_mill = lowered.find(".face_mill(", first_retained + 1)
    if later_face_mill >= 0:
        return (
            "Generated SubCAD sequencing error: face_mill appears after retained "
            "boss/rib/pad machining. Face milling after machine_around/rib/pad "
            "operations erases retained material. Move face_mill before retained "
            "operations or replace it with the correct base/level retained cut."
        )
    height_error = _face_mill_before_retained_height_error(code_no_comments, lowered, first_retained)
    if height_error:
        return height_error
    return None


def _face_mill_before_retained_height_error(
    code_no_comments: str,
    lowered: str,
    first_retained: int,
) -> str | None:
    """Detect facing stock below later retained Z-band requirements."""
    face_index = lowered.find(".face_mill(", 0, first_retained)
    if face_index < 0:
        return None
    env = _simple_numeric_env(code_no_comments)
    stock_height = _first_stock_height(code_no_comments, env)
    face_depth = _first_call_kw_or_arg(code_no_comments[face_index:], "face_mill", "depth", env)
    if stock_height is None or face_depth is None:
        return None
    remaining_height = stock_height - face_depth
    required_top = _max_retained_top(code_no_comments[first_retained:], env)
    if required_top is None:
        return None
    if remaining_height + 1e-6 < required_top:
        return (
            "Generated SubCAD sequencing error: face_mill removes stock below "
            f"later retained feature height. Remaining height is {remaining_height:.3g} mm, "
            f"but retained operations require material up to {required_top:.3g} mm. "
            "Use final stock height and Z-band retained/base cuts instead of "
            "facing down to base thickness before boss/rib machining."
        )
    return None


def _simple_numeric_env(code: str) -> dict[str, float]:
    env: dict[str, float] = {}
    for name, expr in re.findall(r"^\s*([A-Za-z_]\w*)\s*=\s*([0-9A-Za-z_ .+*/()\\-]+)\s*$", code, re.MULTILINE):
        value = _eval_simple_expr(expr, env)
        if value is not None:
            env[name] = value
    return env


def _eval_simple_expr(expr: str, env: dict[str, float]) -> float | None:
    try:
        allowed = {"__builtins__": {}}
        value = eval(expr, allowed, dict(env))
        return float(value) if isinstance(value, (int, float)) else None
    except Exception:
        return None


def _first_stock_height(code: str, env: dict[str, float]) -> float | None:
    match = re.search(r"Stock\.rectangular\s*\((?P<args>[^)]*)\)", code, re.IGNORECASE)
    if not match:
        return None
    args = _split_call_args(match.group("args"))
    kwargs = _call_kwargs(args, env)
    if "height" in kwargs:
        return kwargs["height"]
    if len(args) >= 3 and "=" not in args[2]:
        return _eval_simple_expr(args[2], env)
    return None


def _first_call_kw_or_arg(segment: str, call_name: str, kw_name: str, env: dict[str, float]) -> float | None:
    match = re.search(rf"\.{re.escape(call_name)}\s*\((?P<args>[^)]*)\)", segment, re.IGNORECASE)
    if not match:
        return None
    args = _split_call_args(match.group("args"))
    kwargs = _call_kwargs(args, env)
    if kw_name in kwargs:
        return kwargs[kw_name]
    if args and "=" not in args[0]:
        return _eval_simple_expr(args[0], env)
    return None


def _max_retained_top(segment: str, env: dict[str, float]) -> float | None:
    tops: list[float] = []
    for match in re.finditer(
        r"\.machine_around_(?:profile|profiles|cylinder)\s*\((?P<args>[^)]*)\)",
        segment,
        re.IGNORECASE | re.DOTALL,
    ):
        args = _split_call_args(match.group("args"))
        kwargs = _call_kwargs(args, env)
        height = kwargs.get("height")
        if height is None and "cylinder" in match.group(0).lower() and len(args) >= 2:
            height = _eval_simple_expr(args[1], env)
        if height is None and len(args) >= 2:
            height = _eval_simple_expr(args[1], env)
        base_height = kwargs.get("base_height", 0.0)
        if height is not None:
            tops.append(base_height + height)
    return max(tops) if tops else None


def _split_call_args(arg_text: str) -> list[str]:
    args: list[str] = []
    start = 0
    depth = 0
    for index, char in enumerate(arg_text):
        if char in "([{":
            depth += 1
        elif char in ")]}":
            depth -= 1
        elif char == "," and depth == 0:
            args.append(arg_text[start:index].strip())
            start = index + 1
    tail = arg_text[start:].strip()
    if tail:
        args.append(tail)
    return args


def _call_kwargs(args: list[str], env: dict[str, float]) -> dict[str, float]:
    kwargs: dict[str, float] = {}
    for arg in args:
        if "=" not in arg:
            continue
        key, value = arg.split("=", 1)
        number = _eval_simple_expr(value.strip(), env)
        if number is not None:
            kwargs[key.strip()] = number
    return kwargs


def _is_stock(obj) -> bool:
    """Return True if *obj* is a subCAD ``Stock`` instance."""
    try:
        from src.subcad import Stock
        return isinstance(obj, Stock)
    except ImportError:
        return False


def _is_workplane(obj) -> bool:
    """Return True if *obj* is a CadQuery ``Workplane`` instance."""
    if not _HAS_CADQUERY:
        return False
    return isinstance(obj, cq.Workplane)


def _get_shape(part):
    """Extract the underlying CadQuery ``Shape`` from a Stock or Workplane."""
    try:
        if _is_stock(part):
            return part._shape.val()
        if _is_workplane(part):
            return part.val()
    except Exception:
        pass
    return None


def _load_volume_from_file(filepath: str) -> float:
    """Load volume from a geometry file.

    Uses CadQuery's STEP importer for ``.step``/``.stp`` files (cascadio is
    unavailable).  Falls back to trimesh for ``.stl`` and other mesh formats.
    """
    ext = os.path.splitext(filepath)[1].lower()

    if ext in (".step", ".stp"):
        return _step_volume_cadquery(filepath)

    if ext in (".stl",):
        return _mesh_volume_trimesh(filepath)

    # Unknown format: try CadQuery first, then trimesh
    try:
        return _step_volume_cadquery(filepath)
    except Exception:
        pass

    return _mesh_volume_trimesh(filepath)


def _step_volume_cadquery(filepath: str) -> float:
    """Load a STEP file using CadQuery's built-in importer and return volume.

    Raises RuntimeError if CadQuery is not available or the import fails.
    """
    if not _HAS_CADQUERY:
        raise RuntimeError("CadQuery is not available for STEP import")

    # Use CadQuery's importStep (does NOT require cascadio)
    shape = cq.importers.importStep(filepath)
    # shape is a cadquery.Workplane; extract the solid and compute volume
    solid = shape.val()
    return float(solid.Volume())


def _mesh_volume_trimesh(filepath: str) -> float:
    """Load a mesh file using trimesh and return volume.

    Raises RuntimeError if trimesh is not available or the load fails.
    """
    if not _HAS_TRIMESH:
        raise RuntimeError("trimesh is not available for mesh import")

    mesh = trimesh.load(filepath)
    if mesh is None:
        raise RuntimeError(f"trimesh.load returned None for {filepath}")
    return float(mesh.volume)


# =============================================================================
#  Self-test
# =============================================================================

if __name__ == "__main__":
    print("=== subcad_repl Self-Test ===\n")

    if not _HAS_CADQUERY:
        print("SKIP: cadquery not installed. "
              "Self-tests require cadquery for Stock execution.")
        sys.exit(0)

    _counts = {"passed": 0, "failed": 0}

    def _check(label: str, condition: bool, detail: str = ""):
        if condition:
            _counts["passed"] += 1
            print(f"  PASS  {label}")
        else:
            _counts["failed"] += 1
            print(f"  FAIL  {label}  -- {detail}")

    # ------------------------------------------------------------------
    # Test 1: run_subcad with valid code (Stock.rectangular)
    # ------------------------------------------------------------------
    print("1. run_subcad with valid subCAD code ...")
    code = (
        "from src.subcad import Stock\n"
        "part = Stock.rectangular(100, 50, 20)\n"
    )
    result = run_subcad(code)

    _check("success is True", result["success"],
           f"error: {result.get('error', '')[:100]}")
    _check("volume > 0", result.get("volume", 0) > 0,
           f"got {result.get('volume')}")
    _check("faces >= 6", result.get("faces", 0) >= 6,
           f"got {result.get('faces')}")
    _check("step_path set", result.get("step_path") is not None)
    _check("process_plan is dict", isinstance(result.get("process_plan"), dict))
    _check("part is Stock", _is_stock(result.get("part")),
           f"got {type(result.get('part'))}")

    step_path_val = result.get("step_path")
    print()

    # ------------------------------------------------------------------
    # Test 2: compare_to_reference (self-comparison should match)
    # ------------------------------------------------------------------
    print("2. compare_to_reference (should match itself) ...")
    if step_path_val and os.path.exists(step_path_val):
        comp = compare_to_reference(step_path_val, step_path_val)
        _check("match is True", comp.get("match") is True)
        _check("volume_ratio ~1.0", abs(comp.get("volume_ratio", 0) - 1.0) < 0.001,
               f"got {comp.get('volume_ratio')}")
        _check("target_volume > 0", comp.get("target_volume", 0) > 0)
        _check("candidate_volume > 0", comp.get("candidate_volume", 0) > 0)
    else:
        print("  SKIP: no STEP file produced")
    print()

    # ------------------------------------------------------------------
    # Test 3: run_subcad with code that creates a full chain
    # ------------------------------------------------------------------
    print("3. run_subcad with multi-op chain ...")
    code_chain = (
        "from src.subcad import Stock\n"
        "part = (Stock.rectangular(100, 50, 20)\n"
        "    .face_mill(depth=1.0)\n"
        "    .pocket(width=30, length=20, depth=5)\n"
        "    .drill(diameter=6, cx=25, cy=10, depth=15)\n"
        "    .chamfer(width=0.5)\n"
        ")\n"
    )
    result_chain = run_subcad(code_chain)

    _check("success", result_chain["success"],
           f"error: {result_chain.get('error', '')[:100]}")
    _check("volume < stock volume", result_chain.get("volume", 0) < 100 * 50 * 20)
    _check("operations >= 4",
           len(result_chain.get("process_plan", {}).get("operations", [])) >= 4,
           f"got {len(result_chain.get('process_plan', {}).get('operations', []))}")

    chain_step = result_chain.get("step_path")
    if chain_step:
        os.unlink(chain_step)
    chain_stl = result_chain.get("stl_path")
    if chain_stl:
        os.unlink(chain_stl)
    print()

    # ------------------------------------------------------------------
    # Test 4: run_subcad with invalid code
    # ------------------------------------------------------------------
    print("4. run_subcad with invalid code ...")
    result_err = run_subcad("part = undefined_var + 1")
    _check("success is False", result_err["success"] is False)
    _check("error is string", isinstance(result_err.get("error"), str))
    _check("error has content", len(result_err.get("error", "")) > 0)
    print()

    # ------------------------------------------------------------------
    # Test 5: run_subcad with no 'part' variable
    # ------------------------------------------------------------------
    print("5. run_subcad with no 'part' variable ...")
    result_nopart = run_subcad("x = 42\ny = 'hello'\n")
    _check("success is False", result_nopart["success"] is False)
    _check("error mentions 'part'", "part" in result_nopart.get("error", "").lower())
    print()

    # ------------------------------------------------------------------
    # Test 6: format_feedback with successful result
    # ------------------------------------------------------------------
    print("6. format_feedback ...")
    exec_ok = {"success": True, "volume": 95000.0, "faces": 6,
               "process_plan": {"operations": [
                   {"operation": "face_mill", "depth_mm": 1.0},
                   {"operation": "rough_pocket", "depth_mm": 5.0},
               ]}}
    comp_ok = {"volume_ratio": 0.95, "volume_diff": 5000.0,
               "target_volume": 100000.0, "candidate_volume": 95000.0,
               "match": True}
    fb1 = format_feedback("Stock.rectangular(100,50,20)", exec_ok, comp_ok)
    _check("feedback includes 'EXECUTION'", "[EXECUTION]" in fb1)
    _check("feedback includes 'COMPARISON'", "[COMPARISON]" in fb1)
    _check("feedback includes volume", "95000" in fb1)

    exec_fail = {"success": False, "error": "NameError: name 'part' is not defined"}
    comp_fail = {"volume_ratio": 0.0, "error": "Execution failed"}
    fb2 = format_feedback("", exec_fail, comp_fail)
    _check("feedback includes 'FAILED'", "FAILED" in fb2)
    _check("feedback includes error", "NameError" in fb2)

    # ------------------------------------------------------------------
    # Test 7: compare_to_reference with non-existent path
    # ------------------------------------------------------------------
    print("7. compare_to_reference with bad path ...")
    comp_bad = compare_to_reference("/nonexistent/path.step", "/also/bad.step")
    _check("match is False", comp_bad.get("match") is False)
    _check("error present", "error" in comp_bad)
    print()

    # ------------------------------------------------------------------
    # Cleanup
    # ------------------------------------------------------------------
    if step_path_val and os.path.exists(step_path_val):
        os.unlink(step_path_val)
    stl_path = result.get("stl_path")
    if stl_path and os.path.exists(stl_path):
        os.unlink(stl_path)

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    total = _counts["passed"] + _counts["failed"]
    print(f"=== {'ALL TESTS PASSED' if _counts['failed'] == 0 else 'SOME TESTS FAILED'} "
          f"({_counts['passed']}/{total} passed) ===")
    if _counts["failed"] > 0:
        sys.exit(1)
