# Requirement: SMP-034-03
# Source agent: 034
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_034_sanitary_food_processing_single_metal_parts.json
# Part: Sanitary Butterfly Valve With Pneumatic Actuator - single metal part
# Raw idea: Sanitary Butterfly Valve With Pneumatic Actuator
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 140 x 110 x 54 mm using material stainless_316.
# - Drill two through holes diameter 9 mm on the length centerline at X=22 mm and X=118 mm, Y=55 mm.
# - Machine a central obround slot 46 mm long x 17 mm wide through the part, centered at X=70 mm, Y=55 mm.
# - Mill a rectangular relief pocket 35 mm x 36 mm x 27 mm deep on the top face, centered between the mounting holes.
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
    Stock.rectangular(140, 110, 54, material="stainless_316")
    .drill(diameter=9, cx=-48, cy=0, depth=54, through=True)
    .drill(diameter=9, cx=48, cy=0, depth=54, through=True)
    .slot(length=46, width=17, depth=54, cx=0, cy=0)
    .pocket(width=36, length=35, depth=27, cx=0, cy=0, corner_radius=0.5)
)
