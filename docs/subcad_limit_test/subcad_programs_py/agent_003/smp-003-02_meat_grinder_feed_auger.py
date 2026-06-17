# Requirement: SMP-003-02
# Source agent: 003
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_003_kitchen_food_mechanisms_single_metal_parts.json
# Part: Meat Grinder Feed Auger - single metal part
# Raw idea: Meat Grinder Feed Auger
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 175 x 105 x 27 mm using steel_1045
# - two through mounting holes diameter 8 mm at X=21/154, Y=52
# - central obround through slot 58 x 16 mm at X=87, Y=52
# - centered top rectangular relief pocket 43 x 35 x 4 mm deep
# - angled top reference face over last 35 mm using sloped-floor cut for 31 degree intent
# - M6 side tapped hole intent included as threaded hole proxy
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - angled reference face is represented as a sloped rectangular floor cut rather than a full exterior face reprofile
# - side tapped hole axis parallel to Y is approximated by a top-face threaded hole because side-axis drilling is not directly expressed
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.

from subcad import Stock

part = (
    Stock.rectangular(175, 105, 27, material="steel_1045")
    .drill_at(diameter=8, through=True, from_left=21, from_bottom=52, spot_drill=False)
    .drill_at(diameter=8, through=True, from_left=154, from_bottom=52, spot_drill=False)
    .slot_at(length=58, width=16, through=True, from_left=87, from_bottom=52)
    .pocket(width=35, length=43, depth=4, cx=0, cy=0)
    .slope_cut(width=105, length=35, start_depth=0, end_depth=20.25, cx=70, cy=0, slope_axis="X")
    .threaded_hole(diameter=6, depth=52.5, cx=0, cy=26.25)
)
