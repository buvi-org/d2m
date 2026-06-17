# Requirement: SMP-040-22
# Source agent: 040
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_040_kiosk_payment_hardware_single_metal_parts.json
# Part: Kiosk cash drawer guide rail - single metal part
# Raw idea: Kiosk cash drawer guide rail
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 180 x 65 x 53 mm using aluminum_6061
# - two through mounting holes diameter 10 mm at X=13/167, Y=32
# - central obround through slot 60 x 8 mm at X=90, Y=32
# - centered top rectangular relief pocket 45 x 21 x 12 mm deep
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
    Stock.rectangular(180, 65, 53, material="aluminum_6061")
    .drill_at(diameter=10, through=True, from_left=13, from_bottom=32, spot_drill=False)
    .drill_at(diameter=10, through=True, from_left=167, from_bottom=32, spot_drill=False)
    .slot_at(length=60, width=8, through=True, from_left=90, from_bottom=32)
    .pocket_at(width=21, length=45, depth=12, from_left=90, from_bottom=32)
)
