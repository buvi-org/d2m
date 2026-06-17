# Requirement: SMP-040-29
# Source agent: 040
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_040_kiosk_payment_hardware_single_metal_parts.json
# Part: Bill recycler diverter flap - single metal part
# Raw idea: Bill recycler diverter flap
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 110 x 70 x 70 mm using steel_a36
# - two through mounting holes diameter 12 mm at X=14/96, Y=35
# - central obround through slot 36 x 13 mm at X=55, Y=35
# - centered top rectangular relief pocket 27 x 23 x 34 mm deep
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
    Stock.rectangular(110, 70, 70, material="steel_a36")
    .drill_at(diameter=12, through=True, from_left=14, from_bottom=35, spot_drill=False)
    .drill_at(diameter=12, through=True, from_left=96, from_bottom=35, spot_drill=False)
    .slot_at(length=36, width=13, through=True, from_left=55, from_bottom=35)
    .pocket_at(width=23, length=27, depth=34, from_left=55, from_bottom=35)
)
