# Requirement: SMP-009-09
# Source agent: 009
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_009_furniture_architectural_hardware_single_metal_parts.json
# Part: Adjustable Stair Handrail Glass Clamp - single metal part
# Raw idea: Adjustable Stair Handrail Glass Clamp
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 205 x 45 x 26 mm using steel_1045
# - two through mounting holes diameter 13 mm at X=10/195, Y=22
# - central obround through slot 68 x 13 mm at X=102, Y=22
# - centered top rectangular relief pocket 51 x 18 x 6 mm deep
# - angled top reference face over last 41 mm using sloped-floor cut for 16 degree intent
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
    Stock.rectangular(205, 45, 26, material="steel_1045")
    .drill_at(diameter=13, through=True, from_left=10, from_bottom=22, spot_drill=False)
    .drill_at(diameter=13, through=True, from_left=195, from_bottom=22, spot_drill=False)
    .slot_at(length=68, width=13, through=True, from_left=102, from_bottom=22)
    .pocket(width=18, length=51, depth=6, cx=0, cy=0)
    .slope_cut(width=45, length=41, start_depth=0, end_depth=11.757, cx=82, cy=0, slope_axis="X")
    .threaded_hole(diameter=6, depth=22.5, cx=0, cy=11.25)
)
