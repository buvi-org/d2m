# Requirement: SMP-001-01
# Source agent: 001
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_001_workshop_fixtures_single_metal_parts.json
# Part: Low-Profile V-Block Clamp Jaw - single metal part
# Raw idea: Low-Profile V-Block Clamp Jaw
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 80 x 65 x 55 mm using steel_1045
# - two through mounting holes diameter 7 mm at X=13/67, Y=32
# - central obround through slot 30 x 17 mm at X=40, Y=32
# - centered top rectangular relief pocket 25 x 21 x 24 mm deep
# - central counterbore diameter 25 mm x 6 mm deep around center feature
# - full-length centered groove mouth 32 mm and depth 18 mm
# - angled top reference face over last 18 mm using sloped-floor cut for 18 degree intent
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - counterbore around an obround slot is represented with a circular counterbore operation
# - 90 degree V-groove is approximated by the available rectangular groove operation
# - angled reference face is represented as a sloped rectangular floor cut rather than a full exterior face reprofile
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.

from subcad import Stock

part = (
    Stock.rectangular(80, 65, 55, material="steel_1045")
    .drill_at(diameter=7, through=True, from_left=13, from_bottom=32, spot_drill=False)
    .drill_at(diameter=7, through=True, from_left=67, from_bottom=32, spot_drill=False)
    .slot_at(length=30, width=17, through=True, from_left=40, from_bottom=32)
    .pocket(width=21, length=25, depth=24, cx=0, cy=0)
    .counterbore(hole_diameter=17, counterbore_diameter=25, counterbore_depth=6, cx=0, cy=-0.5, through=True)
    .groove(length=80, width=32, depth=18, cx=0, cy=0)
    .slope_cut(width=65, length=18, start_depth=0, end_depth=5.849, cx=31, cy=0, slope_axis="X")
)
