# Requirement: SMP-040-15
# Source agent: 040
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_040_kiosk_payment_hardware_single_metal_parts.json
# Part: Public kiosk maintenance latch cover - single metal part
# Raw idea: Public kiosk maintenance latch cover
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 135 x 50 x 9 mm using aluminum_6061
# - two through mounting holes diameter 8 mm at X=10/125, Y=25
# - central obround through slot 45 x 17 mm at X=67, Y=25
# - centered top rectangular relief pocket 33 x 18 x 4 mm deep
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
    Stock.rectangular(135, 50, 9, material="aluminum_6061")
    .drill_at(diameter=8, through=True, from_left=10, from_bottom=25, spot_drill=False)
    .drill_at(diameter=8, through=True, from_left=125, from_bottom=25, spot_drill=False)
    .slot_at(length=45, width=17, through=True, from_left=67, from_bottom=25)
    .pocket_at(width=18, length=33, depth=4, from_left=67, from_bottom=25)
)
