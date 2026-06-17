# Requirement: SMP-003-06
# Source agent: 003
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_003_kitchen_food_mechanisms_single_metal_parts.json
# Part: Mandoline Slicer Thickness Ramp Carriage - single metal part
# Raw idea: Mandoline Slicer Thickness Ramp Carriage
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 80 x 70 x 62 mm using steel_a36
# - two through mounting holes diameter 7 mm at X=14/66, Y=35
# - central obround through slot 30 x 18 mm at X=40, Y=35
# - centered top rectangular relief pocket 25 x 23 x 1 mm deep
# - angled top reference face over last 18 mm using sloped-floor cut for 34 degree intent
# - 9 rear-edge serration positions with 2 mm depth intent
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - angled reference face is represented as a sloped rectangular floor cut rather than a full exterior face reprofile
# - triangular serration tooth form is approximated by repeated rectangular groove cuts
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.

from subcad import Stock

part = (
    Stock.rectangular(80, 70, 62, material="steel_a36")
    .drill_at(diameter=7, through=True, from_left=14, from_bottom=35, spot_drill=False)
    .drill_at(diameter=7, through=True, from_left=66, from_bottom=35, spot_drill=False)
    .slot_at(length=30, width=18, through=True, from_left=40, from_bottom=35)
    .pocket(width=23, length=25, depth=1, cx=0, cy=0)
    .slope_cut(width=70, length=18, start_depth=0, end_depth=12.141, cx=31, cy=0, slope_axis="X")
    .groove(length=2, width=5.056, depth=2, cx=-39, cy=-31.111, angle=90)
    .groove(length=2, width=5.056, depth=2, cx=-39, cy=-23.333, angle=90)
    .groove(length=2, width=5.056, depth=2, cx=-39, cy=-15.556, angle=90)
    .groove(length=2, width=5.056, depth=2, cx=-39, cy=-7.778, angle=90)
    .groove(length=2, width=5.056, depth=2, cx=-39, cy=0, angle=90)
    .groove(length=2, width=5.056, depth=2, cx=-39, cy=7.778, angle=90)
    .groove(length=2, width=5.056, depth=2, cx=-39, cy=15.556, angle=90)
    .groove(length=2, width=5.056, depth=2, cx=-39, cy=23.333, angle=90)
    .groove(length=2, width=5.056, depth=2, cx=-39, cy=31.111, angle=90)
)
