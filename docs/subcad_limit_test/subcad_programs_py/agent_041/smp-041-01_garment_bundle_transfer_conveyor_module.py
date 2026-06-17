# Requirement: SMP-041-01
# Source agent: 041
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_041_apparel_production_fixtures_single_metal_parts.json
# Part: Garment Bundle Transfer Conveyor Module - single metal part
# Raw idea: Garment Bundle Transfer Conveyor Module
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 95 x 85 x 69 mm using steel_a36
# - two through mounting holes diameter 5 mm at X=17/78, Y=42
# - central obround through slot 31 x 15 mm at X=47, Y=42
# - centered top rectangular relief pocket 25 x 28 x 33 mm deep
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
    Stock.rectangular(95, 85, 69, material="steel_a36")
    .drill_at(diameter=5, through=True, from_left=17, from_bottom=42, spot_drill=False)
    .drill_at(diameter=5, through=True, from_left=78, from_bottom=42, spot_drill=False)
    .slot_at(length=31, width=15, through=True, from_left=47, from_bottom=42)
    .pocket_at(width=28, length=25, depth=33, from_left=47, from_bottom=42)
)
