# Requirement: SMP-030-02
# Source agent: 030
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_030_appliance_repair_hardware_single_metal_parts.json
# Part: Dryer Idler Pulley Tension Bracket - single metal part
# Raw idea: Dryer Idler Pulley Tension Bracket
# Status: draft_unexecuted
#
# Coverage notes:
# - Created rectangular stock at 185 x 105 x 6 mm using material steel_a36.
# - Drill two through holes diameter 10 mm on the length centerline at X=21 mm and X=164 mm, Y=52 mm.
# - Machine a central obround slot 61 mm long x 16 mm wide through the part, centered at X=92 mm, Y=52 mm.
# - Mill a rectangular relief pocket 46 mm x 35 mm x 1 mm deep on the top face, centered between the mounting holes.
# - Applied a 1.0 mm top-edge chamfer operation.
# - Added 9 rear-edge groove cuts as a serration placeholder.
# - Added a short-end groove to indicate the hook-lip undercut region.
#
# Known gaps:
# - 0.5 mm chamfers specifically on individual hole and slot mouths are not separately modeled; only the global/top chamfer is included.
# - Cut 9 equal triangular serrations across the rear edge, each 5 mm deep. SubCAD does not expose triangular tooth serrations here; draft uses rectangular groove approximations.
# - Leave an integral hook lip on one short end, projecting 10 mm and undercut 4 mm for registration. An integral projecting hook lip beyond/within the stock end is only approximated as a machined groove.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - SubCAD stock is centered at the origin; requirement datum coordinates were converted from lower-left-near X/Y values to centered cx/cy values.

from subcad import Stock

part = (
    Stock.rectangular(185, 105, 6, material="steel_a36")
    .drill(diameter=10, cx=-71.5, cy=-0.5, depth=6, through=True)
    .drill(diameter=10, cx=71.5, cy=-0.5, depth=6, through=True)
    .slot(length=61, width=16, depth=6, cx=-0.5, cy=-0.5)
    .pocket(width=35, length=46, depth=1, cx=0, cy=0, corner_radius=0.5)
    .groove(length=5, width=9.25, depth=5, angle=90, cx=-82.222, cy=50)
    .groove(length=5, width=9.25, depth=5, angle=90, cx=-61.667, cy=50)
    .groove(length=5, width=9.25, depth=5, angle=90, cx=-41.111, cy=50)
    .groove(length=5, width=9.25, depth=5, angle=90, cx=-20.556, cy=50)
    .groove(length=5, width=9.25, depth=5, angle=90, cx=0, cy=50)
    .groove(length=5, width=9.25, depth=5, angle=90, cx=20.556, cy=50)
    .groove(length=5, width=9.25, depth=5, angle=90, cx=41.111, cy=50)
    .groove(length=5, width=9.25, depth=5, angle=90, cx=61.667, cy=50)
    .groove(length=5, width=9.25, depth=5, angle=90, cx=82.222, cy=50)
    .groove(length=10, width=84, depth=4, cx=-87.5, cy=0)
)
