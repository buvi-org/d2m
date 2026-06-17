# Requirement: SMP-005-01
# Source agent: 005
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_005_robotics_automation_single_metal_parts.json
# Part: Collaborative Robot Vacuum Gripper Manifold Block - single metal part
# Raw idea: Collaborative Robot Vacuum Gripper Manifold Block
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 250 x 60 x 9 mm using stainless_316
# - two through mounting holes diameter 9 mm at X=12/238, Y=30
# - central obround through slot 83 x 8 mm at X=125, Y=30
# - centered top rectangular relief pocket 62 x 20 x 1 mm deep
# - central counterbore diameter 20 mm x 3 mm deep around center feature
# - M9 side tapped hole intent included as threaded hole proxy
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - counterbore around an obround slot is represented with a circular counterbore operation
# - side tapped hole axis parallel to Y is approximated by a top-face threaded hole because side-axis drilling is not directly expressed
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.

from subcad import Stock

part = (
    Stock.rectangular(250, 60, 9, material="stainless_316")
    .drill_at(diameter=9, through=True, from_left=12, from_bottom=30, spot_drill=False)
    .drill_at(diameter=9, through=True, from_left=238, from_bottom=30, spot_drill=False)
    .slot_at(length=83, width=8, through=True, from_left=125, from_bottom=30)
    .pocket(width=20, length=62, depth=1, cx=0, cy=0)
    .counterbore(hole_diameter=8, counterbore_diameter=20, counterbore_depth=3, cx=0, cy=0, through=True)
    .threaded_hole(diameter=9, depth=30, cx=0, cy=15)
)
