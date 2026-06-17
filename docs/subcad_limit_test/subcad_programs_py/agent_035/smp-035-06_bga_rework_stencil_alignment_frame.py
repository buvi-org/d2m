# Requirement: SMP-035-06
# Source agent: 035
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_035_electronics_manufacturing_single_metal_parts.json
# Part: BGA Rework Stencil Alignment Frame - single metal part
# Raw idea: BGA Rework Stencil Alignment Frame
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 145 x 65 x 43 mm using material aluminum_6061.
# - Drill two through holes diameter 13 mm on the length centerline at X=13 mm and X=132 mm, Y=32 mm.
# - Machine a central obround slot 48 mm long x 13 mm wide through the part, centered at X=72 mm, Y=32 mm.
# - Mill a rectangular relief pocket 36 mm x 21 mm x 5 mm deep on the top face, centered between the mounting holes.
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
    Stock.rectangular(145, 65, 43, material="aluminum_6061")
    .drill(diameter=13, cx=-59.5, cy=-0.5, depth=43, through=True)
    .drill(diameter=13, cx=59.5, cy=-0.5, depth=43, through=True)
    .slot(length=48, width=13, depth=43, cx=-0.5, cy=-0.5)
    .pocket(width=21, length=36, depth=5, cx=0, cy=0, corner_radius=0.5)
)
