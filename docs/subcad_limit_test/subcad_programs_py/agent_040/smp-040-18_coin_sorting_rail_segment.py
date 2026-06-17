# Requirement: SMP-040-18
# Source agent: 040
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_040_kiosk_payment_hardware_single_metal_parts.json
# Part: Coin sorting rail segment - single metal part
# Raw idea: Coin sorting rail segment
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 175 x 60 x 69 mm using steel_a36
# - two through mounting holes diameter 13 mm at X=12/163, Y=30
# - central obround through slot 58 x 16 mm at X=87, Y=30
# - centered top rectangular relief pocket 43 x 20 x 12 mm deep
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
    Stock.rectangular(175, 60, 69, material="steel_a36")
    .drill_at(diameter=13, through=True, from_left=12, from_bottom=30, spot_drill=False)
    .drill_at(diameter=13, through=True, from_left=163, from_bottom=30, spot_drill=False)
    .slot_at(length=58, width=16, through=True, from_left=87, from_bottom=30)
    .pocket_at(width=20, length=43, depth=12, from_left=87, from_bottom=30)
)
