# Requirement: SMP-018-04
# Source agent: 018
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_018_sports_fitness_rehab_single_metal_parts.json
# Part: Variable Incline Bench Locking Sector - single metal part
# Raw idea: Variable Incline Bench Locking Sector
# Status: draft_unexecuted
#
# Coverage notes:
# - Rectangular stock envelope 195 x 105 x 8 mm with mapped material steel_a36.
# - Two through mounting holes dia 13 mm at X=21/174, Y=52.
# - Central through obround slot 65 x 12 mm at X=97, Y=52.
# - Top relief pocket 48 x 35 x 1 mm deep, centered between mounting holes.
# - 1.0 mm top/outside chamfer represented with Stock.chamfer.
#
# Known gaps:
# - 0.5 mm chamfers on individual hole and slot mouths are not separately selectable in this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Coordinate conversion used Stock centered XY coordinates from the requirement lower-left origin.

from subcad import Stock

part = (
    Stock.rectangular(195, 105, 8, material="steel_a36")
    .drill(diameter=13, cx=-76.5, cy=-0.5, through=True)
    .drill(diameter=13, cx=76.5, cy=-0.5, through=True)
    .slot(length=65, width=12, cx=-0.5, cy=-0.5, through=True)
    .pocket(width=35, length=48, depth=1, cx=0, cy=0)
)
