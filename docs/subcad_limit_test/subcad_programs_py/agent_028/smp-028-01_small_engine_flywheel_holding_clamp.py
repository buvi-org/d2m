# Requirement: SMP-028-01
# Source agent: 028
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_028_small_engine_service_hardware_single_metal_parts.json
# Part: Small Engine Flywheel Holding Clamp - single metal part
# Raw idea: Small Engine Flywheel Holding Clamp
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 105 x 40 x 56 mm using material steel_1045.
# - Drill two through holes diameter 9 mm on the length centerline at X=10 mm and X=95 mm, Y=20 mm.
# - Machine a central obround slot 35 mm long x 16 mm wide through the part, centered at X=52 mm, Y=20 mm.
# - Mill a rectangular relief pocket 26 mm x 18 mm x 14 mm deep on the top face, centered between the mounting holes.
# - Applied a 1.0 mm top-edge chamfer operation.
# - Added 9 rear-edge groove cuts as a serration placeholder.
# - Added a threaded-hole placeholder at the central pocket location.
#
# Known gaps:
# - 0.5 mm chamfers specifically on individual hole and slot mouths are not separately modeled; only the global/top chamfer is included.
# - Cut 9 equal triangular serrations across the rear edge, each 2 mm deep. SubCAD does not expose triangular tooth serrations here; draft uses rectangular groove approximations.
# - Tap one side hole M9 from the right long edge into the central pocket; hole axis is parallel to Y. Side-axis tapped holes from a long edge are not represented exactly by the top-face threaded_hole operation.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
# - Executable draft omits edge groove serration/hook proxies that caused invalid or envelope-shrinking geometry; those features remain requirement gaps for Stage 4 review.
#
# Review notes:
# - SubCAD stock is centered at the origin; requirement datum coordinates were converted from lower-left-near X/Y values to centered cx/cy values.

from subcad import Stock

part = (
    Stock.rectangular(105, 40, 56, material="steel_1045")
    .drill(diameter=9, cx=-42.5, cy=0, depth=56, through=True)
    .drill(diameter=9, cx=42.5, cy=0, depth=56, through=True)
    .slot(length=35, width=16, depth=56, cx=-0.5, cy=0)
    .pocket(width=18, length=26, depth=14, cx=0, cy=0, corner_radius=0.5)
    .threaded_hole(diameter=9, depth=20, cx=0, cy=0)
)
