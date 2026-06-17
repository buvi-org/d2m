# Requirement: SMP-034-07
# Source agent: 034
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_034_sanitary_food_processing_single_metal_parts.json
# Part: Sanitary Conveyor Drip Tray With Lift-Out Screen - single metal part
# Raw idea: Sanitary Conveyor Drip Tray With Lift-Out Screen
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 160 x 60 x 11 mm using material stainless_316.
# - Drill two through holes diameter 12 mm on the length centerline at X=12 mm and X=148 mm, Y=30 mm.
# - Machine a central obround slot 53 mm long x 12 mm wide through the part, centered at X=80 mm, Y=30 mm.
# - Mill a rectangular relief pocket 40 mm x 20 mm x 1 mm deep on the top face, centered between the mounting holes.
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
    Stock.rectangular(160, 60, 11, material="stainless_316")
    .drill(diameter=12, cx=-68, cy=0, depth=11, through=True)
    .drill(diameter=12, cx=68, cy=0, depth=11, through=True)
    .slot(length=53, width=12, depth=11, cx=0, cy=0)
    .pocket(width=20, length=40, depth=1, cx=0, cy=0, corner_radius=0.5)
)
