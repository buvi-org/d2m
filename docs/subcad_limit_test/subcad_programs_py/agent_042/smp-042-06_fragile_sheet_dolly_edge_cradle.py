# Requirement: SMP-042-06
# Source agent: 042
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_042_glass_handling_hardware_single_metal_parts.json
# Part: Fragile Sheet Dolly Edge Cradle - single metal part
# Raw idea: Fragile Sheet Dolly Edge Cradle
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 175 x 125 x 10 mm using steel_a36
# - two through mounting holes diameter 8 mm at X=25/150, Y=62
# - central obround through slot 58 x 15 mm at X=87, Y=62
# - centered top rectangular relief pocket 43 x 41 x 1 mm deep
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
    Stock.rectangular(175, 125, 10, material="steel_a36")
    .drill_at(diameter=8, through=True, from_left=25, from_bottom=62, spot_drill=False)
    .drill_at(diameter=8, through=True, from_left=150, from_bottom=62, spot_drill=False)
    .slot_at(length=58, width=15, through=True, from_left=87, from_bottom=62)
    .pocket_at(width=41, length=43, depth=1, from_left=87, from_bottom=62)
)
