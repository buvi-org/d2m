# Requirement: SMP-002-05
# Source agent: 002
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_002_mobility_hardware_single_metal_parts.json
# Part: Scooter rear suspension rocker link - single metal part
# Raw idea: Scooter rear suspension rocker link
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 180 x 110 x 29 mm using steel_a36
# - two through mounting holes diameter 10 mm at X=22/158, Y=55
# - central obround through slot 60 x 17 mm at X=90, Y=55
# - centered top rectangular relief pocket 45 x 36 x 14 mm deep
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.

from subcad import Stock

part = (
    Stock.rectangular(180, 110, 29, material="steel_a36")
    .drill_at(diameter=10, through=True, from_left=22, from_bottom=55, spot_drill=False)
    .drill_at(diameter=10, through=True, from_left=158, from_bottom=55, spot_drill=False)
    .slot_at(length=60, width=17, through=True, from_left=90, from_bottom=55)
    .pocket(width=36, length=45, depth=14, cx=0, cy=0)
)
