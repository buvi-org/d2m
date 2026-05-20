"""Acceptance tests for Phase 2 SubCAD toolpath integration.

Run after Agents 1-4 integrate Phase 2 neutral toolpaths, process-plan
summaries, preview-only G-code export, validation, and estimation behavior:

    python test_subcad_phase2_toolpaths.py
"""

from __future__ import annotations

import importlib
import json
import sys
from typing import Any

from src.subcad import FixtureCatalog, ProcessPlan, Stock, create_operation
from src.subcad.geometry import _HAS_CADQUERY


if not _HAS_CADQUERY:
    print("SKIP: CadQuery not available")
    sys.exit(0)


passed = 0
failed = 0


PHASE2_SPECS: list[tuple[str, dict[str, Any]]] = [
    ("peck_drill", {"diameter": 6, "depth": 18, "cx": -40, "cy": -25}),
    ("ream", {"diameter": 6, "depth": 12, "cx": -20, "cy": -25}),
    ("bore", {"diameter": 16, "depth": 8, "cx": 0, "cy": -25}),
    ("countersink", {"diameter": 5, "countersink_diameter": 10, "depth": 2, "cx": 20, "cy": -25}),
    ("counterbore", {"hole_diameter": 6, "counterbore_diameter": 12, "counterbore_depth": 4, "cx": 40, "cy": -25}),
    ("thread_mill", {"diameter": 8, "pitch": 1.25, "depth": 10, "cx": -30, "cy": 0}),
    ("t_slot", {"length": 30, "width": 8, "depth": 6, "cx": 0, "cy": 0}),
    ("dovetail", {"length": 30, "width": 8, "depth": 5, "cx": 30, "cy": 0}),
    ("groove", {"length": 35, "width": 6, "depth": 4, "cx": -20, "cy": 25}),
    ("surface_3d", {"stepover": 1.0, "depth": 0.4}),
    ("deburr", {}),
    ("spot_face", {"diameter": 14, "depth": 0.5, "cx": 20, "cy": 25}),
]


def check(label: str, condition: bool, detail: str = "") -> None:
    global passed, failed
    if condition:
        passed += 1
        print(f"  PASS  {label}")
    else:
        failed += 1
        print(f"  FAIL  {label} -- {detail}")


def as_dict(value) -> dict:
    if hasattr(value, "to_dict"):
        return value.to_dict()
    if isinstance(value, dict):
        return value
    return {}


def moves_from_toolpath(toolpath) -> list:
    if hasattr(toolpath, "moves"):
        return list(toolpath.moves)
    if isinstance(toolpath, dict):
        if isinstance(toolpath.get("moves"), list):
            return toolpath["moves"]
        if isinstance(toolpath.get("positions"), list):
            return toolpath["positions"]
    if isinstance(toolpath, list):
        return toolpath
    return []


def move_has_position(move) -> bool:
    if hasattr(move, "position"):
        return True
    if isinstance(move, dict):
        return "position" in move or all(k in move for k in ("x", "y", "z"))
    if isinstance(move, (list, tuple)):
        return len(move) >= 3
    return False


def text_of(value) -> str:
    if isinstance(value, str):
        return value
    try:
        return json.dumps(value)
    except TypeError:
        return str(value)


def make_phase2_part() -> Stock:
    fixture = FixtureCatalog.get("kurt_dx6_vise")
    part = Stock.rectangular(140, 90, 35, material="aluminum_6061").with_fixture(fixture)
    part = part.new_setup("op1_top", face_selector=">Z", work_offset="G54")
    part = part.face_mill(depth=1.0)
    for name, kwargs in PHASE2_SPECS:
        part = getattr(part, name)(**kwargs)
    return part


def call_gcode_preview(part: Stock):
    plan = part.process_plan()

    for owner in (part, getattr(part, "_plan", None)):
        if owner is None:
            continue
        for method_name in (
            "to_gcode_preview",
            "gcode_preview",
            "preview_gcode",
            "export_gcode_preview",
        ):
            method = getattr(owner, method_name, None)
            if method is None:
                continue
            try:
                return method()
            except TypeError:
                return method(preview=True)

    for module_name in ("src.subcad.gcode_preview", "src.subcad.gcode"):
        try:
            module = importlib.import_module(module_name)
        except ImportError:
            continue
        for func_name in (
            "to_gcode_preview",
            "gcode_preview",
            "preview_gcode",
            "export_gcode_preview",
        ):
            func = getattr(module, func_name, None)
            if func is not None:
                return func(plan)

    raise AssertionError("No preview-only G-code adapter API found")


def assert_phase2_toolpath_contract() -> None:
    print("\n1. Every Phase 2 op emits a non-empty neutral toolpath ...")
    valid_move_types = {"rapid", "feed", "plunge", "retract", "dwell", "arc"}

    for name, kwargs in PHASE2_SPECS:
        try:
            op = create_operation(name, **kwargs)
            toolpath = op.to_toolpath()
        except Exception as exc:
            check(f"{name} to_toolpath does not raise", False, str(exc))
            continue

        moves = moves_from_toolpath(toolpath)
        payload = as_dict(toolpath)
        check(f"{name} toolpath is non-empty", len(moves) > 0)
        check(f"{name} toolpath serializes", bool(payload))
        check(f"{name} has at least one positioned move", any(move_has_position(m) for m in moves))

        move_types = []
        for move in moves:
            if hasattr(move, "move_type"):
                move_types.append(move.move_type)
            elif isinstance(move, dict):
                move_types.append(move.get("type") or move.get("move_type"))
        check(
            f"{name} uses neutral move types",
            bool(move_types) and all(mt in valid_move_types for mt in move_types if mt),
            f"move_types={move_types}",
        )
        check(f"{name} reports path length", float(payload.get("length_mm", 0.0)) > 0.0)
        check(f"{name} reports estimated path time", float(payload.get("estimated_time_min", 0.0)) > 0.0)


def assert_process_plan_summaries() -> None:
    print("\n2. Process plans include Phase 2 toolpath summaries ...")
    try:
        part = make_phase2_part()
    except Exception as exc:
        check("phase2 part builds for plan summary", False, str(exc))
        return
    plan = part.process_plan()
    ops = {op.get("operation"): op for op in plan.get("operations", [])}

    for name, _kwargs in PHASE2_SPECS:
        op = ops.get(name)
        check(f"plan includes {name}", op is not None)
        if op is None:
            continue
        check(f"{name} has serialized toolpath", bool(op.get("toolpath")))
        summary = op.get("toolpath_summary")
        check(f"{name} has toolpath_summary", isinstance(summary, dict))
        if isinstance(summary, dict):
            count = summary.get("move_count", summary.get("point_count", 0))
            check(f"{name} summary count > 0", count > 0, f"summary={summary}")
            check(f"{name} summary has length", float(summary.get("length_mm", 0.0)) > 0.0)
            check(f"{name} summary has estimated time", float(summary.get("estimated_time_min", 0.0)) > 0.0)


def assert_gcode_preview_contract() -> None:
    print("\n3. Preview-only G-code adapter exposes review metadata ...")
    try:
        preview = call_gcode_preview(make_phase2_part())
    except Exception as exc:
        check("gcode preview API exists", False, str(exc))
        return

    text = text_of(preview).lower()
    check("gcode preview has content", bool(text.strip()))
    check("preview warning is visible", "preview" in text and any(t in text for t in ("not for production", "non-production", "defer")))
    check("units are included", "mm" in text or "g21" in text)
    check("setup/work offset is included", "setup" in text or "g54" in text or "work offset" in text)
    check("tools are included", "tool" in text)
    check("operations are included", "operation" in text or "op " in text)
    check("feeds are included", "feed" in text or "f" in text)


def assert_validation_flags_malformed_toolpaths() -> None:
    print("\n4. Validation flags malformed toolpaths ...")
    try:
        validation = importlib.import_module("src.subcad.validation")
        validate_all = getattr(validation, "validate_all")
    except Exception as exc:
        check("validation API exists", False, str(exc))
        return

    bad_plan = {
        "schema_version": "subcad.shop_floor.v1",
        "material": "aluminum_6061",
        "stock_dimensions": {"length": 80, "width": 50, "height": 20},
        "operations": [
            {
                "operation": "groove",
                "tool_type": "flat_endmill",
                "tool_diameter_mm": 6,
                "depth_mm": 4,
                "feeds_speeds": {"feed_rate_mm_min": 300},
                "toolpath": [
                    {"type": "rapid", "position": [0, 0, 5]},
                    {"type": "feed"},
                    {"type": "warp", "position": [10, 0, -4]},
                ],
            },
            {
                "operation": "spot_face",
                "tool_type": "flat_endmill",
                "tool_diameter_mm": 12,
                "depth_mm": 1,
                "toolpath": [],
            },
        ],
    }

    result = validate_all(bad_plan, bad_plan["stock_dimensions"], structured=True)
    text = text_of(getattr(result, "messages", result)).lower()
    check(
        "malformed toolpath produces validation issue",
        "toolpath" in text and any(t in text for t in ("malformed", "invalid", "empty", "unsupported", "position")),
    )


def assert_estimation_uses_authored_path() -> None:
    print("\n5. Estimated time uses authored path length ...")
    feeds = {"feed_rate_mm_min": 100.0, "feed_rate_mm_per_min": 100.0}
    short = ProcessPlan(
        material="aluminum_6061",
        stock_dimensions={"length": 80, "width": 50, "height": 20},
        operations=[
            {
                "operation": "groove",
                "tool_type": "flat_endmill",
                "tool_diameter_mm": 6,
                "depth_mm": 2,
                "feeds_speeds": feeds,
                "toolpath": [[0, 0, 5], [10, 0, -2]],
            }
        ],
    )
    long = ProcessPlan(
        material="aluminum_6061",
        stock_dimensions={"length": 80, "width": 50, "height": 20},
        operations=[
            {
                "operation": "groove",
                "tool_type": "flat_endmill",
                "tool_diameter_mm": 6,
                "depth_mm": 2,
                "feeds_speeds": feeds,
                "toolpath": [[0, 0, 5], [100, 0, -2], [200, 0, -2]],
            }
        ],
    )

    short_time = short.estimated_time_minutes
    long_time = long.estimated_time_minutes
    check("short authored path estimate is positive", short_time > 0, f"got {short_time}")
    check("long authored path estimate is larger", long_time > short_time * 5, f"short={short_time}, long={long_time}")


if __name__ == "__main__":
    print("=" * 72)
    print("SubCAD Phase 2 Toolpath Acceptance Test")
    print("=" * 72)

    assert_phase2_toolpath_contract()
    assert_process_plan_summaries()
    assert_gcode_preview_contract()
    assert_validation_flags_malformed_toolpaths()
    assert_estimation_uses_authored_path()

    total = passed + failed
    print("=" * 72)
    if failed:
        print(f"Phase 2 toolpaths: {passed}/{total} passed, {failed} failed")
        sys.exit(1)
    print(f"Phase 2 toolpaths: ALL {passed}/{total} PASSED")
