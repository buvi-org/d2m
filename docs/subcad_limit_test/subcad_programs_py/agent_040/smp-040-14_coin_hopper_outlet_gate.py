# Requirement: SMP-040-14
# Source agent: 040
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_040_kiosk_payment_hardware_single_metal_parts.json
# Part: Coin hopper outlet gate - single metal part
# Raw idea: Coin hopper outlet gate
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 185 x 95 x 24 mm using steel_a36
# - two through mounting holes diameter 12 mm at X=19/166, Y=47
# - central obround through slot 61 x 11 mm at X=92, Y=47
# - centered top rectangular relief pocket 46 x 31 x 3 mm deep
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
    Stock.rectangular(185, 95, 24, material="steel_a36")
    .drill_at(diameter=12, through=True, from_left=19, from_bottom=47, spot_drill=False)
    .drill_at(diameter=12, through=True, from_left=166, from_bottom=47, spot_drill=False)
    .slot_at(length=61, width=11, through=True, from_left=92, from_bottom=47)
    .pocket_at(width=31, length=46, depth=3, from_left=92, from_bottom=47)
)
