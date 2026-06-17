# Requirement: SMP-007-05
# Source agent: 007
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_007_consumer_electronics_single_metal_parts.json
# Part: Gaming Console SSD Expansion Heat Sink Cover - single metal part
# Raw idea: Gaming Console SSD Expansion Heat Sink Cover
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 245 x 145 x 3 mm using steel_a36
# - two through mounting holes diameter 9 mm at X=29/216, Y=72
# - central obround through slot 81 x 13 mm at X=122, Y=72
# - centered top rectangular relief pocket 61 x 48 x 1 mm deep
# - M8 side tapped hole intent included as threaded hole proxy
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
    Stock.rectangular(245, 145, 3, material="steel_a36")
    .drill_at(diameter=9, through=True, from_left=29, from_bottom=72, spot_drill=False)
    .drill_at(diameter=9, through=True, from_left=216, from_bottom=72, spot_drill=False)
    .slot_at(length=81, width=13, through=True, from_left=122, from_bottom=72)
    .pocket(width=48, length=61, depth=1, cx=0, cy=0)
    .threaded_hole(diameter=8, depth=72.5, cx=0, cy=36.25)
)
