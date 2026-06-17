# Requirement: SMP-021-02
# Source agent: 021
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_021_education_lab_apparatus_single_metal_parts.json
# Part: Projectile Launcher Elevation Quadrant - single metal part
# Raw idea: Projectile Launcher Elevation Quadrant
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 190 x 70 x 9 mm.
# - Two through mounting holes diameter 9 mm at X=14 and X=176, Y=35.
# - Central through obround slot 63 x 13 mm at X=95, Y=35.
# - Top relief pocket 47 x 23 x 2 mm centered between mounting holes.
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
    Stock.rectangular(190, 70, 9, material="stainless_316")
    .drill(diameter=9, through=True, cx=-81, cy=0, spot_drill=False)
    .drill(diameter=9, through=True, cx=81, cy=0, spot_drill=False)
    .slot(length=63, width=13, through=True, cx=0, cy=0)
    .pocket(length=47, width=23, depth=2, cx=0, cy=0, corner_radius=0)
)
