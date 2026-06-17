# Requirement: SMP-023-03
# Source agent: 023
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_023_warehouse_logistics_hardware_single_metal_parts.json
# Part: Tote Nesting Locator Plate - single metal part
# Raw idea: Tote Nesting Locator Plate
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 245 x 135 x 3 mm.
# - Two through mounting holes diameter 11 mm at X=27 and X=218, Y=67.
# - Central through obround slot 81 x 14 mm at X=122, Y=67.
# - Top relief pocket 61 x 45 x 1 mm centered between mounting holes.
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
    Stock.rectangular(245, 135, 3, material="aluminum_6061")
    .drill(diameter=11, through=True, cx=-95.5, cy=-0.5, spot_drill=False)
    .drill(diameter=11, through=True, cx=95.5, cy=-0.5, spot_drill=False)
    .slot(length=81, width=14, through=True, cx=-0.5, cy=-0.5)
    .pocket(length=61, width=45, depth=1, cx=0, cy=0, corner_radius=0)
)
