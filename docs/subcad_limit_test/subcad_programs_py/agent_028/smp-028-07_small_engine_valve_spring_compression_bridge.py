# Requirement: SMP-028-07
# Source agent: 028
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_028_small_engine_service_hardware_single_metal_parts.json
# Part: Small Engine Valve Spring Compression Bridge - single metal part
# Raw idea: Small Engine Valve Spring Compression Bridge
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 70 x 65 x 22 mm using material steel_1045.
# - Drill two through holes diameter 11 mm on the length centerline at X=13 mm and X=57 mm, Y=32 mm.
# - Machine a central obround slot 30 mm long x 18 mm wide through the part, centered at X=35 mm, Y=32 mm.
# - Mill a rectangular relief pocket 25 mm x 21 mm x 4 mm deep on the top face, centered between the mounting holes.
# - Applied a 1.0 mm top-edge chamfer operation.
# - Added a threaded-hole placeholder at the central pocket location.
#
# Known gaps:
# - 0.5 mm chamfers specifically on individual hole and slot mouths are not separately modeled; only the global/top chamfer is included.
# - Tap one side hole M7 from the right long edge into the central pocket; hole axis is parallel to Y. Side-axis tapped holes from a long edge are not represented exactly by the top-face threaded_hole operation.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - SubCAD stock is centered at the origin; requirement datum coordinates were converted from lower-left-near X/Y values to centered cx/cy values.

from subcad import Stock

part = (
    Stock.rectangular(70, 65, 22, material="steel_1045")
    .drill(diameter=11, cx=-22, cy=-0.5, depth=22, through=True)
    .drill(diameter=11, cx=22, cy=-0.5, depth=22, through=True)
    .slot(length=30, width=18, depth=22, cx=0, cy=-0.5)
    .pocket(width=21, length=25, depth=4, cx=0, cy=0, corner_radius=0.5)
    .threaded_hole(diameter=7, depth=32.5, cx=0, cy=0)
)
