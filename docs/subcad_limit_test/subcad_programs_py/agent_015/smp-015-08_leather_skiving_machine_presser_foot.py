# Requirement: SMP-015-08
# Source agent: 015
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_015_textile_craft_machine_hardware_single_metal_parts.json
# Part: Leather Skiving Machine Presser Foot - single metal part
# Raw idea: Leather Skiving Machine Presser Foot
# Status: draft_unexecuted
#
# Coverage notes:
# - Rectangular stock envelope 170 x 95 x 69 mm with mapped material steel_1045.
# - Two through mounting holes dia 11 mm at X=19/151, Y=47.
# - Central through obround slot 56 x 8 mm at X=85, Y=47.
# - Top relief pocket 42 x 31 x 31 mm deep, centered between mounting holes.
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
    Stock.rectangular(170, 95, 69, material="steel_1045")
    .drill(diameter=11, cx=-66, cy=-0.5, through=True)
    .drill(diameter=11, cx=66, cy=-0.5, through=True)
    .slot(length=56, width=8, cx=0, cy=-0.5, through=True)
    .pocket(width=31, length=42, depth=31, cx=0, cy=0)
)
