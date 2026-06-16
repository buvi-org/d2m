"""Tests for SubCAD tool assembly and magazine context helpers."""

import sys
from pathlib import Path

from src.subcad.tooling_context import (
    ToolAssembly,
    ToolMagazine,
    ToolingContext,
    load_tooling_context,
    required_tool_types,
)


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


def issue_codes(issues):
    return {issue.get("code") for issue in issues}


root = Path(__file__).resolve().parent

print("=" * 60)
print("SubCAD Tooling Context Test")
print("=" * 60)

print("\n1. Tool assemblies load from dictionaries with short and legacy names ...")
tool = ToolAssembly.from_dict({
    "id": "T99_DR_5",
    "type": "drill",
    "diameter": 5.0,
    "flutes": 2,
    "material": "carbide",
    "coating": "TiAlN",
    "stickout": 44.0,
    "holder": "BT40-ER20",
    "interface": "BT40",
    "coolant_through": "true",
    "safe_limits": {"max_rpm": 7000, "max_feed_mm_per_min": 800},
})
tool_dict = tool.to_dict()
check("short id alias works", tool.id == "T99_DR_5", tool)
check("short type alias works", tool.type == "drill", tool)
check("diameter alias is serialized", tool_dict["diameter"] == 5.0, tool_dict)
check("legacy tool_type alias is serialized", tool_dict["tool_type"] == "drill", tool_dict)
check("safe rpm limit is loaded", tool.max_rpm == 7000, tool.max_rpm)
check("coolant-through string is normalized", tool.coolant_through is True, tool.coolant_through)

print("\n2. Tooling and magazine JSON load together ...")
context = load_tooling_context(
    root / "tooling" / "sample_tooling.json",
    root / "tooling" / "sample_magazine.json",
)
check("five sample assemblies loaded", len(context.tools) == 5, len(context.tools))
check("magazine capacity loaded", context.magazine.capacity == 20, context.magazine)
check("magazine interface loaded", context.magazine.interface == "BT40", context.magazine)
check("tool ids are preserved", "T03_DR_6" in context.tool_ids, context.tool_ids)

print("\n3. Lookup by id, type, and operation metadata works ...")
check("lookup by id is case-insensitive", context.find_by_id("t02_em_10").id == "T02_EM_10")
check("lookup by type finds drill", context.find_by_type("drill")[0].id == "T03_DR_6")
op = {
    "operation": "slot",
    "tool": {"catalog_id": "T02_EM_10", "tool_type": "flat_endmill"},
}
check("operation lookup prefers explicit id", context.tool_for_operation(op).id == "T02_EM_10")
op_by_type = {"operation": "surface_3d", "tool_type": "ball_endmill", "tool_diameter_mm": 6.0}
check("operation lookup can use type and diameter", context.tool_for_operation(op_by_type).id == "T05_BALL_6")

print("\n4. Required tool-type helpers preserve order and report gaps ...")
plan = {
    "operations": [
        {"operation": "face_mill", "tool": {"tool_type": "face_mill"}},
        {"operation": "pocket", "tool_type": "flat_endmill", "tool_diameter_mm": 10.0},
        {"operation": "drill", "tool": {"assembly": {"tool_type": "drill"}}},
        {"operation": "chamfer", "tool": {"type": "chamfer"}},
    ]
}
required = required_tool_types(plan)
check("required types preserve first-use order", required == [
    "face_mill",
    "flat_endmill",
    "drill",
    "chamfer",
], required)
required_from_tools = required_tool_types({"tools_used": [{"tool_type": "drill"}, {"type": "ream"}]})
check("tools_used metadata is accepted", required_from_tools == ["drill", "ream"], required_from_tools)
check("sample context covers required types", context.has_required_tool_types(plan))
missing = context.missing_tool_types({"operations": [{"tool_type": "thread_mill"}]})
check("missing tool types are reported", missing == ["thread_mill"], missing)

print("\n5. Interface and capacity checks are validation-friendly ...")
check("BT40 interface passes", context.interfaces_ok("BT40"), context.interface_mismatches("BT40"))
bad_interface_codes = issue_codes(context.interface_mismatches("HSK-A63"))
check("wrong interface flags magazine", "magazine_interface_mismatch" in bad_interface_codes, bad_interface_codes)
check("wrong interface flags loaded tools", "tool_interface_mismatch" in bad_interface_codes, bad_interface_codes)

tight_magazine = ToolMagazine.from_dict({
    "id": "TIGHT_BT40",
    "capacity": 2,
    "interface": "BT40",
    "slots": [
        {"slot": 1, "tool_id": "T01_FACE_50"},
        {"slot": 3, "tool_id": "T03_DR_6"},
    ],
})
tight_context = ToolingContext(tools=context.tools[:3], magazine=tight_magazine)
tight_codes = issue_codes(tight_context.capacity_issues(required_count=3))
check("capacity helper rejects too many tools", not tight_context.has_capacity(3), tight_codes)
check("slot above capacity is reported", "magazine_slot_over_capacity" in tight_codes, tight_codes)
check("required count above capacity is reported", "magazine_capacity_exceeded" in tight_codes, tight_codes)

print("\n6. Speed, feed, and coolant-through helpers use per-tool limits ...")
check("max rpm helper returns tool limit", context.max_rpm_for("T02_EM_10") == 12000)
check("rpm within limit passes", context.supports_rpm("T02_EM_10", 12000))
check("rpm above limit fails", not context.supports_rpm("T02_EM_10", 13000))
check("feed above limit fails", not context.supports_feed("T03_DR_6", 1500))
check("through-coolant drill reports support", context.coolant_through_supported("T03_DR_6"))
check("through-spindle coolant allowed when supported", context.supports_coolant("T03_DR_6", "through_spindle"))
check("through-spindle coolant rejected without support", not context.supports_coolant("T02_EM_10", "through_spindle"))
check("flood coolant remains allowed", context.supports_coolant("T02_EM_10", "flood"))

print("\n7. Context serializes and reloads as plain data ...")
round_trip = load_tooling_context(context.to_dict())
check("round-trip preserves tool count", len(round_trip.tools) == 5, len(round_trip.tools))
check("round-trip preserves magazine", round_trip.magazine.capacity == 20, round_trip.magazine)
check("round-trip preserves aliases", round_trip.to_dict()["tools"][0]["tool_id"] == "T01_FACE_50")

print("\n" + "=" * 60)
print(f"Passed: {passed}")
print(f"Failed: {failed}")
print("=" * 60)

if failed:
    sys.exit(1)
