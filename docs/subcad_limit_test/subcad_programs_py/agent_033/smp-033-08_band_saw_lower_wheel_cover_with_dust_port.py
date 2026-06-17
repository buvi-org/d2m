# Requirement: SMP-033-08
# Source agent: 033
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_033_woodworking_machines_single_metal_parts.json
# Part: Band saw lower wheel cover with dust port - single metal part
# Raw idea: Band saw lower wheel cover with dust port
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 145 x 105 x 5 mm using material steel_a36.
# - Drill two through holes diameter 12 mm on the length centerline at X=21 mm and X=124 mm, Y=52 mm.
# - Machine a central obround slot 48 mm long x 7 mm wide through the part, centered at X=72 mm, Y=52 mm.
# - Mill a rectangular relief pocket 36 mm x 35 mm x 1 mm deep on the top face, centered between the mounting holes.
# - Applied a 1.0 mm top-edge chamfer operation.
# - Machine one top reference face at 40 degrees over the last 29 mm of length.
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
    Stock.rectangular(145, 105, 5, material="steel_a36")
    .drill(diameter=12, cx=-51.5, cy=-0.5, depth=5, through=True)
    .drill(diameter=12, cx=51.5, cy=-0.5, depth=5, through=True)
    .slot(length=48, width=7, depth=5, cx=-0.5, cy=-0.5)
    .pocket(width=35, length=36, depth=1, cx=0, cy=0, corner_radius=0.5)
    .slope_cut(width=105, length=29, start_depth=0, end_depth=4, cx=58, cy=0, slope_axis="X")
)
