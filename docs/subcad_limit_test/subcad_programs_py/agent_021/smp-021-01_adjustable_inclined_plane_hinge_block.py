# Requirement: SMP-021-01
# Source agent: 021
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_021_education_lab_apparatus_single_metal_parts.json
# Part: Adjustable Inclined Plane Hinge Block - single metal part
# Raw idea: Adjustable Inclined Plane Hinge Block
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 165 x 100 x 9 mm.
# - Two through mounting holes diameter 6 mm at X=20 and X=145, Y=50.
# - Central through obround slot 55 x 15 mm at X=82, Y=50.
# - Top relief pocket 41 x 33 x 2 mm centered between mounting holes.
# - Top outside chamfers represented with 1 mm chamfer operation.
# - Angled reference region over the last 33 mm represented as a sloped top-face cut at the right end.
#
# Known gaps:
# - 0.5 mm chamfers on individual hole and slot mouths are not separately selectable in this draft; only the general top chamfer is modeled.
# - Exact external face angle of 15 degrees is approximated by a sloped pocket depth transition, not a full side-face reprofile.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated directly from frozen Stage 2 requirement text; not executed or visually reviewed yet.
# - Coordinate conversion uses SubCAD centered stock coordinates while requirement text uses lower-left-near datum coordinates.

from subcad import Stock

part = (
    Stock.rectangular(165, 100, 9, material="steel_a36")
    .drill(diameter=6, through=True, cx=-62.5, cy=0, spot_drill=False)
    .drill(diameter=6, through=True, cx=62.5, cy=0, spot_drill=False)
    .slot(length=55, width=15, through=True, cx=-0.5, cy=0)
    .pocket(length=41, width=33, depth=2, cx=0, cy=0, corner_radius=0)
    .slope_cut(width=100, length=33, start_depth=0.5, end_depth=7.65, cx=66, cy=0, slope_axis="X")
)
