# Requirement: SMP-014-08
# Source agent: 014
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_014_musical_instrument_hardware_single_metal_parts.json
# Part: Expression Pedal Rocker Pivot Block - single metal part
# Raw idea: Expression Pedal Rocker Pivot Block
# Status: draft_unexecuted
#
# Coverage notes:
# - Rectangular stock envelope 170 x 105 x 64 mm with mapped material steel_1045.
# - Two through mounting holes dia 8 mm at X=21/149, Y=52.
# - Central through obround slot 56 x 9 mm at X=85, Y=52.
# - Top relief pocket 42 x 35 x 23 mm deep, centered between mounting holes.
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
    Stock.rectangular(170, 105, 64, material="steel_1045")
    .drill(diameter=8, cx=-64, cy=-0.5, through=True)
    .drill(diameter=8, cx=64, cy=-0.5, through=True)
    .slot(length=56, width=9, cx=0, cy=-0.5, through=True)
    .pocket(width=35, length=42, depth=23, cx=0, cy=0)
)
