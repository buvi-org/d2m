# Requirement: SMP-036-05
# Source agent: 036
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_036_sports_safety_gear_single_metal_parts.json
# Part: Ventilated shin guard impact insert carrier - single metal part
# Raw idea: Ventilated shin guard impact insert carrier
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 255 x 145 x 5 mm using material steel_a36.
# - Drill two through holes diameter 9 mm on the length centerline at X=29 mm and X=226 mm, Y=72 mm.
# - Machine a central obround slot 85 mm long x 18 mm wide through the part, centered at X=127 mm, Y=72 mm.
# - Mill a rectangular relief pocket 63 mm x 48 mm x 2 mm deep on the top face, centered between the mounting holes.
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
    Stock.rectangular(255, 145, 5, material="steel_a36")
    .drill(diameter=9, cx=-98.5, cy=-0.5, depth=5, through=True)
    .drill(diameter=9, cx=98.5, cy=-0.5, depth=5, through=True)
    .slot(length=85, width=18, depth=5, cx=-0.5, cy=-0.5)
    .pocket(width=48, length=63, depth=2, cx=0, cy=0, corner_radius=0.5)
)
