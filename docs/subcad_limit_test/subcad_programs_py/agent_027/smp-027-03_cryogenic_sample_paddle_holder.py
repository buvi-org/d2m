# Requirement: SMP-027-03
# Source agent: 027
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_027_scientific_instrument_fixtures_single_metal_parts.json
# Part: Cryogenic Sample Paddle Holder - single metal part
# Raw idea: Cryogenic Sample Paddle Holder
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 140 x 120 x 5 mm.
# - Two through mounting holes diameter 13 mm at X=24 and X=116, Y=60.
# - Central through obround slot 46 x 13 mm at X=70, Y=60.
# - Top relief pocket 35 x 40 x 1 mm centered between mounting holes.
# - Top outside chamfers represented with 1 mm chamfer operation.
# - Angled reference region over the last 28 mm represented as a sloped top-face cut at the right end.
#
# Known gaps:
# - 0.5 mm chamfers on individual hole and slot mouths are not separately selectable in this draft; only the general top chamfer is modeled.
# - Exact external face angle of 24 degrees is approximated by a sloped pocket depth transition, not a full side-face reprofile.
# - Side tapped hole M9 with axis parallel to Y is not modeled; current threaded_hole/tap operations are top-face axial in this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated directly from frozen Stage 2 requirement text; not executed or visually reviewed yet.
# - Coordinate conversion uses SubCAD centered stock coordinates while requirement text uses lower-left-near datum coordinates.

from subcad import Stock

part = (
    Stock.rectangular(140, 120, 5, material="steel_a36")
    .drill(diameter=13, through=True, cx=-46, cy=0, spot_drill=False)
    .drill(diameter=13, through=True, cx=46, cy=0, spot_drill=False)
    .slot(length=46, width=13, through=True, cx=0, cy=0)
    .pocket(length=35, width=40, depth=1, cx=0, cy=0, corner_radius=0)
    .slope_cut(width=120, length=28, start_depth=0.5, end_depth=4.25, cx=56, cy=0, slope_axis="X")
)
