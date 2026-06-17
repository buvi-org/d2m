# Requirement: SMP-002-04
# Source agent: 002
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_002_mobility_hardware_single_metal_parts.json
# Part: Bicycle disc brake flat-mount adapter with cooling fins - single metal part
# Raw idea: Bicycle disc brake flat-mount adapter with cooling fins
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 205 x 105 x 41 mm using steel_a36
# - two through mounting holes diameter 8 mm at X=21/184, Y=52
# - central obround through slot 68 x 12 mm at X=102, Y=52
# - centered top rectangular relief pocket 51 x 35 x 18 mm deep
# - central counterbore diameter 20 mm x 6 mm deep around center feature
# - 11 rear-edge serration positions with 3 mm depth intent
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - counterbore around an obround slot is represented with a circular counterbore operation
# - triangular serration tooth form is approximated by repeated rectangular groove cuts
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.

from subcad import Stock

part = (
    Stock.rectangular(205, 105, 41, material="steel_a36")
    .drill_at(diameter=8, through=True, from_left=21, from_bottom=52, spot_drill=False)
    .drill_at(diameter=8, through=True, from_left=184, from_bottom=52, spot_drill=False)
    .slot_at(length=68, width=12, through=True, from_left=102, from_bottom=52)
    .pocket(width=35, length=51, depth=18, cx=0, cy=0)
    .counterbore(hole_diameter=12, counterbore_diameter=20, counterbore_depth=6, cx=-0.5, cy=-0.5, through=True)
    .groove(length=3, width=6.205, depth=3, cx=-101, cy=-47.727, angle=90)
    .groove(length=3, width=6.205, depth=3, cx=-101, cy=-38.182, angle=90)
    .groove(length=3, width=6.205, depth=3, cx=-101, cy=-28.636, angle=90)
    .groove(length=3, width=6.205, depth=3, cx=-101, cy=-19.091, angle=90)
    .groove(length=3, width=6.205, depth=3, cx=-101, cy=-9.545, angle=90)
    .groove(length=3, width=6.205, depth=3, cx=-101, cy=0, angle=90)
    .groove(length=3, width=6.205, depth=3, cx=-101, cy=9.545, angle=90)
    .groove(length=3, width=6.205, depth=3, cx=-101, cy=19.091, angle=90)
    .groove(length=3, width=6.205, depth=3, cx=-101, cy=28.636, angle=90)
    .groove(length=3, width=6.205, depth=3, cx=-101, cy=38.182, angle=90)
    .groove(length=3, width=6.205, depth=3, cx=-101, cy=47.727, angle=90)
)
