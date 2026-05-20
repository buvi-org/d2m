"""Acceptance tests for SubCAD Manufacturing Economics v1."""

from __future__ import annotations

import os
import shutil
import sys
import tempfile

from src.subcad import Stock, compare_programs, estimate_cost
from src.subcad.geometry import _HAS_CADQUERY


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


def close(actual: float, expected: float, tolerance: float = 1e-6) -> bool:
    return abs(float(actual) - float(expected)) <= tolerance


def base_plan(operations: list[dict]) -> dict:
    return {
        "schema_version": "subcad.shop_floor.v1",
        "material": "aluminum_6061",
        "stock_dimensions": {"length": 100, "width": 50, "height": 20},
        "estimated_time_minutes": sum(
            op.get("toolpath_summary", {}).get("estimated_time_min", 0.0)
            for op in operations
        ),
        "operations": operations,
        "setups": {"op1": {"name": "op1"}},
        "validation_buckets": {"errors": [], "warnings": [], "notes": []},
    }


def op(sequence: int, tool_id: str, minutes: float, tool_cost_per_min: float | None = None) -> dict:
    tool = {"catalog_id": tool_id}
    if tool_cost_per_min is not None:
        tool["cost_per_cutting_min"] = tool_cost_per_min
    return {
        "sequence_number": sequence,
        "operation": "test_cut",
        "tool": tool,
        "toolpath_summary": {"estimated_time_min": minutes},
    }


def test_time_model_and_backward_compatibility() -> None:
    print("\n1. Time model and backward compatibility ...")

    part = (
        Stock.rectangular(60, 40, 16, material="aluminum_6061")
        .face_mill(depth=1.0)
        .pocket(width=18, length=24, depth=4, cx=0, cy=0)
        .drill(diameter=5, depth=10, cx=12, cy=6, spot_drill=False)
    )
    before = part.process_plan()["estimated_time_minutes"]
    report = part.estimate_cost(machine="generic_3axis_mill", quantity=1)
    after = part.process_plan()["estimated_time_minutes"]
    time = report["time_breakdown"]

    check("old estimated_time_minutes remains unchanged", before == after, (before, after))
    check("cutting time remains separate", time["cutting_time_min"] > 0, time)
    check("tool changes have explicit duration", time["tool_change_count"] > 0 and time["tool_change_time_min"] > 0, time)
    check("total time includes non-cutting time", time["total_time_per_part_min"] > time["cutting_time_min"], time)


def test_tool_change_sequence_cost() -> None:
    print("\n2. Tool-change transitions affect total time ...")

    same_tool = base_plan([
        op(1, "EM_12mm", 1.0),
        op(2, "EM_12mm", 1.0),
        op(3, "EM_12mm", 1.0),
    ])
    alternating = base_plan([
        op(1, "EM_12mm", 1.0),
        op(2, "REAM_5mm", 1.0),
        op(3, "EM_12mm", 1.0),
    ])
    same = estimate_cost(same_tool)
    alt = estimate_cost(alternating)

    check("same tool sequence has no in-program changes", same["time_breakdown"]["tool_change_count"] == 0, same)
    check("alternating tools count transitions", alt["time_breakdown"]["tool_change_count"] == 2, alt)
    check("alternating tools increase total time", alt["time_breakdown"]["total_time_per_part_min"] > same["time_breakdown"]["total_time_per_part_min"], (same, alt))


def test_material_tooling_and_quantity_costs() -> None:
    print("\n3. Material, tooling, and quantity costing ...")

    report = estimate_cost(base_plan([op(1, "EM_12mm", 10.0)]), quantity=1)
    material = report["material"]
    cost = report["cost_breakdown"]
    expected_material = 100 * 50 * 20 * 2.70 / 1_000_000.0 * 7.5 * 1.15
    expected_tooling = 10.0 * (82.0 / 300.0)

    check("material mass uses stock dimensions and density", close(material["mass_kg"], 0.27), material)
    check("material cost uses price and waste factor", close(cost["material_cost"], expected_material), cost)
    check("tooling cost uses selected catalog tool life", close(cost["tooling_cost"], expected_tooling), cost)

    one = estimate_cost(base_plan([op(1, "EM_12mm", 2.0)]), quantity=1)
    ten = estimate_cost(base_plan([op(1, "EM_12mm", 2.0)]), quantity=10)
    check(
        "quantity amortizes setup time",
        ten["time_breakdown"]["setup_time_per_part_min"] < one["time_breakdown"]["setup_time_per_part_min"],
        (one["time_breakdown"], ten["time_breakdown"]),
    )
    check(
        "quantity amortizes setup cost",
        ten["cost_breakdown"]["setup_cost"] < one["cost_breakdown"]["setup_cost"],
        (one["cost_breakdown"], ten["cost_breakdown"]),
    )


def test_missing_data_and_program_comparison() -> None:
    print("\n4. Missing data and program comparison ...")

    missing = estimate_cost({
        "material": "mystery_material",
        "stock_dimensions": {"length": 10, "width": 10, "height": 10},
        "operations": [op(1, "UNKNOWN_TOOL", 1.0)],
    }, machine="ghost_machine")
    check("missing cost data returns warnings", len(missing["economics_warnings"]) >= 3, missing["economics_warnings"])
    check("missing cost data does not crash", missing["cost_breakdown"]["total_cost"] >= 0, missing["cost_breakdown"])

    fast_expensive = base_plan([op(1, "FAST_EXPENSIVE", 2.0, tool_cost_per_min=50.0)])
    slow_cheap = base_plan([op(1, "SLOW_CHEAP", 10.0, tool_cost_per_min=0.0)])
    comparison = compare_programs(
        [fast_expensive, slow_cheap],
        weights={"time": 0.5, "cost": 0.5},
    )
    check("comparison identifies fastest", comparison["fastest_index"] == 0, comparison)
    check("comparison identifies cheapest", comparison["cheapest_index"] == 1, comparison)
    check("comparison computes weighted best", comparison["weighted_best_index"] in {0, 1}, comparison)
    check("comparison reports Pareto candidates", set(comparison["pareto_optimal_indices"]) == {0, 1}, comparison)


def test_setup_sheet_and_visualization_economics() -> None:
    print("\n5. Setup sheet and visualization economics output ...")

    part = (
        Stock.rectangular(50, 30, 12, material="aluminum_6061")
        .face_mill(depth=1.0)
        .slot(length=24, width=6, depth=4, cx=0, cy=0)
    )
    economics = part.estimate_cost(quantity=2)
    sheet = part.setup_sheet(economics=economics)
    markdown = part.setup_sheet_markdown(economics=economics)

    check("setup sheet includes economics report", sheet.get("economics", {}).get("schema_version") == "subcad.economics.v1", sheet)
    check("setup sheet exposes total time", sheet.get("total_time_minutes", 0) > sheet.get("estimated_time_minutes", 0), sheet)
    check("setup sheet markdown includes estimate note", "not a production quote" in markdown, markdown)

    tmp_dir = tempfile.mkdtemp()
    try:
        scene = part.visualization_package(os.path.join(tmp_dir, "viz"), economics=economics)
        check("visualization scene includes economics", scene.get("economics", {}).get("schema_version") == "subcad.economics.v1", scene)
        check("visualization operations include economics", all(op.get("economics") for op in scene.get("operations", [])), scene.get("operations"))
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


print("=" * 72)
print("SubCAD Manufacturing Economics v1 Acceptance Test")
print("=" * 72)

test_time_model_and_backward_compatibility()
test_tool_change_sequence_cost()
test_material_tooling_and_quantity_costs()
test_missing_data_and_program_comparison()
test_setup_sheet_and_visualization_economics()

total = passed + failed
print("=" * 72)
print(f"Manufacturing economics v1: {'ALL ' if failed == 0 else ''}{passed}/{total} PASSED")
sys.exit(0 if failed == 0 else 1)
