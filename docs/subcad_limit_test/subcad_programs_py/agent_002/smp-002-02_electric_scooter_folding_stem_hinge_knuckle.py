# Requirement: SMP-002-02
# Source agent: 002
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_002_mobility_hardware_single_metal_parts.json
# Part: Electric scooter folding stem hinge knuckle - single metal part
# Raw idea: Electric scooter folding stem hinge knuckle
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 110 x 90 x 64 mm using steel_a36
# - two through mounting holes diameter 11 mm at X=18/92, Y=45
# - central obround through slot 36 x 17 mm at X=55, Y=45
# - centered top rectangular relief pocket 27 x 30 x 18 mm deep
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
    Stock.rectangular(110, 90, 64, material="steel_a36")
    .drill_at(diameter=11, through=True, from_left=18, from_bottom=45, spot_drill=False)
    .drill_at(diameter=11, through=True, from_left=92, from_bottom=45, spot_drill=False)
    .slot_at(length=36, width=17, through=True, from_left=55, from_bottom=45)
    .pocket(width=30, length=27, depth=18, cx=0, cy=0)
)
