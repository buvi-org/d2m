# Requirement: SMP-040-05
# Source agent: 040
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_040_kiosk_payment_hardware_single_metal_parts.json
# Part: Bill acceptor service cassette handle - single metal part
# Raw idea: Bill acceptor service cassette handle
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 80 x 35 x 64 mm using steel_a36
# - two through mounting holes diameter 13 mm at X=10/70, Y=17
# - central obround through slot 30 x 13 mm at X=40, Y=17
# - centered top rectangular relief pocket 25 x 18 x 4 mm deep
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
    Stock.rectangular(80, 35, 64, material="steel_a36")
    .drill_at(diameter=13, through=True, from_left=10, from_bottom=17, spot_drill=False)
    .drill_at(diameter=13, through=True, from_left=70, from_bottom=17, spot_drill=False)
    .slot_at(length=30, width=13, through=True, from_left=40, from_bottom=17)
    .pocket_at(width=18, length=25, depth=4, from_left=40, from_bottom=17)
)
