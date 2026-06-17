# Requirement: SMP-027-09
# Source agent: 027
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_027_scientific_instrument_fixtures_single_metal_parts.json
# Part: Precision Lab Jack Crosshead Block - single metal part
# Raw idea: Precision Lab Jack Crosshead Block
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 120 x 90 x 68 mm.
# - Two through mounting holes diameter 8 mm at X=18 and X=102, Y=45.
# - Central through obround slot 40 x 8 mm at X=60, Y=45.
# - Top relief pocket 30 x 30 x 23 mm centered between mounting holes.
# - Top outside chamfers represented with 1 mm chamfer operation.
#
# Known gaps:
# - 0.5 mm chamfers on individual hole and slot mouths are not separately selectable in this draft; only the general top chamfer is modeled.
# - Side tapped hole M4 with axis parallel to Y is not modeled; current threaded_hole/tap operations are top-face axial in this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated directly from frozen Stage 2 requirement text; not executed or visually reviewed yet.
# - Coordinate conversion uses SubCAD centered stock coordinates while requirement text uses lower-left-near datum coordinates.

from subcad import Stock

part = (
    Stock.rectangular(120, 90, 68, material="stainless_316")
    .drill(diameter=8, through=True, cx=-42, cy=0, spot_drill=False)
    .drill(diameter=8, through=True, cx=42, cy=0, spot_drill=False)
    .slot(length=40, width=8, through=True, cx=0, cy=0)
    .pocket(length=30, width=30, depth=23, cx=0, cy=0, corner_radius=0)
)
