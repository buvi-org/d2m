# Requirement: SMP-040-27
# Source agent: 040
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_040_kiosk_payment_hardware_single_metal_parts.json
# Part: Parking meter solar panel frame - single metal part
# Raw idea: Parking meter solar panel frame
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 150 x 140 x 3 mm using steel_a36
# - two through mounting holes diameter 11 mm at X=28/122, Y=70
# - central obround through slot 50 x 8 mm at X=75, Y=70
# - centered top rectangular relief pocket 37 x 46 x 1 mm deep
# - angled top reference face over last 30 mm using a sloped-floor cut for 35 degree intent
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - Angled reference face is represented as a sloped rectangular floor cut rather than a true exterior face reprofile.
# - Computed 35 degree slope over 30 mm would remove 21.006 mm, exceeding the 3 mm stock height; draft clamps slope depth to 2.5 mm.
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted by this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.
# - Rectangular/sheet X/Y feature placement uses drill_at/slot_at/pocket_at datum offsets from the lower-left requirement origin where applicable.

from subcad import Stock

part = (
    Stock.rectangular(150, 140, 3, material="steel_a36")
    .drill_at(diameter=11, through=True, from_left=28, from_bottom=70, spot_drill=False)
    .drill_at(diameter=11, through=True, from_left=122, from_bottom=70, spot_drill=False)
    .slot_at(length=50, width=8, through=True, from_left=75, from_bottom=70)
    .pocket_at(width=46, length=37, depth=1, from_left=75, from_bottom=70)
    .slope_cut(width=140, length=30, start_depth=0, end_depth=2.5, cx=60, cy=0, slope_axis="X")
)
