# Requirement: SMP-042-11
# Source agent: 042
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_042_glass_handling_hardware_single_metal_parts.json
# Part: Window Corner Silicone Smoothing Guide - single metal part
# Raw idea: Window Corner Silicone Smoothing Guide
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 135 x 115 x 54 mm using steel_a36
# - two through mounting holes diameter 10 mm at X=23/112, Y=57
# - central obround through slot 45 x 14 mm at X=67, Y=57
# - centered top rectangular relief pocket 33 x 38 x 9 mm deep
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
    Stock.rectangular(135, 115, 54, material="steel_a36")
    .drill_at(diameter=10, through=True, from_left=23, from_bottom=57, spot_drill=False)
    .drill_at(diameter=10, through=True, from_left=112, from_bottom=57, spot_drill=False)
    .slot_at(length=45, width=14, through=True, from_left=67, from_bottom=57)
    .pocket_at(width=38, length=33, depth=9, from_left=67, from_bottom=57)
)
