# Requirement: SMP-023-06
# Source agent: 023
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_023_warehouse_logistics_hardware_single_metal_parts.json
# Part: Pallet Fork Entry Guide Shoe - single metal part
# Raw idea: Pallet Fork Entry Guide Shoe
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 180 x 80 x 35 mm.
# - Two through mounting holes diameter 10 mm at X=16 and X=164, Y=40.
# - Central through obround slot 60 x 8 mm at X=90, Y=40.
# - Top relief pocket 45 x 26 x 15 mm centered between mounting holes.
# - Top outside chamfers represented with 1 mm chamfer operation.
# - Angled reference region over the last 36 mm represented as a sloped top-face cut at the right end.
#
# Known gaps:
# - 0.5 mm chamfers on individual hole and slot mouths are not separately selectable in this draft; only the general top chamfer is modeled.
# - Exact external face angle of 40 degrees is approximated by a sloped pocket depth transition, not a full side-face reprofile.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated directly from frozen Stage 2 requirement text; not executed or visually reviewed yet.
# - Coordinate conversion uses SubCAD centered stock coordinates while requirement text uses lower-left-near datum coordinates.

from subcad import Stock

part = (
    Stock.rectangular(180, 80, 35, material="steel_a36")
    .drill(diameter=10, through=True, cx=-74, cy=0, spot_drill=False)
    .drill(diameter=10, through=True, cx=74, cy=0, spot_drill=False)
    .slot(length=60, width=8, through=True, cx=0, cy=0)
    .pocket(length=45, width=26, depth=15, cx=0, cy=0, corner_radius=0)
    .slope_cut(width=80, length=36, start_depth=0.5, end_depth=29.75, cx=72, cy=0, slope_axis="X")
)
