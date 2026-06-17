# Requirement: SMP-021-03
# Source agent: 021
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_021_education_lab_apparatus_single_metal_parts.json
# Part: Optical Bench Lens Carrier - single metal part
# Raw idea: Optical Bench Lens Carrier
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 185 x 90 x 19 mm.
# - Two through mounting holes diameter 5 mm at X=18 and X=167, Y=45.
# - Central through obround slot 61 x 17 mm at X=92, Y=45.
# - Top relief pocket 46 x 30 x 1 mm centered between mounting holes.
# - Top outside chamfers represented with 1 mm chamfer operation.
#
# Known gaps:
# - 0.5 mm chamfers on individual hole and slot mouths are not separately selectable in this draft; only the general top chamfer is modeled.
# - Side tapped hole M10 with axis parallel to Y is not modeled; current threaded_hole/tap operations are top-face axial in this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated directly from frozen Stage 2 requirement text; not executed or visually reviewed yet.
# - Coordinate conversion uses SubCAD centered stock coordinates while requirement text uses lower-left-near datum coordinates.

from subcad import Stock

part = (
    Stock.rectangular(185, 90, 19, material="steel_a36")
    .drill(diameter=5, through=True, cx=-74.5, cy=0, spot_drill=False)
    .drill(diameter=5, through=True, cx=74.5, cy=0, spot_drill=False)
    .slot(length=61, width=17, through=True, cx=-0.5, cy=0)
    .pocket(length=46, width=30, depth=1, cx=0, cy=0, corner_radius=0)
)
