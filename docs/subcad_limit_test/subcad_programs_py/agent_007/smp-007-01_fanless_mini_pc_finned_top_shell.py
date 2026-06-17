# Requirement: SMP-007-01
# Source agent: 007
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_007_consumer_electronics_single_metal_parts.json
# Part: Fanless Mini PC Finned Top Shell - single metal part
# Raw idea: Fanless Mini PC Finned Top Shell
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 90 x 55 x 33 mm using steel_a36
# - two through mounting holes diameter 11 mm at X=11/79, Y=27
# - central obround through slot 30 x 9 mm at X=45, Y=27
# - centered top rectangular relief pocket 25 x 18 x 5 mm deep
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
    Stock.rectangular(90, 55, 33, material="steel_a36")
    .drill_at(diameter=11, through=True, from_left=11, from_bottom=27, spot_drill=False)
    .drill_at(diameter=11, through=True, from_left=79, from_bottom=27, spot_drill=False)
    .slot_at(length=30, width=9, through=True, from_left=45, from_bottom=27)
    .pocket(width=18, length=25, depth=5, cx=0, cy=0)
    .threaded_hole(diameter=4, depth=27.5, cx=0, cy=13.75)
)
