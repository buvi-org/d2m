# Requirement: SMP-025-03
# Source agent: 025
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_025_jewelry_watchmaking_fixtures_single_metal_parts.json
# Part: Clock Gear Depthing Gauge Frame - single metal part
# Raw idea: Clock Gear Depthing Gauge Frame
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 80 x 40 x 65 mm.
# - Two through mounting holes diameter 9 mm at X=10 and X=70, Y=20.
# - Central through obround slot 30 x 7 mm at X=40, Y=20.
# - Top relief pocket 25 x 18 x 8 mm centered between mounting holes.
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
    Stock.rectangular(80, 40, 65, material="steel_a36")
    .drill(diameter=9, through=True, cx=-30, cy=0, spot_drill=False)
    .drill(diameter=9, through=True, cx=30, cy=0, spot_drill=False)
    .slot(length=30, width=7, through=True, cx=0, cy=0)
    .pocket(length=25, width=18, depth=8, cx=0, cy=0, corner_radius=0)
)
