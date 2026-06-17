# Requirement: SMP-040-17
# Source agent: 040
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_040_kiosk_payment_hardware_single_metal_parts.json
# Part: Kiosk barcode scanner shroud - single metal part
# Raw idea: Kiosk barcode scanner shroud
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 90 x 75 x 65 mm using aluminum_6061
# - two through mounting holes diameter 10 mm at X=15/75, Y=37
# - central obround through slot 30 x 13 mm at X=45, Y=37
# - centered top rectangular relief pocket 25 x 25 x 17 mm deep
# - angled top reference face over last 18 mm using a sloped-floor cut for 29 degree intent
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - Angled reference face is represented as a sloped rectangular floor cut rather than a true exterior face reprofile.
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted by this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.
# - Rectangular/sheet X/Y feature placement uses drill_at/slot_at/pocket_at datum offsets from the lower-left requirement origin where applicable.

from subcad import Stock

part = (
    Stock.rectangular(90, 75, 65, material="aluminum_6061")
    .drill_at(diameter=10, through=True, from_left=15, from_bottom=37, spot_drill=False)
    .drill_at(diameter=10, through=True, from_left=75, from_bottom=37, spot_drill=False)
    .slot_at(length=30, width=13, through=True, from_left=45, from_bottom=37)
    .pocket_at(width=25, length=25, depth=17, from_left=45, from_bottom=37)
    .slope_cut(width=75, length=18, start_depth=0, end_depth=9.978, cx=36, cy=0, slope_axis="X")
)
