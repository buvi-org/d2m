# Requirement: SMP-032-07
# Source agent: 032
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_032_fabrication_gauges_single_metal_parts.json
# Part: Weld Coupon Bend Fixture Locator - single metal part
# Raw idea: Weld Coupon Bend Fixture Locator
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 125 x 100 x 39 mm using material steel_1045.
# - Drill two through holes diameter 9 mm on the length centerline at X=20 mm and X=105 mm, Y=50 mm.
# - Machine a central obround slot 41 mm long x 17 mm wide through the part, centered at X=62 mm, Y=50 mm.
# - Mill a rectangular relief pocket 31 mm x 33 mm x 10 mm deep on the top face, centered between the mounting holes.
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
    Stock.rectangular(125, 100, 39, material="steel_1045")
    .drill(diameter=9, cx=-42.5, cy=0, depth=39, through=True)
    .drill(diameter=9, cx=42.5, cy=0, depth=39, through=True)
    .slot(length=41, width=17, depth=39, cx=-0.5, cy=0)
    .pocket(width=33, length=31, depth=10, cx=0, cy=0, corner_radius=0.5)
)
