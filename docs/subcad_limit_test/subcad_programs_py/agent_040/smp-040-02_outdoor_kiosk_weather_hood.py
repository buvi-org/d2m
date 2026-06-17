# Requirement: SMP-040-02
# Source agent: 040
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_040_kiosk_payment_hardware_single_metal_parts.json
# Part: Outdoor kiosk weather hood - single metal part
# Raw idea: Outdoor kiosk weather hood
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 165 x 35 x 28 mm using aluminum_6061
# - two through mounting holes diameter 6 mm at X=10/155, Y=17
# - central obround through slot 55 x 16 mm at X=82, Y=17
# - centered top rectangular relief pocket 41 x 18 x 3 mm deep
# - angled top reference face over last 33 mm using a sloped-floor cut for 14 degree intent
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
    Stock.rectangular(165, 35, 28, material="aluminum_6061")
    .drill_at(diameter=6, through=True, from_left=10, from_bottom=17, spot_drill=False)
    .drill_at(diameter=6, through=True, from_left=155, from_bottom=17, spot_drill=False)
    .slot_at(length=55, width=16, through=True, from_left=82, from_bottom=17)
    .pocket_at(width=18, length=41, depth=3, from_left=82, from_bottom=17)
    .slope_cut(width=35, length=33, start_depth=0, end_depth=8.228, cx=66, cy=0, slope_axis="X")
)
