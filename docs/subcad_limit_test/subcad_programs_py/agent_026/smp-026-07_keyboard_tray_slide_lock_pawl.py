# Requirement: SMP-026-07
# Source agent: 026
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_026_office_equipment_hardware_single_metal_parts.json
# Part: Keyboard Tray Slide Lock Pawl - single metal part
# Raw idea: Keyboard Tray Slide Lock Pawl
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 210 x 135 x 7 mm.
# - Two through mounting holes diameter 13 mm at X=27 and X=183, Y=67.
# - Central through obround slot 70 x 18 mm at X=105, Y=67.
# - Top relief pocket 52 x 45 x 3 mm centered between mounting holes.
# - Top outside chamfers represented with 1 mm chamfer operation.
# - Rear serration positions represented as 7 repeated edge grooves 3 mm deep.
# - Angled reference region over the last 42 mm represented as a sloped top-face cut at the right end.
#
# Known gaps:
# - 0.5 mm chamfers on individual hole and slot mouths are not separately selectable in this draft; only the general top chamfer is modeled.
# - Triangular serration tooth form is approximated with rectangular grooves because current fluent operations do not define triangular edge teeth.
# - Exact external face angle of 35 degrees is approximated by a sloped pocket depth transition, not a full side-face reprofile.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated directly from frozen Stage 2 requirement text; not executed or visually reviewed yet.
# - Coordinate conversion uses SubCAD centered stock coordinates while requirement text uses lower-left-near datum coordinates.

from subcad import Stock

part = (
    Stock.rectangular(210, 135, 7, material="steel_a36")
    .drill(diameter=13, through=True, cx=-78, cy=-0.5, spot_drill=False)
    .drill(diameter=13, through=True, cx=78, cy=-0.5, spot_drill=False)
    .slot(length=70, width=18, through=True, cx=0, cy=-0.5)
    .pocket(length=52, width=45, depth=3, cx=0, cy=0, corner_radius=0)
    .groove(length=13.5, width=3, depth=0.84, cx=-90, cy=66)
    .groove(length=13.5, width=3, depth=0.84, cx=-60, cy=66)
    .groove(length=13.5, width=3, depth=0.84, cx=-30, cy=66)
    .groove(length=13.5, width=3, depth=0.84, cx=0, cy=66)
    .groove(length=13.5, width=3, depth=0.84, cx=30, cy=66)
    .groove(length=13.5, width=3, depth=0.84, cx=60, cy=66)
    .groove(length=13.5, width=3, depth=0.84, cx=90, cy=66)
    .slope_cut(width=135, length=42, start_depth=0.5, end_depth=5.95, cx=84, cy=0, slope_axis="X")
)
