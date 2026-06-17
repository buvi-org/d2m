# Requirement: SMP-032-04
# Source agent: 032
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_032_fabrication_gauges_single_metal_parts.json
# Part: Pipe Saddle Layout Wrap Gauge - single metal part
# Raw idea: Pipe Saddle Layout Wrap Gauge
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 160 x 85 x 49 mm using material steel_1045.
# - Drill two through holes diameter 13 mm on the length centerline at X=17 mm and X=143 mm, Y=42 mm.
# - Machine a central obround slot 53 mm long x 8 mm wide through the part, centered at X=80 mm, Y=42 mm.
# - Mill a rectangular relief pocket 40 mm x 28 mm x 14 mm deep on the top face, centered between the mounting holes.
# - Applied a 1.0 mm top-edge chamfer operation.
# - Added a centered dovetail-style cut to stand in for the V-groove.
#
# Known gaps:
# - 0.5 mm chamfers specifically on individual hole and slot mouths are not separately modeled; only the global/top chamfer is included.
# - Cut a 90 degree V-groove along the full X length on the top face, groove mouth 42 mm wide and depth 16 mm. Exact V-groove included angle/profile is approximated with the available dovetail operation.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - SubCAD stock is centered at the origin; requirement datum coordinates were converted from lower-left-near X/Y values to centered cx/cy values.

from subcad import Stock

part = (
    Stock.rectangular(160, 85, 49, material="steel_1045")
    .drill(diameter=13, cx=-63, cy=-0.5, depth=49, through=True)
    .drill(diameter=13, cx=63, cy=-0.5, depth=49, through=True)
    .slot(length=53, width=8, depth=49, cx=0, cy=-0.5)
    .pocket(width=28, length=40, depth=14, cx=0, cy=0, corner_radius=0.5)
    .dovetail(length=120, width=90, depth=42, angle=90, cx=0, cy=0)
)
