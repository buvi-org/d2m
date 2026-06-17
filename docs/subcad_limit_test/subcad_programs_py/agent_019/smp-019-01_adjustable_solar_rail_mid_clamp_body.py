# Requirement: SMP-019-01
# Source agent: 019
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_019_renewable_energy_hardware_single_metal_parts.json
# Part: Adjustable Solar Rail Mid-Clamp Body - single metal part
# Raw idea: Adjustable Solar Rail Mid-Clamp Body
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 80 x 80 x 47 mm.
# - Two through mounting holes diameter 13 mm at X=16 and X=64, Y=40.
# - Central through obround slot 30 x 10 mm at X=40, Y=40.
# - Top relief pocket 25 x 26 x 10 mm centered between mounting holes.
# - Top outside chamfers represented with 1 mm chamfer operation.
# - Rear serration positions represented as 8 repeated edge grooves 4 mm deep.
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
    Stock.rectangular(80, 80, 47, material="steel_1045")
    .drill(diameter=13, through=True, cx=-24, cy=0, spot_drill=False)
    .drill(diameter=13, through=True, cx=24, cy=0, spot_drill=False)
    .slot(length=30, width=10, through=True, cx=0, cy=0)
    .pocket(length=25, width=26, depth=10, cx=0, cy=0, corner_radius=0)
    .groove(length=4.5, width=4, depth=4, cx=-35, cy=38)
    .groove(length=4.5, width=4, depth=4, cx=-25, cy=38)
    .groove(length=4.5, width=4, depth=4, cx=-15, cy=38)
    .groove(length=4.5, width=4, depth=4, cx=-5, cy=38)
    .groove(length=4.5, width=4, depth=4, cx=5, cy=38)
    .groove(length=4.5, width=4, depth=4, cx=15, cy=38)
    .groove(length=4.5, width=4, depth=4, cx=25, cy=38)
    .groove(length=4.5, width=4, depth=4, cx=35, cy=38)
)
