# Requirement: SMP-040-21
# Source agent: 040
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_040_kiosk_payment_hardware_single_metal_parts.json
# Part: Vending machine cup drop carousel plate - single metal part
# Raw idea: Vending machine cup drop carousel plate
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 100 x 85 x 7 mm using steel_a36
# - two through mounting holes diameter 12 mm at X=17/83, Y=42
# - central obround through slot 33 x 11 mm at X=50, Y=42
# - centered top rectangular relief pocket 25 x 28 x 2 mm deep
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
    Stock.rectangular(100, 85, 7, material="steel_a36")
    .drill_at(diameter=12, through=True, from_left=17, from_bottom=42, spot_drill=False)
    .drill_at(diameter=12, through=True, from_left=83, from_bottom=42, spot_drill=False)
    .slot_at(length=33, width=11, through=True, from_left=50, from_bottom=42)
    .pocket_at(width=28, length=25, depth=2, from_left=50, from_bottom=42)
)
