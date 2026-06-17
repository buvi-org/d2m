# Requirement: SMP-041-21
# Source agent: 041
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_041_apparel_production_fixtures_single_metal_parts.json
# Part: Garment Hanger Loading Funnel - single metal part
# Raw idea: Garment Hanger Loading Funnel
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 120 x 110 x 48 mm using steel_a36
# - two through mounting holes diameter 10 mm at X=22/98, Y=55
# - central obround through slot 40 x 8 mm at X=60, Y=55
# - centered top rectangular relief pocket 30 x 36 x 19 mm deep
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
    Stock.rectangular(120, 110, 48, material="steel_a36")
    .drill_at(diameter=10, through=True, from_left=22, from_bottom=55, spot_drill=False)
    .drill_at(diameter=10, through=True, from_left=98, from_bottom=55, spot_drill=False)
    .slot_at(length=40, width=8, through=True, from_left=60, from_bottom=55)
    .pocket_at(width=36, length=30, depth=19, from_left=60, from_bottom=55)
)
