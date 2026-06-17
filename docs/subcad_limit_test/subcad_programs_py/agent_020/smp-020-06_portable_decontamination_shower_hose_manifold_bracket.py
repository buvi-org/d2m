# Requirement: SMP-020-06
# Source agent: 020
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_020_rescue_service_hardware_single_metal_parts.json
# Part: Portable Decontamination Shower Hose Manifold Bracket - single metal part
# Raw idea: Portable Decontamination Shower Hose Manifold Bracket
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 170 x 80 x 6 mm.
# - Two through mounting holes diameter 6 mm at X=16 and X=154, Y=40.
# - Central through obround slot 56 x 15 mm at X=85, Y=40.
# - Top relief pocket 42 x 26 x 3 mm centered between mounting holes.
# - Top outside chamfers represented with 1 mm chamfer operation.
# - Angled reference region over the last 34 mm represented as a sloped top-face cut at the right end.
#
# Known gaps:
# - 0.5 mm chamfers on individual hole and slot mouths are not separately selectable in this draft; only the general top chamfer is modeled.
# - Exact external face angle of 39 degrees is approximated by a sloped pocket depth transition, not a full side-face reprofile.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated directly from frozen Stage 2 requirement text; not executed or visually reviewed yet.
# - Coordinate conversion uses SubCAD centered stock coordinates while requirement text uses lower-left-near datum coordinates.

from subcad import Stock

part = (
    Stock.rectangular(170, 80, 6, material="steel_a36")
    .drill(diameter=6, through=True, cx=-69, cy=0, spot_drill=False)
    .drill(diameter=6, through=True, cx=69, cy=0, spot_drill=False)
    .slot(length=56, width=15, through=True, cx=0, cy=0)
    .pocket(length=42, width=26, depth=3, cx=0, cy=0, corner_radius=0)
    .slope_cut(width=80, length=34, start_depth=0.5, end_depth=5.1, cx=68, cy=0, slope_axis="X")
)
