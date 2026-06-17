# Requirement: SMP-041-29
# Source agent: 041
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_041_apparel_production_fixtures_single_metal_parts.json
# Part: Soft Goods Transfer Paddle - single metal part
# Raw idea: Soft Goods Transfer Paddle
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 190 x 130 x 12 mm using aluminum_6061
# - two through mounting holes diameter 12 mm at X=26/164, Y=65
# - central obround through slot 63 x 14 mm at X=95, Y=65
# - centered top rectangular relief pocket 47 x 43 x 1 mm deep
# - angled top reference face over last 38 mm using a sloped-floor cut for 30 degree intent
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - Angled reference face is represented as a sloped rectangular floor cut rather than a true exterior face reprofile.
# - Computed 30 degree slope over 38 mm would remove 21.939 mm, exceeding the 12 mm stock height; draft clamps slope depth to 11.5 mm.
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted by this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.
# - Rectangular/sheet X/Y feature placement uses drill_at/slot_at/pocket_at datum offsets from the lower-left requirement origin where applicable.

from subcad import Stock

part = (
    Stock.rectangular(190, 130, 12, material="aluminum_6061")
    .drill_at(diameter=12, through=True, from_left=26, from_bottom=65, spot_drill=False)
    .drill_at(diameter=12, through=True, from_left=164, from_bottom=65, spot_drill=False)
    .slot_at(length=63, width=14, through=True, from_left=95, from_bottom=65)
    .pocket_at(width=43, length=47, depth=1, from_left=95, from_bottom=65)
    .slope_cut(width=130, length=38, start_depth=0, end_depth=11.5, cx=76, cy=0, slope_axis="X")
)
