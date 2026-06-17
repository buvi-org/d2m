# Requirement: SMP-015-03
# Source agent: 015
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_015_textile_craft_machine_hardware_single_metal_parts.json
# Part: Embroidery Hoop Quick-Lock Cam Clamp - single metal part
# Raw idea: Embroidery Hoop Quick-Lock Cam Clamp
# Status: draft_unexecuted
#
# Coverage notes:
# - Rectangular stock envelope 180 x 85 x 19 mm with mapped material steel_1045.
# - Two through mounting holes dia 7 mm at X=17/163, Y=42.
# - Central through obround slot 60 x 14 mm at X=90, Y=42.
# - Top relief pocket 45 x 28 x 2 mm deep, centered between mounting holes.
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
    Stock.rectangular(180, 85, 19, material="steel_1045")
    .drill(diameter=7, cx=-73, cy=-0.5, through=True)
    .drill(diameter=7, cx=73, cy=-0.5, through=True)
    .slot(length=60, width=14, cx=0, cy=-0.5, through=True)
    .pocket(width=28, length=45, depth=2, cx=0, cy=0)
)
