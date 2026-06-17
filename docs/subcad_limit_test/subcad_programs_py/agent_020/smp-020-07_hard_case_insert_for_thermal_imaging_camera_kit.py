# Requirement: SMP-020-07
# Source agent: 020
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_020_rescue_service_hardware_single_metal_parts.json
# Part: Hard Case Insert for Thermal Imaging Camera Kit - single metal part
# Raw idea: Hard Case Insert for Thermal Imaging Camera Kit
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 150 x 100 x 25 mm.
# - Two through mounting holes diameter 6 mm at X=20 and X=130, Y=50.
# - Central through obround slot 50 x 10 mm at X=75, Y=50.
# - Top relief pocket 37 x 33 x 6 mm centered between mounting holes.
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
    Stock.rectangular(150, 100, 25, material="aluminum_6061")
    .drill(diameter=6, through=True, cx=-55, cy=0, spot_drill=False)
    .drill(diameter=6, through=True, cx=55, cy=0, spot_drill=False)
    .slot(length=50, width=10, through=True, cx=0, cy=0)
    .pocket(length=37, width=33, depth=6, cx=0, cy=0, corner_radius=0)
)
