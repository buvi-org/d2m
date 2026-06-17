# Requirement: SMP-010-04
# Source agent: 010
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_010_outdoor_marine_field_gear_single_metal_parts.json
# Part: Marine Cleat Quick-Release Fairlead - single metal part
# Raw idea: Marine Cleat Quick-Release Fairlead
# Status: draft_unexecuted
#
# Coverage notes:
# - Rectangular stock envelope 120 x 90 x 46 mm with mapped material stainless_316.
# - Two through mounting holes dia 13 mm at X=18/102, Y=45.
# - Central through obround slot 40 x 7 mm at X=60, Y=45.
# - Top relief pocket 30 x 30 x 2 mm deep, centered between mounting holes.
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
    Stock.rectangular(120, 90, 46, material="stainless_316")
    .drill(diameter=13, cx=-42, cy=0, through=True)
    .drill(diameter=13, cx=42, cy=0, through=True)
    .slot(length=40, width=7, cx=0, cy=0, through=True)
    .pocket(width=30, length=30, depth=2, cx=0, cy=0)
)
