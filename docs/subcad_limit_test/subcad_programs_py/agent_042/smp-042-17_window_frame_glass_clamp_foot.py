# Requirement: SMP-042-17
# Source agent: 042
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_042_glass_handling_hardware_single_metal_parts.json
# Part: Window Frame Glass Clamp Foot - single metal part
# Raw idea: Window Frame Glass Clamp Foot
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 150 x 115 x 49 mm using steel_1045
# - two through mounting holes diameter 13 mm at X=23/127, Y=57
# - central obround through slot 50 x 7 mm at X=75, Y=57
# - centered top rectangular relief pocket 37 x 38 x 21 mm deep
# - 7 rear-edge serration positions with 5 mm depth intent
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - Triangular serration tooth form is approximated by repeated rectangular groove cuts.
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted by this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.
# - Rectangular/sheet X/Y feature placement uses drill_at/slot_at/pocket_at datum offsets from the lower-left requirement origin where applicable.

from subcad import Stock

part = (
    Stock.rectangular(150, 115, 49, material="steel_1045")
    .drill_at(diameter=13, through=True, from_left=23, from_bottom=57, spot_drill=False)
    .drill_at(diameter=13, through=True, from_left=127, from_bottom=57, spot_drill=False)
    .slot_at(length=50, width=7, through=True, from_left=75, from_bottom=57)
    .pocket_at(width=38, length=37, depth=21, from_left=75, from_bottom=57)
    .groove(length=5, width=10.679, depth=5, cx=-72.5, cy=-49.286, angle=90)
    .groove(length=5, width=10.679, depth=5, cx=-72.5, cy=-32.857, angle=90)
    .groove(length=5, width=10.679, depth=5, cx=-72.5, cy=-16.429, angle=90)
    .groove(length=5, width=10.679, depth=5, cx=-72.5, cy=0, angle=90)
    .groove(length=5, width=10.679, depth=5, cx=-72.5, cy=16.429, angle=90)
    .groove(length=5, width=10.679, depth=5, cx=-72.5, cy=32.857, angle=90)
    .groove(length=5, width=10.679, depth=5, cx=-72.5, cy=49.286, angle=90)
)
