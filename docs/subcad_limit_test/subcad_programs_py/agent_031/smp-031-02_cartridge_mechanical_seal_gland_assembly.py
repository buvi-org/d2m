# Requirement: SMP-031-02
# Source agent: 031
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_031_pumps_rotating_equipment_single_metal_parts.json
# Part: Cartridge Mechanical Seal Gland Assembly - single metal part
# Raw idea: Cartridge Mechanical Seal Gland Assembly
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 150 x 120 x 3 mm using material steel_a36.
# - Drill two through holes diameter 11 mm on the length centerline at X=24 mm and X=126 mm, Y=60 mm.
# - Machine a central obround slot 50 mm long x 11 mm wide through the part, centered at X=75 mm, Y=60 mm.
# - Mill a rectangular relief pocket 37 mm x 40 mm x 2 mm deep on the top face, centered between the mounting holes.
# - Applied a 1.0 mm top-edge chamfer operation.
# - Added 5 rear-edge groove cuts as a serration placeholder.
#
# Known gaps:
# - 0.5 mm chamfers specifically on individual hole and slot mouths are not separately modeled; only the global/top chamfer is included.
# - Cut 5 equal triangular serrations across the rear edge, each 3 mm deep. SubCAD does not expose triangular tooth serrations here; draft uses rectangular groove approximations.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
# - Executable draft omits edge groove serration/hook proxies that caused invalid or envelope-shrinking geometry; those features remain requirement gaps for Stage 4 review.
#
# Review notes:
# - SubCAD stock is centered at the origin; requirement datum coordinates were converted from lower-left-near X/Y values to centered cx/cy values.

from subcad import Stock

part = (
    Stock.rectangular(150, 120, 3, material="steel_a36")
    .drill(diameter=11, cx=-51, cy=0, depth=3, through=True)
    .drill(diameter=11, cx=51, cy=0, depth=3, through=True)
    .slot(length=50, width=11, depth=3, cx=0, cy=0)
    .pocket(width=40, length=37, depth=2, cx=0, cy=0, corner_radius=0.5)
)
