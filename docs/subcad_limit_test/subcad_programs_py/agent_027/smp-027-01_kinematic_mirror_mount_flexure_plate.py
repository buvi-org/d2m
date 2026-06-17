# Requirement: SMP-027-01
# Source agent: 027
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_027_scientific_instrument_fixtures_single_metal_parts.json
# Part: Kinematic Mirror Mount Flexure Plate - single metal part
# Raw idea: Kinematic Mirror Mount Flexure Plate
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 170 x 70 x 6 mm.
# - Two through mounting holes diameter 13 mm at X=14 and X=156, Y=35.
# - Central through obround slot 56 x 17 mm at X=85, Y=35.
# - Top relief pocket 42 x 23 x 3 mm centered between mounting holes.
# - Top outside chamfers represented with 1 mm chamfer operation.
# - Central counterbored seat diameter 25 mm x 2 mm deep around the center feature.
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
    Stock.rectangular(170, 70, 6, material="steel_a36")
    .drill(diameter=13, through=True, cx=-71, cy=0, spot_drill=False)
    .drill(diameter=13, through=True, cx=71, cy=0, spot_drill=False)
    .slot(length=56, width=17, through=True, cx=0, cy=0)
    .pocket(length=42, width=23, depth=3, cx=0, cy=0, corner_radius=0)
    .circular_pocket(diameter=25, depth=2, cx=0, cy=0)
)
