# Requirement: SMP-023-01
# Source agent: 023
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_023_warehouse_logistics_hardware_single_metal_parts.json
# Part: Adjustable Conveyor Side Guide Bracket - single metal part
# Raw idea: Adjustable Conveyor Side Guide Bracket
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 220 x 65 x 6 mm.
# - Two through mounting holes diameter 6 mm at X=13 and X=207, Y=32.
# - Central through obround slot 73 x 8 mm at X=110, Y=32.
# - Top relief pocket 55 x 21 x 2 mm centered between mounting holes.
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
    Stock.rectangular(220, 65, 6, material="steel_a36")
    .drill(diameter=6, through=True, cx=-97, cy=-0.5, spot_drill=False)
    .drill(diameter=6, through=True, cx=97, cy=-0.5, spot_drill=False)
    .slot(length=73, width=8, through=True, cx=0, cy=-0.5)
    .pocket(length=55, width=21, depth=2, cx=0, cy=0, corner_radius=0)
)
