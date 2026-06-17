# Requirement: SMP-032-02
# Source agent: 032
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_032_fabrication_gauges_single_metal_parts.json
# Part: Magnetic Tack Weld Corner Holding Fixture - single metal part
# Raw idea: Magnetic Tack Weld Corner Holding Fixture
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 165 x 120 x 33 mm using material steel_1045.
# - Drill two through holes diameter 8 mm on the length centerline at X=24 mm and X=141 mm, Y=60 mm.
# - Machine a central obround slot 55 mm long x 16 mm wide through the part, centered at X=82 mm, Y=60 mm.
# - Mill a rectangular relief pocket 41 mm x 40 mm x 5 mm deep on the top face, centered between the mounting holes.
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
    Stock.rectangular(165, 120, 33, material="steel_1045")
    .drill(diameter=8, cx=-58.5, cy=0, depth=33, through=True)
    .drill(diameter=8, cx=58.5, cy=0, depth=33, through=True)
    .slot(length=55, width=16, depth=33, cx=-0.5, cy=0)
    .pocket(width=40, length=41, depth=5, cx=0, cy=0, corner_radius=0.5)
)
