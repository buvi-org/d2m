# Requirement: SMP-042-19
# Source agent: 042
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_042_glass_handling_hardware_single_metal_parts.json
# Part: Fragile Sheet Carry Strap Corner Saddle - single metal part
# Raw idea: Fragile Sheet Carry Strap Corner Saddle
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 195 x 135 x 11 mm using steel_a36
# - two through mounting holes diameter 5 mm at X=27/168, Y=67
# - central obround through slot 65 x 17 mm at X=97, Y=67
# - centered top rectangular relief pocket 48 x 45 x 4 mm deep
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
    Stock.rectangular(195, 135, 11, material="steel_a36")
    .drill_at(diameter=5, through=True, from_left=27, from_bottom=67, spot_drill=False)
    .drill_at(diameter=5, through=True, from_left=168, from_bottom=67, spot_drill=False)
    .slot_at(length=65, width=17, through=True, from_left=97, from_bottom=67)
    .pocket_at(width=45, length=48, depth=4, from_left=97, from_bottom=67)
)
