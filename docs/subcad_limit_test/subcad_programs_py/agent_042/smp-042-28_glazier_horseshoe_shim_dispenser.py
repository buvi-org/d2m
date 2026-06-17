# Requirement: SMP-042-28
# Source agent: 042
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_042_glass_handling_hardware_single_metal_parts.json
# Part: Glazier Horseshoe Shim Dispenser - single metal part
# Raw idea: Glazier Horseshoe Shim Dispenser
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 195 x 95 x 19 mm using steel_a36
# - two through mounting holes diameter 6 mm at X=19/176, Y=47
# - central obround through slot 65 x 11 mm at X=97, Y=47
# - centered top rectangular relief pocket 48 x 31 x 3 mm deep
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
    Stock.rectangular(195, 95, 19, material="steel_a36")
    .drill_at(diameter=6, through=True, from_left=19, from_bottom=47, spot_drill=False)
    .drill_at(diameter=6, through=True, from_left=176, from_bottom=47, spot_drill=False)
    .slot_at(length=65, width=11, through=True, from_left=97, from_bottom=47)
    .pocket_at(width=31, length=48, depth=3, from_left=97, from_bottom=47)
)
