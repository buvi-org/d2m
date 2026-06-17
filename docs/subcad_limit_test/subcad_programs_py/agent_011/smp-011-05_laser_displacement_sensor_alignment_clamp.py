# Requirement: SMP-011-05
# Source agent: 011
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_011_industrial_measurement_fixtures_single_metal_parts.json
# Part: Laser Displacement Sensor Alignment Clamp - single metal part
# Raw idea: Laser Displacement Sensor Alignment Clamp
# Status: draft_unexecuted
#
# Coverage notes:
# - Rectangular stock envelope 220 x 40 x 27 mm with mapped material steel_1045.
# - Two through mounting holes dia 7 mm at X=10/210, Y=20.
# - Central through obround slot 73 x 8 mm at X=110, Y=20.
# - Top relief pocket 55 x 18 x 9 mm deep, centered between mounting holes.
# - M6 tapped hole represented with threaded_hole near the right side/c. pocket region.
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
    Stock.rectangular(220, 40, 27, material="steel_1045")
    .drill(diameter=7, cx=-100, cy=0, through=True)
    .drill(diameter=7, cx=100, cy=0, through=True)
    .slot(length=73, width=8, cx=0, cy=0, through=True)
    .pocket(width=18, length=55, depth=9, cx=0, cy=0)
    .threaded_hole(diameter=6, depth=20, cx=104, cy=0)
)
