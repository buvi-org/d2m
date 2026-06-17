# Requirement: SMP-034-05
# Source agent: 034
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_034_sanitary_food_processing_single_metal_parts.json
# Part: Brewery Whirlpool Tangential Inlet Nozzle - single metal part
# Raw idea: Brewery Whirlpool Tangential Inlet Nozzle
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 185 x 75 x 36 mm using material steel_a36.
# - Drill two through holes diameter 11 mm on the length centerline at X=15 mm and X=170 mm, Y=37 mm.
# - Machine a central obround slot 61 mm long x 12 mm wide through the part, centered at X=92 mm, Y=37 mm.
# - Mill a rectangular relief pocket 46 mm x 25 mm x 9 mm deep on the top face, centered between the mounting holes.
# - Applied a 1.0 mm top-edge chamfer operation.
# - Machine one top reference face at 43 degrees over the last 37 mm of length.
#
# Known gaps:
# - 0.5 mm chamfers specifically on individual hole and slot mouths are not separately modeled; only the global/top chamfer is included.
# - Angled reference face is approximated as a sloped top cut over the final length; exact edge transitions may need review.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - SubCAD stock is centered at the origin; requirement datum coordinates were converted from lower-left-near X/Y values to centered cx/cy values.

from subcad import Stock

part = (
    Stock.rectangular(185, 75, 36, material="steel_a36")
    .drill(diameter=11, cx=-77.5, cy=-0.5, depth=36, through=True)
    .drill(diameter=11, cx=77.5, cy=-0.5, depth=36, through=True)
    .slot(length=61, width=12, depth=36, cx=-0.5, cy=-0.5)
    .pocket(width=25, length=46, depth=9, cx=0, cy=0, corner_radius=0.5)
    .slope_cut(width=75, length=37, start_depth=0, end_depth=28.8, cx=74, cy=0, slope_axis="X")
)
