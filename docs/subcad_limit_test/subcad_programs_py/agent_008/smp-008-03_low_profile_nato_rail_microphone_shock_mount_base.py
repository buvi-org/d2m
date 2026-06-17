# Requirement: SMP-008-03
# Source agent: 008
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_008_creator_rigging_hardware_single_metal_parts.json
# Part: Low-Profile NATO Rail Microphone Shock Mount Base - single metal part
# Raw idea: Low-Profile NATO Rail Microphone Shock Mount Base
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 140 x 70 x 70 mm using aluminum_6061
# - two through mounting holes diameter 13 mm at X=14/126, Y=35
# - central obround through slot 46 x 16 mm at X=70, Y=35
# - centered top rectangular relief pocket 35 x 23 x 17 mm deep
# - dovetail groove length 116 mm, throat 14 mm, included angle 60 degrees
# - angled top reference face over last 28 mm using sloped-floor cut for 17 degree intent
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
# - Dovetail depth was inferred because the requirement gives throat and angle but not groove depth.
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.

from subcad import Stock

part = (
    Stock.rectangular(140, 70, 70, material="aluminum_6061")
    .drill_at(diameter=13, through=True, from_left=14, from_bottom=35, spot_drill=False)
    .drill_at(diameter=13, through=True, from_left=126, from_bottom=35, spot_drill=False)
    .slot_at(length=46, width=16, through=True, from_left=70, from_bottom=35)
    .pocket(width=23, length=35, depth=17, cx=0, cy=0)
    .dovetail(length=116, width=14, depth=15.4, angle=60, cx=0, cy=0)
    .slope_cut(width=70, length=28, start_depth=0, end_depth=8.56, cx=56, cy=0, slope_axis="X")
    .threaded_hole(diameter=6, depth=35, cx=0, cy=17.5)
)
