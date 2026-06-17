# Requirement: SMP-042-30
# Source agent: 042
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_042_glass_handling_hardware_single_metal_parts.json
# Part: Window Spacer Frame Corner Crimper - single metal part
# Raw idea: Window Spacer Frame Corner Crimper
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 75 x 70 x 20 mm using steel_a36
# - two through mounting holes diameter 11 mm at X=14/61, Y=35
# - central obround through slot 30 x 10 mm at X=37, Y=35
# - centered top rectangular relief pocket 25 x 23 x 1 mm deep
# - angled top reference face over last 18 mm using a sloped-floor cut for 28 degree intent
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
    Stock.rectangular(75, 70, 20, material="steel_a36")
    .drill_at(diameter=11, through=True, from_left=14, from_bottom=35, spot_drill=False)
    .drill_at(diameter=11, through=True, from_left=61, from_bottom=35, spot_drill=False)
    .slot_at(length=30, width=10, through=True, from_left=37, from_bottom=35)
    .pocket_at(width=23, length=25, depth=1, from_left=37, from_bottom=35)
    .slope_cut(width=70, length=18, start_depth=0, end_depth=9.571, cx=28.5, cy=0, slope_axis="X")
)
