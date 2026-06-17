# Requirement: SMP-036-10
# Source agent: 036
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_036_sports_safety_gear_single_metal_parts.json
# Part: Pull-tab release buckle guard - single metal part
# Raw idea: Pull-tab release buckle guard
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 175 x 120 x 3 mm using material stainless_316.
# - Drill two through holes diameter 11 mm on the length centerline at X=24 mm and X=151 mm, Y=60 mm.
# - Machine a central obround slot 58 mm long x 13 mm wide through the part, centered at X=87 mm, Y=60 mm.
# - Mill a rectangular relief pocket 43 mm x 40 mm x 2 mm deep on the top face, centered between the mounting holes.
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
    Stock.rectangular(175, 120, 3, material="stainless_316")
    .drill(diameter=11, cx=-63.5, cy=0, depth=3, through=True)
    .drill(diameter=11, cx=63.5, cy=0, depth=3, through=True)
    .slot(length=58, width=13, depth=3, cx=-0.5, cy=0)
    .pocket(width=40, length=43, depth=2, cx=0, cy=0, corner_radius=0.5)
)
