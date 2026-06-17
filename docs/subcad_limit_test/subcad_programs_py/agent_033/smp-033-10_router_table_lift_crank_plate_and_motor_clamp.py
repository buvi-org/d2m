# Requirement: SMP-033-10
# Source agent: 033
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_033_woodworking_machines_single_metal_parts.json
# Part: Router table lift crank plate and motor clamp - single metal part
# Raw idea: Router table lift crank plate and motor clamp
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 175 x 120 x 3 mm using material steel_1045.
# - Drill two through holes diameter 7 mm on the length centerline at X=24 mm and X=151 mm, Y=60 mm.
# - Machine a central obround slot 58 mm long x 17 mm wide through the part, centered at X=87 mm, Y=60 mm.
# - Mill a rectangular relief pocket 43 mm x 40 mm x 1 mm deep on the top face, centered between the mounting holes.
# - Applied a 1.0 mm top-edge chamfer operation.
# - Added a threaded-hole placeholder at the central pocket location.
#
# Known gaps:
# - 0.5 mm chamfers specifically on individual hole and slot mouths are not separately modeled; only the global/top chamfer is included.
# - Tap one side hole M4 from the right long edge into the central pocket; hole axis is parallel to Y. Side-axis tapped holes from a long edge are not represented exactly by the top-face threaded_hole operation.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - SubCAD stock is centered at the origin; requirement datum coordinates were converted from lower-left-near X/Y values to centered cx/cy values.

from subcad import Stock

part = (
    Stock.rectangular(175, 120, 3, material="steel_1045")
    .drill(diameter=7, cx=-63.5, cy=0, depth=3, through=True)
    .drill(diameter=7, cx=63.5, cy=0, depth=3, through=True)
    .slot(length=58, width=17, depth=3, cx=-0.5, cy=0)
    .pocket(width=40, length=43, depth=1, cx=0, cy=0, corner_radius=0.5)
    .threaded_hole(diameter=4, depth=60, cx=0, cy=0)
)
