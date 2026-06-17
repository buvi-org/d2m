# Requirement: SMP-032-09
# Source agent: 032
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_032_fabrication_gauges_single_metal_parts.json
# Part: Torch Nozzle Standoff Gauge Ring - single metal part
# Raw idea: Torch Nozzle Standoff Gauge Ring
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 125 x 45 x 48 mm using material steel_1045.
# - Drill two through holes diameter 7 mm on the length centerline at X=10 mm and X=115 mm, Y=22 mm.
# - Machine a central obround slot 41 mm long x 11 mm wide through the part, centered at X=62 mm, Y=22 mm.
# - Mill a rectangular relief pocket 31 mm x 18 mm x 2 mm deep on the top face, centered between the mounting holes.
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
    Stock.rectangular(125, 45, 48, material="steel_1045")
    .drill(diameter=7, cx=-52.5, cy=-0.5, depth=48, through=True)
    .drill(diameter=7, cx=52.5, cy=-0.5, depth=48, through=True)
    .slot(length=41, width=11, depth=48, cx=-0.5, cy=-0.5)
    .pocket(width=18, length=31, depth=2, cx=0, cy=0, corner_radius=0.5)
)
