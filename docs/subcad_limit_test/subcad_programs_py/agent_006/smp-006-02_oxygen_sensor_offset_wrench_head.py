# Requirement: SMP-006-02
# Source agent: 006
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_006_automotive_service_tools_single_metal_parts.json
# Part: Oxygen Sensor Offset Wrench Head - single metal part
# Raw idea: Oxygen Sensor Offset Wrench Head
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 105 x 70 x 51 mm using steel_a36
# - two through mounting holes diameter 6 mm at X=14/91, Y=35
# - central obround through slot 35 x 9 mm at X=52, Y=35
# - centered top rectangular relief pocket 26 x 23 x 17 mm deep
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
    Stock.rectangular(105, 70, 51, material="steel_a36")
    .drill_at(diameter=6, through=True, from_left=14, from_bottom=35, spot_drill=False)
    .drill_at(diameter=6, through=True, from_left=91, from_bottom=35, spot_drill=False)
    .slot_at(length=35, width=9, through=True, from_left=52, from_bottom=35)
    .pocket(width=23, length=26, depth=17, cx=0, cy=0)
)
