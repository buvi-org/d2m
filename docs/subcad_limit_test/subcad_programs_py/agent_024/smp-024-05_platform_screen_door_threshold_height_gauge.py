# Requirement: SMP-024-05
# Source agent: 024
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_024_rail_transit_service_tools_single_metal_parts.json
# Part: Platform Screen Door Threshold Height Gauge - single metal part
# Raw idea: Platform Screen Door Threshold Height Gauge
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 100 x 70 x 68 mm.
# - Two through mounting holes diameter 11 mm at X=14 and X=86, Y=35.
# - Central through obround slot 33 x 7 mm at X=50, Y=35.
# - Top relief pocket 25 x 23 x 15 mm centered between mounting holes.
# - Top outside chamfers represented with 1 mm chamfer operation.
# - Rear serration positions represented as 5 repeated edge grooves 5 mm deep.
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
    Stock.rectangular(100, 70, 68, material="steel_a36")
    .drill(diameter=11, through=True, cx=-36, cy=0, spot_drill=False)
    .drill(diameter=11, through=True, cx=36, cy=0, spot_drill=False)
    .slot(length=33, width=7, through=True, cx=0, cy=0)
    .pocket(length=25, width=23, depth=15, cx=0, cy=0, corner_radius=0)
    .groove(length=9, width=5, depth=5, cx=-40, cy=32.5)
    .groove(length=9, width=5, depth=5, cx=-20, cy=32.5)
    .groove(length=9, width=5, depth=5, cx=0, cy=32.5)
    .groove(length=9, width=5, depth=5, cx=20, cy=32.5)
    .groove(length=9, width=5, depth=5, cx=40, cy=32.5)
)
