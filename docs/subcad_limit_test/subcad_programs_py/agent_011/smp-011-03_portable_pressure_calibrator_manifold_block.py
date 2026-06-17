# Requirement: SMP-011-03
# Source agent: 011
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_011_industrial_measurement_fixtures_single_metal_parts.json
# Part: Portable Pressure Calibrator Manifold Block - single metal part
# Raw idea: Portable Pressure Calibrator Manifold Block
# Status: draft_unexecuted
#
# Coverage notes:
# - Rectangular stock envelope 220 x 115 x 23 mm with mapped material steel_1045.
# - Two through mounting holes dia 7 mm at X=23/197, Y=57.
# - Central through obround slot 73 x 18 mm at X=110, Y=57.
# - Top relief pocket 55 x 38 x 3 mm deep, centered between mounting holes.
# - Central counterbored seat diameter 26 mm x 6 mm deep around the center feature.
# - M7 tapped hole represented with threaded_hole near the right side/c. pocket region.
# - 1.0 mm top/outside chamfer represented with Stock.chamfer.
#
# Known gaps:
# - Counterbored seat is modeled as a centered counterbore proxy over/near the obround slot, not a true counterbore blended around an obround opening.
# - Side tapped hole axis parallel to Y is not represented exactly; program uses a top-face vertical threaded-hole proxy.
# - 0.5 mm chamfers on individual hole and slot mouths are not separately selectable in this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Coordinate conversion used Stock centered XY coordinates from the requirement lower-left origin.

from subcad import Stock

part = (
    Stock.rectangular(220, 115, 23, material="steel_1045")
    .drill(diameter=7, cx=-87, cy=-0.5, through=True)
    .drill(diameter=7, cx=87, cy=-0.5, through=True)
    .slot(length=73, width=18, cx=0, cy=-0.5, through=True)
    .pocket(width=38, length=55, depth=3, cx=0, cy=0)
    .counterbore(hole_diameter=18, counterbore_diameter=26, counterbore_depth=6, cx=0, cy=0)
    .threaded_hole(diameter=7, depth=57.5, cx=103, cy=0)
)
