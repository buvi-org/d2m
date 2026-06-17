# Requirement: SMP-006-04
# Source agent: 006
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_006_automotive_service_tools_single_metal_parts.json
# Part: Wheel Stud Press Support Cup - single metal part
# Raw idea: Wheel Stud Press Support Cup
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 255 x 100 x 5 mm using steel_1045
# - two through mounting holes diameter 8 mm at X=20/235, Y=50
# - central obround through slot 85 x 13 mm at X=127, Y=50
# - centered top rectangular relief pocket 63 x 33 x 2 mm deep
# - 10 rear-edge serration positions with 2 mm depth intent
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - triangular serration tooth form is approximated by repeated rectangular groove cuts
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.

from subcad import Stock

part = (
    Stock.rectangular(255, 100, 5, material="steel_1045")
    .drill_at(diameter=8, through=True, from_left=20, from_bottom=50, spot_drill=False)
    .drill_at(diameter=8, through=True, from_left=235, from_bottom=50, spot_drill=False)
    .slot_at(length=85, width=13, through=True, from_left=127, from_bottom=50)
    .pocket(width=33, length=63, depth=2, cx=0, cy=0)
    .groove(length=2, width=6.5, depth=2, cx=-126.5, cy=-45, angle=90)
    .groove(length=2, width=6.5, depth=2, cx=-126.5, cy=-35, angle=90)
    .groove(length=2, width=6.5, depth=2, cx=-126.5, cy=-25, angle=90)
    .groove(length=2, width=6.5, depth=2, cx=-126.5, cy=-15, angle=90)
    .groove(length=2, width=6.5, depth=2, cx=-126.5, cy=-5, angle=90)
    .groove(length=2, width=6.5, depth=2, cx=-126.5, cy=5, angle=90)
    .groove(length=2, width=6.5, depth=2, cx=-126.5, cy=15, angle=90)
    .groove(length=2, width=6.5, depth=2, cx=-126.5, cy=25, angle=90)
    .groove(length=2, width=6.5, depth=2, cx=-126.5, cy=35, angle=90)
    .groove(length=2, width=6.5, depth=2, cx=-126.5, cy=45, angle=90)
)
