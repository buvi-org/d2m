# Requirement: SMP-040-07
# Source agent: 040
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_040_kiosk_payment_hardware_single_metal_parts.json
# Part: Self-service kiosk card reader bezel - single metal part
# Raw idea: Self-service kiosk card reader bezel
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 135 x 70 x 8 mm using aluminum_6061
# - two through mounting holes diameter 13 mm at X=14/121, Y=35
# - central obround through slot 45 x 9 mm at X=67, Y=35
# - centered top rectangular relief pocket 33 x 23 x 3 mm deep
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - Tap one side hole M4 from the right long edge into the central pocket; hole axis is parallel to Y. SubCAD has no side-entry tapped-hole axis selection in the inspected Stock API, so this side hole is not modeled.
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted by this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.
# - Rectangular/sheet X/Y feature placement uses drill_at/slot_at/pocket_at datum offsets from the lower-left requirement origin where applicable.

from subcad import Stock

part = (
    Stock.rectangular(135, 70, 8, material="aluminum_6061")
    .drill_at(diameter=13, through=True, from_left=14, from_bottom=35, spot_drill=False)
    .drill_at(diameter=13, through=True, from_left=121, from_bottom=35, spot_drill=False)
    .slot_at(length=45, width=9, through=True, from_left=67, from_bottom=35)
    .pocket_at(width=23, length=33, depth=3, from_left=67, from_bottom=35)
)
