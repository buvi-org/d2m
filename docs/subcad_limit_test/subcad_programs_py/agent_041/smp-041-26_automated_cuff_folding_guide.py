# Requirement: SMP-041-26
# Source agent: 041
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_041_apparel_production_fixtures_single_metal_parts.json
# Part: Automated Cuff Folding Guide - single metal part
# Raw idea: Automated Cuff Folding Guide
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 190 x 115 x 44 mm using steel_a36
# - two through mounting holes diameter 5 mm at X=23/167, Y=57
# - central obround through slot 63 x 10 mm at X=95, Y=57
# - centered top rectangular relief pocket 47 x 38 x 2 mm deep
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
    Stock.rectangular(190, 115, 44, material="steel_a36")
    .drill_at(diameter=5, through=True, from_left=23, from_bottom=57, spot_drill=False)
    .drill_at(diameter=5, through=True, from_left=167, from_bottom=57, spot_drill=False)
    .slot_at(length=63, width=10, through=True, from_left=95, from_bottom=57)
    .pocket_at(width=38, length=47, depth=2, from_left=95, from_bottom=57)
)
