# Requirement: SMP-024-07
# Source agent: 024
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_024_rail_transit_service_tools_single_metal_parts.json
# Part: Escalator Comb Plate Tooth Inspection Fixture - single metal part
# Raw idea: Escalator Comb Plate Tooth Inspection Fixture
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 180 x 85 x 10 mm.
# - Two through mounting holes diameter 8 mm at X=17 and X=163, Y=42.
# - Central through obround slot 60 x 15 mm at X=90, Y=42.
# - Top relief pocket 45 x 28 x 3 mm centered between mounting holes.
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
    Stock.rectangular(180, 85, 10, material="steel_a36")
    .drill(diameter=8, through=True, cx=-73, cy=-0.5, spot_drill=False)
    .drill(diameter=8, through=True, cx=73, cy=-0.5, spot_drill=False)
    .slot(length=60, width=15, through=True, cx=0, cy=-0.5)
    .pocket(length=45, width=28, depth=3, cx=0, cy=0, corner_radius=0)
)
