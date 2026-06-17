# Requirement: SMP-018-07
# Source agent: 018
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_018_sports_fitness_rehab_single_metal_parts.json
# Part: Treadmill Deck Flexion Hinge Block - single metal part
# Raw idea: Treadmill Deck Flexion Hinge Block
# Status: draft_unexecuted
#
# Coverage notes:
# - Rectangular stock envelope 175 x 85 x 34 mm with mapped material steel_a36.
# - Two through mounting holes dia 8 mm at X=17/158, Y=42.
# - Central through obround slot 58 x 7 mm at X=87, Y=42.
# - Top relief pocket 43 x 28 x 17 mm deep, centered between mounting holes.
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
    Stock.rectangular(175, 85, 34, material="steel_a36")
    .drill(diameter=8, cx=-70.5, cy=-0.5, through=True)
    .drill(diameter=8, cx=70.5, cy=-0.5, through=True)
    .slot(length=58, width=7, cx=-0.5, cy=-0.5, through=True)
    .pocket(width=28, length=43, depth=17, cx=0, cy=0)
)
