# Requirement: SMP-016-02
# Source agent: 016
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_016_packaging_machinery_single_metal_parts.json
# Part: Neck guide rail for trigger-spray bottle transfer - single metal part
# Raw idea: Neck guide rail for trigger-spray bottle transfer
# Status: draft_unexecuted
#
# Coverage notes:
# - Rectangular stock envelope 160 x 65 x 41 mm with mapped material steel_a36.
# - Two through mounting holes dia 10 mm at X=13/147, Y=32.
# - Central through obround slot 53 x 10 mm at X=80, Y=32.
# - Top relief pocket 40 x 21 x 5 mm deep, centered between mounting holes.
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
    Stock.rectangular(160, 65, 41, material="steel_a36")
    .drill(diameter=10, cx=-67, cy=-0.5, through=True)
    .drill(diameter=10, cx=67, cy=-0.5, through=True)
    .slot(length=53, width=10, cx=0, cy=-0.5, through=True)
    .pocket(width=21, length=40, depth=5, cx=0, cy=0)
)
