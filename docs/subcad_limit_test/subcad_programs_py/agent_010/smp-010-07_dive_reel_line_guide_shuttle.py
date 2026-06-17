# Requirement: SMP-010-07
# Source agent: 010
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_010_outdoor_marine_field_gear_single_metal_parts.json
# Part: Dive Reel Line Guide Shuttle - single metal part
# Raw idea: Dive Reel Line Guide Shuttle
# Status: draft_unexecuted
#
# Coverage notes:
# - Rectangular stock envelope 75 x 60 x 44 mm with mapped material steel_a36.
# - Two through mounting holes dia 9 mm at X=12/63, Y=30.
# - Central through obround slot 30 x 10 mm at X=37, Y=30.
# - Top relief pocket 25 x 20 x 16 mm deep, centered between mounting holes.
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
    Stock.rectangular(75, 60, 44, material="steel_a36")
    .drill(diameter=9, cx=-25.5, cy=0, through=True)
    .drill(diameter=9, cx=25.5, cy=0, through=True)
    .slot(length=30, width=10, cx=-0.5, cy=0, through=True)
    .pocket(width=20, length=25, depth=16, cx=0, cy=0)
)
