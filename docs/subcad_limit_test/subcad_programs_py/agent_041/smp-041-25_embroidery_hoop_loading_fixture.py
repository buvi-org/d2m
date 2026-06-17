# Requirement: SMP-041-25
# Source agent: 041
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_041_apparel_production_fixtures_single_metal_parts.json
# Part: Embroidery Hoop Loading Fixture - single metal part
# Raw idea: Embroidery Hoop Loading Fixture
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 145 x 60 x 20 mm using steel_a36
# - two through mounting holes diameter 13 mm at X=12/133, Y=30
# - central obround through slot 48 x 7 mm at X=72, Y=30
# - centered top rectangular relief pocket 36 x 20 x 8 mm deep
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
    Stock.rectangular(145, 60, 20, material="steel_a36")
    .drill_at(diameter=13, through=True, from_left=12, from_bottom=30, spot_drill=False)
    .drill_at(diameter=13, through=True, from_left=133, from_bottom=30, spot_drill=False)
    .slot_at(length=48, width=7, through=True, from_left=72, from_bottom=30)
    .pocket_at(width=20, length=36, depth=8, from_left=72, from_bottom=30)
)
