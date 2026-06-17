# Requirement: SMP-016-09
# Source agent: 016
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_016_packaging_machinery_single_metal_parts.json
# Part: Puck nest for unstable cosmetic bottle - single metal part
# Raw idea: Puck nest for unstable cosmetic bottle
# Status: draft_unexecuted
#
# Coverage notes:
# - Rectangular stock envelope 175 x 100 x 67 mm with mapped material stainless_316.
# - Two through mounting holes dia 6 mm at X=20/155, Y=50.
# - Central through obround slot 58 x 9 mm at X=87, Y=50.
# - Top relief pocket 43 x 33 x 28 mm deep, centered between mounting holes.
# - 1.0 mm top/outside chamfer represented with Stock.chamfer.
#
# Known gaps:
# - 0.5 mm chamfers on individual hole and slot mouths are not separately selectable in this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Coordinate conversion used Stock centered XY coordinates from the requirement lower-left origin.

from subcad import Stock

part = (
    Stock.rectangular(175, 100, 67, material="stainless_316")
    .drill(diameter=6, cx=-67.5, cy=0, through=True)
    .drill(diameter=6, cx=67.5, cy=0, through=True)
    .slot(length=58, width=9, cx=-0.5, cy=0, through=True)
    .pocket(width=33, length=43, depth=28, cx=0, cy=0)
)
