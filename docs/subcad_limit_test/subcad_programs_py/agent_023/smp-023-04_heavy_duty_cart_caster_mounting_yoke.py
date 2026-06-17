# Requirement: SMP-023-04
# Source agent: 023
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_023_warehouse_logistics_hardware_single_metal_parts.json
# Part: Heavy-Duty Cart Caster Mounting Yoke - single metal part
# Raw idea: Heavy-Duty Cart Caster Mounting Yoke
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 115 x 105 x 11 mm.
# - Two through mounting holes diameter 7 mm at X=21 and X=94, Y=52.
# - Central through obround slot 38 x 15 mm at X=57, Y=52.
# - Top relief pocket 28 x 35 x 1 mm centered between mounting holes.
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
    Stock.rectangular(115, 105, 11, material="steel_a36")
    .drill(diameter=7, through=True, cx=-36.5, cy=-0.5, spot_drill=False)
    .drill(diameter=7, through=True, cx=36.5, cy=-0.5, spot_drill=False)
    .slot(length=38, width=15, through=True, cx=-0.5, cy=-0.5)
    .pocket(length=28, width=35, depth=1, cx=0, cy=0, corner_radius=0)
)
