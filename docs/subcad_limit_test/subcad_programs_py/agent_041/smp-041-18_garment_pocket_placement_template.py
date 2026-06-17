# Requirement: SMP-041-18
# Source agent: 041
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_041_apparel_production_fixtures_single_metal_parts.json
# Part: Garment Pocket Placement Template - single metal part
# Raw idea: Garment Pocket Placement Template
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 140 x 105 x 12 mm using steel_a36
# - two through mounting holes diameter 7 mm at X=21/119, Y=52
# - central obround through slot 46 x 8 mm at X=70, Y=52
# - centered top rectangular relief pocket 35 x 35 x 6 mm deep
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted by this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.
# - Rectangular/sheet X/Y feature placement uses drill_at/slot_at/pocket_at datum offsets from the lower-left requirement origin where applicable.

from subcad import Stock

part = (
    Stock.rectangular(140, 105, 12, material="steel_a36")
    .drill_at(diameter=7, through=True, from_left=21, from_bottom=52, spot_drill=False)
    .drill_at(diameter=7, through=True, from_left=119, from_bottom=52, spot_drill=False)
    .slot_at(length=46, width=8, through=True, from_left=70, from_bottom=52)
    .pocket_at(width=35, length=35, depth=6, from_left=70, from_bottom=52)
)
