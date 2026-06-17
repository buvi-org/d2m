# Requirement: SMP-033-02
# Source agent: 033
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_033_woodworking_machines_single_metal_parts.json
# Part: Tilting table saw blade guard and riving knife bracket - single metal part
# Raw idea: Tilting table saw blade guard and riving knife bracket
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 140 x 105 x 6 mm using material steel_a36.
# - Drill two through holes diameter 8 mm on the length centerline at X=21 mm and X=119 mm, Y=52 mm.
# - Machine a central obround slot 46 mm long x 8 mm wide through the part, centered at X=70 mm, Y=52 mm.
# - Mill a rectangular relief pocket 35 mm x 35 mm x 1 mm deep on the top face, centered between the mounting holes.
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
    Stock.rectangular(140, 105, 6, material="steel_a36")
    .drill(diameter=8, cx=-49, cy=-0.5, depth=6, through=True)
    .drill(diameter=8, cx=49, cy=-0.5, depth=6, through=True)
    .slot(length=46, width=8, depth=6, cx=0, cy=-0.5)
    .pocket(width=35, length=35, depth=1, cx=0, cy=0, corner_radius=0.5)
)
