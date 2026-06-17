# Requirement: SMP-021-09
# Source agent: 021
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_021_education_lab_apparatus_single_metal_parts.json
# Part: Magnetic Field Coil Stand Bracket - single metal part
# Raw idea: Magnetic Field Coil Stand Bracket
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 245 x 115 x 8 mm.
# - Two through mounting holes diameter 12 mm at X=23 and X=222, Y=57.
# - Central through obround slot 81 x 12 mm at X=122, Y=57.
# - Top relief pocket 61 x 38 x 4 mm centered between mounting holes.
# - Top outside chamfers represented with 1 mm chamfer operation.
#
# Known gaps:
# - 0.5 mm chamfers on individual hole and slot mouths are not separately selectable in this draft; only the general top chamfer is modeled.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated directly from frozen Stage 2 requirement text; not executed or visually reviewed yet.
# - Coordinate conversion uses SubCAD centered stock coordinates while requirement text uses lower-left-near datum coordinates.

from subcad import Stock

part = (
    Stock.rectangular(245, 115, 8, material="stainless_316")
    .drill(diameter=12, through=True, cx=-99.5, cy=-0.5, spot_drill=False)
    .drill(diameter=12, through=True, cx=99.5, cy=-0.5, spot_drill=False)
    .slot(length=81, width=12, through=True, cx=-0.5, cy=-0.5)
    .pocket(length=61, width=38, depth=4, cx=0, cy=0, corner_radius=0)
)
