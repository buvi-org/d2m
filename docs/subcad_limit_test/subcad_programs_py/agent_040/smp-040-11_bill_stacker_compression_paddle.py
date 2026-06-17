# Requirement: SMP-040-11
# Source agent: 040
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_040_kiosk_payment_hardware_single_metal_parts.json
# Part: Bill stacker compression paddle - single metal part
# Raw idea: Bill stacker compression paddle
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 205 x 70 x 64 mm using steel_1045
# - two through mounting holes diameter 6 mm at X=14/191, Y=35
# - central obround through slot 68 x 18 mm at X=102, Y=35
# - centered top rectangular relief pocket 51 x 23 x 25 mm deep
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
    Stock.rectangular(205, 70, 64, material="steel_1045")
    .drill_at(diameter=6, through=True, from_left=14, from_bottom=35, spot_drill=False)
    .drill_at(diameter=6, through=True, from_left=191, from_bottom=35, spot_drill=False)
    .slot_at(length=68, width=18, through=True, from_left=102, from_bottom=35)
    .pocket_at(width=23, length=51, depth=25, from_left=102, from_bottom=35)
)
