# Requirement: SMP-007-09
# Source agent: 007
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_007_consumer_electronics_single_metal_parts.json
# Part: Docking Station Heat-Spreader Bottom Chassis - single metal part
# Raw idea: Docking Station Heat-Spreader Bottom Chassis
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 110 x 45 x 63 mm using steel_a36
# - two through mounting holes diameter 13 mm at X=10/100, Y=22
# - central obround through slot 36 x 14 mm at X=55, Y=22
# - centered top rectangular relief pocket 27 x 18 x 7 mm deep
# - M10 side tapped hole intent included as threaded hole proxy
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
    Stock.rectangular(110, 45, 63, material="steel_a36")
    .drill_at(diameter=13, through=True, from_left=10, from_bottom=22, spot_drill=False)
    .drill_at(diameter=13, through=True, from_left=100, from_bottom=22, spot_drill=False)
    .slot_at(length=36, width=14, through=True, from_left=55, from_bottom=22)
    .pocket(width=18, length=27, depth=7, cx=0, cy=0)
    .threaded_hole(diameter=10, depth=22.5, cx=0, cy=11.25)
)
