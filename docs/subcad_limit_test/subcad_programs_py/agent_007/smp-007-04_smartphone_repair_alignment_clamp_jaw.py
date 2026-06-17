# Requirement: SMP-007-04
# Source agent: 007
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_007_consumer_electronics_single_metal_parts.json
# Part: Smartphone Repair Alignment Clamp Jaw - single metal part
# Raw idea: Smartphone Repair Alignment Clamp Jaw
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 210 x 60 x 70 mm using steel_1045
# - two through mounting holes diameter 5 mm at X=12/198, Y=30
# - central obround through slot 70 x 17 mm at X=105, Y=30
# - centered top rectangular relief pocket 52 x 20 x 9 mm deep
# - dovetail groove length 186 mm, throat 12 mm, included angle 60 degrees
# - 8 rear-edge serration positions with 2 mm depth intent
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - triangular serration tooth form is approximated by repeated rectangular groove cuts
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Dovetail depth was inferred because the requirement gives throat and angle but not groove depth.
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.

from subcad import Stock

part = (
    Stock.rectangular(210, 60, 70, material="steel_1045")
    .drill_at(diameter=5, through=True, from_left=12, from_bottom=30, spot_drill=False)
    .drill_at(diameter=5, through=True, from_left=198, from_bottom=30, spot_drill=False)
    .slot_at(length=70, width=17, through=True, from_left=105, from_bottom=30)
    .pocket(width=20, length=52, depth=9, cx=0, cy=0)
    .dovetail(length=186, width=12, depth=15.4, angle=60, cx=0, cy=0)
    .groove(length=2, width=4.875, depth=2, cx=-104, cy=-26.25, angle=90)
    .groove(length=2, width=4.875, depth=2, cx=-104, cy=-18.75, angle=90)
    .groove(length=2, width=4.875, depth=2, cx=-104, cy=-11.25, angle=90)
    .groove(length=2, width=4.875, depth=2, cx=-104, cy=-3.75, angle=90)
    .groove(length=2, width=4.875, depth=2, cx=-104, cy=3.75, angle=90)
    .groove(length=2, width=4.875, depth=2, cx=-104, cy=11.25, angle=90)
    .groove(length=2, width=4.875, depth=2, cx=-104, cy=18.75, angle=90)
    .groove(length=2, width=4.875, depth=2, cx=-104, cy=26.25, angle=90)
)
