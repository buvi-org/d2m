"""Focused validation tests for SubCAD Manufacturing Trust v1 clearance checks."""

from __future__ import annotations

import sys

from src.subcad import Stock, ToolRequirement, select_tool
from src.subcad.operations import SlotOp
from src.subcad.tool_library import ToolCatalog, ToolSpec
from src.subcad.validation import ValidationReport, validate_all


passed = failed = 0


def check(label: str, condition: bool, detail: str = "") -> None:
    global passed, failed
    if condition:
        passed += 1
        print(f"  PASS  {label}")
    else:
        failed += 1
        print(f"  FAIL  {label} -- {detail}")


def _tool(tool_id: str = "EM_6_TEST") -> dict:
    return {
        "catalog_id": tool_id,
        "tool_type": "flat_endmill",
        "diameter_mm": 6.0,
        "flute_length_mm": 12.0,
        "assembly": {
            "tool_id": tool_id,
            "tool_type": "flat_endmill",
            "cutter_diameter_mm": 6.0,
            "flute_length_mm": 12.0,
            "shank_diameter_mm": 6.0,
            "stickout_mm": 20.0,
            "holder_id": "ER16_TEST",
            "holder_diameter_mm": 30.0,
            "holder_length_mm": 40.0,
        },
    }


def _base_plan() -> dict:
    return {
        "schema_version": "subcad.shop_floor.v1",
        "material": "aluminum_6061",
        "stock_dimensions": {"length": 80.0, "width": 40.0, "height": 20.0},
        "fixture": {
            "name": "trust_fixture",
            "clamping_zones": [
                {
                    "label": "front_clamp",
                    "x_min": 10.0,
                    "x_max": 20.0,
                    "y_min": -4.0,
                    "y_max": 4.0,
                    "z_min": 0.0,
                    "z_max": 12.0,
                    "margin_mm": 0.0,
                }
            ],
            "clearance_zones": [
                {
                    "label": "holder_keepout",
                    "x_min": 10.0,
                    "x_max": 20.0,
                    "y_min": -5.0,
                    "y_max": 5.0,
                    "z_min": 20.0,
                    "z_max": 45.0,
                    "margin_mm": 0.0,
                }
            ],
        },
        "setups": {
            "op1": {"name": "op1", "face_selector": ">Z", "work_offset": "G54"},
        },
        "operations": [],
    }


print("=" * 72)
print("SubCAD Manufacturing Trust Validation Test")
print("=" * 72)

print("\n1. Sampled cutter envelope catches clamp crossing between endpoints ...")
plan = _base_plan()
plan["operations"] = [
    {
        "operation": "slot",
        "setup": "op1",
        "face_selector": ">Z",
        "tool": _tool("EM_6_TEST"),
        "toolpath": {
            "moves": [
                {"type": "feed", "position": [0.0, 0.0, 3.0]},
                {"type": "feed", "position": [30.0, 0.0, 3.0]},
                {"type": "retract", "position": [30.0, 0.0, 25.0]},
            ]
        },
    }
]
report = validate_all(plan, {}, structured=True)
codes = [issue.code for issue in report.issues]
hits = [issue for issue in report.issues if issue.code == "fixture_toolpath_clearance"]
check("structured report returned", isinstance(report, ValidationReport))
check("sampled clamp hit reported", bool(hits), f"codes={codes}")
if hits:
    hit = hits[0]
    check("operation index recorded", hit.operation_index == 0, hit)
    check("tool id recorded", hit.context.get("tool_id") == "EM_6_TEST", hit.context)
    check("zone recorded", hit.context.get("zone") == "front_clamp", hit.context)
    check("component recorded", hit.context.get("component") == "cutter", hit.context)
    check("clearance context recorded", "clearance_mm" in hit.context, hit.context)

print("\n2. Holder envelope checks fixture clearance zones ...")
plan = _base_plan()
plan["operations"] = [
    {
        "operation": "pocket",
        "setup": "op1",
        "face_selector": ">Z",
        "tool": _tool("EM_6_HOLDER_TEST"),
        "toolpath": {
            "moves": [
                {"type": "feed", "position": [0.0, 0.0, -1.0]},
                {"type": "feed", "position": [30.0, 0.0, -1.0]},
                {"type": "retract", "position": [30.0, 0.0, 25.0]},
            ]
        },
    }
]
report = validate_all(plan, {}, structured=True)
holder_hits = [
    issue for issue in report.issues
    if issue.code == "fixture_toolpath_clearance_zone"
    and issue.context.get("component") == "holder"
]
check("holder clearance zone hit reported", bool(holder_hits), report.messages)
if holder_hits:
    hit = holder_hits[0]
    check("fixture id recorded", hit.context.get("fixture_id") == "trust_fixture", hit.context)
    check("holder zone recorded", hit.context.get("zone") == "holder_keepout", hit.context)
    check("envelope radius recorded", hit.context.get("envelope_radius_mm") == 15.0, hit.context)

print("\n3. High safe path avoids z-overlap false positive ...")
plan = _base_plan()
plan["operations"] = [
    {
        "operation": "slot",
        "setup": "op1",
        "face_selector": ">Z",
        "tool": _tool("EM_6_CLEAR_TEST"),
        "toolpath": {
            "moves": [
                {"type": "rapid", "position": [0.0, 0.0, 60.0]},
                {"type": "rapid", "position": [30.0, 0.0, 60.0]},
                {"type": "retract", "position": [30.0, 0.0, 60.0]},
            ]
        },
    }
]
report = validate_all(plan, {}, structured=True)
clearance_codes = {
    issue.code for issue in report.issues
    if issue.code.startswith("fixture_toolpath_clearance")
}
check("no fixture clearance warning at high z", not clearance_codes, f"got {clearance_codes}")

print("\n4. Legacy validate_all output remains list[str] ...")
legacy = validate_all(_base_plan() | {"operations": plan["operations"]}, {})
check("legacy output is list", isinstance(legacy, list), type(legacy).__name__)
check("legacy list contains strings", all(isinstance(item, str) for item in legacy), legacy)

print("\n5. Tool selector uses available inventory and reports failures ...")
try:
    ToolCatalog.register(
        "TRUST_PROBE_UNAVAILABLE_4",
        ToolSpec("trust_probe", 4.0, flute_length=30.0, catalog_id="TRUST_PROBE_UNAVAILABLE_4", inventory_count=0),
    )
except ValueError:
    pass
try:
    ToolCatalog.register(
        "TRUST_PROBE_AVAILABLE_6",
        ToolSpec("trust_probe", 6.0, flute_length=30.0, catalog_id="TRUST_PROBE_AVAILABLE_6", inventory_count=1),
    )
except ValueError:
    pass
selection = select_tool(ToolRequirement("trust_probe", min_diameter_mm=4.0, max_diameter_mm=8.0))
check("selector chooses available tool", selection.selected_tool is not None and selection.selected_tool.catalog_id == "TRUST_PROBE_AVAILABLE_6", selection.to_dict())
check("selector records unavailable rejection", any("unavailable" in item["reasons"] for item in selection.rejected_tools), selection.to_dict())
missing = select_tool(ToolRequirement("trust_missing_probe", min_diameter_mm=1.0))
check("missing tool reports structured error", missing.selected_tool is None and bool(missing.errors), missing.to_dict())

print("\n6. Pass plans and tool selection reach process plans ...")
small_tool_slot = SlotOp(length=24, width=10, depth=4, tool=ToolSpec("flat_endmill", 2.0, flute_length=20.0))
large_tool_slot = SlotOp(length=24, width=10, depth=4, tool=ToolSpec("flat_endmill", 8.0, flute_length=20.0))
small_passes = small_tool_slot.to_toolpath().metadata["pass_plan"]["total_passes"]
large_passes = large_tool_slot.to_toolpath().metadata["pass_plan"]["total_passes"]
check("smaller slot tool creates more passes", small_passes > large_passes, f"small={small_passes} large={large_passes}")
part = Stock.rectangular(60, 40, 15).slot(length=24, width=8, depth=4)
op = part.process_plan()["operations"][0]
check("operation records selected tool", bool((op.get("tool_selection") or {}).get("selected_tool_id")), op)
check("operation records pass plan", bool(op.get("pass_plan", {}).get("total_passes")), op)

total = passed + failed
print("=" * 72)
print(f"Manufacturing trust validation: {'ALL ' if failed == 0 else ''}{passed}/{total} PASSED")
sys.exit(0 if failed == 0 else 1)
