# Requirement: SMP-041-14
# Source agent: 041
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_041_apparel_production_fixtures_single_metal_parts.json
# Part: Garment Bundle Compression Shelf - single metal part
# Raw idea: Garment Bundle Compression Shelf
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 210 x 140 x 12 mm using steel_1045
# - two through mounting holes diameter 9 mm at X=28/182, Y=70
# - central obround through slot 70 x 10 mm at X=105, Y=70
# - centered top rectangular relief pocket 52 x 46 x 6 mm deep
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
    Stock.rectangular(210, 140, 12, material="steel_1045")
    .drill_at(diameter=9, through=True, from_left=28, from_bottom=70, spot_drill=False)
    .drill_at(diameter=9, through=True, from_left=182, from_bottom=70, spot_drill=False)
    .slot_at(length=70, width=10, through=True, from_left=105, from_bottom=70)
    .pocket_at(width=46, length=52, depth=6, from_left=105, from_bottom=70)
)
