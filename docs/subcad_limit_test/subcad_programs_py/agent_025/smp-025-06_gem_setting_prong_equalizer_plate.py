# Requirement: SMP-025-06
# Source agent: 025
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_025_jewelry_watchmaking_fixtures_single_metal_parts.json
# Part: Gem Setting Prong Equalizer Plate - single metal part
# Raw idea: Gem Setting Prong Equalizer Plate
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 165 x 80 x 11 mm.
# - Two through mounting holes diameter 7 mm at X=16 and X=149, Y=40.
# - Central through obround slot 55 x 15 mm at X=82, Y=40.
# - Top relief pocket 41 x 26 x 3 mm centered between mounting holes.
# - Top outside chamfers represented with 1 mm chamfer operation.
# - Angled reference region over the last 33 mm represented as a sloped top-face cut at the right end.
#
# Known gaps:
# - 0.5 mm chamfers on individual hole and slot mouths are not separately selectable in this draft; only the general top chamfer is modeled.
# - Exact external face angle of 26 degrees is approximated by a sloped pocket depth transition, not a full side-face reprofile.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated directly from frozen Stage 2 requirement text; not executed or visually reviewed yet.
# - Coordinate conversion uses SubCAD centered stock coordinates while requirement text uses lower-left-near datum coordinates.

from subcad import Stock

part = (
    Stock.rectangular(165, 80, 11, material="steel_a36")
    .drill(diameter=7, through=True, cx=-66.5, cy=0, spot_drill=False)
    .drill(diameter=7, through=True, cx=66.5, cy=0, spot_drill=False)
    .slot(length=55, width=15, through=True, cx=-0.5, cy=0)
    .pocket(length=41, width=26, depth=3, cx=0, cy=0, corner_radius=0)
    .slope_cut(width=80, length=33, start_depth=0.5, end_depth=9.35, cx=66, cy=0, slope_axis="X")
)
