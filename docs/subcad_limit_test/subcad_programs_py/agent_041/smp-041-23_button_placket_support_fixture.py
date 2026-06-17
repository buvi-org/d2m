# Requirement: SMP-041-23
# Source agent: 041
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_041_apparel_production_fixtures_single_metal_parts.json
# Part: Button Placket Support Fixture - single metal part
# Raw idea: Button Placket Support Fixture
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 215 x 90 x 62 mm using steel_a36
# - two through mounting holes diameter 6 mm at X=18/197, Y=45
# - central obround through slot 71 x 17 mm at X=107, Y=45
# - centered top rectangular relief pocket 53 x 30 x 17 mm deep
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
    Stock.rectangular(215, 90, 62, material="steel_a36")
    .drill_at(diameter=6, through=True, from_left=18, from_bottom=45, spot_drill=False)
    .drill_at(diameter=6, through=True, from_left=197, from_bottom=45, spot_drill=False)
    .slot_at(length=71, width=17, through=True, from_left=107, from_bottom=45)
    .pocket_at(width=30, length=53, depth=17, from_left=107, from_bottom=45)
)
