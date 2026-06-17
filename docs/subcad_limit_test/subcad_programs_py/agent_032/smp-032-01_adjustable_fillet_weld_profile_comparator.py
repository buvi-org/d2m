# Requirement: SMP-032-01
# Source agent: 032
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_032_fabrication_gauges_single_metal_parts.json
# Part: Adjustable Fillet Weld Profile Comparator - single metal part
# Raw idea: Adjustable Fillet Weld Profile Comparator
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 90 x 65 x 68 mm using material steel_1045.
# - Drill two through holes diameter 11 mm on the length centerline at X=13 mm and X=77 mm, Y=32 mm.
# - Machine a central obround slot 30 mm long x 18 mm wide through the part, centered at X=45 mm, Y=32 mm.
# - Mill a rectangular relief pocket 25 mm x 21 mm x 12 mm deep on the top face, centered between the mounting holes.
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
    Stock.rectangular(90, 65, 68, material="steel_1045")
    .drill(diameter=11, cx=-32, cy=-0.5, depth=68, through=True)
    .drill(diameter=11, cx=32, cy=-0.5, depth=68, through=True)
    .slot(length=30, width=18, depth=68, cx=0, cy=-0.5)
    .pocket(width=21, length=25, depth=12, cx=0, cy=0, corner_radius=0.5)
)
