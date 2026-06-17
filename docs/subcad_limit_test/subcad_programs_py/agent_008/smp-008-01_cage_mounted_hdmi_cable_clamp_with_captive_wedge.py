# Requirement: SMP-008-01
# Source agent: 008
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_008_creator_rigging_hardware_single_metal_parts.json
# Part: Cage-Mounted HDMI Cable Clamp With Captive Wedge - single metal part
# Raw idea: Cage-Mounted HDMI Cable Clamp With Captive Wedge
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 180 x 35 x 63 mm using aluminum_6061
# - two through mounting holes diameter 8 mm at X=10/170, Y=17
# - central obround through slot 60 x 14 mm at X=90, Y=17
# - centered top rectangular relief pocket 45 x 18 x 27 mm deep
# - central counterbore diameter 22 mm x 6 mm deep around center feature
# - angled top reference face over last 36 mm using sloped-floor cut for 18 degree intent
# - 7 rear-edge serration positions with 5 mm depth intent
# - M10 side tapped hole intent included as threaded hole proxy
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - counterbore around an obround slot is represented with a circular counterbore operation
# - angled reference face is represented as a sloped rectangular floor cut rather than a full exterior face reprofile
# - triangular serration tooth form is approximated by repeated rectangular groove cuts
# - side tapped hole axis parallel to Y is approximated by a top-face threaded hole because side-axis drilling is not directly expressed
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.

from subcad import Stock

part = (
    Stock.rectangular(180, 35, 63, material="aluminum_6061")
    .drill_at(diameter=8, through=True, from_left=10, from_bottom=17, spot_drill=False)
    .drill_at(diameter=8, through=True, from_left=170, from_bottom=17, spot_drill=False)
    .slot_at(length=60, width=14, through=True, from_left=90, from_bottom=17)
    .pocket(width=18, length=45, depth=27, cx=0, cy=0)
    .counterbore(hole_diameter=14, counterbore_diameter=22, counterbore_depth=6, cx=0, cy=-0.5, through=True)
    .slope_cut(width=35, length=36, start_depth=0, end_depth=11.697, cx=72, cy=0, slope_axis="X")
    .groove(length=5, width=3.25, depth=5, cx=-87.5, cy=-15, angle=90)
    .groove(length=5, width=3.25, depth=5, cx=-87.5, cy=-10, angle=90)
    .groove(length=5, width=3.25, depth=5, cx=-87.5, cy=-5, angle=90)
    .groove(length=5, width=3.25, depth=5, cx=-87.5, cy=0, angle=90)
    .groove(length=5, width=3.25, depth=5, cx=-87.5, cy=5, angle=90)
    .groove(length=5, width=3.25, depth=5, cx=-87.5, cy=10, angle=90)
    .groove(length=5, width=3.25, depth=5, cx=-87.5, cy=15, angle=90)
    .threaded_hole(diameter=10, depth=17.5, cx=0, cy=8.75)
)
