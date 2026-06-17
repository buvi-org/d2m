# Requirement: SMP-042-29
# Source agent: 042
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_042_glass_handling_hardware_single_metal_parts.json
# Part: Fragile Sheet Truck Side Retainer - single metal part
# Raw idea: Fragile Sheet Truck Side Retainer
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 230 x 115 x 12 mm using steel_a36
# - two through mounting holes diameter 8 mm at X=23/207, Y=57
# - central obround through slot 76 x 13 mm at X=115, Y=57
# - centered top rectangular relief pocket 57 x 38 x 3 mm deep
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted by this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.
# - Rectangular/sheet X/Y feature placement uses drill_at/slot_at/pocket_at datum offsets from the lower-left requirement origin where applicable.

from subcad import Stock

part = (
    Stock.rectangular(230, 115, 12, material="steel_a36")
    .drill_at(diameter=8, through=True, from_left=23, from_bottom=57, spot_drill=False)
    .drill_at(diameter=8, through=True, from_left=207, from_bottom=57, spot_drill=False)
    .slot_at(length=76, width=13, through=True, from_left=115, from_bottom=57)
    .pocket_at(width=38, length=57, depth=3, from_left=115, from_bottom=57)
)
