# Requirement: SMP-009-05
# Source agent: 009
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_009_furniture_architectural_hardware_single_metal_parts.json
# Part: Architectural Curtain Wall T-Slot Anchor Clamp - single metal part
# Raw idea: Architectural Curtain Wall T-Slot Anchor Clamp
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 155 x 95 x 69 mm using steel_1045
# - two through mounting holes diameter 10 mm at X=19/136, Y=47
# - central obround through slot 51 x 18 mm at X=77, Y=47
# - centered top rectangular relief pocket 38 x 31 x 5 mm deep
# - angled top reference face over last 31 mm using sloped-floor cut for 12 degree intent
# - M5 side tapped hole intent included as threaded hole proxy
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
    Stock.rectangular(155, 95, 69, material="steel_1045")
    .drill_at(diameter=10, through=True, from_left=19, from_bottom=47, spot_drill=False)
    .drill_at(diameter=10, through=True, from_left=136, from_bottom=47, spot_drill=False)
    .slot_at(length=51, width=18, through=True, from_left=77, from_bottom=47)
    .pocket(width=31, length=38, depth=5, cx=0, cy=0)
    .slope_cut(width=95, length=31, start_depth=0, end_depth=6.589, cx=62, cy=0, slope_axis="X")
    .threaded_hole(diameter=5, depth=47.5, cx=0, cy=23.75)
)
