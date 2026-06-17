# Requirement: SMP-015-09
# Source agent: 015
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_015_textile_craft_machine_hardware_single_metal_parts.json
# Part: Embroidery Thread Tension Disc Hub - single metal part
# Raw idea: Embroidery Thread Tension Disc Hub
# Status: draft_unexecuted
#
# Coverage notes:
# - Rectangular stock envelope 185 x 40 x 23 mm with mapped material steel_a36.
# - Two through mounting holes dia 7 mm at X=10/175, Y=20.
# - Central through obround slot 61 x 15 mm at X=92, Y=20.
# - Top relief pocket 46 x 18 x 11 mm deep, centered between mounting holes.
# - M8 tapped hole represented with threaded_hole near the right side/c. pocket region.
# - 5 triangular rear-edge serrations, each 5 mm deep, represented by repeated triangular profile_cutout operations.
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
    Stock.rectangular(185, 40, 23, material="steel_a36")
    .drill(diameter=7, cx=-82.5, cy=0, through=True)
    .drill(diameter=7, cx=82.5, cy=0, through=True)
    .slot(length=61, width=15, cx=-0.5, cy=0, through=True)
    .pocket(width=18, length=46, depth=11, cx=0, cy=0)
    .threaded_hole(diameter=8, depth=20, cx=84.5, cy=0)
)
