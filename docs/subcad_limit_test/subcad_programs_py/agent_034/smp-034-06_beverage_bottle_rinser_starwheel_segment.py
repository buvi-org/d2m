# Requirement: SMP-034-06
# Source agent: 034
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_034_sanitary_food_processing_single_metal_parts.json
# Part: Beverage Bottle Rinser Starwheel Segment - single metal part
# Raw idea: Beverage Bottle Rinser Starwheel Segment
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 165 x 100 x 11 mm using material steel_a36.
# - Drill two through holes diameter 10 mm on the length centerline at X=20 mm and X=145 mm, Y=50 mm.
# - Machine a central obround slot 55 mm long x 14 mm wide through the part, centered at X=82 mm, Y=50 mm.
# - Mill a rectangular relief pocket 41 mm x 33 mm x 1 mm deep on the top face, centered between the mounting holes.
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
    Stock.rectangular(165, 100, 11, material="steel_a36")
    .drill(diameter=10, cx=-62.5, cy=0, depth=11, through=True)
    .drill(diameter=10, cx=62.5, cy=0, depth=11, through=True)
    .slot(length=55, width=14, depth=11, cx=-0.5, cy=0)
    .pocket(width=33, length=41, depth=1, cx=0, cy=0, corner_radius=0.5)
)
