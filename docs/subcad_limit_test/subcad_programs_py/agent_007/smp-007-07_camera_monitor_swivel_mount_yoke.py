# Requirement: SMP-007-07
# Source agent: 007
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_007_consumer_electronics_single_metal_parts.json
# Part: Camera Monitor Swivel Mount Yoke - single metal part
# Raw idea: Camera Monitor Swivel Mount Yoke
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 135 x 90 x 53 mm using aluminum_6061
# - two through mounting holes diameter 12 mm at X=18/117, Y=45
# - central obround through slot 45 x 16 mm at X=67, Y=45
# - centered top rectangular relief pocket 33 x 30 x 18 mm deep
# - 11 rear-edge serration positions with 2 mm depth intent
# - M5 side tapped hole intent included as threaded hole proxy
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - triangular serration tooth form is approximated by repeated rectangular groove cuts
# - side tapped hole axis parallel to Y is approximated by a top-face threaded hole because side-axis drilling is not directly expressed
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.

from subcad import Stock

part = (
    Stock.rectangular(135, 90, 53, material="aluminum_6061")
    .drill_at(diameter=12, through=True, from_left=18, from_bottom=45, spot_drill=False)
    .drill_at(diameter=12, through=True, from_left=117, from_bottom=45, spot_drill=False)
    .slot_at(length=45, width=16, through=True, from_left=67, from_bottom=45)
    .pocket(width=30, length=33, depth=18, cx=0, cy=0)
    .groove(length=2, width=5.318, depth=2, cx=-66.5, cy=-40.909, angle=90)
    .groove(length=2, width=5.318, depth=2, cx=-66.5, cy=-32.727, angle=90)
    .groove(length=2, width=5.318, depth=2, cx=-66.5, cy=-24.545, angle=90)
    .groove(length=2, width=5.318, depth=2, cx=-66.5, cy=-16.364, angle=90)
    .groove(length=2, width=5.318, depth=2, cx=-66.5, cy=-8.182, angle=90)
    .groove(length=2, width=5.318, depth=2, cx=-66.5, cy=0, angle=90)
    .groove(length=2, width=5.318, depth=2, cx=-66.5, cy=8.182, angle=90)
    .groove(length=2, width=5.318, depth=2, cx=-66.5, cy=16.364, angle=90)
    .groove(length=2, width=5.318, depth=2, cx=-66.5, cy=24.545, angle=90)
    .groove(length=2, width=5.318, depth=2, cx=-66.5, cy=32.727, angle=90)
    .groove(length=2, width=5.318, depth=2, cx=-66.5, cy=40.909, angle=90)
    .threaded_hole(diameter=5, depth=45, cx=0, cy=22.5)
)
