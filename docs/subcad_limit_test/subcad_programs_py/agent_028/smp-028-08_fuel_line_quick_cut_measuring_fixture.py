# Requirement: SMP-028-08
# Source agent: 028
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_028_small_engine_service_hardware_single_metal_parts.json
# Part: Fuel Line Quick-Cut Measuring Fixture - single metal part
# Raw idea: Fuel Line Quick-Cut Measuring Fixture
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 115 x 70 x 24 mm using material steel_a36.
# - Drill two through holes diameter 13 mm on the length centerline at X=14 mm and X=101 mm, Y=35 mm.
# - Machine a central obround slot 38 mm long x 12 mm wide through the part, centered at X=57 mm, Y=35 mm.
# - Mill a rectangular relief pocket 28 mm x 23 mm x 9 mm deep on the top face, centered between the mounting holes.
# - Applied a 1.0 mm top-edge chamfer operation.
#
# Known gaps:
# - 0.5 mm chamfers specifically on individual hole and slot mouths are not separately modeled; only the global/top chamfer is included.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - SubCAD stock is centered at the origin; requirement datum coordinates were converted from lower-left-near X/Y values to centered cx/cy values.

from subcad import Stock

part = (
    Stock.rectangular(115, 70, 24, material="steel_a36")
    .drill(diameter=13, cx=-43.5, cy=0, depth=24, through=True)
    .drill(diameter=13, cx=43.5, cy=0, depth=24, through=True)
    .slot(length=38, width=12, depth=24, cx=-0.5, cy=0)
    .pocket(width=23, length=28, depth=9, cx=0, cy=0, corner_radius=0.5)
)
