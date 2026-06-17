# Requirement: SMP-020-09
# Source agent: 020
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_020_rescue_service_hardware_single_metal_parts.json
# Part: Temporary Command Post Cable Crossover Protector - single metal part
# Raw idea: Temporary Command Post Cable Crossover Protector
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 90 x 55 x 22 mm.
# - Two through mounting holes diameter 5 mm at X=11 and X=79, Y=27.
# - Central through obround slot 30 x 17 mm at X=45, Y=27.
# - Top relief pocket 25 x 18 x 2 mm centered between mounting holes.
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
    Stock.rectangular(90, 55, 22, material="steel_a36")
    .drill(diameter=5, through=True, cx=-34, cy=-0.5, spot_drill=False)
    .drill(diameter=5, through=True, cx=34, cy=-0.5, spot_drill=False)
    .slot(length=30, width=17, through=True, cx=0, cy=-0.5)
    .pocket(length=25, width=18, depth=2, cx=0, cy=0, corner_radius=0)
)
