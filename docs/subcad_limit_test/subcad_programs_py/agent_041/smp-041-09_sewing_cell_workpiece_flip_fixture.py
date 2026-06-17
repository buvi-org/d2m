# Requirement: SMP-041-09
# Source agent: 041
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_041_apparel_production_fixtures_single_metal_parts.json
# Part: Sewing Cell Workpiece Flip Fixture - single metal part
# Raw idea: Sewing Cell Workpiece Flip Fixture
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 155 x 100 x 50 mm using steel_a36
# - two through mounting holes diameter 8 mm at X=20/135, Y=50
# - central obround through slot 51 x 16 mm at X=77, Y=50
# - centered top rectangular relief pocket 38 x 33 x 12 mm deep
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
    Stock.rectangular(155, 100, 50, material="steel_a36")
    .drill_at(diameter=8, through=True, from_left=20, from_bottom=50, spot_drill=False)
    .drill_at(diameter=8, through=True, from_left=135, from_bottom=50, spot_drill=False)
    .slot_at(length=51, width=16, through=True, from_left=77, from_bottom=50)
    .pocket_at(width=33, length=38, depth=12, from_left=77, from_bottom=50)
)
