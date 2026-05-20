"""Focused test for SubCAD visualization package export."""

import json
import os
import shutil
import sys
import tempfile

from src.subcad import FixtureCatalog, Stock
from src.subcad.geometry import _HAS_CADQUERY

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


print("=" * 60)
print("SubCAD Visualization Package Test")
print("=" * 60)

tmp_dir = tempfile.mkdtemp()
try:
    part = (
        Stock.rectangular(60, 40, 16, material="aluminum_6061")
        .with_fixture(FixtureCatalog.get("kurt_dx6_vise"))
        .new_setup("op1_top", face_selector=">Z", work_offset="G54")
        .face_mill(depth=1.0)
        .pocket(width=18, length=24, depth=4, cx=0, cy=0)
        .drill(diameter=5, depth=10, cx=12, cy=6, spot_drill=False)
    )

    package_dir = os.path.join(tmp_dir, "viz")
    scene = part.visualization_package(package_dir)

    scene_path = os.path.join(package_dir, "scene.json")
    toolpath_path = os.path.join(package_dir, "toolpath.json")
    stock_path = os.path.join(package_dir, "stock.stl")

    check("scene dict returned", isinstance(scene, dict))
    check("scene.json written", os.path.exists(scene_path))
    check("toolpath.json written", os.path.exists(toolpath_path))
    check("stock.stl written", os.path.getsize(stock_path) > 1000)

    with open(scene_path, "r", encoding="utf-8") as fh:
        scene_json = json.load(fh)
    with open(toolpath_path, "r", encoding="utf-8") as fh:
        toolpath_json = json.load(fh)

    check("scene schema version present", scene_json.get("schema_version") == "subcad.visualization_package.v1")
    check("scene references stock mesh", scene_json["assets"]["stock_mesh"]["path"] == "stock.stl")
    check("scene references toolpath", scene_json["assets"]["toolpath"]["path"] == "toolpath.json")
    stock_states = scene_json["assets"].get("stock_states", [])
    check("scene references stock state timeline", len(stock_states) == part.process_plan()["total_operations"] + 1)
    check("scene exports fixtures", len(scene_json.get("fixtures", [])) == 1)
    check("fixture asset metadata present", "fixtures" in scene_json["assets"])
    check("fixture clamp zones exported", len(scene_json["fixtures"][0].get("clamping_zones", [])) > 0)
    check("operation exports tool assembly", all(op.get("tool_assembly") for op in scene_json["operations"]))
    check("timeline starts from initial stock", stock_states[0]["sequence_number"] == 0)
    check("timeline ends after final operation", stock_states[-1]["sequence_number"] == part.process_plan()["total_operations"])
    check(
        "timeline state meshes written",
        all(os.path.getsize(os.path.join(package_dir, state["path"])) > 0 for state in stock_states),
    )
    check("scene operations mirror plan", len(scene_json["operations"]) == part.process_plan()["total_operations"])
    check("toolpath has operations", len(toolpath_json["operations"]) == part.process_plan()["total_operations"])
    check("toolpath has moves", toolpath_json["summary"]["move_count"] > 0)

    target_dir = os.path.join(tmp_dir, "viz_with_target")
    target_scene = part.visualization_package(
        target_dir,
        target=part,
        tolerance_mm=0.25,
        include_diff_mesh=True,
    )
    check("target scene returned", isinstance(target_scene, dict))
    check("target.stl written", os.path.getsize(os.path.join(target_dir, "target.stl")) > 1000)
    check("comparison.json written", os.path.exists(os.path.join(target_dir, "comparison.json")))
    check("scene references comparison", target_scene["assets"]["comparison"]["path"] == "comparison.json")

    diff_asset = target_scene["assets"].get("diff_mesh")
    if diff_asset is not None:
        diff_path = os.path.join(target_dir, diff_asset["path"])
        check("optional diff mesh exists when referenced", os.path.exists(diff_path))
finally:
    shutil.rmtree(tmp_dir, ignore_errors=True)

total = passed + failed
print("=" * 60)
if failed == 0:
    print(f"Visualization package test: ALL {passed}/{total} PASSED")
else:
    print(f"Visualization package test: {passed}/{total} passed, {failed} FAILED")
    sys.exit(1)
