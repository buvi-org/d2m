# Requirement: SMP-040-10
# Source agent: 040
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_040_kiosk_payment_hardware_single_metal_parts.json
# Part: Kiosk receipt bin overflow guard - single metal part
# Raw idea: Kiosk receipt bin overflow guard
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 250 x 65 x 10 mm using aluminum_6061
# - two through mounting holes diameter 12 mm at X=13/237, Y=32
# - central obround through slot 83 x 13 mm at X=125, Y=32
# - centered top rectangular relief pocket 62 x 21 x 5 mm deep
# - angled top reference face over last 50 mm using a sloped-floor cut for 32 degree intent
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - Angled reference face is represented as a sloped rectangular floor cut rather than a true exterior face reprofile.
# - Computed 32 degree slope over 50 mm would remove 31.243 mm, exceeding the 10 mm stock height; draft clamps slope depth to 9.5 mm.
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted by this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.
# - Rectangular/sheet X/Y feature placement uses drill_at/slot_at/pocket_at datum offsets from the lower-left requirement origin where applicable.

from subcad import Stock

part = (
    Stock.rectangular(250, 65, 10, material="aluminum_6061")
    .drill_at(diameter=12, through=True, from_left=13, from_bottom=32, spot_drill=False)
    .drill_at(diameter=12, through=True, from_left=237, from_bottom=32, spot_drill=False)
    .slot_at(length=83, width=13, through=True, from_left=125, from_bottom=32)
    .pocket_at(width=21, length=62, depth=5, from_left=125, from_bottom=32)
    .slope_cut(width=65, length=50, start_depth=0, end_depth=9.5, cx=100, cy=0, slope_axis="X")
)
