# Requirement: SMP-024-06
# Source agent: 024
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_024_rail_transit_service_tools_single_metal_parts.json
# Part: Rail Switch Point Gap Setting Wedge - single metal part
# Raw idea: Rail Switch Point Gap Setting Wedge
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 145 x 70 x 49 mm.
# - Two through mounting holes diameter 6 mm at X=14 and X=131, Y=35.
# - Central through obround slot 48 x 14 mm at X=72, Y=35.
# - Top relief pocket 36 x 23 x 17 mm centered between mounting holes.
# - Top outside chamfers represented with 1 mm chamfer operation.
# - Angled reference region over the last 29 mm represented as a sloped top-face cut at the right end.
#
# Known gaps:
# - 0.5 mm chamfers on individual hole and slot mouths are not separately selectable in this draft; only the general top chamfer is modeled.
# - Exact external face angle of 18 degrees is approximated by a sloped pocket depth transition, not a full side-face reprofile.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated directly from frozen Stage 2 requirement text; not executed or visually reviewed yet.
# - Coordinate conversion uses SubCAD centered stock coordinates while requirement text uses lower-left-near datum coordinates.

from subcad import Stock

part = (
    Stock.rectangular(145, 70, 49, material="steel_a36")
    .drill(diameter=6, through=True, cx=-58.5, cy=0, spot_drill=False)
    .drill(diameter=6, through=True, cx=58.5, cy=0, spot_drill=False)
    .slot(length=48, width=14, through=True, cx=-0.5, cy=0)
    .pocket(length=36, width=23, depth=17, cx=0, cy=0, corner_radius=0)
    .slope_cut(width=70, length=29, start_depth=0.5, end_depth=9.423, cx=58, cy=0, slope_axis="X")
)
