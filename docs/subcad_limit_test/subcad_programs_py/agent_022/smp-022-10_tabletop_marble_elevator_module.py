# Requirement: SMP-022-10
# Source agent: 022
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_022_toys_hobby_mechanisms_single_metal_parts.json
# Part: Tabletop marble elevator module - single metal part
# Raw idea: Tabletop marble elevator module
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 75 x 70 x 58 mm.
# - Two through mounting holes diameter 11 mm at X=14 and X=61, Y=35.
# - Central through obround slot 30 x 17 mm at X=37, Y=35.
# - Top relief pocket 25 x 23 x 9 mm centered between mounting holes.
# - Top outside chamfers represented with 1 mm chamfer operation.
# - Rear serration positions represented as 12 repeated edge grooves 3 mm deep.
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
    Stock.rectangular(75, 70, 58, material="steel_a36")
    .drill(diameter=11, through=True, cx=-23.5, cy=0, spot_drill=False)
    .drill(diameter=11, through=True, cx=23.5, cy=0, spot_drill=False)
    .slot(length=30, width=17, through=True, cx=-0.5, cy=0)
    .pocket(length=25, width=23, depth=9, cx=0, cy=0, corner_radius=0)
    .groove(length=2.812, width=3, depth=3, cx=-34.375, cy=33.5)
    .groove(length=2.812, width=3, depth=3, cx=-28.125, cy=33.5)
    .groove(length=2.812, width=3, depth=3, cx=-21.875, cy=33.5)
    .groove(length=2.812, width=3, depth=3, cx=-15.625, cy=33.5)
    .groove(length=2.812, width=3, depth=3, cx=-9.375, cy=33.5)
    .groove(length=2.812, width=3, depth=3, cx=-3.125, cy=33.5)
    .groove(length=2.812, width=3, depth=3, cx=3.125, cy=33.5)
    .groove(length=2.812, width=3, depth=3, cx=9.375, cy=33.5)
    .groove(length=2.812, width=3, depth=3, cx=15.625, cy=33.5)
    .groove(length=2.812, width=3, depth=3, cx=21.875, cy=33.5)
    .groove(length=2.812, width=3, depth=3, cx=28.125, cy=33.5)
    .groove(length=2.812, width=3, depth=3, cx=34.375, cy=33.5)
)
