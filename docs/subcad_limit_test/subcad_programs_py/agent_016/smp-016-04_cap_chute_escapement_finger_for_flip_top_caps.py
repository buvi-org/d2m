# Requirement: SMP-016-04
# Source agent: 016
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_016_packaging_machinery_single_metal_parts.json
# Part: Cap chute escapement finger for flip-top caps - single metal part
# Raw idea: Cap chute escapement finger for flip-top caps
# Status: draft_unexecuted
#
# Coverage notes:
# - Rectangular stock envelope 220 x 85 x 58 mm with mapped material steel_a36.
# - Two through mounting holes dia 9 mm at X=17/203, Y=42.
# - Central through obround slot 73 x 10 mm at X=110, Y=42.
# - Top relief pocket 55 x 28 x 20 mm deep, centered between mounting holes.
# - 5 triangular rear-edge serrations, each 2 mm deep, represented by repeated triangular profile_cutout operations.
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
    Stock.rectangular(220, 85, 58, material="steel_a36")
    .drill(diameter=9, cx=-93, cy=-0.5, through=True)
    .drill(diameter=9, cx=93, cy=-0.5, through=True)
    .slot(length=73, width=10, cx=0, cy=-0.5, through=True)
    .pocket(width=28, length=55, depth=20, cx=0, cy=0)
)
