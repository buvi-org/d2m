# Requirement: SMP-042-15
# Source agent: 042
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_042_glass_handling_hardware_single_metal_parts.json
# Part: Sliding Door Glass Stop Bracket - single metal part
# Raw idea: Sliding Door Glass Stop Bracket
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 85 x 75 x 4 mm using steel_a36
# - two through mounting holes diameter 5 mm at X=15/70, Y=37
# - central obround through slot 30 x 12 mm at X=42, Y=37
# - centered top rectangular relief pocket 25 x 25 x 1 mm deep
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
    Stock.rectangular(85, 75, 4, material="steel_a36")
    .drill_at(diameter=5, through=True, from_left=15, from_bottom=37, spot_drill=False)
    .drill_at(diameter=5, through=True, from_left=70, from_bottom=37, spot_drill=False)
    .slot_at(length=30, width=12, through=True, from_left=42, from_bottom=37)
    .pocket_at(width=25, length=25, depth=1, from_left=42, from_bottom=37)
)
