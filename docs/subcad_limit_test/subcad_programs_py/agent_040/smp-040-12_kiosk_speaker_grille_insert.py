# Requirement: SMP-040-12
# Source agent: 040
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_040_kiosk_payment_hardware_single_metal_parts.json
# Part: Kiosk speaker grille insert - single metal part
# Raw idea: Kiosk speaker grille insert
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 205 x 110 x 30 mm using aluminum_6061
# - two through mounting holes diameter 10 mm at X=22/183, Y=55
# - central obround through slot 68 x 9 mm at X=102, Y=55
# - centered top rectangular relief pocket 51 x 36 x 1 mm deep
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
    Stock.rectangular(205, 110, 30, material="aluminum_6061")
    .drill_at(diameter=10, through=True, from_left=22, from_bottom=55, spot_drill=False)
    .drill_at(diameter=10, through=True, from_left=183, from_bottom=55, spot_drill=False)
    .slot_at(length=68, width=9, through=True, from_left=102, from_bottom=55)
    .pocket_at(width=36, length=51, depth=1, from_left=102, from_bottom=55)
)
