# Requirement: SMP-015-07
# Source agent: 015
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_015_textile_craft_machine_hardware_single_metal_parts.json
# Part: Buttonhole Attachment Template Cam - single metal part
# Raw idea: Buttonhole Attachment Template Cam
# Status: draft_unexecuted
#
# Coverage notes:
# - Rectangular stock envelope 90 x 45 x 8 mm with mapped material steel_a36.
# - Two through mounting holes dia 8 mm at X=10/80, Y=22.
# - Central through obround slot 30 x 18 mm at X=45, Y=22.
# - Top relief pocket 25 x 18 x 1 mm deep, centered between mounting holes.
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
    Stock.rectangular(90, 45, 8, material="steel_a36")
    .drill(diameter=8, cx=-35, cy=-0.5, through=True)
    .drill(diameter=8, cx=35, cy=-0.5, through=True)
    .slot(length=30, width=18, cx=0, cy=-0.5, through=True)
    .pocket(width=18, length=25, depth=1, cx=0, cy=0)
)
