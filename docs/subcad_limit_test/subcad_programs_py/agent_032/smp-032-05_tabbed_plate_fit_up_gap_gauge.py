# Requirement: SMP-032-05
# Source agent: 032
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_032_fabrication_gauges_single_metal_parts.json
# Part: Tabbed Plate Fit-Up Gap Gauge - single metal part
# Raw idea: Tabbed Plate Fit-Up Gap Gauge
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 180 x 110 x 4 mm using material steel_1045.
# - Drill two through holes diameter 12 mm on the length centerline at X=22 mm and X=158 mm, Y=55 mm.
# - Machine a central obround slot 60 mm long x 7 mm wide through the part, centered at X=90 mm, Y=55 mm.
# - Mill a rectangular relief pocket 45 mm x 36 mm x 1 mm deep on the top face, centered between the mounting holes.
# - Applied a 1.0 mm top-edge chamfer operation.
# - Added 9 rear-edge groove cuts as a serration placeholder.
#
# Known gaps:
# - 0.5 mm chamfers specifically on individual hole and slot mouths are not separately modeled; only the global/top chamfer is included.
# - Cut 9 equal triangular serrations across the rear edge, each 5 mm deep. SubCAD does not expose triangular tooth serrations here; draft uses rectangular groove approximations.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - SubCAD stock is centered at the origin; requirement datum coordinates were converted from lower-left-near X/Y values to centered cx/cy values.

from subcad import Stock

part = (
    Stock.rectangular(180, 110, 4, material="steel_1045")
    .drill(diameter=12, cx=-68, cy=0, depth=4, through=True)
    .drill(diameter=12, cx=68, cy=0, depth=4, through=True)
    .slot(length=60, width=7, depth=4, cx=0, cy=0)
    .pocket(width=36, length=45, depth=1, cx=0, cy=0, corner_radius=0.5)
    .groove(length=5, width=9, depth=4, angle=90, cx=-80, cy=52.5)
    .groove(length=5, width=9, depth=4, angle=90, cx=-60, cy=52.5)
    .groove(length=5, width=9, depth=4, angle=90, cx=-40, cy=52.5)
    .groove(length=5, width=9, depth=4, angle=90, cx=-20, cy=52.5)
    .groove(length=5, width=9, depth=4, angle=90, cx=0, cy=52.5)
    .groove(length=5, width=9, depth=4, angle=90, cx=20, cy=52.5)
    .groove(length=5, width=9, depth=4, angle=90, cx=40, cy=52.5)
    .groove(length=5, width=9, depth=4, angle=90, cx=60, cy=52.5)
    .groove(length=5, width=9, depth=4, angle=90, cx=80, cy=52.5)
)
