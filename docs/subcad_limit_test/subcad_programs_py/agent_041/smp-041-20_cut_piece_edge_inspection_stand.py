# Requirement: SMP-041-20
# Source agent: 041
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_041_apparel_production_fixtures_single_metal_parts.json
# Part: Cut Piece Edge Inspection Stand - single metal part
# Raw idea: Cut Piece Edge Inspection Stand
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 190 x 70 x 62 mm using steel_a36
# - two through mounting holes diameter 6 mm at X=14/176, Y=35
# - central obround through slot 63 x 11 mm at X=95, Y=35
# - centered top rectangular relief pocket 47 x 23 x 14 mm deep
# - angled top reference face over last 38 mm using a sloped-floor cut for 32 degree intent
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
    Stock.rectangular(190, 70, 62, material="steel_a36")
    .drill_at(diameter=6, through=True, from_left=14, from_bottom=35, spot_drill=False)
    .drill_at(diameter=6, through=True, from_left=176, from_bottom=35, spot_drill=False)
    .slot_at(length=63, width=11, through=True, from_left=95, from_bottom=35)
    .pocket_at(width=23, length=47, depth=14, from_left=95, from_bottom=35)
    .slope_cut(width=70, length=38, start_depth=0, end_depth=23.745, cx=76, cy=0, slope_axis="X")
)
