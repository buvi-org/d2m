# Requirement: SMP-041-02
# Source agent: 041
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_041_apparel_production_fixtures_single_metal_parts.json
# Part: Hanging Garment Rail Diverter - single metal part
# Raw idea: Hanging Garment Rail Diverter
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 155 x 55 x 25 mm using steel_a36
# - two through mounting holes diameter 6 mm at X=11/144, Y=27
# - central obround through slot 51 x 16 mm at X=77, Y=27
# - centered top rectangular relief pocket 38 x 18 x 1 mm deep
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
    Stock.rectangular(155, 55, 25, material="steel_a36")
    .drill_at(diameter=6, through=True, from_left=11, from_bottom=27, spot_drill=False)
    .drill_at(diameter=6, through=True, from_left=144, from_bottom=27, spot_drill=False)
    .slot_at(length=51, width=16, through=True, from_left=77, from_bottom=27)
    .pocket_at(width=18, length=38, depth=1, from_left=77, from_bottom=27)
)
