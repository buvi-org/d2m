# Requirement: SMP-040-25
# Source agent: 040
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_040_kiosk_payment_hardware_single_metal_parts.json
# Part: Coin return acoustic dampener insert - single metal part
# Raw idea: Coin return acoustic dampener insert
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 100 x 65 x 48 mm using steel_a36
# - two through mounting holes diameter 7 mm at X=13/87, Y=32
# - central obround through slot 33 x 12 mm at X=50, Y=32
# - centered top rectangular relief pocket 25 x 21 x 3 mm deep
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
    Stock.rectangular(100, 65, 48, material="steel_a36")
    .drill_at(diameter=7, through=True, from_left=13, from_bottom=32, spot_drill=False)
    .drill_at(diameter=7, through=True, from_left=87, from_bottom=32, spot_drill=False)
    .slot_at(length=33, width=12, through=True, from_left=50, from_bottom=32)
    .pocket_at(width=21, length=25, depth=3, from_left=50, from_bottom=32)
)
