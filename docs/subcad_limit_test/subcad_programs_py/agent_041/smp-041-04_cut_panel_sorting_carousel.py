# Requirement: SMP-041-04
# Source agent: 041
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_041_apparel_production_fixtures_single_metal_parts.json
# Part: Cut Panel Sorting Carousel - single metal part
# Raw idea: Cut Panel Sorting Carousel
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 145 x 65 x 8 mm using steel_a36
# - two through mounting holes diameter 9 mm at X=13/132, Y=32
# - central obround through slot 48 x 7 mm at X=72, Y=32
# - centered top rectangular relief pocket 36 x 21 x 2 mm deep
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
    Stock.rectangular(145, 65, 8, material="steel_a36")
    .drill_at(diameter=9, through=True, from_left=13, from_bottom=32, spot_drill=False)
    .drill_at(diameter=9, through=True, from_left=132, from_bottom=32, spot_drill=False)
    .slot_at(length=48, width=7, through=True, from_left=72, from_bottom=32)
    .pocket_at(width=21, length=36, depth=2, from_left=72, from_bottom=32)
)
