# Requirement: SMP-024-04
# Source agent: 024
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_024_rail_transit_service_tools_single_metal_parts.json
# Part: Elevator Guide Rail Fishplate Drilling Template - single metal part
# Raw idea: Elevator Guide Rail Fishplate Drilling Template
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 180 x 145 x 11 mm.
# - Two through mounting holes diameter 12 mm at X=29 and X=151, Y=72.
# - Central through obround slot 60 x 18 mm at X=90, Y=72.
# - Top relief pocket 45 x 48 x 2 mm centered between mounting holes.
# - Top outside chamfers represented with 1 mm chamfer operation.
# - Central counterbored seat diameter 26 mm x 3 mm deep around the center feature.
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
    Stock.rectangular(180, 145, 11, material="steel_a36")
    .drill(diameter=12, through=True, cx=-61, cy=-0.5, spot_drill=False)
    .drill(diameter=12, through=True, cx=61, cy=-0.5, spot_drill=False)
    .slot(length=60, width=18, through=True, cx=0, cy=-0.5)
    .pocket(length=45, width=48, depth=2, cx=0, cy=0, corner_radius=0)
    .circular_pocket(diameter=26, depth=3, cx=0, cy=-0.5)
)
