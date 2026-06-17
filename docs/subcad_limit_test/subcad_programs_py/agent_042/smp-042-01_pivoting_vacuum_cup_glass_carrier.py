# Requirement: SMP-042-01
# Source agent: 042
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_042_glass_handling_hardware_single_metal_parts.json
# Part: Pivoting Vacuum Cup Glass Carrier - single metal part
# Raw idea: Pivoting Vacuum Cup Glass Carrier
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 185 x 40 x 60 mm using steel_a36
# - two through mounting holes diameter 9 mm at X=10/175, Y=20
# - central obround through slot 61 x 11 mm at X=92, Y=20
# - centered top rectangular relief pocket 46 x 18 x 29 mm deep
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
    Stock.rectangular(185, 40, 60, material="steel_a36")
    .drill_at(diameter=9, through=True, from_left=10, from_bottom=20, spot_drill=False)
    .drill_at(diameter=9, through=True, from_left=175, from_bottom=20, spot_drill=False)
    .slot_at(length=61, width=11, through=True, from_left=92, from_bottom=20)
    .pocket_at(width=18, length=46, depth=29, from_left=92, from_bottom=20)
)
