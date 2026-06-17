# Requirement: SMP-020-01
# Source agent: 020
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_020_rescue_service_hardware_single_metal_parts.json
# Part: Rugged Waterproof Drone Battery Transit Case - single metal part
# Raw idea: Rugged Waterproof Drone Battery Transit Case
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 175 x 110 x 7 mm.
# - Two through mounting holes diameter 7 mm at X=22 and X=153, Y=55.
# - Central through obround slot 58 x 11 mm at X=87, Y=55.
# - Top relief pocket 43 x 36 x 3 mm centered between mounting holes.
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
    Stock.rectangular(175, 110, 7, material="aluminum_6061")
    .drill(diameter=7, through=True, cx=-65.5, cy=0, spot_drill=False)
    .drill(diameter=7, through=True, cx=65.5, cy=0, spot_drill=False)
    .slot(length=58, width=11, through=True, cx=-0.5, cy=0)
    .pocket(length=43, width=36, depth=3, cx=0, cy=0, corner_radius=0)
)
