"""Executable SubCAD example for an open-top box formed from one sheet."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from examples.sheet_metal_u_bracket import export_previews
from src.subcad import Stock


OUTPUT_DIR = Path("renders/sheet_metal_open_box")


def build_part():
    """Return an open-top utility box/tray made from a single laser-cut sheet."""
    base_length = 100.0
    base_width = 70.0
    wall_height = 35.0
    thickness = 1.2

    half_l = base_length / 2.0
    half_w = base_width / 2.0
    sheet_length = base_length + 2.0 * wall_height
    sheet_width = base_width + 2.0 * wall_height

    # Cross blank: center bottom plus four fold-up side panels. The missing
    # corners are laser-cut reliefs so adjacent walls can bend cleanly.
    blank_outline = {
        "type": "polygon",
        "points": [
            (-half_l, -half_w - wall_height),
            (half_l, -half_w - wall_height),
            (half_l, -half_w),
            (half_l + wall_height, -half_w),
            (half_l + wall_height, half_w),
            (half_l, half_w),
            (half_l, half_w + wall_height),
            (-half_l, half_w + wall_height),
            (-half_l, half_w),
            (-half_l - wall_height, half_w),
            (-half_l - wall_height, -half_w),
            (-half_l, -half_w),
        ],
    }

    return (
        Stock.sheet(sheet_length, sheet_width, thickness, material="steel_a36")
        .laser_cut_profile(blank_outline, kerf_width=0.18, assist_gas="nitrogen")
        .laser_cut_hole(diameter=5.0, cx=-30.0, cy=-20.0)
        .laser_cut_hole(diameter=5.0, cx=30.0, cy=-20.0)
        .laser_cut_hole(diameter=5.0, cx=-30.0, cy=20.0)
        .laser_cut_hole(diameter=5.0, cx=30.0, cy=20.0)
        .press_brake_bend(axis="X", position=half_w, angle=90, side="positive", radius=1.5)
        .press_brake_bend(axis="X", position=-half_w, angle=-90, side="negative", radius=1.5)
        .press_brake_bend(axis="Y", position=half_l, angle=-90, side="positive", radius=1.5)
        .press_brake_bend(axis="Y", position=-half_l, angle=90, side="negative", radius=1.5)
    )


def export_example(output_dir: Path = OUTPUT_DIR):
    output_dir.mkdir(parents=True, exist_ok=True)
    part = build_part()
    step_path = output_dir / "sheet_metal_open_box.step"
    stl_path = output_dir / "sheet_metal_open_box.stl"
    part.to_step(str(step_path))
    part.to_stl(str(stl_path))
    part.save_process_plan(str(output_dir / "process_plan.json"))
    part.visualization_package(output_dir / "viz")
    export_previews(part, stl_path, output_dir)
    return part


if __name__ == "__main__":
    result = export_example()
    print(result)
    print(result.bounding_box)
