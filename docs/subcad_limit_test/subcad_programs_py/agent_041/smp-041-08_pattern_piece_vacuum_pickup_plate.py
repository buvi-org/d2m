# Requirement: SMP-041-08
# Source agent: 041
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_041_apparel_production_fixtures_single_metal_parts.json
# Part: Pattern Piece Vacuum Pickup Plate - single metal part
# Raw idea: Pattern Piece Vacuum Pickup Plate
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 245 x 135 x 11 mm using aluminum_6061
# - two through mounting holes diameter 8 mm at X=27/218, Y=67
# - central obround through slot 81 x 8 mm at X=122, Y=67
# - centered top rectangular relief pocket 61 x 45 x 3 mm deep
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
    Stock.rectangular(245, 135, 11, material="aluminum_6061")
    .drill_at(diameter=8, through=True, from_left=27, from_bottom=67, spot_drill=False)
    .drill_at(diameter=8, through=True, from_left=218, from_bottom=67, spot_drill=False)
    .slot_at(length=81, width=8, through=True, from_left=122, from_bottom=67)
    .pocket_at(width=45, length=61, depth=3, from_left=122, from_bottom=67)
)
