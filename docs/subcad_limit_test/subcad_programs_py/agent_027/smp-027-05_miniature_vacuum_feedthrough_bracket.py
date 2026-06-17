# Requirement: SMP-027-05
# Source agent: 027
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_027_scientific_instrument_fixtures_single_metal_parts.json
# Part: Miniature Vacuum Feedthrough Bracket - single metal part
# Raw idea: Miniature Vacuum Feedthrough Bracket
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 125 x 100 x 5 mm.
# - Two through mounting holes diameter 5 mm at X=20 and X=105, Y=50.
# - Central through obround slot 41 x 12 mm at X=62, Y=50.
# - Top relief pocket 31 x 33 x 2 mm centered between mounting holes.
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
    Stock.rectangular(125, 100, 5, material="stainless_316")
    .drill(diameter=5, through=True, cx=-42.5, cy=0, spot_drill=False)
    .drill(diameter=5, through=True, cx=42.5, cy=0, spot_drill=False)
    .slot(length=41, width=12, through=True, cx=-0.5, cy=0)
    .pocket(length=31, width=33, depth=2, cx=0, cy=0, corner_radius=0)
)
