# Requirement: SMP-013-07
# Source agent: 013
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_013_aerospace_uav_hardware_single_metal_parts.json
# Part: RC Aircraft Retractable Landing-Gear Trunnion - single metal part
# Raw idea: RC Aircraft Retractable Landing-Gear Trunnion
# Status: draft_unexecuted
#
# Coverage notes:
# - Rectangular stock envelope 180 x 100 x 64 mm with mapped material aluminum_6061.
# - Two through mounting holes dia 8 mm at X=20/160, Y=50.
# - Central through obround slot 60 x 8 mm at X=90, Y=50.
# - Top relief pocket 45 x 33 x 11 mm deep, centered between mounting holes.
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
    Stock.rectangular(180, 100, 64, material="aluminum_6061")
    .drill(diameter=8, cx=-70, cy=0, through=True)
    .drill(diameter=8, cx=70, cy=0, through=True)
    .slot(length=60, width=8, cx=0, cy=0, through=True)
    .pocket(width=33, length=45, depth=11, cx=0, cy=0)
)
