"""Integration tests for process contexts plus natural placement."""

import sys
from pathlib import Path

from src.subcad import Stock
from src.subcad.geometry import _HAS_CADQUERY
from src.subcad.tooling_context import load_tooling_context
from src.subcad.validation import validate_all


if not _HAS_CADQUERY:
    print("SKIP: CadQuery not available")
    sys.exit(0)


passed = 0
failed = 0


def check(label, condition, detail=""):
    global passed, failed
    if condition:
        passed += 1
        print(f"  PASS  {label}")
    else:
        failed += 1
        print(f"  FAIL  {label}  -- {detail}")


def _drill_positions(part):
    return [
        tuple(round(value, 6) for value in op["position"])
        for op in part.process_plan()["operations"]
        if op["operation"] == "drill"
    ]


root = Path(__file__).resolve().parent
tooling = load_tooling_context(
    root / "tooling" / "sample_tooling.json",
    root / "tooling" / "sample_magazine.json",
)
relaxed_tooling = tooling.to_dict()
for tool in relaxed_tooling["tools"]:
    if tool.get("tool_id") == "T03_DR_6":
        tool["max_feed_mm_per_min"] = 2500

setup_intent = {
    "setup_id": "op1_top",
    "workholding": {"name": "kurt_dx6_vise", "fixture_type": "vise"},
    "part_orientation": {"primary_face": "top"},
    "accessible_faces": ["top"],
    "operation_side": "top",
    "work_offset": "G54",
    "setup_count": 1,
}

quality = {
    "tolerances": {"default": {"linear_mm": 0.1, "methods": ["caliper"]}},
    "inspection": {"required": False, "methods": ["caliper"]},
    "collision_policy": {"enabled": False, "required": False},
}


print("=" * 60)
print("SubCAD Process Context Integration Test")
print("=" * 60)

print("\n1. Context-rich natural drilling matches explicit cx/cy ...")
natural = (
    Stock.rectangular(120, 80, 6)
    .with_process_context(
        machine="generic_3axis",
        controller="generic_3axis_debug",
        setup_intent=setup_intent,
        tooling=relaxed_tooling,
        quality=quality,
    )
    .drill_at(6, depth=5, from_left=10, from_top=12, spot_drill=False)
)
explicit = (
    Stock.rectangular(120, 80, 6)
    .with_process_context(
        machine="generic_3axis",
        controller="generic_3axis_debug",
        setup_intent=setup_intent,
        tooling=relaxed_tooling,
        quality=quality,
    )
    .drill(6, depth=5, cx=-50, cy=28, spot_drill=False)
)
check(
    "natural drill compiles to same position as explicit drill",
    _drill_positions(natural) == _drill_positions(explicit),
    f"{_drill_positions(natural)} != {_drill_positions(explicit)}",
)

plan = natural.process_plan()
check("machine context serialized", plan["machine"]["machine_id"] == "generic_3axis")
check("controller context serialized", plan["controller"]["controller_id"] == "generic_3axis_debug")
check("setup intent serialized", plan["setup_intent"]["setup_id"] == "op1_top")
check("setup metadata generated", plan["setups"]["op1_top"]["face_selector"] == ">Z")
check("operation assigned to generated setup", plan["operations"][0]["setup"] == "op1_top")
check("tooling magazine serialized", plan["tooling"]["magazine"]["capacity"] == 20)
check("quality context serialized", "tolerances" in plan["quality"])

report = natural.validate_shop_floor(structured=True)
check("context-rich natural plan has no validation errors", report.errors == [], report.errors)

print("\n2. Validation catches unsupported process-context choices ...")
bad_plan = {
    "schema_version": "subcad.shop_floor.v1",
    "material": "aluminum_6061",
    "stock_dimensions": {"length": 120, "width": 80, "height": 6},
    "machine": plan["machine"],
    "controller": plan["controller"],
    "setup_intent": setup_intent,
    "tooling": plan["tooling"],
    "quality": {
        "inspection": {
            "required": True,
            "methods": ["on_machine_probe"],
            "requires_probe": True,
        },
        "collision_policy": {"enabled": True, "required": True},
    },
    "collision_policy": {"enabled": True, "required": True},
    "operations": [
        {
            "operation": "thread_mill",
            "tool_type": "thread_mill",
            "tool_diameter_mm": 8.0,
            "position": [0, 0],
            "face_selector": "<Z",
            "controller_cycle": "G234",
            "coolant": "through_spindle",
            "feeds_speeds": {"spindle_rpm": 1000, "feed_rate_mm_per_min": 100},
        }
    ],
}
bad_report = validate_all(bad_plan, bad_plan["stock_dimensions"], structured=True)
codes = {issue.code for issue in bad_report.issues}
for code in (
    "controller_cycle_unsupported",
    "controller_coolant_unsupported",
    "setup_face_not_accessible",
    "tooling_tool_missing",
    "quality_probe_unsupported",
    "collision_toolpath_missing",
):
    check(f"reports {code}", code in codes, codes)

print("\n3. Malformed machine context remains validation-safe ...")
malformed_machine_plan = dict(bad_plan)
malformed_machine_plan["machine"] = {
    "machine_id": "bad_axis_limits",
    "processes": ["milling"],
    "axis_limits": "not-a-dictionary",
}
malformed_report = validate_all(
    malformed_machine_plan,
    malformed_machine_plan["stock_dimensions"],
    structured=True,
)
check("non-dict axis_limits does not crash validation", hasattr(malformed_report, "issues"))

print("\n" + "=" * 60)
print(f"Passed: {passed}")
print(f"Failed: {failed}")
print("=" * 60)

if failed:
    sys.exit(1)
