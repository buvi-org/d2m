# Requirement: SMP-034-10
# Source agent: 034
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_034_sanitary_food_processing_single_metal_parts.json
# Part: Brewery Dry-Hop Dosing Hopper With Sight Window - single metal part
# Raw idea: Brewery Dry-Hop Dosing Hopper With Sight Window
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 130 x 95 x 30 mm using material steel_a36.
# - Drill two through holes diameter 12 mm on the length centerline at X=19 mm and X=111 mm, Y=47 mm.
# - Machine a central obround slot 43 mm long x 18 mm wide through the part, centered at X=65 mm, Y=47 mm.
# - Mill a rectangular relief pocket 32 mm x 31 mm x 5 mm deep on the top face, centered between the mounting holes.
# - Applied a 1.0 mm top-edge chamfer operation.
# - Machine one top reference face at 34 degrees over the last 26 mm of length.
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
    Stock.rectangular(130, 95, 30, material="steel_a36")
    .drill(diameter=12, cx=-46, cy=-0.5, depth=30, through=True)
    .drill(diameter=12, cx=46, cy=-0.5, depth=30, through=True)
    .slot(length=43, width=18, depth=30, cx=0, cy=-0.5)
    .pocket(width=31, length=32, depth=5, cx=0, cy=0, corner_radius=0.5)
    .slope_cut(width=95, length=26, start_depth=0, end_depth=17.537, cx=52, cy=0, slope_axis="X")
)
