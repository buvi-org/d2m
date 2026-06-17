# Requirement: SMP-023-08
# Source agent: 023
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_023_warehouse_logistics_hardware_single_metal_parts.json
# Part: Tote Transfer Corner Deflector - single metal part
# Raw idea: Tote Transfer Corner Deflector
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 90 x 80 x 3 mm.
# - Two through mounting holes diameter 5 mm at X=16 and X=74, Y=40.
# - Central through obround slot 30 x 9 mm at X=45, Y=40.
# - Top relief pocket 25 x 26 x 2 mm centered between mounting holes.
# - Top outside chamfers represented with 1 mm chamfer operation.
#
# Known gaps:
# - 0.5 mm chamfers on individual hole and slot mouths are not separately selectable in this draft; only the general top chamfer is modeled.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated directly from frozen Stage 2 requirement text; not executed or visually reviewed yet.
# - Coordinate conversion uses SubCAD centered stock coordinates while requirement text uses lower-left-near datum coordinates.

from subcad import Stock

part = (
    Stock.rectangular(90, 80, 3, material="steel_a36")
    .drill(diameter=5, through=True, cx=-29, cy=0, spot_drill=False)
    .drill(diameter=5, through=True, cx=29, cy=0, spot_drill=False)
    .slot(length=30, width=9, through=True, cx=0, cy=0)
    .pocket(length=25, width=26, depth=2, cx=0, cy=0, corner_radius=0)
)
