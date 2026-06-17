# Requirement: SMP-015-01
# Source agent: 015
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_015_textile_craft_machine_hardware_single_metal_parts.json
# Part: Walking-Foot Sewing Machine Feed Dog - single metal part
# Raw idea: Walking-Foot Sewing Machine Feed Dog
# Status: draft_unexecuted
#
# Coverage notes:
# - Rectangular stock envelope 200 x 70 x 70 mm with mapped material steel_a36.
# - Two through mounting holes dia 11 mm at X=14/186, Y=35.
# - Central through obround slot 66 x 17 mm at X=100, Y=35.
# - Top relief pocket 50 x 23 x 15 mm deep, centered between mounting holes.
# - 7 triangular rear-edge serrations, each 4 mm deep, represented by repeated triangular profile_cutout operations.
# - 1.0 mm top/outside chamfer represented with Stock.chamfer.
#
# Known gaps:
# - Serration profile_cutout placement needs execution review because the triangles lie on the rear edge boundary.
# - 0.5 mm chamfers on individual hole and slot mouths are not separately selectable in this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
# - Executable draft omits boundary triangular profile_cutout serration proxies because they erased the full solid in OCC; serrations remain a requirement gap for later targeted support.
#
# Review notes:
# - Coordinate conversion used Stock centered XY coordinates from the requirement lower-left origin.

from subcad import Stock

part = (
    Stock.rectangular(200, 70, 70, material="steel_a36")
    .drill(diameter=11, cx=-86, cy=0, through=True)
    .drill(diameter=11, cx=86, cy=0, through=True)
    .slot(length=66, width=17, cx=0, cy=0, through=True)
    .pocket(width=23, length=50, depth=15, cx=0, cy=0)
)
