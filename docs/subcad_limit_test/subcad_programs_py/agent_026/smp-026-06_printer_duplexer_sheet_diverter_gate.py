# Requirement: SMP-026-06
# Source agent: 026
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_026_office_equipment_hardware_single_metal_parts.json
# Part: Printer Duplexer Sheet Diverter Gate - single metal part
# Raw idea: Printer Duplexer Sheet Diverter Gate
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 115 x 80 x 5 mm.
# - Two through mounting holes diameter 10 mm at X=16 and X=99, Y=40.
# - Central through obround slot 38 x 17 mm at X=57, Y=40.
# - Top relief pocket 28 x 26 x 1 mm centered between mounting holes.
# - Top outside chamfers represented with 1 mm chamfer operation.
#
# Known gaps:
# - 0.5 mm chamfers on individual hole and slot mouths are not separately selectable in this draft; only the general top chamfer is modeled.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated directly from frozen Stage 2 requirement text; not executed or visually reviewed yet.
# - Coordinate conversion uses SubCAD centered stock coordinates while requirement text uses lower-left-near datum coordinates.

from subcad import Stock

part = (
    Stock.rectangular(115, 80, 5, material="steel_a36")
    .drill(diameter=10, through=True, cx=-41.5, cy=0, spot_drill=False)
    .drill(diameter=10, through=True, cx=41.5, cy=0, spot_drill=False)
    .slot(length=38, width=17, through=True, cx=-0.5, cy=0)
    .pocket(length=28, width=26, depth=1, cx=0, cy=0, corner_radius=0)
)
