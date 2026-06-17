# Requirement: SMP-020-03
# Source agent: 020
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_020_rescue_service_hardware_single_metal_parts.json
# Part: Flood-Rescue Throw Bag Belt Dock - single metal part
# Raw idea: Flood-Rescue Throw Bag Belt Dock
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 150 x 85 x 24 mm.
# - Two through mounting holes diameter 11 mm at X=17 and X=133, Y=42.
# - Central through obround slot 50 x 17 mm at X=75, Y=42.
# - Top relief pocket 37 x 28 x 1 mm centered between mounting holes.
# - Top outside chamfers represented with 1 mm chamfer operation.
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
    Stock.rectangular(150, 85, 24, material="steel_a36")
    .drill(diameter=11, through=True, cx=-58, cy=-0.5, spot_drill=False)
    .drill(diameter=11, through=True, cx=58, cy=-0.5, spot_drill=False)
    .slot(length=50, width=17, through=True, cx=0, cy=-0.5)
    .pocket(length=37, width=28, depth=1, cx=0, cy=0, corner_radius=0)
)
