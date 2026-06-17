# Requirement: SMP-025-07
# Source agent: 025
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_025_jewelry_watchmaking_fixtures_single_metal_parts.json
# Part: Pocket Watch Case Hinge Alignment Jig - single metal part
# Raw idea: Pocket Watch Case Hinge Alignment Jig
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 155 x 80 x 30 mm.
# - Two through mounting holes diameter 7 mm at X=16 and X=139, Y=40.
# - Central through obround slot 51 x 17 mm at X=77, Y=40.
# - Top relief pocket 38 x 26 x 15 mm centered between mounting holes.
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
    Stock.rectangular(155, 80, 30, material="steel_a36")
    .drill(diameter=7, through=True, cx=-61.5, cy=0, spot_drill=False)
    .drill(diameter=7, through=True, cx=61.5, cy=0, spot_drill=False)
    .slot(length=51, width=17, through=True, cx=-0.5, cy=0)
    .pocket(length=38, width=26, depth=15, cx=0, cy=0, corner_radius=0)
)
