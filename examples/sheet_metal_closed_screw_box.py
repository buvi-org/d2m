"""Closed screw-fastened sheet-metal box made from one sheet blank.

This example models a practical one-piece electronics enclosure:

- bottom, four side walls, top lid, and front closing lip are one sheet
- laser-cut corner reliefs allow the walls and lid to fold
- the lid front lip screws to the front wall with M4 screws
- four corner return tabs screw side seams with M3 screws

The final geometry is modeled as the formed enclosure so the rendered result is
a true closed box. The process plan records the flat-blank cutting and bending
sequence needed to make it from one sheet.
"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import cadquery as cq

from examples.sheet_metal_u_bracket import _render_preview_matplotlib, _render_preview_vtk
from src.subcad import ProcessPlan, Stock


OUTPUT_DIR = Path("renders/sheet_metal_closed_screw_box")


def _box(size, center):
    return cq.Workplane("XY").box(*size, centered=True).translate(center)


def _cut_y_hole(shape, *, x: float, z: float, y_center: float, diameter: float, depth: float):
    cutter = (
        cq.Workplane("XZ")
        .center(x, z)
        .circle(diameter / 2.0)
        .extrude(depth)
        .translate((0.0, y_center + depth / 2.0, 0.0))
    )
    return shape.cut(cutter)


def _cut_x_hole(shape, *, y: float, z: float, x_center: float, diameter: float, depth: float):
    cutter = (
        cq.Workplane("YZ")
        .center(y, z)
        .circle(diameter / 2.0)
        .extrude(depth)
        .translate((x_center - depth / 2.0, 0.0, 0.0))
    )
    return shape.cut(cutter)


def build_part():
    """Return a closed screw-fastened enclosure as a SubCAD Stock object."""
    length = 120.0
    width = 80.0
    height = 50.0
    thickness = 1.2
    lid_lip = 22.0
    corner_tab_y = 24.0
    corner_tab_z = 30.0
    material = "steel_a36"

    half_l = length / 2.0
    half_w = width / 2.0

    final = _box((length, width, thickness), (0.0, 0.0, thickness / 2.0))
    panels = [
        _box((length, thickness, height), (0.0, -half_w - thickness / 2.0, height / 2.0)),
        _box((length, thickness, height), (0.0, half_w + thickness / 2.0, height / 2.0)),
        _box((thickness, width, height), (-half_l - thickness / 2.0, 0.0, height / 2.0)),
        _box((thickness, width, height), (half_l + thickness / 2.0, 0.0, height / 2.0)),
        _box((length, width, thickness), (0.0, 0.0, height + thickness / 2.0)),
        _box((length, thickness, lid_lip), (0.0, -half_w - 1.5 * thickness, height - lid_lip / 2.0)),
    ]

    # Corner return tabs overlap the side walls and are screwed through.
    tab_centers = [
        (-half_l - 1.5 * thickness, -half_w + corner_tab_y / 2.0, height / 2.0),
        (half_l + 1.5 * thickness, -half_w + corner_tab_y / 2.0, height / 2.0),
        (-half_l - 1.5 * thickness, half_w - corner_tab_y / 2.0, height / 2.0),
        (half_l + 1.5 * thickness, half_w - corner_tab_y / 2.0, height / 2.0),
    ]
    panels.extend(
        _box((thickness, corner_tab_y, corner_tab_z), center)
        for center in tab_centers
    )

    for panel in panels:
        final = final.union(panel)

    # Three M4 front-lip closure holes, through both the lid lip and front wall.
    for x in (-40.0, 0.0, 40.0):
        final = _cut_y_hole(
            final,
            x=x,
            z=height - lid_lip / 2.0,
            y_center=-half_w - thickness,
            diameter=4.5,
            depth=6.0 * thickness,
        )

    # Two M3 corner seam screws per tab, through tab and side wall.
    for x_center in (-half_l - thickness, half_l + thickness):
        for y in (-half_w + 8.0, -half_w + 18.0, half_w - 8.0, half_w - 18.0):
            for z in (height * 0.35, height * 0.68):
                final = _cut_x_hole(
                    final,
                    y=y,
                    z=z,
                    x_center=x_center,
                    diameter=3.4,
                    depth=6.0 * thickness,
                )

    stock_dims = {
        "length": length + 2.0 * height,
        "width": width + 2.0 * height + lid_lip,
        "height": thickness,
        "thickness": thickness,
        "stock_form": "sheet",
        "process_family": "sheet_metal",
        "formed_enclosure": {
            "inside_length_mm": length,
            "inside_width_mm": width,
            "inside_height_mm": height,
            "lid_lip_mm": lid_lip,
        },
    }
    plan = ProcessPlan(
        material=material,
        stock_dimensions=stock_dims,
        operations=_process_operations(length, width, height, thickness, lid_lip),
    )
    return Stock._from_parts(
        final,
        material,
        stock_dims,
        plan,
        len(plan.operations) + 1,
        state_history=[{
            "sequence_number": plan.total_operations,
            "operation": "formed_closed_box",
            "label": "Final closed screw-fastened box",
            "shape": final,
        }],
    )


def _process_operations(length: float, width: float, height: float, thickness: float, lid_lip: float):
    half_l = length / 2.0
    half_w = width / 2.0
    return [
        {
            "operation": "laser_cut_profile",
            "process": "laser_cut",
            "operation_family": "sheet_metal_cutting",
            "tool_type": "fiber_laser",
            "tool_diameter_mm": 0.18,
            "kerf_width_mm": 0.18,
            "notes": (
                "Cut one-piece enclosure blank: bottom, four walls, top lid, "
                "front screw lip, four corner return tabs, and corner reliefs."
            ),
        },
        {
            "operation": "laser_cut_internal",
            "process": "laser_cut",
            "operation_family": "sheet_metal_cutting",
            "tool_type": "fiber_laser",
            "tool_diameter_mm": 0.18,
            "notes": "Cut 3 x M4.5 front-lip closure holes and 16 x M3.4 corner-tab seam holes.",
        },
        {
            "operation": "press_brake_bend",
            "process": "press_brake",
            "axis": "X",
            "bend_line_position_mm": -half_w,
            "angle_deg": -90,
            "inside_radius_mm": 1.5,
            "sheet_thickness_mm": thickness,
            "tool_type": "press_brake_punch",
            "tool_diameter_mm": 3.0,
            "notes": "Fold front wall up.",
        },
        {
            "operation": "press_brake_bend",
            "process": "press_brake",
            "axis": "X",
            "bend_line_position_mm": half_w,
            "angle_deg": 90,
            "inside_radius_mm": 1.5,
            "sheet_thickness_mm": thickness,
            "tool_type": "press_brake_punch",
            "tool_diameter_mm": 3.0,
            "notes": "Fold back wall up with attached lid panel.",
        },
        {
            "operation": "press_brake_bend",
            "process": "press_brake",
            "axis": "Y",
            "bend_line_position_mm": -half_l,
            "angle_deg": 90,
            "inside_radius_mm": 1.5,
            "sheet_thickness_mm": thickness,
            "tool_type": "press_brake_punch",
            "tool_diameter_mm": 3.0,
            "notes": "Fold left wall up.",
        },
        {
            "operation": "press_brake_bend",
            "process": "press_brake",
            "axis": "Y",
            "bend_line_position_mm": half_l,
            "angle_deg": -90,
            "inside_radius_mm": 1.5,
            "sheet_thickness_mm": thickness,
            "tool_type": "press_brake_punch",
            "tool_diameter_mm": 3.0,
            "notes": "Fold right wall up.",
        },
        {
            "operation": "press_brake_bend",
            "process": "press_brake",
            "axis": "X",
            "bend_line_position_mm": height,
            "angle_deg": 90,
            "inside_radius_mm": 1.5,
            "sheet_thickness_mm": thickness,
            "tool_type": "press_brake_punch",
            "tool_diameter_mm": 3.0,
            "notes": "Fold top lid over the box.",
        },
        {
            "operation": "press_brake_bend",
            "process": "press_brake",
            "axis": "X",
            "bend_line_position_mm": lid_lip,
            "angle_deg": 90,
            "inside_radius_mm": 1.5,
            "sheet_thickness_mm": thickness,
            "tool_type": "press_brake_punch",
            "tool_diameter_mm": 3.0,
            "notes": "Fold front screw lip down over front wall.",
        },
        {
            "operation": "press_brake_bend",
            "process": "press_brake",
            "operation_family": "sheet_metal_forming",
            "tool_type": "press_brake_punch",
            "tool_diameter_mm": 3.0,
            "notes": "Fold four corner return tabs 90 degrees and screw them to side walls.",
        },
        {
            "operation": "assembly_fasteners",
            "process": "assembly",
            "tool_type": "screwdriver",
            "tool_diameter_mm": 0.0,
            "notes": "Install 3 x M4 screws on front lid lip and 16 x M3 screws on corner seam tabs.",
        },
    ]


def export_example(output_dir: Path = OUTPUT_DIR):
    output_dir.mkdir(parents=True, exist_ok=True)
    part = build_part()
    step_path = output_dir / "sheet_metal_closed_screw_box.step"
    stl_path = output_dir / "sheet_metal_closed_screw_box.stl"
    part.to_step(str(step_path))
    part.to_stl(str(stl_path))
    part.save_process_plan(str(output_dir / "process_plan.json"))
    part.visualization_package(output_dir / "viz")
    export_previews(part, stl_path, output_dir)
    return part


def export_previews(part, stl_path: Path, output_dir: Path) -> None:
    clean = output_dir / "preview_clean.png"
    iso = output_dir / "preview_iso.png"
    if not _render_preview_vtk(stl_path, clean, camera=(1.75, -2.10, 0.95)):
        _render_preview_matplotlib(part, clean, azim=-55, elev=22)
    if not _render_preview_vtk(stl_path, iso, camera=(-1.80, -2.00, 1.10)):
        _render_preview_matplotlib(part, iso, azim=-135, elev=28)


if __name__ == "__main__":
    result = export_example()
    print(result)
    print(result.bounding_box)
