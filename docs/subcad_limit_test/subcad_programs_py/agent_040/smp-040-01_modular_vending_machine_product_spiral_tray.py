# Requirement: SMP-040-01
# Source agent: 040
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_040_kiosk_payment_hardware_single_metal_parts.json
# Part: Modular vending machine product spiral tray - single metal part
# Raw idea: Modular vending machine product spiral tray
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 105 x 90 x 9 mm using steel_a36
# - two through mounting holes diameter 6 mm at X=18/87, Y=45
# - central obround through slot 35 x 10 mm at X=52, Y=45
# - centered top rectangular relief pocket 26 x 30 x 2 mm deep
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
    Stock.rectangular(105, 90, 9, material="steel_a36")
    .drill_at(diameter=6, through=True, from_left=18, from_bottom=45, spot_drill=False)
    .drill_at(diameter=6, through=True, from_left=87, from_bottom=45, spot_drill=False)
    .slot_at(length=35, width=10, through=True, from_left=52, from_bottom=45)
    .pocket_at(width=30, length=26, depth=2, from_left=52, from_bottom=45)
)
