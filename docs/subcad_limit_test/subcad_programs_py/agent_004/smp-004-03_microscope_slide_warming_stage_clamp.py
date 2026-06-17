# Requirement: SMP-004-03
# Source agent: 004
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_004_medical_lab_dental_hardware_single_metal_parts.json
# Part: Microscope Slide Warming Stage Clamp - single metal part
# Raw idea: Microscope Slide Warming Stage Clamp
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 115 x 105 x 33 mm using stainless_316
# - two through mounting holes diameter 9 mm at X=21/94, Y=52
# - central obround through slot 38 x 11 mm at X=57, Y=52
# - centered top rectangular relief pocket 28 x 35 x 13 mm deep
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.

from subcad import Stock

part = (
    Stock.rectangular(115, 105, 33, material="stainless_316")
    .drill_at(diameter=9, through=True, from_left=21, from_bottom=52, spot_drill=False)
    .drill_at(diameter=9, through=True, from_left=94, from_bottom=52, spot_drill=False)
    .slot_at(length=38, width=11, through=True, from_left=57, from_bottom=52)
    .pocket(width=35, length=28, depth=13, cx=0, cy=0)
)
