# Requirement: SMP-026-03
# Source agent: 026
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_026_office_equipment_hardware_single_metal_parts.json
# Part: Adjustable Monitor Arm Tilt Knuckle - single metal part
# Raw idea: Adjustable Monitor Arm Tilt Knuckle
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 145 x 115 x 35 mm.
# - Two through mounting holes diameter 8 mm at X=23 and X=122, Y=57.
# - Central through obround slot 48 x 14 mm at X=72, Y=57.
# - Top relief pocket 36 x 38 x 6 mm centered between mounting holes.
# - Top outside chamfers represented with 1 mm chamfer operation.
# - Rear serration positions represented as 9 repeated edge grooves 4 mm deep.
#
# Known gaps:
# - 0.5 mm chamfers on individual hole and slot mouths are not separately selectable in this draft; only the general top chamfer is modeled.
# - Triangular serration tooth form is approximated with rectangular grooves because current fluent operations do not define triangular edge teeth.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated directly from frozen Stage 2 requirement text; not executed or visually reviewed yet.
# - Coordinate conversion uses SubCAD centered stock coordinates while requirement text uses lower-left-near datum coordinates.

from subcad import Stock

part = (
    Stock.rectangular(145, 115, 35, material="steel_a36")
    .drill(diameter=8, through=True, cx=-49.5, cy=-0.5, spot_drill=False)
    .drill(diameter=8, through=True, cx=49.5, cy=-0.5, spot_drill=False)
    .slot(length=48, width=14, through=True, cx=-0.5, cy=-0.5)
    .pocket(length=36, width=38, depth=6, cx=0, cy=0, corner_radius=0)
    .groove(length=7.25, width=4, depth=4, cx=-64.444, cy=55.5)
    .groove(length=7.25, width=4, depth=4, cx=-48.333, cy=55.5)
    .groove(length=7.25, width=4, depth=4, cx=-32.222, cy=55.5)
    .groove(length=7.25, width=4, depth=4, cx=-16.111, cy=55.5)
    .groove(length=7.25, width=4, depth=4, cx=0, cy=55.5)
    .groove(length=7.25, width=4, depth=4, cx=16.111, cy=55.5)
    .groove(length=7.25, width=4, depth=4, cx=32.222, cy=55.5)
    .groove(length=7.25, width=4, depth=4, cx=48.333, cy=55.5)
    .groove(length=7.25, width=4, depth=4, cx=64.444, cy=55.5)
)
