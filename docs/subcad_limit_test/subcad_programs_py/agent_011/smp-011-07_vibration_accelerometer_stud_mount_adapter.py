# Requirement: SMP-011-07
# Source agent: 011
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_011_industrial_measurement_fixtures_single_metal_parts.json
# Part: Vibration Accelerometer Stud-Mount Adapter - single metal part
# Raw idea: Vibration Accelerometer Stud-Mount Adapter
# Status: draft_unexecuted
#
# Coverage notes:
# - Rectangular stock envelope 180 x 105 x 53 mm with mapped material steel_a36.
# - Two through mounting holes dia 7 mm at X=21/159, Y=52.
# - Central through obround slot 60 x 16 mm at X=90, Y=52.
# - Top relief pocket 45 x 35 x 10 mm deep, centered between mounting holes.
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
    Stock.rectangular(180, 105, 53, material="steel_a36")
    .drill(diameter=7, cx=-69, cy=-0.5, through=True)
    .drill(diameter=7, cx=69, cy=-0.5, through=True)
    .slot(length=60, width=16, cx=0, cy=-0.5, through=True)
    .pocket(width=35, length=45, depth=10, cx=0, cy=0)
    .threaded_hole(diameter=7, depth=52.5, cx=83, cy=0)
)
