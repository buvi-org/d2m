# Requirement: SMP-018-03
# Source agent: 018
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_018_sports_fitness_rehab_single_metal_parts.json
# Part: Rehabilitation Ankle Resistance Pedal - single metal part
# Raw idea: Rehabilitation Ankle Resistance Pedal
# Status: draft_unexecuted
#
# Coverage notes:
# - Rectangular stock envelope 145 x 80 x 11 mm with mapped material steel_a36.
# - Two through mounting holes dia 6 mm at X=16/129, Y=40.
# - Central through obround slot 48 x 12 mm at X=72, Y=40.
# - Top relief pocket 36 x 26 x 1 mm deep, centered between mounting holes.
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
    Stock.rectangular(145, 80, 11, material="steel_a36")
    .drill(diameter=6, cx=-56.5, cy=0, through=True)
    .drill(diameter=6, cx=56.5, cy=0, through=True)
    .slot(length=48, width=12, cx=-0.5, cy=0, through=True)
    .pocket(width=26, length=36, depth=1, cx=0, cy=0)
)
