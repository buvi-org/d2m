# Requirement: SMP-020-02
# Source agent: 020
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_020_rescue_service_hardware_single_metal_parts.json
# Part: Ambulance Rail-Mount Oxygen Regulator Guard - single metal part
# Raw idea: Ambulance Rail-Mount Oxygen Regulator Guard
# Status: draft_unexecuted
#
# Coverage notes:
# - Base rectangular stock envelope 250 x 75 x 6 mm.
# - Two through mounting holes diameter 13 mm at X=15 and X=235, Y=37.
# - Central through obround slot 83 x 13 mm at X=125, Y=37.
# - Top relief pocket 62 x 25 x 1 mm centered between mounting holes.
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
    Stock.rectangular(250, 75, 6, material="stainless_316")
    .drill(diameter=13, through=True, cx=-110, cy=-0.5, spot_drill=False)
    .drill(diameter=13, through=True, cx=110, cy=-0.5, spot_drill=False)
    .slot(length=83, width=13, through=True, cx=0, cy=-0.5)
    .pocket(length=62, width=25, depth=1, cx=0, cy=0, corner_radius=0)
)
