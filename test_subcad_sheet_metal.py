"""Sheet-metal SubCAD coverage: laser-cut blank plus press-brake bends."""

import os
import shutil
import sys
import tempfile

from src.subcad import Stock
from src.subcad.geometry import _HAS_CADQUERY

if not _HAS_CADQUERY:
    print("SKIP: CadQuery not available")
    sys.exit(0)


def check(condition, label):
    if not condition:
        raise AssertionError(label)
    print(f"  PASS  {label}")


def example_bracket():
    blank = {
        "type": "polygon",
        "points": [
            (-70, -45), (70, -45), (70, -30), (65, -30),
            (65, 30), (70, 30), (70, 45), (-70, 45),
            (-70, 30), (-65, 30), (-65, -30), (-70, -30),
        ],
    }
    return (
        Stock.sheet(140, 90, 1.6, material="steel_a36")
        .laser_cut_profile(blank, kerf_width=0.18)
        .laser_cut_slot(length=18, width=6, cx=-42, cy=0)
        .laser_cut_slot(length=18, width=6, cx=42, cy=0)
        .laser_cut_hole(diameter=4.5, cx=-25, cy=35)
        .laser_cut_hole(diameter=4.5, cx=25, cy=35)
        .laser_cut_hole(diameter=4.5, cx=-25, cy=-35)
        .laser_cut_hole(diameter=4.5, cx=25, cy=-35)
        .press_brake_bend(axis="X", position=25, angle=90, side="positive", radius=2.0)
        .press_brake_bend(axis="X", position=-25, angle=-90, side="negative", radius=2.0)
    )


print("1. Sheet stock and laser-cut operations record sheet-metal intent ...")
flat = (
    Stock.sheet(80, 50, 1.2, material="steel_a36")
    .laser_cut_hole(diameter=6, cx=0, cy=0)
    .laser_cut_slot(length=18, width=5, cx=20, cy=0, angle=30)
)
flat_plan = flat.process_plan()
check(flat_plan["stock_dimensions"]["stock_form"] == "sheet", "sheet stock form recorded")
check(flat_plan["operations"][0]["process"] == "laser_cut", "laser hole uses laser_cut process")
check(flat_plan["operations"][1]["tool_type"] == "fiber_laser", "laser slot records laser tool")
check(flat_plan["operations"][1]["toolpath_summary"]["point_count"] > 10, "laser slot emits contour toolpath")
check(flat.volume < Stock.sheet(80, 50, 1.2, material="steel_a36").volume, "laser cuts remove material")


print("\n2. Two press-brake bends form a visible U-channel bracket ...")
part = example_bracket()
bbox = part.bounding_box
plan = part.process_plan()
check(plan["total_operations"] == 9, "example has 7 laser cuts plus 2 bends")
check(plan["operations"][-2]["operation"] == "press_brake_bend", "first bend recorded")
check(plan["operations"][-1]["bend_line_position_mm"] == -25, "second bend line recorded")
check(bbox["height"] > 20.0, "formed flanges raise bracket height")
check(50.0 < bbox["width"] < 56.0, "base width remains near bend-line spacing")
check(part.volume > 18000, "formed part retains sheet volume after cutting")


print("\n3. Export and visualization package include sheet-metal stock states ...")
tmp_dir = tempfile.mkdtemp()
try:
    step_path = os.path.join(tmp_dir, "sheet_metal_bracket.step")
    part.to_step(step_path)
    check(os.path.getsize(step_path) > 1000, "STEP export written")

    scene = part.visualization_package(os.path.join(tmp_dir, "viz"))
    check(scene["assets"]["toolpath"]["operation_count"] == 9, "visualization includes all operations")
    check(len(scene["assets"]["stock_states"]) == 10, "stock-state timeline includes initial plus operations")
finally:
    shutil.rmtree(tmp_dir, ignore_errors=True)

print("\nALL PASSED")
