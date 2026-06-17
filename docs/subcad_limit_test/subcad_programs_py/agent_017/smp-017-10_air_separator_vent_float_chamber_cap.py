# Requirement: SMP-017-10
# Source agent: 017
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_017_hvac_plumbing_hardware_single_metal_parts.json
# Part: Air Separator Vent Float Chamber Cap - single metal part
# Raw idea: Air Separator Vent Float Chamber Cap
# Status: draft_unexecuted
#
# Coverage notes:
# - Rectangular stock envelope 90 x 90 x 7 mm with mapped material steel_a36.
# - Two through mounting holes dia 8 mm at X=18/72, Y=45.
# - Central through obround slot 30 x 13 mm at X=45, Y=45.
# - Top relief pocket 25 x 30 x 3 mm deep, centered between mounting holes.
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
    Stock.rectangular(90, 90, 7, material="steel_a36")
    .drill(diameter=8, cx=-27, cy=0, through=True)
    .drill(diameter=8, cx=27, cy=0, through=True)
    .slot(length=30, width=13, cx=0, cy=0, through=True)
    .pocket(width=30, length=25, depth=3, cx=0, cy=0)
    .threaded_hole(diameter=8, depth=45, cx=37, cy=0)
)
