# Requirement: SMP-042-09
# Source agent: 042
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_042_glass_handling_hardware_single_metal_parts.json
# Part: Mirror Stand-Off Rosette Mount - single metal part
# Raw idea: Mirror Stand-Off Rosette Mount
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 200 x 90 x 50 mm using steel_a36
# - two through mounting holes diameter 11 mm at X=18/182, Y=45
# - central obround through slot 66 x 8 mm at X=100, Y=45
# - centered top rectangular relief pocket 50 x 30 x 7 mm deep
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - Tap one side hole M10 from the right long edge into the central pocket; hole axis is parallel to Y. SubCAD has no side-entry tapped-hole axis selection in the inspected Stock API, so this side hole is not modeled.
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted by this draft.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.
# - Rectangular/sheet X/Y feature placement uses drill_at/slot_at/pocket_at datum offsets from the lower-left requirement origin where applicable.

from subcad import Stock

part = (
    Stock.rectangular(200, 90, 50, material="steel_a36")
    .drill_at(diameter=11, through=True, from_left=18, from_bottom=45, spot_drill=False)
    .drill_at(diameter=11, through=True, from_left=182, from_bottom=45, spot_drill=False)
    .slot_at(length=66, width=8, through=True, from_left=100, from_bottom=45)
    .pocket_at(width=30, length=50, depth=7, from_left=100, from_bottom=45)
)
