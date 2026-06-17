# Requirement: SMP-021-08
# Source agent: 021
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_021_education_lab_apparatus_single_metal_parts.json
# Part: Resonance Beam Clamp Support - single metal part
# Raw idea: Resonance Beam Clamp Support
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 115 x 95 x 58 mm.
# - Two through mounting holes diameter 10 mm at X=19 and X=96, Y=47.
# - Central through obround slot 38 x 8 mm at X=57, Y=47.
# - Top relief pocket 28 x 31 x 8 mm centered between mounting holes.
# - Top outside chamfers represented with 1 mm chamfer operation.
# - Rear serration positions represented as 10 repeated edge grooves 5 mm deep.
#
# Known gaps:
# - 0.5 mm chamfers on individual hole and slot mouths are not separately selectable in this draft; only the general top chamfer is modeled.
# - Triangular serration tooth form is approximated with rectangular grooves because current fluent operations do not define triangular edge teeth.
# - Side tapped hole M4 with axis parallel to Y is not modeled; current threaded_hole/tap operations are top-face axial in this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated directly from frozen Stage 2 requirement text; not executed or visually reviewed yet.
# - Coordinate conversion uses SubCAD centered stock coordinates while requirement text uses lower-left-near datum coordinates.

from subcad import Stock

part = (
    Stock.rectangular(115, 95, 58, material="steel_1045")
    .drill(diameter=10, through=True, cx=-38.5, cy=-0.5, spot_drill=False)
    .drill(diameter=10, through=True, cx=38.5, cy=-0.5, spot_drill=False)
    .slot(length=38, width=8, through=True, cx=-0.5, cy=-0.5)
    .pocket(length=28, width=31, depth=8, cx=0, cy=0, corner_radius=0)
    .groove(length=5.175, width=5, depth=5, cx=-51.75, cy=45)
    .groove(length=5.175, width=5, depth=5, cx=-40.25, cy=45)
    .groove(length=5.175, width=5, depth=5, cx=-28.75, cy=45)
    .groove(length=5.175, width=5, depth=5, cx=-17.25, cy=45)
    .groove(length=5.175, width=5, depth=5, cx=-5.75, cy=45)
    .groove(length=5.175, width=5, depth=5, cx=5.75, cy=45)
    .groove(length=5.175, width=5, depth=5, cx=17.25, cy=45)
    .groove(length=5.175, width=5, depth=5, cx=28.75, cy=45)
    .groove(length=5.175, width=5, depth=5, cx=40.25, cy=45)
    .groove(length=5.175, width=5, depth=5, cx=51.75, cy=45)
)
