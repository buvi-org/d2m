# Requirement: SMP-040-04
# Source agent: 040
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_040_kiosk_payment_hardware_single_metal_parts.json
# Part: Coin validator removable funnel - single metal part
# Raw idea: Coin validator removable funnel
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 125 x 115 x 50 mm using aluminum_6061
# - two through mounting holes diameter 6 mm at X=23/102, Y=57
# - central obround through slot 41 x 18 mm at X=62, Y=57
# - centered top rectangular relief pocket 31 x 38 x 12 mm deep
# - angled top reference face over last 25 mm using a sloped-floor cut for 10 degree intent
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
    Stock.rectangular(125, 115, 50, material="aluminum_6061")
    .drill_at(diameter=6, through=True, from_left=23, from_bottom=57, spot_drill=False)
    .drill_at(diameter=6, through=True, from_left=102, from_bottom=57, spot_drill=False)
    .slot_at(length=41, width=18, through=True, from_left=62, from_bottom=57)
    .pocket_at(width=38, length=31, depth=12, from_left=62, from_bottom=57)
    .slope_cut(width=115, length=25, start_depth=0, end_depth=4.408, cx=50, cy=0, slope_axis="X")
)
