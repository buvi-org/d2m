# Requirement: SMP-014-02
# Source agent: 014
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_014_musical_instrument_hardware_single_metal_parts.json
# Part: Kick Drum Pedal Cam Hub - single metal part
# Raw idea: Kick Drum Pedal Cam Hub
# Status: draft_unexecuted
#
# Coverage notes:
# - Rectangular stock envelope 105 x 90 x 63 mm with mapped material steel_a36.
# - Two through mounting holes dia 9 mm at X=18/87, Y=45.
# - Central through obround slot 35 x 8 mm at X=52, Y=45.
# - Top relief pocket 26 x 30 x 8 mm deep, centered between mounting holes.
# - M7 tapped hole represented with threaded_hole near the right side/c. pocket region.
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
    Stock.rectangular(105, 90, 63, material="steel_a36")
    .drill(diameter=9, cx=-34.5, cy=0, through=True)
    .drill(diameter=9, cx=34.5, cy=0, through=True)
    .slot(length=35, width=8, cx=-0.5, cy=0, through=True)
    .pocket(width=30, length=26, depth=8, cx=0, cy=0)
    .threaded_hole(diameter=7, depth=45, cx=45.5, cy=0)
)
