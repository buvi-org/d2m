# Requirement: SMP-002-01
# Source agent: 002
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_002_mobility_hardware_single_metal_parts.json
# Part: Bicycle thru-axle chain tensioner dropout insert - single metal part
# Raw idea: Bicycle thru-axle chain tensioner dropout insert
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 105 x 105 x 36 mm using steel_a36
# - two through mounting holes diameter 9 mm at X=21/84, Y=52
# - central obround through slot 35 x 11 mm at X=52, Y=52
# - centered top rectangular relief pocket 26 x 35 x 15 mm deep
# - M4 side tapped hole intent included as threaded hole proxy
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - side tapped hole axis parallel to Y is approximated by a top-face threaded hole because side-axis drilling is not directly expressed
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.

from subcad import Stock

part = (
    Stock.rectangular(105, 105, 36, material="steel_a36")
    .drill_at(diameter=9, through=True, from_left=21, from_bottom=52, spot_drill=False)
    .drill_at(diameter=9, through=True, from_left=84, from_bottom=52, spot_drill=False)
    .slot_at(length=35, width=11, through=True, from_left=52, from_bottom=52)
    .pocket(width=35, length=26, depth=15, cx=0, cy=0)
    .threaded_hole(diameter=4, depth=52.5, cx=0, cy=26.25)
)
