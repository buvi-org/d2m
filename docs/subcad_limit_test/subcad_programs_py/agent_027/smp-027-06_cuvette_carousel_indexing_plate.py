# Requirement: SMP-027-06
# Source agent: 027
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_027_scientific_instrument_fixtures_single_metal_parts.json
# Part: Cuvette Carousel Indexing Plate - single metal part
# Raw idea: Cuvette Carousel Indexing Plate
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 210 x 80 x 7 mm.
# - Two through mounting holes diameter 8 mm at X=16 and X=194, Y=40.
# - Central through obround slot 70 x 14 mm at X=105, Y=40.
# - Top relief pocket 52 x 26 x 2 mm centered between mounting holes.
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
    Stock.rectangular(210, 80, 7, material="steel_a36")
    .drill(diameter=8, through=True, cx=-89, cy=0, spot_drill=False)
    .drill(diameter=8, through=True, cx=89, cy=0, spot_drill=False)
    .slot(length=70, width=14, through=True, cx=0, cy=0)
    .pocket(length=52, width=26, depth=2, cx=0, cy=0, corner_radius=0)
)
