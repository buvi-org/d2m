# Requirement: SMP-023-10
# Source agent: 023
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_023_warehouse_logistics_hardware_single_metal_parts.json
# Part: Cart Handle Height Adjustment Index Plate - single metal part
# Raw idea: Cart Handle Height Adjustment Index Plate
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 195 x 130 x 10 mm.
# - Two through mounting holes diameter 7 mm at X=26 and X=169, Y=65.
# - Central through obround slot 65 x 8 mm at X=97, Y=65.
# - Top relief pocket 48 x 43 x 5 mm centered between mounting holes.
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
    Stock.rectangular(195, 130, 10, material="steel_a36")
    .drill(diameter=7, through=True, cx=-71.5, cy=0, spot_drill=False)
    .drill(diameter=7, through=True, cx=71.5, cy=0, spot_drill=False)
    .slot(length=65, width=8, through=True, cx=-0.5, cy=0)
    .pocket(length=48, width=43, depth=5, cx=0, cy=0, corner_radius=0)
)
