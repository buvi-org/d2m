# Requirement: SMP-041-10
# Source agent: 041
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_041_apparel_production_fixtures_single_metal_parts.json
# Part: Cutting Table Scrap Collection Trough - single metal part
# Raw idea: Cutting Table Scrap Collection Trough
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 125 x 65 x 64 mm using steel_a36
# - two through mounting holes diameter 5 mm at X=13/112, Y=32
# - central obround through slot 41 x 18 mm at X=62, Y=32
# - centered top rectangular relief pocket 31 x 21 x 7 mm deep
# - angled top reference face over last 25 mm using a sloped-floor cut for 21 degree intent
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
    Stock.rectangular(125, 65, 64, material="steel_a36")
    .drill_at(diameter=5, through=True, from_left=13, from_bottom=32, spot_drill=False)
    .drill_at(diameter=5, through=True, from_left=112, from_bottom=32, spot_drill=False)
    .slot_at(length=41, width=18, through=True, from_left=62, from_bottom=32)
    .pocket_at(width=21, length=31, depth=7, from_left=62, from_bottom=32)
    .slope_cut(width=65, length=25, start_depth=0, end_depth=9.597, cx=50, cy=0, slope_axis="X")
)
