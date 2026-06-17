# Requirement: SMP-042-12
# Source agent: 042
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_042_glass_handling_hardware_single_metal_parts.json
# Part: Glass Sheet Separation Wedge Pair - single metal part
# Raw idea: Glass Sheet Separation Wedge Pair
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 205 x 65 x 5 mm using steel_a36
# - two through mounting holes diameter 7 mm at X=13/192, Y=32
# - central obround through slot 68 x 15 mm at X=102, Y=32
# - centered top rectangular relief pocket 51 x 21 x 1 mm deep
# - angled top reference face over last 41 mm using a sloped-floor cut for 18 degree intent
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - Angled reference face is represented as a sloped rectangular floor cut rather than a true exterior face reprofile.
# - Computed 18 degree slope over 41 mm would remove 13.322 mm, exceeding the 5 mm stock height; draft clamps slope depth to 4.5 mm.
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted by this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.
# - Rectangular/sheet X/Y feature placement uses drill_at/slot_at/pocket_at datum offsets from the lower-left requirement origin where applicable.

from subcad import Stock

part = (
    Stock.rectangular(205, 65, 5, material="steel_a36")
    .drill_at(diameter=7, through=True, from_left=13, from_bottom=32, spot_drill=False)
    .drill_at(diameter=7, through=True, from_left=192, from_bottom=32, spot_drill=False)
    .slot_at(length=68, width=15, through=True, from_left=102, from_bottom=32)
    .pocket_at(width=21, length=51, depth=1, from_left=102, from_bottom=32)
    .slope_cut(width=65, length=41, start_depth=0, end_depth=4.5, cx=82, cy=0, slope_axis="X")
)
