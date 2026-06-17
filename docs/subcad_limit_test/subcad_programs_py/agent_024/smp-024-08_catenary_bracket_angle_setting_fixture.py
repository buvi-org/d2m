# Requirement: SMP-024-08
# Source agent: 024
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_024_rail_transit_service_tools_single_metal_parts.json
# Part: Catenary Bracket Angle Setting Fixture - single metal part
# Raw idea: Catenary Bracket Angle Setting Fixture
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 220 x 60 x 11 mm.
# - Two through mounting holes diameter 9 mm at X=12 and X=208, Y=30.
# - Central through obround slot 73 x 13 mm at X=110, Y=30.
# - Top relief pocket 55 x 20 x 5 mm centered between mounting holes.
# - Top outside chamfers represented with 1 mm chamfer operation.
# - Angled reference region over the last 44 mm represented as a sloped top-face cut at the right end.
#
# Known gaps:
# - 0.5 mm chamfers on individual hole and slot mouths are not separately selectable in this draft; only the general top chamfer is modeled.
# - Exact external face angle of 11 degrees is approximated by a sloped pocket depth transition, not a full side-face reprofile.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated directly from frozen Stage 2 requirement text; not executed or visually reviewed yet.
# - Coordinate conversion uses SubCAD centered stock coordinates while requirement text uses lower-left-near datum coordinates.

from subcad import Stock

part = (
    Stock.rectangular(220, 60, 11, material="steel_a36")
    .drill(diameter=9, through=True, cx=-98, cy=0, spot_drill=False)
    .drill(diameter=9, through=True, cx=98, cy=0, spot_drill=False)
    .slot(length=73, width=13, through=True, cx=0, cy=0)
    .pocket(length=55, width=20, depth=5, cx=0, cy=0, corner_radius=0)
    .slope_cut(width=60, length=44, start_depth=0.5, end_depth=8.553, cx=88, cy=0, slope_axis="X")
)
