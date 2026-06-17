# Requirement: SMP-040-13
# Source agent: 040
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_040_kiosk_payment_hardware_single_metal_parts.json
# Part: Ticket dispenser tear bar carrier - single metal part
# Raw idea: Ticket dispenser tear bar carrier
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 110 x 75 x 57 mm using steel_a36
# - two through mounting holes diameter 10 mm at X=15/95, Y=37
# - central obround through slot 36 x 17 mm at X=55, Y=37
# - centered top rectangular relief pocket 27 x 25 x 15 mm deep
# - 5 rear-edge serration positions with 4 mm depth intent
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - Triangular serration tooth form is approximated by repeated rectangular groove cuts.
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted by this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.
# - Rectangular/sheet X/Y feature placement uses drill_at/slot_at/pocket_at datum offsets from the lower-left requirement origin where applicable.

from subcad import Stock

part = (
    Stock.rectangular(110, 75, 57, material="steel_a36")
    .drill_at(diameter=10, through=True, from_left=15, from_bottom=37, spot_drill=False)
    .drill_at(diameter=10, through=True, from_left=95, from_bottom=37, spot_drill=False)
    .slot_at(length=36, width=17, through=True, from_left=55, from_bottom=37)
    .pocket_at(width=25, length=27, depth=15, from_left=55, from_bottom=37)
    .groove(length=4, width=9.75, depth=4, cx=-53, cy=-30, angle=90)
    .groove(length=4, width=9.75, depth=4, cx=-53, cy=-15, angle=90)
    .groove(length=4, width=9.75, depth=4, cx=-53, cy=0, angle=90)
    .groove(length=4, width=9.75, depth=4, cx=-53, cy=15, angle=90)
    .groove(length=4, width=9.75, depth=4, cx=-53, cy=30, angle=90)
)
