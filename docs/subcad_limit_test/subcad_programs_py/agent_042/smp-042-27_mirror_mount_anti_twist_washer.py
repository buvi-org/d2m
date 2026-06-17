# Requirement: SMP-042-27
# Source agent: 042
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_042_glass_handling_hardware_single_metal_parts.json
# Part: Mirror Mount Anti-Twist Washer - single metal part
# Raw idea: Mirror Mount Anti-Twist Washer
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 80 x 65 x 44 mm using steel_a36
# - two through mounting holes diameter 13 mm at X=13/67, Y=32
# - central obround through slot 30 x 14 mm at X=40, Y=32
# - centered top rectangular relief pocket 25 x 21 x 20 mm deep
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
    Stock.rectangular(80, 65, 44, material="steel_a36")
    .drill_at(diameter=13, through=True, from_left=13, from_bottom=32, spot_drill=False)
    .drill_at(diameter=13, through=True, from_left=67, from_bottom=32, spot_drill=False)
    .slot_at(length=30, width=14, through=True, from_left=40, from_bottom=32)
    .pocket_at(width=21, length=25, depth=20, from_left=40, from_bottom=32)
)
