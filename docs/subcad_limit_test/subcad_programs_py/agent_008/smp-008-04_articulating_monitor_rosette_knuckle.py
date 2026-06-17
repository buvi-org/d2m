# Requirement: SMP-008-04
# Source agent: 008
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_008_creator_rigging_hardware_single_metal_parts.json
# Part: Articulating Monitor Rosette Knuckle - single metal part
# Raw idea: Articulating Monitor Rosette Knuckle
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 205 x 65 x 65 mm using aluminum_6061
# - two through mounting holes diameter 13 mm at X=13/192, Y=32
# - central obround through slot 68 x 12 mm at X=102, Y=32
# - centered top rectangular relief pocket 51 x 21 x 29 mm deep
# - 7 rear-edge serration positions with 3 mm depth intent
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - triangular serration tooth form is approximated by repeated rectangular groove cuts
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.

from subcad import Stock

part = (
    Stock.rectangular(205, 65, 65, material="aluminum_6061")
    .drill_at(diameter=13, through=True, from_left=13, from_bottom=32, spot_drill=False)
    .drill_at(diameter=13, through=True, from_left=192, from_bottom=32, spot_drill=False)
    .slot_at(length=68, width=12, through=True, from_left=102, from_bottom=32)
    .pocket(width=21, length=51, depth=29, cx=0, cy=0)
    .groove(length=3, width=6.036, depth=3, cx=-101, cy=-27.857, angle=90)
    .groove(length=3, width=6.036, depth=3, cx=-101, cy=-18.571, angle=90)
    .groove(length=3, width=6.036, depth=3, cx=-101, cy=-9.286, angle=90)
    .groove(length=3, width=6.036, depth=3, cx=-101, cy=0, angle=90)
    .groove(length=3, width=6.036, depth=3, cx=-101, cy=9.286, angle=90)
    .groove(length=3, width=6.036, depth=3, cx=-101, cy=18.571, angle=90)
    .groove(length=3, width=6.036, depth=3, cx=-101, cy=27.857, angle=90)
)
