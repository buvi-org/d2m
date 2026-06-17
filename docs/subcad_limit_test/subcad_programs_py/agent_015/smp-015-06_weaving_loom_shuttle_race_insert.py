# Requirement: SMP-015-06
# Source agent: 015
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_015_textile_craft_machine_hardware_single_metal_parts.json
# Part: Weaving Loom Shuttle Race Insert - single metal part
# Raw idea: Weaving Loom Shuttle Race Insert
# Status: draft_unexecuted
#
# Coverage notes:
# - Rectangular stock envelope 205 x 35 x 33 mm with mapped material steel_a36.
# - Two through mounting holes dia 8 mm at X=10/195, Y=17.
# - Central through obround slot 68 x 9 mm at X=102, Y=17.
# - Top relief pocket 51 x 18 x 1 mm deep, centered between mounting holes.
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
    Stock.rectangular(205, 35, 33, material="steel_a36")
    .drill(diameter=8, cx=-92.5, cy=-0.5, through=True)
    .drill(diameter=8, cx=92.5, cy=-0.5, through=True)
    .slot(length=68, width=9, cx=-0.5, cy=-0.5, through=True)
    .pocket(width=18, length=51, depth=1, cx=0, cy=0)
)
