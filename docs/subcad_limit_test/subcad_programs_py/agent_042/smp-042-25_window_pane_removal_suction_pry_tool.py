# Requirement: SMP-042-25
# Source agent: 042
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_042_glass_handling_hardware_single_metal_parts.json
# Part: Window Pane Removal Suction Pry Tool - single metal part
# Raw idea: Window Pane Removal Suction Pry Tool
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 135 x 125 x 8 mm using steel_a36
# - two through mounting holes diameter 11 mm at X=25/110, Y=62
# - central obround through slot 45 x 10 mm at X=67, Y=62
# - centered top rectangular relief pocket 33 x 41 x 2 mm deep
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
    Stock.rectangular(135, 125, 8, material="steel_a36")
    .drill_at(diameter=11, through=True, from_left=25, from_bottom=62, spot_drill=False)
    .drill_at(diameter=11, through=True, from_left=110, from_bottom=62, spot_drill=False)
    .slot_at(length=45, width=10, through=True, from_left=67, from_bottom=62)
    .pocket_at(width=41, length=33, depth=2, from_left=67, from_bottom=62)
)
