# Requirement: SMP-028-09
# Source agent: 028
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_028_small_engine_service_hardware_single_metal_parts.json
# Part: Generator Wheel Kit Axle Spacer Block - single metal part
# Raw idea: Generator Wheel Kit Axle Spacer Block
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 215 x 50 x 66 mm using material steel_a36.
# - Drill two through holes diameter 11 mm on the length centerline at X=10 mm and X=205 mm, Y=25 mm.
# - Machine a central obround slot 71 mm long x 18 mm wide through the part, centered at X=107 mm, Y=25 mm.
# - Mill a rectangular relief pocket 53 mm x 18 mm x 16 mm deep on the top face, centered between the mounting holes.
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
    Stock.rectangular(215, 50, 66, material="steel_a36")
    .drill(diameter=11, cx=-97.5, cy=0, depth=66, through=True)
    .drill(diameter=11, cx=97.5, cy=0, depth=66, through=True)
    .slot(length=71, width=18, depth=66, cx=-0.5, cy=0)
    .pocket(width=18, length=53, depth=16, cx=0, cy=0, corner_radius=0.5)
)
