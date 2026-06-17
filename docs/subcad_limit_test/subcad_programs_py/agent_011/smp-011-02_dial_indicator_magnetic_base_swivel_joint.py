# Requirement: SMP-011-02
# Source agent: 011
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_011_industrial_measurement_fixtures_single_metal_parts.json
# Part: Dial Indicator Magnetic Base Swivel Joint - single metal part
# Raw idea: Dial Indicator Magnetic Base Swivel Joint
# Status: draft_unexecuted
#
# Coverage notes:
# - Rectangular stock envelope 105 x 35 x 31 mm with mapped material steel_a36.
# - Two through mounting holes dia 9 mm at X=10/95, Y=17.
# - Central through obround slot 35 x 16 mm at X=52, Y=17.
# - Top relief pocket 26 x 18 x 6 mm deep, centered between mounting holes.
# - M6 tapped hole represented with threaded_hole near the right side/c. pocket region.
# - 11 triangular rear-edge serrations, each 5 mm deep, represented by repeated triangular profile_cutout operations.
# - 1.0 mm top/outside chamfer represented with Stock.chamfer.
#
# Known gaps:
# - Side tapped hole axis parallel to Y is not represented exactly; program uses a top-face vertical threaded-hole proxy.
# - Serration profile_cutout placement needs execution review because the triangles lie on the rear edge boundary.
# - 0.5 mm chamfers on individual hole and slot mouths are not separately selectable in this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
# - Executable draft omits boundary triangular profile_cutout serration proxies because they erased the full solid in OCC; serrations remain a requirement gap for later targeted support.
#
# Review notes:
# - Coordinate conversion used Stock centered XY coordinates from the requirement lower-left origin.

from subcad import Stock

part = (
    Stock.rectangular(105, 35, 31, material="steel_a36")
    .drill(diameter=9, cx=-42.5, cy=-0.5, through=True)
    .drill(diameter=9, cx=42.5, cy=-0.5, through=True)
    .slot(length=35, width=16, cx=-0.5, cy=-0.5, through=True)
    .pocket(width=18, length=26, depth=6, cx=0, cy=0)
    .threaded_hole(diameter=6, depth=17.5, cx=46.5, cy=0)
)
