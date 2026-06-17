# Requirement: SMP-034-02
# Source agent: 034
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_034_sanitary_food_processing_single_metal_parts.json
# Part: Bakery Dough Chunker Infeed Guard Assembly - single metal part
# Raw idea: Bakery Dough Chunker Infeed Guard Assembly
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 130 x 50 x 6 mm using material steel_a36.
# - Drill two through holes diameter 7 mm on the length centerline at X=10 mm and X=120 mm, Y=25 mm.
# - Machine a central obround slot 43 mm long x 10 mm wide through the part, centered at X=65 mm, Y=25 mm.
# - Mill a rectangular relief pocket 32 mm x 18 mm x 1 mm deep on the top face, centered between the mounting holes.
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
    Stock.rectangular(130, 50, 6, material="steel_a36")
    .drill(diameter=7, cx=-55, cy=0, depth=6, through=True)
    .drill(diameter=7, cx=55, cy=0, depth=6, through=True)
    .slot(length=43, width=10, depth=6, cx=0, cy=0)
    .pocket(width=18, length=32, depth=1, cx=0, cy=0, corner_radius=0.5)
)
