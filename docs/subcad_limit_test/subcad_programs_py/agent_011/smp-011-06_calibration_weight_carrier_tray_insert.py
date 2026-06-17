# Requirement: SMP-011-06
# Source agent: 011
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_011_industrial_measurement_fixtures_single_metal_parts.json
# Part: Calibration Weight Carrier Tray Insert - single metal part
# Raw idea: Calibration Weight Carrier Tray Insert
# Status: draft_unexecuted
#
# Coverage notes:
# - Rectangular stock envelope 125 x 60 x 7 mm with mapped material stainless_316.
# - Two through mounting holes dia 10 mm at X=12/113, Y=30.
# - Central through obround slot 41 x 8 mm at X=62, Y=30.
# - Top relief pocket 31 x 20 x 1 mm deep, centered between mounting holes.
# - 7 triangular rear-edge serrations, each 3 mm deep, represented by repeated triangular profile_cutout operations.
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
    Stock.rectangular(125, 60, 7, material="stainless_316")
    .drill(diameter=10, cx=-50.5, cy=0, through=True)
    .drill(diameter=10, cx=50.5, cy=0, through=True)
    .slot(length=41, width=8, cx=-0.5, cy=0, through=True)
    .pocket(width=20, length=31, depth=1, cx=0, cy=0)
)
