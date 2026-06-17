# Requirement: SMP-041-28
# Source agent: 041
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_041_apparel_production_fixtures_single_metal_parts.json
# Part: Fabric Pattern Weight Placement Rack - single metal part
# Raw idea: Fabric Pattern Weight Placement Rack
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 210 x 35 x 38 mm using steel_a36
# - two through mounting holes diameter 13 mm at X=10/200, Y=17
# - central obround through slot 70 x 12 mm at X=105, Y=17
# - centered top rectangular relief pocket 52 x 18 x 5 mm deep
# - angled top reference face over last 42 mm using a sloped-floor cut for 39 degree intent
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
    Stock.rectangular(210, 35, 38, material="steel_a36")
    .drill_at(diameter=13, through=True, from_left=10, from_bottom=17, spot_drill=False)
    .drill_at(diameter=13, through=True, from_left=200, from_bottom=17, spot_drill=False)
    .slot_at(length=70, width=12, through=True, from_left=105, from_bottom=17)
    .pocket_at(width=18, length=52, depth=5, from_left=105, from_bottom=17)
    .slope_cut(width=35, length=42, start_depth=0, end_depth=34.011, cx=84, cy=0, slope_axis="X")
)
