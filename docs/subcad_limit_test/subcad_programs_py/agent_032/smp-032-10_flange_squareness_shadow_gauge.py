# Requirement: SMP-032-10
# Source agent: 032
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_032_fabrication_gauges_single_metal_parts.json
# Part: Flange Squareness Shadow Gauge - single metal part
# Raw idea: Flange Squareness Shadow Gauge
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 145 x 130 x 4 mm using material steel_1045.
# - Drill two through holes diameter 11 mm on the length centerline at X=26 mm and X=119 mm, Y=65 mm.
# - Machine a central obround slot 48 mm long x 10 mm wide through the part, centered at X=72 mm, Y=65 mm.
# - Mill a rectangular relief pocket 36 mm x 43 mm x 2 mm deep on the top face, centered between the mounting holes.
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
    Stock.rectangular(145, 130, 4, material="steel_1045")
    .drill(diameter=11, cx=-46.5, cy=0, depth=4, through=True)
    .drill(diameter=11, cx=46.5, cy=0, depth=4, through=True)
    .slot(length=48, width=10, depth=4, cx=-0.5, cy=0)
    .pocket(width=43, length=36, depth=2, cx=0, cy=0, corner_radius=0.5)
)
