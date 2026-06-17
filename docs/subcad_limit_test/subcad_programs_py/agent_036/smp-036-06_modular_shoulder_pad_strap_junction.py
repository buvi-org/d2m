# Requirement: SMP-036-06
# Source agent: 036
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_036_sports_safety_gear_single_metal_parts.json
# Part: Modular shoulder pad strap junction - single metal part
# Raw idea: Modular shoulder pad strap junction
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 220 x 50 x 10 mm using material steel_a36.
# - Drill two through holes diameter 6 mm on the length centerline at X=10 mm and X=210 mm, Y=25 mm.
# - Machine a central obround slot 73 mm long x 12 mm wide through the part, centered at X=110 mm, Y=25 mm.
# - Mill a rectangular relief pocket 55 mm x 18 mm x 4 mm deep on the top face, centered between the mounting holes.
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
    Stock.rectangular(220, 50, 10, material="steel_a36")
    .drill(diameter=6, cx=-100, cy=0, depth=10, through=True)
    .drill(diameter=6, cx=100, cy=0, depth=10, through=True)
    .slot(length=73, width=12, depth=10, cx=0, cy=0)
    .pocket(width=18, length=55, depth=4, cx=0, cy=0, corner_radius=0.5)
)
