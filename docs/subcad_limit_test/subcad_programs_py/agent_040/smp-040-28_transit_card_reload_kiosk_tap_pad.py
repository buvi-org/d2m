# Requirement: SMP-040-28
# Source agent: 040
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_040_kiosk_payment_hardware_single_metal_parts.json
# Part: Transit card reload kiosk tap pad - single metal part
# Raw idea: Transit card reload kiosk tap pad
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 130 x 115 x 8 mm using aluminum_6061
# - two through mounting holes diameter 11 mm at X=23/107, Y=57
# - central obround through slot 43 x 14 mm at X=65, Y=57
# - centered top rectangular relief pocket 32 x 38 x 3 mm deep
# - end hook lip/undercut proxy: projection 18 mm, undercut 6 mm
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - Leave an integral hook lip on one short end, projecting 18 mm and undercut 6 mm for registration. A projecting integral hook lip is approximated by an end groove within the rectangular envelope.
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted by this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.
# - Rectangular/sheet X/Y feature placement uses drill_at/slot_at/pocket_at datum offsets from the lower-left requirement origin where applicable.

from subcad import Stock

part = (
    Stock.rectangular(130, 115, 8, material="aluminum_6061")
    .drill_at(diameter=11, through=True, from_left=23, from_bottom=57, spot_drill=False)
    .drill_at(diameter=11, through=True, from_left=107, from_bottom=57, spot_drill=False)
    .slot_at(length=43, width=14, through=True, from_left=65, from_bottom=57)
    .pocket_at(width=38, length=32, depth=3, from_left=65, from_bottom=57)
    .groove(length=18, width=115, depth=6, cx=-56, cy=0)
)
