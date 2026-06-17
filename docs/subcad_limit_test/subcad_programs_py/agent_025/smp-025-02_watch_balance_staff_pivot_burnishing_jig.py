# Requirement: SMP-025-02
# Source agent: 025
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_025_jewelry_watchmaking_fixtures_single_metal_parts.json
# Part: Watch Balance Staff Pivot Burnishing Jig - single metal part
# Raw idea: Watch Balance Staff Pivot Burnishing Jig
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 100 x 75 x 58 mm.
# - Two through mounting holes diameter 13 mm at X=15 and X=85, Y=37.
# - Central through obround slot 33 x 9 mm at X=50, Y=37.
# - Top relief pocket 25 x 25 x 7 mm centered between mounting holes.
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
    Stock.rectangular(100, 75, 58, material="steel_a36")
    .drill(diameter=13, through=True, cx=-35, cy=-0.5, spot_drill=False)
    .drill(diameter=13, through=True, cx=35, cy=-0.5, spot_drill=False)
    .slot(length=33, width=9, through=True, cx=0, cy=-0.5)
    .pocket(length=25, width=25, depth=7, cx=0, cy=0, corner_radius=0)
)
