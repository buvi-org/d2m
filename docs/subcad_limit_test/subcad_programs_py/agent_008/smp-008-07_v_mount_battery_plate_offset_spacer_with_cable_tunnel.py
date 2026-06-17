# Requirement: SMP-008-07
# Source agent: 008
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_008_creator_rigging_hardware_single_metal_parts.json
# Part: V-Mount Battery Plate Offset Spacer With Cable Tunnel - single metal part
# Raw idea: V-Mount Battery Plate Offset Spacer With Cable Tunnel
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 215 x 65 x 10 mm using aluminum_6061
# - two through mounting holes diameter 13 mm at X=13/202, Y=32
# - central obround through slot 71 x 17 mm at X=107, Y=32
# - centered top rectangular relief pocket 53 x 21 x 3 mm deep
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
    Stock.rectangular(215, 65, 10, material="aluminum_6061")
    .drill_at(diameter=13, through=True, from_left=13, from_bottom=32, spot_drill=False)
    .drill_at(diameter=13, through=True, from_left=202, from_bottom=32, spot_drill=False)
    .slot_at(length=71, width=17, through=True, from_left=107, from_bottom=32)
    .pocket(width=21, length=53, depth=3, cx=0, cy=0)
)
