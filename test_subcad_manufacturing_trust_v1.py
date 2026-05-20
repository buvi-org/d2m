"""Benchmark-style acceptance tests for SubCAD Manufacturing Trust v1.

These tests focus on reliability signals rather than broad feature coverage:
target comparison must catch known-good/known-bad geometry, simulation must
return a stable timing/status-shaped result, and fixture/toolpath interference
must be visible through structured validation.
"""

from __future__ import annotations

import copy
import sys

from src.subcad import FixtureCatalog, Stock
from src.subcad.geometry import _HAS_CADQUERY
from src.subcad.validation import validate_all


if not _HAS_CADQUERY:
    print("SKIP: CadQuery not available")
    sys.exit(0)


passed = 0
failed = 0


def check(label: str, condition: bool, detail="") -> None:
    global passed, failed
    if condition:
        passed += 1
        print(f"  PASS  {label}")
    else:
        failed += 1
        print(f"  FAIL  {label} -- {detail}")


def issue_codes(report) -> set[str]:
    return {issue.code for issue in getattr(report, "issues", [])}


def comparison_has_deviation(result: dict) -> bool:
    return (
        result.get("max_overcut_mm", 0.0) > 0.0
        or result.get("max_undercut_mm", 0.0) > 0.0
        or result.get("overcut_vertices", 0) > 0
        or result.get("undercut_vertices", 0) > 0
    )


def make_slot_part(*, depth: float, cx: float = 0.0) -> Stock:
    return Stock.rectangular(50, 30, 12, material="aluminum_6061").slot(
        length=24,
        width=6,
        depth=depth,
        cx=cx,
        cy=0,
    )


def make_drill_part(*, cx: float) -> Stock:
    return Stock.rectangular(50, 30, 12, material="aluminum_6061").drill(
        diameter=5,
        depth=8,
        cx=cx,
        cy=4,
        spot_drill=False,
    )


def test_target_comparison_benchmark_cases() -> None:
    print("\n1. Target comparison benchmark cases ...")

    target_slot = make_slot_part(depth=4)
    same_slot = make_slot_part(depth=4)
    overcut_slot = make_slot_part(depth=7)
    undercut_slot = make_slot_part(depth=2)
    shifted_slot = make_slot_part(depth=4, cx=8)

    good = same_slot.compare_to_target(target_slot, tolerance_mm=0.2)
    overcut = overcut_slot.compare_to_target(target_slot, tolerance_mm=0.2)
    undercut = undercut_slot.compare_to_target(target_slot, tolerance_mm=0.2)
    shifted = shifted_slot.compare_to_target(target_slot, tolerance_mm=0.2)

    check("same slot geometry passes", good["status"] in {"pass", "warning"}, good)
    check("deeper slot fails as overcut", overcut["status"] == "fail", overcut)
    check("deeper slot reports overcut magnitude", overcut["max_overcut_mm"] > 0.2, overcut)
    check("deeper slot reports overcut regions", len(overcut["overcut_regions"]) > 0, overcut)
    check("shallow slot fails as undercut", undercut["status"] == "fail", undercut)
    check("shallow slot reports undercut magnitude", undercut["max_undercut_mm"] > 0.2, undercut)
    check("shallow slot reports undercut regions", len(undercut["undercut_regions"]) > 0, undercut)
    check("shifted slot fails", shifted["status"] == "fail", shifted)
    check("shifted slot reports mixed deviation", shifted["overcut_vertices"] > 0 and shifted["undercut_vertices"] > 0, shifted)

    target_drill = make_drill_part(cx=8)
    wrong_drill = make_drill_part(cx=-8)
    drill_cmp = wrong_drill.compare_to_target(target_drill, tolerance_mm=0.2)
    check("wrong drill location fails", drill_cmp["status"] == "fail", drill_cmp)
    check("wrong drill location reports deviation", comparison_has_deviation(drill_cmp), drill_cmp)
    check("wrong drill location has feedback text", isinstance(drill_cmp.get("feedback"), str), drill_cmp)


def test_simulation_result_shape_and_timing() -> None:
    print("\n2. Simulation result timing/status shape ...")

    part = (
        Stock.rectangular(50, 30, 12, material="aluminum_6061")
        .face_mill(depth=1)
        .slot(length=24, width=6, depth=4, cx=0, cy=0)
        .drill(diameter=5, depth=8, cx=10, cy=4, spot_drill=False)
    )
    plan = part.process_plan()
    result = part.simulate(toolpath_precision=2.0)

    check("simulation does not return error", "error" not in result, result)
    for key in ("final_volume_mm3", "volume_removed_mm3", "cycle_time_minutes", "ops_simulated"):
        check(f"simulation includes {key}", key in result, result)
    check("simulation final volume is numeric", isinstance(result.get("final_volume_mm3"), (int, float)), result)
    check("simulation removed volume is positive", result.get("volume_removed_mm3", 0) > 0, result)
    check("simulation cycle time is positive", result.get("cycle_time_minutes", 0) > 0, result)
    check("simulation uses process-plan operation count", result.get("ops_simulated") == plan["total_operations"], result)
    check("simulation timing mirrors plan estimate", result.get("cycle_time_minutes") == plan["estimated_time_minutes"], result)
    if "status" in result:
        check("simulation status is structured text", result["status"] in {"pass", "warning", "fail", "error"}, result)


def test_fixture_toolpath_interference_validation() -> None:
    print("\n3. Fixture/toolpath interference validation ...")

    part = (
        Stock.rectangular(120, 80, 20, material="aluminum_6061")
        .with_fixture(FixtureCatalog.get("toe_clamps_4corner"))
        .new_setup("op1_top", face_selector=">Z", work_offset="G54")
        .slot(length=20, width=6, depth=3, cx=0, cy=0)
    )
    safe_plan = part.process_plan()
    safe_report = part.validate_shop_floor(structured=True)
    safe_codes = issue_codes(safe_report)
    check("safe benchmark has structured validation report", hasattr(safe_report, "issues"))
    check("safe benchmark has no clamp toolpath hit", "fixture_toolpath_clearance" not in safe_codes, safe_codes)

    bad_plan = copy.deepcopy(safe_plan)
    bad_plan["operations"][0]["toolpath"] = {
        "safe_z": 5.0,
        "moves": [
            {"type": "rapid", "position": [0, 0, 5.0]},
            {"type": "plunge", "position": [-50, -25, -1.0]},
            {"type": "feed", "position": [50, -25, -1.0]},
            {"type": "retract", "position": [50, -25, 5.0]},
        ],
    }
    bad_report = validate_all(bad_plan, bad_plan["stock_dimensions"], structured=True)
    bad_codes = issue_codes(bad_report)
    check("interference benchmark reports clamp-zone hit", "fixture_toolpath_clearance" in bad_codes, bad_codes)
    issue = next((item for item in bad_report.issues if item.code == "fixture_toolpath_clearance"), None)
    check("interference issue identifies operation", issue is not None and issue.operation_index == 0, getattr(issue, "context", {}))
    check("interference issue identifies clamp zone", issue is not None and "zone" in issue.context, getattr(issue, "context", {}))


print("=" * 72)
print("SubCAD Manufacturing Trust v1 Acceptance Test")
print("=" * 72)

test_target_comparison_benchmark_cases()
test_simulation_result_shape_and_timing()
test_fixture_toolpath_interference_validation()

total = passed + failed
print("=" * 72)
print(f"Manufacturing trust v1: {'ALL ' if failed == 0 else ''}{passed}/{total} PASSED")
sys.exit(0 if failed == 0 else 1)
