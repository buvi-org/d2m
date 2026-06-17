# Requirement: SMP-031-04
# Source agent: 031
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_031_pumps_rotating_equipment_single_metal_parts.json
# Part: Pump Impeller Puller Yoke - single metal part
# Raw idea: Pump Impeller Puller Yoke
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 195 x 50 x 45 mm using material steel_a36.
# - Drill two through holes diameter 12 mm on the length centerline at X=10 mm and X=185 mm, Y=25 mm.
# - Machine a central obround slot 65 mm long x 11 mm wide through the part, centered at X=97 mm, Y=25 mm.
# - Mill a rectangular relief pocket 48 mm x 18 mm x 16 mm deep on the top face, centered between the mounting holes.
# - Applied a 1.0 mm top-edge chamfer operation.
# - Added a threaded-hole placeholder at the central pocket location.
#
# Known gaps:
# - 0.5 mm chamfers specifically on individual hole and slot mouths are not separately modeled; only the global/top chamfer is included.
# - Tap one side hole M6 from the right long edge into the central pocket; hole axis is parallel to Y. Side-axis tapped holes from a long edge are not represented exactly by the top-face threaded_hole operation.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - SubCAD stock is centered at the origin; requirement datum coordinates were converted from lower-left-near X/Y values to centered cx/cy values.

from subcad import Stock

part = (
    Stock.rectangular(195, 50, 45, material="steel_a36")
    .drill(diameter=12, cx=-87.5, cy=0, depth=45, through=True)
    .drill(diameter=12, cx=87.5, cy=0, depth=45, through=True)
    .slot(length=65, width=11, depth=45, cx=-0.5, cy=0)
    .pocket(width=18, length=48, depth=16, cx=0, cy=0, corner_radius=0.5)
    .threaded_hole(diameter=6, depth=25, cx=0, cy=0)
)
