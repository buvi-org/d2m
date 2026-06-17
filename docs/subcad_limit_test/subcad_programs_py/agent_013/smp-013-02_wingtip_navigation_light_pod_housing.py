# Requirement: SMP-013-02
# Source agent: 013
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_013_aerospace_uav_hardware_single_metal_parts.json
# Part: Wingtip Navigation-Light Pod Housing - single metal part
# Raw idea: Wingtip Navigation-Light Pod Housing
# Status: draft_unexecuted
#
# Coverage notes:
# - Rectangular stock envelope 110 x 90 x 6 mm with mapped material aluminum_6061.
# - Two through mounting holes dia 9 mm at X=18/92, Y=45.
# - Central through obround slot 36 x 18 mm at X=55, Y=45.
# - Top relief pocket 27 x 30 x 3 mm deep, centered between mounting holes.
# - M8 tapped hole represented with threaded_hole near the right side/c. pocket region.
# - 1.0 mm top/outside chamfer represented with Stock.chamfer.
#
# Known gaps:
# - Side tapped hole axis parallel to Y is not represented exactly; program uses a top-face vertical threaded-hole proxy.
# - 0.5 mm chamfers on individual hole and slot mouths are not separately selectable in this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Coordinate conversion used Stock centered XY coordinates from the requirement lower-left origin.

from subcad import Stock

part = (
    Stock.rectangular(110, 90, 6, material="aluminum_6061")
    .drill(diameter=9, cx=-37, cy=0, through=True)
    .drill(diameter=9, cx=37, cy=0, through=True)
    .slot(length=36, width=18, cx=0, cy=0, through=True)
    .pocket(width=30, length=27, depth=3, cx=0, cy=0)
    .threaded_hole(diameter=8, depth=45, cx=47, cy=0)
)
