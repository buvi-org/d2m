# Requirement: SMP-020-04
# Source agent: 020
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_020_rescue_service_hardware_single_metal_parts.json
# Part: Field Radio Shock-Isolation Corner Frame - single metal part
# Raw idea: Field Radio Shock-Isolation Corner Frame
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 200 x 95 x 26 mm.
# - Two through mounting holes diameter 13 mm at X=19 and X=181, Y=47.
# - Central through obround slot 66 x 16 mm at X=100, Y=47.
# - Top relief pocket 50 x 31 x 7 mm centered between mounting holes.
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
    Stock.rectangular(200, 95, 26, material="steel_a36")
    .drill(diameter=13, through=True, cx=-81, cy=-0.5, spot_drill=False)
    .drill(diameter=13, through=True, cx=81, cy=-0.5, spot_drill=False)
    .slot(length=66, width=16, through=True, cx=0, cy=-0.5)
    .pocket(length=50, width=31, depth=7, cx=0, cy=0, corner_radius=0)
)
