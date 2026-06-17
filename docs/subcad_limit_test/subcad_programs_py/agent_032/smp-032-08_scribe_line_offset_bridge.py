# Requirement: SMP-032-08
# Source agent: 032
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_032_fabrication_gauges_single_metal_parts.json
# Part: Scribe Line Offset Bridge - single metal part
# Raw idea: Scribe Line Offset Bridge
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 140 x 55 x 52 mm using material steel_1045.
# - Drill two through holes diameter 6 mm on the length centerline at X=11 mm and X=129 mm, Y=27 mm.
# - Machine a central obround slot 46 mm long x 10 mm wide through the part, centered at X=70 mm, Y=27 mm.
# - Mill a rectangular relief pocket 35 mm x 18 mm x 2 mm deep on the top face, centered between the mounting holes.
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
    Stock.rectangular(140, 55, 52, material="steel_1045")
    .drill(diameter=6, cx=-59, cy=-0.5, depth=52, through=True)
    .drill(diameter=6, cx=59, cy=-0.5, depth=52, through=True)
    .slot(length=46, width=10, depth=52, cx=0, cy=-0.5)
    .pocket(width=18, length=35, depth=2, cx=0, cy=0, corner_radius=0.5)
)
