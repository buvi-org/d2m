# Requirement: SMP-040-09
# Source agent: 040
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_040_kiosk_payment_hardware_single_metal_parts.json
# Part: Vending pickup bay anti-theft flap - single metal part
# Raw idea: Vending pickup bay anti-theft flap
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 235 x 75 x 7 mm using steel_a36
# - two through mounting holes diameter 5 mm at X=15/220, Y=37
# - central obround through slot 78 x 17 mm at X=117, Y=37
# - centered top rectangular relief pocket 58 x 25 x 2 mm deep
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
    Stock.rectangular(235, 75, 7, material="steel_a36")
    .drill_at(diameter=5, through=True, from_left=15, from_bottom=37, spot_drill=False)
    .drill_at(diameter=5, through=True, from_left=220, from_bottom=37, spot_drill=False)
    .slot_at(length=78, width=17, through=True, from_left=117, from_bottom=37)
    .pocket_at(width=25, length=58, depth=2, from_left=117, from_bottom=37)
)
