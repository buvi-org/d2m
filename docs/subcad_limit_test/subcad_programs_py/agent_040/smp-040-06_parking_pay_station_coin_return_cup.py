# Requirement: SMP-040-06
# Source agent: 040
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_040_kiosk_payment_hardware_single_metal_parts.json
# Part: Parking pay station coin return cup - single metal part
# Raw idea: Parking pay station coin return cup
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 145 x 55 x 37 mm using steel_a36
# - two through mounting holes diameter 7 mm at X=11/134, Y=27
# - central obround through slot 48 x 8 mm at X=72, Y=27
# - centered top rectangular relief pocket 36 x 18 x 18 mm deep
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
    Stock.rectangular(145, 55, 37, material="steel_a36")
    .drill_at(diameter=7, through=True, from_left=11, from_bottom=27, spot_drill=False)
    .drill_at(diameter=7, through=True, from_left=134, from_bottom=27, spot_drill=False)
    .slot_at(length=48, width=8, through=True, from_left=72, from_bottom=27)
    .pocket_at(width=18, length=36, depth=18, from_left=72, from_bottom=27)
)
