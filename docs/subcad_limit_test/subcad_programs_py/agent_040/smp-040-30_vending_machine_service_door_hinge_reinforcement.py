# Requirement: SMP-040-30
# Source agent: 040
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_040_kiosk_payment_hardware_single_metal_parts.json
# Part: Vending machine service door hinge reinforcement - single metal part
# Raw idea: Vending machine service door hinge reinforcement
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 210 x 115 x 6 mm using steel_a36
# - two through mounting holes diameter 13 mm at X=23/187, Y=57
# - central obround through slot 70 x 8 mm at X=105, Y=57
# - centered top rectangular relief pocket 52 x 38 x 1 mm deep
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
    Stock.rectangular(210, 115, 6, material="steel_a36")
    .drill_at(diameter=13, through=True, from_left=23, from_bottom=57, spot_drill=False)
    .drill_at(diameter=13, through=True, from_left=187, from_bottom=57, spot_drill=False)
    .slot_at(length=70, width=8, through=True, from_left=105, from_bottom=57)
    .pocket_at(width=38, length=52, depth=1, from_left=105, from_bottom=57)
)
