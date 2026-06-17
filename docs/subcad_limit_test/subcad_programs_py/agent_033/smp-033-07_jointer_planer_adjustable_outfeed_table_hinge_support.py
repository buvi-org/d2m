# Requirement: SMP-033-07
# Source agent: 033
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_033_woodworking_machines_single_metal_parts.json
# Part: Jointer planer adjustable outfeed table hinge support - single metal part
# Raw idea: Jointer planer adjustable outfeed table hinge support
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 95 x 85 x 42 mm using material steel_a36.
# - Drill two through holes diameter 5 mm on the length centerline at X=17 mm and X=78 mm, Y=42 mm.
# - Machine a central obround slot 31 mm long x 18 mm wide through the part, centered at X=47 mm, Y=42 mm.
# - Mill a rectangular relief pocket 25 mm x 28 mm x 12 mm deep on the top face, centered between the mounting holes.
# - Applied a 1.0 mm top-edge chamfer operation.
# - Added a threaded-hole placeholder at the central pocket location.
#
# Known gaps:
# - 0.5 mm chamfers specifically on individual hole and slot mouths are not separately modeled; only the global/top chamfer is included.
# - Tap one side hole M8 from the right long edge into the central pocket; hole axis is parallel to Y. Side-axis tapped holes from a long edge are not represented exactly by the top-face threaded_hole operation.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - SubCAD stock is centered at the origin; requirement datum coordinates were converted from lower-left-near X/Y values to centered cx/cy values.

from subcad import Stock

part = (
    Stock.rectangular(95, 85, 42, material="steel_a36")
    .drill(diameter=5, cx=-30.5, cy=-0.5, depth=42, through=True)
    .drill(diameter=5, cx=30.5, cy=-0.5, depth=42, through=True)
    .slot(length=31, width=18, depth=42, cx=-0.5, cy=-0.5)
    .pocket(width=28, length=25, depth=12, cx=0, cy=0, corner_radius=0.5)
    .threaded_hole(diameter=8, depth=42.5, cx=0, cy=0)
)
