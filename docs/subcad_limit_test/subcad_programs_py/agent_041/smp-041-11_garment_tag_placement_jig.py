# Requirement: SMP-041-11
# Source agent: 041
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_041_apparel_production_fixtures_single_metal_parts.json
# Part: Garment Tag Placement Jig - single metal part
# Raw idea: Garment Tag Placement Jig
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 140 x 80 x 61 mm using stainless_316
# - two through mounting holes diameter 9 mm at X=16/124, Y=40
# - central obround through slot 46 x 14 mm at X=70, Y=40
# - centered top rectangular relief pocket 35 x 26 x 5 mm deep
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
    Stock.rectangular(140, 80, 61, material="stainless_316")
    .drill_at(diameter=9, through=True, from_left=16, from_bottom=40, spot_drill=False)
    .drill_at(diameter=9, through=True, from_left=124, from_bottom=40, spot_drill=False)
    .slot_at(length=46, width=14, through=True, from_left=70, from_bottom=40)
    .pocket_at(width=26, length=35, depth=5, from_left=70, from_bottom=40)
)
