# Requirement: SMP-031-05
# Source agent: 031
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_031_pumps_rotating_equipment_single_metal_parts.json
# Part: Bearing Heater Support Cradle - single metal part
# Raw idea: Bearing Heater Support Cradle
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 175 x 45 x 25 mm using material steel_a36.
# - Drill two through holes diameter 5 mm on the length centerline at X=10 mm and X=165 mm, Y=22 mm.
# - Machine a central obround slot 58 mm long x 17 mm wide through the part, centered at X=87 mm, Y=22 mm.
# - Mill a rectangular relief pocket 43 mm x 18 mm x 3 mm deep on the top face, centered between the mounting holes.
# - Applied a 1.0 mm top-edge chamfer operation.
# - Machine one top reference face at 44 degrees over the last 35 mm of length.
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
    Stock.rectangular(175, 45, 25, material="steel_a36")
    .drill(diameter=5, cx=-77.5, cy=-0.5, depth=25, through=True)
    .drill(diameter=5, cx=77.5, cy=-0.5, depth=25, through=True)
    .slot(length=58, width=17, depth=25, cx=-0.5, cy=-0.5)
    .pocket(width=18, length=43, depth=3, cx=0, cy=0, corner_radius=0.5)
    .slope_cut(width=45, length=35, start_depth=0, end_depth=20, cx=70, cy=0, slope_axis="X")
)
