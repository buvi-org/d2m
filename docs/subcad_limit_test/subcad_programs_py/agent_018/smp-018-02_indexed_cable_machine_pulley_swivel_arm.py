# Requirement: SMP-018-02
# Source agent: 018
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_018_sports_fitness_rehab_single_metal_parts.json
# Part: Indexed Cable Machine Pulley Swivel Arm - single metal part
# Raw idea: Indexed Cable Machine Pulley Swivel Arm
# Status: draft_unexecuted
#
# Coverage notes:
# - Rectangular stock envelope 220 x 75 x 35 mm with mapped material steel_a36.
# - Two through mounting holes dia 12 mm at X=15/205, Y=37.
# - Central through obround slot 73 x 12 mm at X=110, Y=37.
# - Top relief pocket 55 x 25 x 4 mm deep, centered between mounting holes.
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
    Stock.rectangular(220, 75, 35, material="steel_a36")
    .drill(diameter=12, cx=-95, cy=-0.5, through=True)
    .drill(diameter=12, cx=95, cy=-0.5, through=True)
    .slot(length=73, width=12, cx=0, cy=-0.5, through=True)
    .pocket(width=25, length=55, depth=4, cx=0, cy=0)
)
