# Requirement: SMP-030-05
# Source agent: 030
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_030_appliance_repair_hardware_single_metal_parts.json
# Part: Washing Machine Motor Alignment Shim Gauge - single metal part
# Raw idea: Washing Machine Motor Alignment Shim Gauge
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 185 x 140 x 9 mm using material steel_a36.
# - Drill two through holes diameter 7 mm on the length centerline at X=28 mm and X=157 mm, Y=70 mm.
# - Machine a central obround slot 61 mm long x 8 mm wide through the part, centered at X=92 mm, Y=70 mm.
# - Mill a rectangular relief pocket 46 mm x 46 mm x 3 mm deep on the top face, centered between the mounting holes.
# - Applied a 1.0 mm top-edge chamfer operation.
# - Added 9 rear-edge groove cuts as a serration placeholder.
#
# Known gaps:
# - 0.5 mm chamfers specifically on individual hole and slot mouths are not separately modeled; only the global/top chamfer is included.
# - Cut 9 equal triangular serrations across the rear edge, each 2 mm deep. SubCAD does not expose triangular tooth serrations here; draft uses rectangular groove approximations.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
# - Executable draft omits edge groove serration/hook proxies that caused invalid or envelope-shrinking geometry; those features remain requirement gaps for Stage 4 review.
#
# Review notes:
# - SubCAD stock is centered at the origin; requirement datum coordinates were converted from lower-left-near X/Y values to centered cx/cy values.

from subcad import Stock

part = (
    Stock.rectangular(185, 140, 9, material="steel_a36")
    .drill(diameter=7, cx=-64.5, cy=0, depth=9, through=True)
    .drill(diameter=7, cx=64.5, cy=0, depth=9, through=True)
    .slot(length=61, width=8, depth=9, cx=-0.5, cy=0)
    .pocket(width=46, length=46, depth=3, cx=0, cy=0, corner_radius=0.5)
)
