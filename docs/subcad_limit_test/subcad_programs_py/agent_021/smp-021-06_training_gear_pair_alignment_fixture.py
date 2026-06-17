# Requirement: SMP-021-06
# Source agent: 021
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_021_education_lab_apparatus_single_metal_parts.json
# Part: Training Gear Pair Alignment Fixture - single metal part
# Raw idea: Training Gear Pair Alignment Fixture
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 145 x 130 x 6 mm.
# - Two through mounting holes diameter 11 mm at X=26 and X=119, Y=65.
# - Central through obround slot 48 x 7 mm at X=72, Y=65.
# - Top relief pocket 36 x 43 x 1 mm centered between mounting holes.
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
    Stock.rectangular(145, 130, 6, material="steel_a36")
    .drill(diameter=11, through=True, cx=-46.5, cy=0, spot_drill=False)
    .drill(diameter=11, through=True, cx=46.5, cy=0, spot_drill=False)
    .slot(length=48, width=7, through=True, cx=-0.5, cy=0)
    .pocket(length=36, width=43, depth=1, cx=0, cy=0, corner_radius=0)
)
