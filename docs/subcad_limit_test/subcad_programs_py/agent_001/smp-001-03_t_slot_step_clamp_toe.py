# Requirement: SMP-001-03
# Source agent: 001
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_001_workshop_fixtures_single_metal_parts.json
# Part: T-Slot Step Clamp Toe - single metal part
# Raw idea: T-Slot Step Clamp Toe
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 155 x 95 x 44 mm using steel_1045
# - two through mounting holes diameter 8 mm at X=19/136, Y=47
# - central obround through slot 51 x 15 mm at X=77, Y=47
# - centered top rectangular relief pocket 38 x 31 x 3 mm deep
# - angled top reference face over last 31 mm using sloped-floor cut for 11 degree intent
# - 12 rear-edge serration positions with 3 mm depth intent
# - end hook lip undercut proxy: projection 11 mm, undercut 4 mm
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - angled reference face is represented as a sloped rectangular floor cut rather than a full exterior face reprofile
# - triangular serration tooth form is approximated by repeated rectangular groove cuts
# - integral projecting hook lip is approximated by an end undercut within the rectangular envelope
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.

from subcad import Stock

part = (
    Stock.rectangular(155, 95, 44, material="steel_1045")
    .drill_at(diameter=8, through=True, from_left=19, from_bottom=47, spot_drill=False)
    .drill_at(diameter=8, through=True, from_left=136, from_bottom=47, spot_drill=False)
    .slot_at(length=51, width=15, through=True, from_left=77, from_bottom=47)
    .pocket(width=31, length=38, depth=3, cx=0, cy=0)
    .slope_cut(width=95, length=31, start_depth=0, end_depth=6.026, cx=62, cy=0, slope_axis="X")
    .groove(length=3, width=5.146, depth=3, cx=-76, cy=-43.542, angle=90)
    .groove(length=3, width=5.146, depth=3, cx=-76, cy=-35.625, angle=90)
    .groove(length=3, width=5.146, depth=3, cx=-76, cy=-27.708, angle=90)
    .groove(length=3, width=5.146, depth=3, cx=-76, cy=-19.792, angle=90)
    .groove(length=3, width=5.146, depth=3, cx=-76, cy=-11.875, angle=90)
    .groove(length=3, width=5.146, depth=3, cx=-76, cy=-3.958, angle=90)
    .groove(length=3, width=5.146, depth=3, cx=-76, cy=3.958, angle=90)
    .groove(length=3, width=5.146, depth=3, cx=-76, cy=11.875, angle=90)
    .groove(length=3, width=5.146, depth=3, cx=-76, cy=19.792, angle=90)
    .groove(length=3, width=5.146, depth=3, cx=-76, cy=27.708, angle=90)
    .groove(length=3, width=5.146, depth=3, cx=-76, cy=35.625, angle=90)
    .groove(length=3, width=5.146, depth=3, cx=-76, cy=43.542, angle=90)
    .groove(length=11, width=95, depth=4, cx=-72, cy=0)
)
