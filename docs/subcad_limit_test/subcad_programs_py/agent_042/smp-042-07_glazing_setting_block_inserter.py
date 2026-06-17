# Requirement: SMP-042-07
# Source agent: 042
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_042_glass_handling_hardware_single_metal_parts.json
# Part: Glazing Setting Block Inserter - single metal part
# Raw idea: Glazing Setting Block Inserter
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 130 x 75 x 17 mm using steel_a36
# - two through mounting holes diameter 7 mm at X=15/115, Y=37
# - central obround through slot 43 x 16 mm at X=65, Y=37
# - centered top rectangular relief pocket 32 x 25 x 7 mm deep
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
    Stock.rectangular(130, 75, 17, material="steel_a36")
    .drill_at(diameter=7, through=True, from_left=15, from_bottom=37, spot_drill=False)
    .drill_at(diameter=7, through=True, from_left=115, from_bottom=37, spot_drill=False)
    .slot_at(length=43, width=16, through=True, from_left=65, from_bottom=37)
    .pocket_at(width=25, length=32, depth=7, from_left=65, from_bottom=37)
)
