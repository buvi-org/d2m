# Requirement: SMP-040-24
# Source agent: 040
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_040_kiosk_payment_hardware_single_metal_parts.json
# Part: Payment kiosk privacy side wing - single metal part
# Raw idea: Payment kiosk privacy side wing
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 100 x 90 x 10 mm using aluminum_6061
# - two through mounting holes diameter 8 mm at X=18/82, Y=45
# - central obround through slot 33 x 18 mm at X=50, Y=45
# - centered top rectangular relief pocket 25 x 30 x 1 mm deep
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
    Stock.rectangular(100, 90, 10, material="aluminum_6061")
    .drill_at(diameter=8, through=True, from_left=18, from_bottom=45, spot_drill=False)
    .drill_at(diameter=8, through=True, from_left=82, from_bottom=45, spot_drill=False)
    .slot_at(length=33, width=18, through=True, from_left=50, from_bottom=45)
    .pocket_at(width=30, length=25, depth=1, from_left=50, from_bottom=45)
)
