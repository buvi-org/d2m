# Requirement: SMP-002-09
# Source agent: 002
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_002_mobility_hardware_single_metal_parts.json
# Part: Bicycle dynamo hub wire-exit strain relief cap - single metal part
# Raw idea: Bicycle dynamo hub wire-exit strain relief cap
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 175 x 60 x 10 mm using steel_a36
# - two through mounting holes diameter 8 mm at X=12/163, Y=30
# - central obround through slot 58 x 17 mm at X=87, Y=30
# - centered top rectangular relief pocket 43 x 20 x 3 mm deep
# - M7 side tapped hole intent included as threaded hole proxy
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
    Stock.rectangular(175, 60, 10, material="steel_a36")
    .drill_at(diameter=8, through=True, from_left=12, from_bottom=30, spot_drill=False)
    .drill_at(diameter=8, through=True, from_left=163, from_bottom=30, spot_drill=False)
    .slot_at(length=58, width=17, through=True, from_left=87, from_bottom=30)
    .pocket(width=20, length=43, depth=3, cx=0, cy=0)
    .threaded_hole(diameter=7, depth=30, cx=0, cy=15)
)
