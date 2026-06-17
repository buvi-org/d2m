# Requirement: SMP-027-02
# Source agent: 027
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_027_scientific_instrument_fixtures_single_metal_parts.json
# Part: Vacuum Flange Optical Window Clamp Ring - single metal part
# Raw idea: Vacuum Flange Optical Window Clamp Ring
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 190 x 80 x 12 mm.
# - Two through mounting holes diameter 11 mm at X=16 and X=174, Y=40.
# - Central through obround slot 63 x 16 mm at X=95, Y=40.
# - Top relief pocket 47 x 26 x 3 mm centered between mounting holes.
# - Top outside chamfers represented with 1 mm chamfer operation.
# - Rear serration positions represented as 6 repeated edge grooves 2 mm deep.
#
# Known gaps:
# - 0.5 mm chamfers on individual hole and slot mouths are not separately selectable in this draft; only the general top chamfer is modeled.
# - Triangular serration tooth form is approximated with rectangular grooves because current fluent operations do not define triangular edge teeth.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated directly from frozen Stage 2 requirement text; not executed or visually reviewed yet.
# - Coordinate conversion uses SubCAD centered stock coordinates while requirement text uses lower-left-near datum coordinates.

from subcad import Stock

part = (
    Stock.rectangular(190, 80, 12, material="steel_1045")
    .drill(diameter=11, through=True, cx=-79, cy=0, spot_drill=False)
    .drill(diameter=11, through=True, cx=79, cy=0, spot_drill=False)
    .slot(length=63, width=16, through=True, cx=0, cy=0)
    .pocket(length=47, width=26, depth=3, cx=0, cy=0, corner_radius=0)
    .groove(length=14.25, width=2, depth=1.44, cx=-79.167, cy=39)
    .groove(length=14.25, width=2, depth=1.44, cx=-47.5, cy=39)
    .groove(length=14.25, width=2, depth=1.44, cx=-15.833, cy=39)
    .groove(length=14.25, width=2, depth=1.44, cx=15.833, cy=39)
    .groove(length=14.25, width=2, depth=1.44, cx=47.5, cy=39)
    .groove(length=14.25, width=2, depth=1.44, cx=79.167, cy=39)
)
