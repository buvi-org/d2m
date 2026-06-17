# Requirement: SMP-032-03
# Source agent: 032
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_032_fabrication_gauges_single_metal_parts.json
# Part: Sheet Metal Edge Burr Detection Comb - single metal part
# Raw idea: Sheet Metal Edge Burr Detection Comb
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 205 x 120 x 10 mm using material steel_a36.
# - Drill two through holes diameter 5 mm on the length centerline at X=24 mm and X=181 mm, Y=60 mm.
# - Machine a central obround slot 68 mm long x 9 mm wide through the part, centered at X=102 mm, Y=60 mm.
# - Mill a rectangular relief pocket 51 mm x 40 mm x 5 mm deep on the top face, centered between the mounting holes.
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
    Stock.rectangular(205, 120, 10, material="steel_a36")
    .drill(diameter=5, cx=-78.5, cy=0, depth=10, through=True)
    .drill(diameter=5, cx=78.5, cy=0, depth=10, through=True)
    .slot(length=68, width=9, depth=10, cx=-0.5, cy=0)
    .pocket(width=40, length=51, depth=5, cx=0, cy=0, corner_radius=0.5)
)
