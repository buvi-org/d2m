# Requirement: SMP-005-10
# Source agent: 005
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_005_robotics_automation_single_metal_parts.json
# Part: Micro Gripper Parallel Jaw Stroke Limiter - single metal part
# Raw idea: Micro Gripper Parallel Jaw Stroke Limiter
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 110 x 75 x 66 mm using stainless_316
# - two through mounting holes diameter 13 mm at X=15/95, Y=37
# - central obround through slot 36 x 8 mm at X=55, Y=37
# - centered top rectangular relief pocket 27 x 25 x 8 mm deep
# - M9 side tapped hole intent included as threaded hole proxy
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - side tapped hole axis parallel to Y is approximated by a top-face threaded hole because side-axis drilling is not directly expressed
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.

from subcad import Stock

part = (
    Stock.rectangular(110, 75, 66, material="stainless_316")
    .drill_at(diameter=13, through=True, from_left=15, from_bottom=37, spot_drill=False)
    .drill_at(diameter=13, through=True, from_left=95, from_bottom=37, spot_drill=False)
    .slot_at(length=36, width=8, through=True, from_left=55, from_bottom=37)
    .pocket(width=25, length=27, depth=8, cx=0, cy=0)
    .threaded_hole(diameter=9, depth=37.5, cx=0, cy=18.75)
)
