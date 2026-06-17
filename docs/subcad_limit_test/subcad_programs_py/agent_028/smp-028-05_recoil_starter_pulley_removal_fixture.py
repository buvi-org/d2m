# Requirement: SMP-028-05
# Source agent: 028
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_028_small_engine_service_hardware_single_metal_parts.json
# Part: Recoil Starter Pulley Removal Fixture - single metal part
# Raw idea: Recoil Starter Pulley Removal Fixture
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 230 x 100 x 5 mm using material steel_a36.
# - Drill two through holes diameter 7 mm on the length centerline at X=20 mm and X=210 mm, Y=50 mm.
# - Machine a central obround slot 76 mm long x 15 mm wide through the part, centered at X=115 mm, Y=50 mm.
# - Mill a rectangular relief pocket 57 mm x 33 mm x 2 mm deep on the top face, centered between the mounting holes.
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
    Stock.rectangular(230, 100, 5, material="steel_a36")
    .drill(diameter=7, cx=-95, cy=0, depth=5, through=True)
    .drill(diameter=7, cx=95, cy=0, depth=5, through=True)
    .slot(length=76, width=15, depth=5, cx=0, cy=0)
    .pocket(width=33, length=57, depth=2, cx=0, cy=0, corner_radius=0.5)
)
