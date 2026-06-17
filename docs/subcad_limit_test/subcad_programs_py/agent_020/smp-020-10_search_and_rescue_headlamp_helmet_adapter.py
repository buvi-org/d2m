# Requirement: SMP-020-10
# Source agent: 020
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_020_rescue_service_hardware_single_metal_parts.json
# Part: Search-and-Rescue Headlamp Helmet Adapter - single metal part
# Raw idea: Search-and-Rescue Headlamp Helmet Adapter
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 160 x 80 x 3 mm.
# - Two through mounting holes diameter 12 mm at X=16 and X=144, Y=40.
# - Central through obround slot 53 x 17 mm at X=80, Y=40.
# - Top relief pocket 40 x 26 x 1 mm centered between mounting holes.
# - Top outside chamfers represented with 1 mm chamfer operation.
# - Hook lip undercut region approximated with a 2 mm deep end groove.
#
# Known gaps:
# - 0.5 mm chamfers on individual hole and slot mouths are not separately selectable in this draft; only the general top chamfer is modeled.
# - Integral projecting hook lip cannot be grown beyond the rectangular stock envelope; only the undercut relief is represented.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated directly from frozen Stage 2 requirement text; not executed or visually reviewed yet.
# - Coordinate conversion uses SubCAD centered stock coordinates while requirement text uses lower-left-near datum coordinates.

from subcad import Stock

part = (
    Stock.rectangular(160, 80, 3, material="steel_a36")
    .drill(diameter=12, through=True, cx=-64, cy=0, spot_drill=False)
    .drill(diameter=12, through=True, cx=64, cy=0, spot_drill=False)
    .slot(length=53, width=17, through=True, cx=0, cy=0)
    .pocket(length=40, width=26, depth=1, cx=0, cy=0, corner_radius=0)
    .groove(length=7, width=80, depth=2, cx=-76.5, cy=0)
)
