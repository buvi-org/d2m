# Requirement: SMP-020-08
# Source agent: 020
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_020_rescue_service_hardware_single_metal_parts.json
# Part: Rescue Saw Blade Transport Shield - single metal part
# Raw idea: Rescue Saw Blade Transport Shield
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 135 x 135 x 12 mm.
# - Two through mounting holes diameter 13 mm at X=27 and X=108, Y=67.
# - Central through obround slot 45 x 18 mm at X=67, Y=67.
# - Top relief pocket 33 x 45 x 4 mm centered between mounting holes.
# - Top outside chamfers represented with 1 mm chamfer operation.
# - Rear serration positions represented as 10 repeated edge grooves 4 mm deep.
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
    Stock.rectangular(135, 135, 12, material="steel_a36")
    .drill(diameter=13, through=True, cx=-40.5, cy=-0.5, spot_drill=False)
    .drill(diameter=13, through=True, cx=40.5, cy=-0.5, spot_drill=False)
    .slot(length=45, width=18, through=True, cx=-0.5, cy=-0.5)
    .pocket(length=33, width=45, depth=4, cx=0, cy=0, corner_radius=0)
    .groove(length=6.075, width=4, depth=1.44, cx=-60.75, cy=65.5)
    .groove(length=6.075, width=4, depth=1.44, cx=-47.25, cy=65.5)
    .groove(length=6.075, width=4, depth=1.44, cx=-33.75, cy=65.5)
    .groove(length=6.075, width=4, depth=1.44, cx=-20.25, cy=65.5)
    .groove(length=6.075, width=4, depth=1.44, cx=-6.75, cy=65.5)
    .groove(length=6.075, width=4, depth=1.44, cx=6.75, cy=65.5)
    .groove(length=6.075, width=4, depth=1.44, cx=20.25, cy=65.5)
    .groove(length=6.075, width=4, depth=1.44, cx=33.75, cy=65.5)
    .groove(length=6.075, width=4, depth=1.44, cx=47.25, cy=65.5)
    .groove(length=6.075, width=4, depth=1.44, cx=60.75, cy=65.5)
)
