# Requirement: SMP-004-01
# Source agent: 004
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_004_medical_lab_dental_hardware_single_metal_parts.json
# Part: Dental Handpiece Sterilization Cassette Hinge Block - single metal part
# Raw idea: Dental Handpiece Sterilization Cassette Hinge Block
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 125 x 40 x 35 mm using stainless_316
# - two through mounting holes diameter 13 mm at X=10/115, Y=20
# - central obround through slot 41 x 12 mm at X=62, Y=20
# - centered top rectangular relief pocket 31 x 18 x 3 mm deep
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
    Stock.rectangular(125, 40, 35, material="stainless_316")
    .drill_at(diameter=13, through=True, from_left=10, from_bottom=20, spot_drill=False)
    .drill_at(diameter=13, through=True, from_left=115, from_bottom=20, spot_drill=False)
    .slot_at(length=41, width=12, through=True, from_left=62, from_bottom=20)
    .pocket(width=18, length=31, depth=3, cx=0, cy=0)
)
