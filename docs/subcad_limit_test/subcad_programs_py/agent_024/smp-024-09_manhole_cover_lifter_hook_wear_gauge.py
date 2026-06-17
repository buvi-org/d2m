# Requirement: SMP-024-09
# Source agent: 024
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_024_rail_transit_service_tools_single_metal_parts.json
# Part: Manhole Cover Lifter Hook Wear Gauge - single metal part
# Raw idea: Manhole Cover Lifter Hook Wear Gauge
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 115 x 85 x 9 mm.
# - Two through mounting holes diameter 5 mm at X=17 and X=98, Y=42.
# - Central through obround slot 38 x 8 mm at X=57, Y=42.
# - Top relief pocket 28 x 28 x 3 mm centered between mounting holes.
# - Top outside chamfers represented with 1 mm chamfer operation.
# - Rear serration positions represented as 10 repeated edge grooves 5 mm deep.
# - Hook lip undercut region approximated with a 2 mm deep end groove.
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
    Stock.rectangular(115, 85, 9, material="steel_a36")
    .drill(diameter=5, through=True, cx=-40.5, cy=-0.5, spot_drill=False)
    .drill(diameter=5, through=True, cx=40.5, cy=-0.5, spot_drill=False)
    .slot(length=38, width=8, through=True, cx=-0.5, cy=-0.5)
    .pocket(length=28, width=28, depth=3, cx=0, cy=0, corner_radius=0)
    .groove(length=5.175, width=5, depth=1.08, cx=-51.75, cy=40)
    .groove(length=5.175, width=5, depth=1.08, cx=-40.25, cy=40)
    .groove(length=5.175, width=5, depth=1.08, cx=-28.75, cy=40)
    .groove(length=5.175, width=5, depth=1.08, cx=-17.25, cy=40)
    .groove(length=5.175, width=5, depth=1.08, cx=-5.75, cy=40)
    .groove(length=5.175, width=5, depth=1.08, cx=5.75, cy=40)
    .groove(length=5.175, width=5, depth=1.08, cx=17.25, cy=40)
    .groove(length=5.175, width=5, depth=1.08, cx=28.75, cy=40)
    .groove(length=5.175, width=5, depth=1.08, cx=40.25, cy=40)
    .groove(length=5.175, width=5, depth=1.08, cx=51.75, cy=40)
    .groove(length=9, width=85, depth=2, cx=-53, cy=0)
)
