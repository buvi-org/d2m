# Requirement: SMP-030-01
# Source agent: 030
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_030_appliance_repair_hardware_single_metal_parts.json
# Part: Washing Machine Drum Spider Arm Replacement Hub - single metal part
# Raw idea: Washing Machine Drum Spider Arm Replacement Hub
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 215 x 55 x 58 mm using material steel_a36.
# - Drill two through holes diameter 8 mm on the length centerline at X=11 mm and X=204 mm, Y=27 mm.
# - Machine a central obround slot 71 mm long x 13 mm wide through the part, centered at X=107 mm, Y=27 mm.
# - Mill a rectangular relief pocket 53 mm x 18 mm x 6 mm deep on the top face, centered between the mounting holes.
# - Applied a 1.0 mm top-edge chamfer operation.
# - Machine one top reference face at 24 degrees over the last 43 mm of length.
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
    Stock.rectangular(215, 55, 58, material="steel_a36")
    .drill(diameter=8, cx=-96.5, cy=-0.5, depth=58, through=True)
    .drill(diameter=8, cx=96.5, cy=-0.5, depth=58, through=True)
    .slot(length=71, width=13, depth=58, cx=-0.5, cy=-0.5)
    .pocket(width=18, length=53, depth=6, cx=0, cy=0, corner_radius=0.5)
    .slope_cut(width=55, length=43, start_depth=0, end_depth=19.145, cx=86, cy=0, slope_axis="X")
)
