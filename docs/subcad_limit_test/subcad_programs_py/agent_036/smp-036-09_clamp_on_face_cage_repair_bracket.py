# Requirement: SMP-036-09
# Source agent: 036
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_036_sports_safety_gear_single_metal_parts.json
# Part: Clamp-on face cage repair bracket - single metal part
# Raw idea: Clamp-on face cage repair bracket
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 135 x 60 x 6 mm using material steel_1045.
# - Drill two through holes diameter 6 mm on the length centerline at X=12 mm and X=123 mm, Y=30 mm.
# - Machine a central obround slot 45 mm long x 10 mm wide through the part, centered at X=67 mm, Y=30 mm.
# - Mill a rectangular relief pocket 33 mm x 20 mm x 3 mm deep on the top face, centered between the mounting holes.
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
    Stock.rectangular(135, 60, 6, material="steel_1045")
    .drill(diameter=6, cx=-55.5, cy=0, depth=6, through=True)
    .drill(diameter=6, cx=55.5, cy=0, depth=6, through=True)
    .slot(length=45, width=10, depth=6, cx=-0.5, cy=0)
    .pocket(width=20, length=33, depth=3, cx=0, cy=0, corner_radius=0.5)
    .threaded_hole(diameter=7, depth=30, cx=0, cy=0)
)
