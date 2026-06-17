# Requirement: SMP-031-10
# Source agent: 031
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_031_pumps_rotating_equipment_single_metal_parts.json
# Part: Coupling Hub Keyway Inspection Gauge - single metal part
# Raw idea: Coupling Hub Keyway Inspection Gauge
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 120 x 85 x 70 mm using material steel_a36.
# - Drill two through holes diameter 8 mm on the length centerline at X=17 mm and X=103 mm, Y=42 mm.
# - Machine a central obround slot 40 mm long x 16 mm wide through the part, centered at X=60 mm, Y=42 mm.
# - Mill a rectangular relief pocket 30 mm x 28 mm x 32 mm deep on the top face, centered between the mounting holes.
# - Applied a 1.0 mm top-edge chamfer operation.
# - Added 12 rear-edge groove cuts as a serration placeholder.
#
# Known gaps:
# - 0.5 mm chamfers specifically on individual hole and slot mouths are not separately modeled; only the global/top chamfer is included.
# - Cut 12 equal triangular serrations across the rear edge, each 2 mm deep. SubCAD does not expose triangular tooth serrations here; draft uses rectangular groove approximations.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
# - Executable draft omits edge groove serration/hook proxies that caused invalid or envelope-shrinking geometry; those features remain requirement gaps for Stage 4 review.
#
# Review notes:
# - SubCAD stock is centered at the origin; requirement datum coordinates were converted from lower-left-near X/Y values to centered cx/cy values.

from subcad import Stock

part = (
    Stock.rectangular(120, 85, 70, material="steel_a36")
    .drill(diameter=8, cx=-43, cy=-0.5, depth=70, through=True)
    .drill(diameter=8, cx=43, cy=-0.5, depth=70, through=True)
    .slot(length=40, width=16, depth=70, cx=0, cy=-0.5)
    .pocket(width=28, length=30, depth=32, cx=0, cy=0, corner_radius=0.5)
)
