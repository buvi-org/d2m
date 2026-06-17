# Requirement: SMP-041-15
# Source agent: 041
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_041_apparel_production_fixtures_single_metal_parts.json
# Part: Robotic Hem Feed Guide - single metal part
# Raw idea: Robotic Hem Feed Guide
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 100 x 70 x 70 mm using aluminum_6061
# - two through mounting holes diameter 6 mm at X=14/86, Y=35
# - central obround through slot 33 x 8 mm at X=50, Y=35
# - centered top rectangular relief pocket 25 x 23 x 1 mm deep
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
    Stock.rectangular(100, 70, 70, material="aluminum_6061")
    .drill_at(diameter=6, through=True, from_left=14, from_bottom=35, spot_drill=False)
    .drill_at(diameter=6, through=True, from_left=86, from_bottom=35, spot_drill=False)
    .slot_at(length=33, width=8, through=True, from_left=50, from_bottom=35)
    .pocket_at(width=23, length=25, depth=1, from_left=50, from_bottom=35)
)
