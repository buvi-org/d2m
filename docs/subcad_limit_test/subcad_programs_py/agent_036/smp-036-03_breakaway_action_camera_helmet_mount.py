# Requirement: SMP-036-03
# Source agent: 036
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_036_sports_safety_gear_single_metal_parts.json
# Part: Breakaway action camera helmet mount - single metal part
# Raw idea: Breakaway action camera helmet mount
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 140 x 90 x 42 mm using material aluminum_6061.
# - Drill two through holes diameter 8 mm on the length centerline at X=18 mm and X=122 mm, Y=45 mm.
# - Machine a central obround slot 46 mm long x 7 mm wide through the part, centered at X=70 mm, Y=45 mm.
# - Mill a rectangular relief pocket 35 mm x 30 mm x 11 mm deep on the top face, centered between the mounting holes.
# - Applied a 1.0 mm top-edge chamfer operation.
# - Machine a straight dovetail groove on the top face, length 116 mm, throat 18 mm, included angle 60 degrees.
#
# Known gaps:
# - 0.5 mm chamfers specifically on individual hole and slot mouths are not separately modeled; only the global/top chamfer is included.
# - Dovetail slide depth is inferred because the frozen requirement gives length, throat, and angle but not a groove depth.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - SubCAD stock is centered at the origin; requirement datum coordinates were converted from lower-left-near X/Y values to centered cx/cy values.

from subcad import Stock

part = (
    Stock.rectangular(140, 90, 42, material="aluminum_6061")
    .drill(diameter=8, cx=-52, cy=0, depth=42, through=True)
    .drill(diameter=8, cx=52, cy=0, depth=42, through=True)
    .slot(length=46, width=7, depth=42, cx=0, cy=0)
    .pocket(width=30, length=35, depth=11, cx=0, cy=0, corner_radius=0.5)
    .dovetail(length=116, width=18, depth=6, angle=60, cx=0, cy=0)
)
