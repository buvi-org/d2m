# Requirement: SMP-040-08
# Source agent: 040
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_040_kiosk_payment_hardware_single_metal_parts.json
# Part: Transit gate token escrow door - single metal part
# Raw idea: Transit gate token escrow door
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 180 x 55 x 9 mm using steel_a36
# - two through mounting holes diameter 5 mm at X=11/169, Y=27
# - central obround through slot 60 x 11 mm at X=90, Y=27
# - centered top rectangular relief pocket 45 x 18 x 1 mm deep
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
    Stock.rectangular(180, 55, 9, material="steel_a36")
    .drill_at(diameter=5, through=True, from_left=11, from_bottom=27, spot_drill=False)
    .drill_at(diameter=5, through=True, from_left=169, from_bottom=27, spot_drill=False)
    .slot_at(length=60, width=11, through=True, from_left=90, from_bottom=27)
    .pocket_at(width=18, length=45, depth=1, from_left=90, from_bottom=27)
)
