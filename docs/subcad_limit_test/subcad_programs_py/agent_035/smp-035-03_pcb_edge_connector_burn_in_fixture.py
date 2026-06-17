# Requirement: SMP-035-03
# Source agent: 035
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_035_electronics_manufacturing_single_metal_parts.json
# Part: PCB Edge-Connector Burn-In Fixture - single metal part
# Raw idea: PCB Edge-Connector Burn-In Fixture
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 175 x 65 x 60 mm using material aluminum_6061.
# - Drill two through holes diameter 6 mm on the length centerline at X=13 mm and X=162 mm, Y=32 mm.
# - Machine a central obround slot 58 mm long x 12 mm wide through the part, centered at X=87 mm, Y=32 mm.
# - Mill a rectangular relief pocket 43 mm x 21 mm x 2 mm deep on the top face, centered between the mounting holes.
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
    Stock.rectangular(175, 65, 60, material="aluminum_6061")
    .drill(diameter=6, cx=-74.5, cy=-0.5, depth=60, through=True)
    .drill(diameter=6, cx=74.5, cy=-0.5, depth=60, through=True)
    .slot(length=58, width=12, depth=60, cx=-0.5, cy=-0.5)
    .pocket(width=21, length=43, depth=2, cx=0, cy=0, corner_radius=0.5)
)
