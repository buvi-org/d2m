# Requirement: SMP-028-06
# Source agent: 028
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_028_small_engine_service_hardware_single_metal_parts.json
# Part: Primer Bulb Retainer Ring Press Tool - single metal part
# Raw idea: Primer Bulb Retainer Ring Press Tool
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 170 x 90 x 53 mm using material steel_1045.
# - Drill two through holes diameter 12 mm on the length centerline at X=18 mm and X=152 mm, Y=45 mm.
# - Machine a central obround slot 56 mm long x 17 mm wide through the part, centered at X=85 mm, Y=45 mm.
# - Mill a rectangular relief pocket 42 mm x 30 mm x 6 mm deep on the top face, centered between the mounting holes.
# - Applied a 1.0 mm top-edge chamfer operation.
# - Added 9 rear-edge groove cuts as a serration placeholder.
#
# Known gaps:
# - 0.5 mm chamfers specifically on individual hole and slot mouths are not separately modeled; only the global/top chamfer is included.
# - Cut 9 equal triangular serrations across the rear edge, each 4 mm deep. SubCAD does not expose triangular tooth serrations here; draft uses rectangular groove approximations.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
# - Executable draft omits edge groove serration/hook proxies that caused invalid or envelope-shrinking geometry; those features remain requirement gaps for Stage 4 review.
#
# Review notes:
# - SubCAD stock is centered at the origin; requirement datum coordinates were converted from lower-left-near X/Y values to centered cx/cy values.

from subcad import Stock

part = (
    Stock.rectangular(170, 90, 53, material="steel_1045")
    .drill(diameter=12, cx=-67, cy=0, depth=53, through=True)
    .drill(diameter=12, cx=67, cy=0, depth=53, through=True)
    .slot(length=56, width=17, depth=53, cx=0, cy=0)
    .pocket(width=30, length=42, depth=6, cx=0, cy=0, corner_radius=0.5)
)
