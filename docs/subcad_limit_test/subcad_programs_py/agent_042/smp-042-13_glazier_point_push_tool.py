# Requirement: SMP-042-13
# Source agent: 042
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_042_glass_handling_hardware_single_metal_parts.json
# Part: Glazier Point Push Tool - single metal part
# Raw idea: Glazier Point Push Tool
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 210 x 115 x 36 mm using steel_1045
# - two through mounting holes diameter 6 mm at X=23/187, Y=57
# - central obround through slot 70 x 13 mm at X=105, Y=57
# - centered top rectangular relief pocket 52 x 38 x 2 mm deep
# - angled top reference face over last 42 mm using a sloped-floor cut for 42 degree intent
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - Angled reference face is represented as a sloped rectangular floor cut rather than a true exterior face reprofile.
# - Computed 42 degree slope over 42 mm would remove 37.817 mm, exceeding the 36 mm stock height; draft clamps slope depth to 35.5 mm.
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted by this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.
# - Rectangular/sheet X/Y feature placement uses drill_at/slot_at/pocket_at datum offsets from the lower-left requirement origin where applicable.

from subcad import Stock

part = (
    Stock.rectangular(210, 115, 36, material="steel_1045")
    .drill_at(diameter=6, through=True, from_left=23, from_bottom=57, spot_drill=False)
    .drill_at(diameter=6, through=True, from_left=187, from_bottom=57, spot_drill=False)
    .slot_at(length=70, width=13, through=True, from_left=105, from_bottom=57)
    .pocket_at(width=38, length=52, depth=2, from_left=105, from_bottom=57)
    .slope_cut(width=115, length=42, start_depth=0, end_depth=35.5, cx=84, cy=0, slope_axis="X")
)
