# Requirement: SMP-004-05
# Source agent: 004
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_004_medical_lab_dental_hardware_single_metal_parts.json
# Part: Lab Pipette Calibration Weight Cradle - single metal part
# Raw idea: Lab Pipette Calibration Weight Cradle
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 85 x 75 x 44 mm using stainless_316
# - two through mounting holes diameter 6 mm at X=15/70, Y=37
# - central obround through slot 30 x 12 mm at X=42, Y=37
# - centered top rectangular relief pocket 25 x 25 x 11 mm deep
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
    Stock.rectangular(85, 75, 44, material="stainless_316")
    .drill_at(diameter=6, through=True, from_left=15, from_bottom=37, spot_drill=False)
    .drill_at(diameter=6, through=True, from_left=70, from_bottom=37, spot_drill=False)
    .slot_at(length=30, width=12, through=True, from_left=42, from_bottom=37)
    .pocket(width=25, length=25, depth=11, cx=0, cy=0)
)
