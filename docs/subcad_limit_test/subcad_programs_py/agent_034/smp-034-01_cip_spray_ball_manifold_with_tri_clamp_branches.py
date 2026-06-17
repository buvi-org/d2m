# Requirement: SMP-034-01
# Source agent: 034
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_034_sanitary_food_processing_single_metal_parts.json
# Part: CIP Spray Ball Manifold With Tri-Clamp Branches - single metal part
# Raw idea: CIP Spray Ball Manifold With Tri-Clamp Branches
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 185 x 55 x 44 mm using material stainless_316.
# - Drill two through holes diameter 9 mm on the length centerline at X=11 mm and X=174 mm, Y=27 mm.
# - Machine a central obround slot 61 mm long x 15 mm wide through the part, centered at X=92 mm, Y=27 mm.
# - Mill a rectangular relief pocket 46 mm x 18 mm x 3 mm deep on the top face, centered between the mounting holes.
# - Applied a 1.0 mm top-edge chamfer operation.
# - Machine one top reference face at 37 degrees over the last 37 mm of length.
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
    Stock.rectangular(185, 55, 44, material="stainless_316")
    .drill(diameter=9, cx=-81.5, cy=-0.5, depth=44, through=True)
    .drill(diameter=9, cx=81.5, cy=-0.5, depth=44, through=True)
    .slot(length=61, width=15, depth=44, cx=-0.5, cy=-0.5)
    .pocket(width=18, length=46, depth=3, cx=0, cy=0, corner_radius=0.5)
    .slope_cut(width=55, length=37, start_depth=0, end_depth=27.881, cx=74, cy=0, slope_axis="X")
)
