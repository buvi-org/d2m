# Requirement: SMP-024-10
# Source agent: 024
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_024_rail_transit_service_tools_single_metal_parts.json
# Part: Elevator Brake Pad Centering Fixture - single metal part
# Raw idea: Elevator Brake Pad Centering Fixture
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 165 x 110 x 55 mm.
# - Two through mounting holes diameter 13 mm at X=22 and X=143, Y=55.
# - Central through obround slot 55 x 18 mm at X=82, Y=55.
# - Top relief pocket 41 x 36 x 7 mm centered between mounting holes.
# - Top outside chamfers represented with 1 mm chamfer operation.
#
# Known gaps:
# - 0.5 mm chamfers on individual hole and slot mouths are not separately selectable in this draft; only the general top chamfer is modeled.
# - Side tapped hole M9 with axis parallel to Y is not modeled; current threaded_hole/tap operations are top-face axial in this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated directly from frozen Stage 2 requirement text; not executed or visually reviewed yet.
# - Coordinate conversion uses SubCAD centered stock coordinates while requirement text uses lower-left-near datum coordinates.

from subcad import Stock

part = (
    Stock.rectangular(165, 110, 55, material="steel_a36")
    .drill(diameter=13, through=True, cx=-60.5, cy=0, spot_drill=False)
    .drill(diameter=13, through=True, cx=60.5, cy=0, spot_drill=False)
    .slot(length=55, width=18, through=True, cx=-0.5, cy=0)
    .pocket(length=41, width=36, depth=7, cx=0, cy=0, corner_radius=0)
)
