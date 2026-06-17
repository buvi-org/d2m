# Requirement: SMP-041-24
# Source agent: 041
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_041_apparel_production_fixtures_single_metal_parts.json
# Part: Textile Selvage Trim Conveyor Guide - single metal part
# Raw idea: Textile Selvage Trim Conveyor Guide
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 120 x 55 x 51 mm using steel_a36
# - two through mounting holes diameter 8 mm at X=11/109, Y=27
# - central obround through slot 40 x 18 mm at X=60, Y=27
# - centered top rectangular relief pocket 30 x 18 x 24 mm deep
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
    Stock.rectangular(120, 55, 51, material="steel_a36")
    .drill_at(diameter=8, through=True, from_left=11, from_bottom=27, spot_drill=False)
    .drill_at(diameter=8, through=True, from_left=109, from_bottom=27, spot_drill=False)
    .slot_at(length=40, width=18, through=True, from_left=60, from_bottom=27)
    .pocket_at(width=18, length=30, depth=24, from_left=60, from_bottom=27)
)
