# Requirement: SMP-005-09
# Source agent: 005
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_005_robotics_automation_single_metal_parts.json
# Part: Force-Torque Sensor Cable-Safe Spacer Ring - single metal part
# Raw idea: Force-Torque Sensor Cable-Safe Spacer Ring
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 200 x 115 x 58 mm using aluminum_6061
# - two through mounting holes diameter 13 mm at X=23/177, Y=57
# - central obround through slot 66 x 8 mm at X=100, Y=57
# - centered top rectangular relief pocket 50 x 38 x 19 mm deep
# - central counterbore diameter 20 mm x 6 mm deep around center feature
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - counterbore around an obround slot is represented with a circular counterbore operation
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.

from subcad import Stock

part = (
    Stock.rectangular(200, 115, 58, material="aluminum_6061")
    .drill_at(diameter=13, through=True, from_left=23, from_bottom=57, spot_drill=False)
    .drill_at(diameter=13, through=True, from_left=177, from_bottom=57, spot_drill=False)
    .slot_at(length=66, width=8, through=True, from_left=100, from_bottom=57)
    .pocket(width=38, length=50, depth=19, cx=0, cy=0)
    .counterbore(hole_diameter=8, counterbore_diameter=20, counterbore_depth=6, cx=0, cy=-0.5, through=True)
)
