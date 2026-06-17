# Requirement: SMP-025-01
# Source agent: 025
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_025_jewelry_watchmaking_fixtures_single_metal_parts.json
# Part: Ring Shank Ovalizing Mandrel Block - single metal part
# Raw idea: Ring Shank Ovalizing Mandrel Block
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 120 x 85 x 27 mm.
# - Two through mounting holes diameter 7 mm at X=17 and X=103, Y=42.
# - Central through obround slot 40 x 15 mm at X=60, Y=42.
# - Top relief pocket 30 x 28 x 10 mm centered between mounting holes.
# - Top outside chamfers represented with 1 mm chamfer operation.
# - Rear serration positions represented as 5 repeated edge grooves 4 mm deep.
#
# Known gaps:
# - 0.5 mm chamfers on individual hole and slot mouths are not separately selectable in this draft; only the general top chamfer is modeled.
# - Triangular serration tooth form is approximated with rectangular grooves because current fluent operations do not define triangular edge teeth.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated directly from frozen Stage 2 requirement text; not executed or visually reviewed yet.
# - Coordinate conversion uses SubCAD centered stock coordinates while requirement text uses lower-left-near datum coordinates.

from subcad import Stock

part = (
    Stock.rectangular(120, 85, 27, material="steel_a36")
    .drill(diameter=7, through=True, cx=-43, cy=-0.5, spot_drill=False)
    .drill(diameter=7, through=True, cx=43, cy=-0.5, spot_drill=False)
    .slot(length=40, width=15, through=True, cx=0, cy=-0.5)
    .pocket(length=30, width=28, depth=10, cx=0, cy=0, corner_radius=0)
    .groove(length=10.8, width=4, depth=3.24, cx=-48, cy=40.5)
    .groove(length=10.8, width=4, depth=3.24, cx=-24, cy=40.5)
    .groove(length=10.8, width=4, depth=3.24, cx=0, cy=40.5)
    .groove(length=10.8, width=4, depth=3.24, cx=24, cy=40.5)
    .groove(length=10.8, width=4, depth=3.24, cx=48, cy=40.5)
)
