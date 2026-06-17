# Requirement: SMP-040-20
# Source agent: 040
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_040_kiosk_payment_hardware_single_metal_parts.json
# Part: Laundry payment kiosk coin vault liner - single metal part
# Raw idea: Laundry payment kiosk coin vault liner
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 75 x 50 x 20 mm using aluminum_6061
# - two through mounting holes diameter 10 mm at X=10/65, Y=25
# - central obround through slot 30 x 18 mm at X=37, Y=25
# - centered top rectangular relief pocket 25 x 18 x 3 mm deep
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
    Stock.rectangular(75, 50, 20, material="aluminum_6061")
    .drill_at(diameter=10, through=True, from_left=10, from_bottom=25, spot_drill=False)
    .drill_at(diameter=10, through=True, from_left=65, from_bottom=25, spot_drill=False)
    .slot_at(length=30, width=18, through=True, from_left=37, from_bottom=25)
    .pocket_at(width=18, length=25, depth=3, from_left=37, from_bottom=25)
)
