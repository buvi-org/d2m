"""Acceptance tests for the SubCAD Shop-Floor v1 integration contract.

Run after the schema, neutral toolpath, setup-sheet, validation, and simulation
bridge work from the implementation agents is integrated:

    python test_subcad_shopfloor_v1.py
"""

from __future__ import annotations

import importlib
import json
import os
import sys
import tempfile
from pathlib import Path

from src.subcad import FixtureCatalog, Stock
from src.subcad.geometry import _HAS_CADQUERY


if not _HAS_CADQUERY:
    print("SKIP: CadQuery not available")
    sys.exit(0)


passed = 0
failed = 0


def check(label: str, condition: bool, detail: str = "") -> None:
    global passed, failed
    if condition:
        passed += 1
        print(f"  PASS  {label}")
    else:
        failed += 1
        print(f"  FAIL  {label} -- {detail}")


def require(label: str, value, detail: str = ""):
    check(label, value is not None, detail)
    return value


def warnings_as_text(validation_result) -> str:
    if isinstance(validation_result, dict):
        values = []
        for key in ("errors", "warnings", "notes"):
            values.extend(validation_result.get(key, []) or [])
        return "\n".join(str(v) for v in values).lower()
    if isinstance(validation_result, list):
        return "\n".join(str(v) for v in validation_result).lower()
    return str(validation_result).lower()


def make_shopfloor_part() -> Stock:
    fixture = FixtureCatalog.get("kurt_dx6_vise")
    return (
        Stock.rectangular(100, 60, 25, material="aluminum_6061")
        .with_fixture(fixture)
        .new_setup("op1_top", face_selector=">Z", work_offset="G54")
        .face_mill(depth=1.0)
        .pocket(width=30, length=40, depth=6, corner_radius=2)
        .drill(diameter=6, cx=12, cy=8, depth=12)
        .chamfer(width=0.5)
    )


def export_setup_sheet(part: Stock, output_dir: str) -> tuple[dict, str]:
    """Call whichever setup-sheet API the integration exposes."""
    json_path = os.path.join(output_dir, "setup_sheet.json")
    md_path = os.path.join(output_dir, "setup_sheet.md")

    for method_name in (
        "export_setup_sheet",
        "save_setup_sheet",
        "to_setup_sheet",
        "setup_sheet",
    ):
        method = getattr(part, method_name, None)
        if method is None:
            continue

        result = method(json_path) if method_name.startswith(("export", "save", "to")) else method()
        if isinstance(result, dict):
            sheet = result
        elif os.path.exists(json_path):
            with open(json_path, "r", encoding="utf-8") as fh:
                sheet = json.load(fh)
        else:
            sheet = {"text": str(result)}

        text = ""
        if os.path.exists(md_path):
            text = Path(md_path).read_text(encoding="utf-8")
        elif isinstance(result, str):
            text = result
        else:
            text = json.dumps(sheet)
        return sheet, text

    try:
        mod = importlib.import_module("src.subcad.setup_sheet")
    except ImportError:
        return {}, ""

    for func_name in ("export_setup_sheet", "setup_sheet", "build_setup_sheet"):
        func = getattr(mod, func_name, None)
        if func is None:
            continue
        result = func(part, json_path)
        if isinstance(result, dict):
            return result, json.dumps(result)
        if os.path.exists(json_path):
            with open(json_path, "r", encoding="utf-8") as fh:
                sheet = json.load(fh)
            return sheet, json.dumps(sheet)
        return {"text": str(result)}, str(result)

    return {}, ""


def test_schema_v1_required_and_backward_fields() -> None:
    print("\n1. Schema v1 required fields and backward compatibility ...")
    part = make_shopfloor_part()
    plan = part.process_plan()

    check("plan schema_version", plan.get("schema_version") == "subcad.shop_floor.v1")
    for key in (
        "material",
        "stock_dimensions",
        "units",
        "operations",
        "tools_used",
        "total_operations",
        "estimated_time_minutes",
        "tool_change_count",
        "validation",
    ):
        check(f"plan has {key}", key in plan)

    ops = plan.get("operations", [])
    check("operations non-empty", len(ops) > 0)
    for op in ops:
        op_name = op.get("operation", "<missing>")
        check(f"{op_name} has schema_version", op.get("schema_version") == "subcad.shop_floor.v1")
        for legacy_key in ("operation", "tool_type", "tool_diameter_mm"):
            check(f"{op_name} keeps {legacy_key}", legacy_key in op)
        check(f"{op_name} has structured tool", isinstance(op.get("tool"), dict))
        check(f"{op_name} has validation buckets", isinstance(op.get("validation_buckets"), dict))


def test_core_operations_have_neutral_toolpaths() -> None:
    print("\n2. Core operations emit non-empty neutral toolpaths ...")
    try:
        from src.subcad.operations import create_operation
    except ImportError as exc:
        check("create_operation import", False, str(exc))
        return

    core_specs = [
        ("face_mill", {"depth": 1.0}),
        ("pocket", {"width": 20, "length": 30, "depth": 4}),
        ("drill", {"diameter": 6, "depth": 12, "spot_drill": False}),
        ("slot", {"length": 35, "width": 6, "depth": 4}),
        ("chamfer", {"width": 0.5}),
    ]

    for name, kwargs in core_specs:
        op = create_operation(name, **kwargs)
        try:
            toolpath = op.to_toolpath()
        except Exception as exc:
            check(f"{name} toolpath does not raise", False, str(exc))
            continue

        try:
            path_len = len(toolpath)
        except TypeError:
            path_len = 0
        check(f"{name} toolpath is non-empty", path_len > 0)
        if path_len > 0:
            first = toolpath[0]
            serial = first.to_dict() if hasattr(first, "to_dict") else first
            check(f"{name} first move is serializable", isinstance(serial, dict))
            check(f"{name} first move has position", "position" in serial)


def test_setup_sheet_export_contains_shopfloor_sections() -> None:
    print("\n3. Setup-sheet export contains shop-floor sections ...")
    part = make_shopfloor_part()
    with tempfile.TemporaryDirectory() as tmp:
        sheet, text = export_setup_sheet(part, tmp)

    check("setup-sheet export exists", bool(sheet or text))
    combined = (json.dumps(sheet) + "\n" + text).lower()
    for token in ("stock", "material", "tool", "operation", "warning"):
        check(f"setup sheet mentions {token}", token in combined)
    check("setup sheet documents deferred g-code", "g-code" in combined and "defer" in combined)


def test_fluent_phase2_api_works() -> None:
    print("\n4. Fluent Phase 2 API works ...")
    phase2_methods = [
        "peck_drill",
        "ream",
        "bore",
        "countersink",
        "counterbore",
        "thread_mill",
        "t_slot",
        "dovetail",
        "groove",
        "surface_3d",
        "deburr",
        "spot_face",
    ]

    missing = [name for name in phase2_methods if not hasattr(Stock, name)]
    check("Stock exposes Phase 2 fluent methods", not missing, f"missing {missing}")
    if missing:
        return

    part = Stock.rectangular(120, 80, 30, material="aluminum_6061")
    calls = [
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

    for method_name, kwargs in calls:
        try:
            part = getattr(part, method_name)(**kwargs)
            check(f"{method_name} fluent call", isinstance(part, Stock))
        except Exception as exc:
            check(f"{method_name} fluent call", False, str(exc))

    names = [op.get("operation") for op in part.process_plan().get("operations", [])]
    for expected in (
        "peck_drill",
        "ream",
        "bore",
        "countersink",
        "counterbore",
        "thread_mill",
        "t_slot",
        "dovetail",
        "groove",
        "surface_3d",
        "deburr",
        "spot_face",
    ):
        check(f"plan includes {expected}", expected in names)


def test_validation_catches_key_issues() -> None:
    print("\n5. Validation catches key shop-floor issues ...")
    try:
        validation = importlib.import_module("src.subcad.validation")
    except ImportError as exc:
        check("validation module import", False, str(exc))
        return

    validate_all = require("validate_all exists", getattr(validation, "validate_all", None))
    if validate_all is None:
        return

    bad_plan = {
        "material": "",
        "stock_dimensions": {"length": 60, "width": 40, "height": 10},
        "operations": [
            {"operation": "tap", "tool_type": "tap", "tool_diameter_mm": 6, "depth_mm": 8},
            {"operation": "face_mill", "tool_type": "face_mill", "tool_diameter_mm": 50, "depth_mm": 1},
            {"operation": "drill", "tool_type": "drill", "tool_diameter_mm": 6, "depth_mm": 120},
        ],
    }
    result = validate_all(bad_plan, bad_plan["stock_dimensions"])
    text = warnings_as_text(result)
    check("validation returns issues", bool(text))
    check("tap without drill is flagged", "tap" in text and "drill" in text)
    check("face mill order is flagged", "face" in text and "first" in text)
    check("missing material/schema issue is flagged", "material" in text or "schema" in text)


def test_simulation_bridge_toolpath_preference_and_fallback() -> None:
    print("\n6. Simulation bridge prefers neutral toolpaths and keeps fallback ...")
    try:
        stock_mod = importlib.import_module("src.subcad.stock")
        helper = getattr(stock_mod, "_op_to_simple_toolpath", None)
    except ImportError as exc:
        check("stock module import", False, str(exc))
        return

    helper = require("_op_to_simple_toolpath exists", helper)
    if helper is None:
        return

    bbox = {"x_min": -10, "x_max": 10, "y_min": -5, "y_max": 5, "z_max": 3}
    fallback = helper({"operation": "drill", "depth_mm": 4, "position": [1, 2]}, bbox)
    check("legacy operation fallback produces poses", isinstance(fallback, list) and len(fallback) > 0)

    authored = [
        {"type": "rapid", "position": [0, 0, 5]},
        {"type": "plunge", "position": [0, 0, -2]},
        {"type": "retract", "position": [0, 0, 5]},
    ]
    preferred = helper(
        {
            "operation": "drill",
            "depth_mm": 2,
            "position": [5, 5],
            "toolpath": authored,
        },
        bbox,
    )
    check("authored neutral toolpath is preferred", len(preferred) == len(authored))


if __name__ == "__main__":
    print("=" * 72)
    print("SubCAD Shop-Floor v1 Acceptance Test")
    print("=" * 72)

    test_schema_v1_required_and_backward_fields()
    test_core_operations_have_neutral_toolpaths()
    test_setup_sheet_export_contains_shopfloor_sections()
    test_fluent_phase2_api_works()
    test_validation_catches_key_issues()
    test_simulation_bridge_toolpath_preference_and_fallback()

    total = passed + failed
    print("=" * 72)
    if failed:
        print(f"Shop-Floor v1: {passed}/{total} passed, {failed} failed")
        sys.exit(1)
    print(f"Shop-Floor v1: ALL {passed}/{total} PASSED")
