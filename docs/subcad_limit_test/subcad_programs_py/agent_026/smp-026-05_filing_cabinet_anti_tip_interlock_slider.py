# Requirement: SMP-026-05
# Source agent: 026
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_026_office_equipment_hardware_single_metal_parts.json
# Part: Filing Cabinet Anti-Tip Interlock Slider - single metal part
# Raw idea: Filing Cabinet Anti-Tip Interlock Slider
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 140 x 75 x 23 mm.
# - Two through mounting holes diameter 11 mm at X=15 and X=125, Y=37.
# - Central through obround slot 46 x 18 mm at X=70, Y=37.
# - Top relief pocket 35 x 25 x 3 mm centered between mounting holes.
# - Top outside chamfers represented with 1 mm chamfer operation.
# - Rear serration positions represented as 8 repeated edge grooves 4 mm deep.
#
# Known gaps:
# - 0.5 mm chamfers on individual hole and slot mouths are not separately selectable in this draft; only the general top chamfer is modeled.
# - Triangular serration tooth form is approximated with rectangular grooves because current fluent operations do not define triangular edge teeth.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated directly from frozen Stage 2 requirement text; not executed or visually reviewed yet.
# - Coordinate conversion uses SubCAD centered stock coordinates while requirement text uses lower-left-near datum coordinates.

from subcad import Stock

part = (
    Stock.rectangular(140, 75, 23, material="steel_a36")
    .drill(diameter=11, through=True, cx=-55, cy=-0.5, spot_drill=False)
    .drill(diameter=11, through=True, cx=55, cy=-0.5, spot_drill=False)
    .slot(length=46, width=18, through=True, cx=0, cy=-0.5)
    .pocket(length=35, width=25, depth=3, cx=0, cy=0, corner_radius=0)
    .groove(length=7.875, width=4, depth=2.76, cx=-61.25, cy=35.5)
    .groove(length=7.875, width=4, depth=2.76, cx=-43.75, cy=35.5)
    .groove(length=7.875, width=4, depth=2.76, cx=-26.25, cy=35.5)
    .groove(length=7.875, width=4, depth=2.76, cx=-8.75, cy=35.5)
    .groove(length=7.875, width=4, depth=2.76, cx=8.75, cy=35.5)
    .groove(length=7.875, width=4, depth=2.76, cx=26.25, cy=35.5)
    .groove(length=7.875, width=4, depth=2.76, cx=43.75, cy=35.5)
    .groove(length=7.875, width=4, depth=2.76, cx=61.25, cy=35.5)
)
