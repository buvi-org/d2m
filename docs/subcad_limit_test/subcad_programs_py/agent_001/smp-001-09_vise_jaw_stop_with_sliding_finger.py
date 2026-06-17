# Requirement: SMP-001-09
# Source agent: 001
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_001_workshop_fixtures_single_metal_parts.json
# Part: Vise Jaw Stop With Sliding Finger - single metal part
# Raw idea: Vise Jaw Stop With Sliding Finger
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 205 x 45 x 30 mm using steel_1045
# - two through mounting holes diameter 6 mm at X=10/195, Y=22
# - central obround through slot 68 x 16 mm at X=102, Y=22
# - centered top rectangular relief pocket 51 x 18 x 8 mm deep
# - dovetail groove length 181 mm, throat 12 mm, included angle 60 degrees
# - end hook lip undercut proxy: projection 14 mm, undercut 5 mm
# - M9 side tapped hole intent included as threaded hole proxy
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - integral projecting hook lip is approximated by an end undercut within the rectangular envelope
# - side tapped hole axis parallel to Y is approximated by a top-face threaded hole because side-axis drilling is not directly expressed
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Dovetail depth was inferred because the requirement gives throat and angle but not groove depth.
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.

from subcad import Stock

part = (
    Stock.rectangular(205, 45, 30, material="steel_1045")
    .drill_at(diameter=6, through=True, from_left=10, from_bottom=22, spot_drill=False)
    .drill_at(diameter=6, through=True, from_left=195, from_bottom=22, spot_drill=False)
    .slot_at(length=68, width=16, through=True, from_left=102, from_bottom=22)
    .pocket(width=18, length=51, depth=8, cx=0, cy=0)
    .dovetail(length=181, width=12, depth=6.6, angle=60, cx=0, cy=0)
    .groove(length=14, width=45, depth=5, cx=-95.5, cy=0)
    .threaded_hole(diameter=9, depth=22.5, cx=0, cy=11.25)
)
