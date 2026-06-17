# Requirement: SMP-003-03
# Source agent: 003
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_003_kitchen_food_mechanisms_single_metal_parts.json
# Part: Citrus Juicer Reamer Cone - single metal part
# Raw idea: Citrus Juicer Reamer Cone
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 110 x 70 x 54 mm using steel_a36
# - two through mounting holes diameter 12 mm at X=14/96, Y=35
# - central obround through slot 36 x 8 mm at X=55, Y=35
# - centered top rectangular relief pocket 27 x 23 x 22 mm deep
# - angled top reference face over last 22 mm using sloped-floor cut for 11 degree intent
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - angled reference face is represented as a sloped rectangular floor cut rather than a full exterior face reprofile
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.

from subcad import Stock

part = (
    Stock.rectangular(110, 70, 54, material="steel_a36")
    .drill_at(diameter=12, through=True, from_left=14, from_bottom=35, spot_drill=False)
    .drill_at(diameter=12, through=True, from_left=96, from_bottom=35, spot_drill=False)
    .slot_at(length=36, width=8, through=True, from_left=55, from_bottom=35)
    .pocket(width=23, length=27, depth=22, cx=0, cy=0)
    .slope_cut(width=70, length=22, start_depth=0, end_depth=4.276, cx=44, cy=0, slope_axis="X")
)
