# Requirement: SMP-005-08
# Source agent: 005
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_005_robotics_automation_single_metal_parts.json
# Part: Conveyor Diverter Mini Rocker Arm - single metal part
# Raw idea: Conveyor Diverter Mini Rocker Arm
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 190 x 65 x 47 mm using steel_a36
# - two through mounting holes diameter 12 mm at X=13/177, Y=32
# - central obround through slot 63 x 7 mm at X=95, Y=32
# - centered top rectangular relief pocket 47 x 21 x 6 mm deep
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.

from subcad import Stock

part = (
    Stock.rectangular(190, 65, 47, material="steel_a36")
    .drill_at(diameter=12, through=True, from_left=13, from_bottom=32, spot_drill=False)
    .drill_at(diameter=12, through=True, from_left=177, from_bottom=32, spot_drill=False)
    .slot_at(length=63, width=7, through=True, from_left=95, from_bottom=32)
    .pocket(width=21, length=47, depth=6, cx=0, cy=0)
)
