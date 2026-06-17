# Requirement: SMP-013-06
# Source agent: 013
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_013_aerospace_uav_hardware_single_metal_parts.json
# Part: UAV Payload Bay Blind-Mate Connector Carrier - single metal part
# Raw idea: UAV Payload Bay Blind-Mate Connector Carrier
# Status: draft_unexecuted
#
# Coverage notes:
# - Rectangular stock envelope 115 x 90 x 41 mm with mapped material aluminum_6061.
# - Two through mounting holes dia 7 mm at X=18/97, Y=45.
# - Central through obround slot 38 x 9 mm at X=57, Y=45.
# - Top relief pocket 28 x 30 x 3 mm deep, centered between mounting holes.
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
    Stock.rectangular(115, 90, 41, material="aluminum_6061")
    .drill(diameter=7, cx=-39.5, cy=0, through=True)
    .drill(diameter=7, cx=39.5, cy=0, through=True)
    .slot(length=38, width=9, cx=-0.5, cy=0, through=True)
    .pocket(width=30, length=28, depth=3, cx=0, cy=0)
)
