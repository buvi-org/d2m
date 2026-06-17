# Requirement: SMP-024-01
# Source agent: 024
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_024_rail_transit_service_tools_single_metal_parts.json
# Part: Rail Clip Tension Verification Gauge - single metal part
# Raw idea: Rail Clip Tension Verification Gauge
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 230 x 135 x 5 mm.
# - Two through mounting holes diameter 11 mm at X=27 and X=203, Y=67.
# - Central through obround slot 76 x 14 mm at X=115, Y=67.
# - Top relief pocket 57 x 45 x 1 mm centered between mounting holes.
# - Top outside chamfers represented with 1 mm chamfer operation.
# - Rear serration positions represented as 9 repeated edge grooves 5 mm deep.
# - Hook lip undercut region approximated with a 5 mm deep end groove.
#
# Known gaps:
# - 0.5 mm chamfers on individual hole and slot mouths are not separately selectable in this draft; only the general top chamfer is modeled.
# - Triangular serration tooth form is approximated with rectangular grooves because current fluent operations do not define triangular edge teeth.
# - Integral projecting hook lip cannot be grown beyond the rectangular stock envelope; only the undercut relief is represented.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated directly from frozen Stage 2 requirement text; not executed or visually reviewed yet.
# - Coordinate conversion uses SubCAD centered stock coordinates while requirement text uses lower-left-near datum coordinates.

from subcad import Stock

part = (
    Stock.rectangular(230, 135, 5, material="steel_a36")
    .drill(diameter=11, through=True, cx=-88, cy=-0.5, spot_drill=False)
    .drill(diameter=11, through=True, cx=88, cy=-0.5, spot_drill=False)
    .slot(length=76, width=14, through=True, cx=0, cy=-0.5)
    .pocket(length=57, width=45, depth=1, cx=0, cy=0, corner_radius=0)
    .groove(length=11.5, width=5, depth=0.6, cx=-102.222, cy=65)
    .groove(length=11.5, width=5, depth=0.6, cx=-76.667, cy=65)
    .groove(length=11.5, width=5, depth=0.6, cx=-51.111, cy=65)
    .groove(length=11.5, width=5, depth=0.6, cx=-25.556, cy=65)
    .groove(length=11.5, width=5, depth=0.6, cx=0, cy=65)
    .groove(length=11.5, width=5, depth=0.6, cx=25.556, cy=65)
    .groove(length=11.5, width=5, depth=0.6, cx=51.111, cy=65)
    .groove(length=11.5, width=5, depth=0.6, cx=76.667, cy=65)
    .groove(length=11.5, width=5, depth=0.6, cx=102.222, cy=65)
    .groove(length=16, width=135, depth=5, cx=-107, cy=0)
)
