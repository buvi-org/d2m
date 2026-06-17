# Requirement: SMP-012-10
# Source agent: 012
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_012_agriculture_garden_hardware_single_metal_parts.json
# Part: Rain Barrel Spigot Bulkhead Nut - single metal part
# Raw idea: Rain Barrel Spigot Bulkhead Nut
# Status: draft_unexecuted
#
# Coverage notes:
# - Rectangular stock envelope 205 x 60 x 57 mm with mapped material steel_1045.
# - Two through mounting holes dia 12 mm at X=12/193, Y=30.
# - Central through obround slot 68 x 17 mm at X=102, Y=30.
# - Top relief pocket 51 x 20 x 4 mm deep, centered between mounting holes.
# - M10 tapped hole represented with threaded_hole near the right side/c. pocket region.
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
    Stock.rectangular(205, 60, 57, material="steel_1045")
    .drill(diameter=12, cx=-90.5, cy=0, through=True)
    .drill(diameter=12, cx=90.5, cy=0, through=True)
    .slot(length=68, width=17, cx=-0.5, cy=0, through=True)
    .pocket(width=20, length=51, depth=4, cx=0, cy=0)
    .threaded_hole(diameter=10, depth=30, cx=92.5, cy=0)
)
