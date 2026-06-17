# Requirement: SMP-040-03
# Source agent: 040
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_040_kiosk_payment_hardware_single_metal_parts.json
# Part: Ticket machine printer paper guide - single metal part
# Raw idea: Ticket machine printer paper guide
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 120 x 80 x 35 mm using steel_a36
# - two through mounting holes diameter 10 mm at X=16/104, Y=40
# - central obround through slot 40 x 14 mm at X=60, Y=40
# - centered top rectangular relief pocket 30 x 26 x 14 mm deep
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
    Stock.rectangular(120, 80, 35, material="steel_a36")
    .drill_at(diameter=10, through=True, from_left=16, from_bottom=40, spot_drill=False)
    .drill_at(diameter=10, through=True, from_left=104, from_bottom=40, spot_drill=False)
    .slot_at(length=40, width=14, through=True, from_left=60, from_bottom=40)
    .pocket_at(width=26, length=30, depth=14, from_left=60, from_bottom=40)
)
