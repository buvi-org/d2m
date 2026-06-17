# Requirement: SMP-041-07
# Source agent: 041
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_041_apparel_production_fixtures_single_metal_parts.json
# Part: Fabric Edge Tracking Conveyor Section - single metal part
# Raw idea: Fabric Edge Tracking Conveyor Section
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 165 x 45 x 20 mm using steel_a36
# - two through mounting holes diameter 10 mm at X=10/155, Y=22
# - central obround through slot 55 x 18 mm at X=82, Y=22
# - centered top rectangular relief pocket 41 x 18 x 8 mm deep
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
    Stock.rectangular(165, 45, 20, material="steel_a36")
    .drill_at(diameter=10, through=True, from_left=10, from_bottom=22, spot_drill=False)
    .drill_at(diameter=10, through=True, from_left=155, from_bottom=22, spot_drill=False)
    .slot_at(length=55, width=18, through=True, from_left=82, from_bottom=22)
    .pocket_at(width=18, length=41, depth=8, from_left=82, from_bottom=22)
)
