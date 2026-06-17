# Requirement: SMP-027-07
# Source agent: 027
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_027_scientific_instrument_fixtures_single_metal_parts.json
# Part: Adjustable Slit Jaw Carrier - single metal part
# Raw idea: Adjustable Slit Jaw Carrier
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 100 x 55 x 20 mm.
# - Two through mounting holes diameter 7 mm at X=11 and X=89, Y=27.
# - Central through obround slot 33 x 11 mm at X=50, Y=27.
# - Top relief pocket 25 x 18 x 5 mm centered between mounting holes.
# - Top outside chamfers represented with 1 mm chamfer operation.
#
# Known gaps:
# - 0.5 mm chamfers on individual hole and slot mouths are not separately selectable in this draft; only the general top chamfer is modeled.
# - Side tapped hole M8 with axis parallel to Y is not modeled; current threaded_hole/tap operations are top-face axial in this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated directly from frozen Stage 2 requirement text; not executed or visually reviewed yet.
# - Coordinate conversion uses SubCAD centered stock coordinates while requirement text uses lower-left-near datum coordinates.

from subcad import Stock

part = (
    Stock.rectangular(100, 55, 20, material="aluminum_6061")
    .drill(diameter=7, through=True, cx=-39, cy=-0.5, spot_drill=False)
    .drill(diameter=7, through=True, cx=39, cy=-0.5, spot_drill=False)
    .slot(length=33, width=11, through=True, cx=0, cy=-0.5)
    .pocket(length=25, width=18, depth=5, cx=0, cy=0, corner_radius=0)
)
