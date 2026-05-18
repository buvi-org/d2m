"""SubCAD validation -- pre-operation feasibility and DFM checks."""

from __future__ import annotations
from typing import Optional


def check_wall_thickness(shape, operation, min_wall_mm: float = 1.0) -> list[str]:
    """Check if an operation would leave walls thinner than min_wall_mm."""
    return []  # placeholder, returns empty for now


def check_tool_reach(operation, stock_dims: dict, tool) -> list[str]:
    """Check if the tool can physically reach the operation position."""
    warnings = []
    # Check if drill/pocket depth exceeds tool flute_length
    flute = getattr(tool, 'flute_length', 50.0)
    depth = getattr(operation, 'depth', 0.0)
    if depth > flute:
        warnings.append(f"Depth ({depth}mm) exceeds tool flute length ({flute}mm).")
    return warnings


def check_operation_order(operations: list[dict]) -> list[str]:
    """Validate operation ordering (face_mill first, chamfer last, etc.)."""
    warnings = []
    op_names = [op.get("operation", "") for op in operations]

    # Face mill should be first
    if "face_mill" in op_names and op_names[0] != "face_mill":
        warnings.append("Face mill should be the first operation for proper datum.")

    # Tap after drill
    for i, name in enumerate(op_names):
        if name == "tap":
            if "drill" not in op_names[:i]:
                warnings.append(f"Tap at position {i} has no preceding drill.")

    return warnings


def validate_all(process_plan_dict: dict, stock_dims: dict,
                 tool_specs: Optional[list] = None) -> list[str]:
    """Run all validation checks against a complete process plan."""
    warnings = []
    ops = process_plan_dict.get("operations", [])
    warnings.extend(check_operation_order(ops))
    # Add more checks as they're implemented
    return warnings


# =============================================================================
#  Self-test
# =============================================================================

if __name__ == "__main__":
    print("=== SubCAD Validation Self-Test ===\n")
    passed = 0
    failed = 0

    def _check(label: str, condition: bool, detail: str = ""):
        global passed, failed
        if condition:
            passed += 1
            print(f"  PASS  {label}")
        else:
            failed += 1
            print(f"  FAIL  {label}  -- {detail}")

    # ------------------------------------------------------------------
    # 1. check_wall_thickness (placeholder)
    # ------------------------------------------------------------------
    print("1. check_wall_thickness ...")
    result = check_wall_thickness(None, None)
    _check("returns list", isinstance(result, list))
    _check("empty for now", len(result) == 0)
    print()

    # ------------------------------------------------------------------
    # 2. check_tool_reach
    # ------------------------------------------------------------------
    print("2. check_tool_reach ...")
    from dataclasses import dataclass

    @dataclass
    class FakeTool:
        flute_length: float = 50.0

    @dataclass
    class FakeOp:
        depth: float = 0.0

    tool = FakeTool(flute_length=30.0)
    shallow_op = FakeOp(depth=10.0)
    w = check_tool_reach(shallow_op, {}, tool)
    _check("shallow op OK", len(w) == 0, f"got {w}")

    deep_op = FakeOp(depth=40.0)
    w = check_tool_reach(deep_op, {}, tool)
    _check("deep op warns", len(w) == 1, f"got {len(w)}")
    if w:
        _check("mentions flute length", "flute" in w[0].lower())
    print()

    # ------------------------------------------------------------------
    # 3. check_operation_order
    # ------------------------------------------------------------------
    print("3. check_operation_order ...")

    # Correct order
    ops_ok = [
        {"operation": "face_mill"},
        {"operation": "drill"},
        {"operation": "tap"},
        {"operation": "chamfer"},
    ]
    w = check_operation_order(ops_ok)
    _check("correct order OK", len(w) == 0, f"got {w}")

    # Face mill not first
    ops_bad1 = [
        {"operation": "drill"},
        {"operation": "face_mill"},
    ]
    w = check_operation_order(ops_bad1)
    _check("face_mill not first warns", len(w) == 1, f"got {len(w)}")

    # Tap without drill
    ops_bad2 = [
        {"operation": "tap"},
    ]
    w = check_operation_order(ops_bad2)
    _check("tap without drill warns", len(w) == 1, f"got {len(w)}")
    print()

    # ------------------------------------------------------------------
    # 4. validate_all
    # ------------------------------------------------------------------
    print("4. validate_all ...")
    plan = {
        "operations": [
            {"operation": "face_mill"},
            {"operation": "drill"},
        ],
    }
    w = validate_all(plan, {})
    _check("returns list", isinstance(w, list))
    _check("no warnings for valid plan", len(w) == 0, f"got {w}")

    plan_bad = {
        "operations": [
            {"operation": "drill"},
            {"operation": "face_mill"},
        ],
    }
    w = validate_all(plan_bad, {})
    _check("warns for bad order", len(w) == 1, f"got {len(w)}")
    print()

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    total = passed + failed
    print(f"=== {'ALL TESTS PASSED' if failed == 0 else 'SOME TESTS FAILED'} "
          f"({passed}/{total} passed) ===")
    if failed > 0:
        import sys
        sys.exit(1)
