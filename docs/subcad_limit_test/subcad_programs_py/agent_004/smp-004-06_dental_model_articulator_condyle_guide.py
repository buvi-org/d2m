# Requirement: SMP-004-06
# Source agent: 004
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_004_medical_lab_dental_hardware_single_metal_parts.json
# Part: Dental Model Articulator Condyle Guide - single metal part
# Raw idea: Dental Model Articulator Condyle Guide
# Status: draft_unexecuted
#
# Coverage notes:
# - rectangular stock envelope 190 x 80 x 33 mm using stainless_316
# - two through mounting holes diameter 5 mm at X=16/174, Y=40
# - central obround through slot 63 x 15 mm at X=95, Y=40
# - centered top rectangular relief pocket 47 x 26 x 8 mm deep
# - central counterbore diameter 23 mm x 6 mm deep around center feature
# - angled top reference face over last 38 mm using sloped-floor cut for 29 degree intent
# - M5 side tapped hole intent included as threaded hole proxy
# - 1.0 mm top outside chamfer pass
#
# Known gaps:
# - counterbore around an obround slot is represented with a circular counterbore operation
# - angled reference face is represented as a sloped rectangular floor cut rather than a full exterior face reprofile
# - side tapped hole axis parallel to Y is approximated by a top-face threaded hole because side-axis drilling is not directly expressed
# - 0.5 mm chamfers on individual hole and slot mouths are not separately targeted
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.

from subcad import Stock

part = (
    Stock.rectangular(190, 80, 33, material="stainless_316")
    .drill_at(diameter=5, through=True, from_left=16, from_bottom=40, spot_drill=False)
    .drill_at(diameter=5, through=True, from_left=174, from_bottom=40, spot_drill=False)
    .slot_at(length=63, width=15, through=True, from_left=95, from_bottom=40)
    .pocket(width=26, length=47, depth=8, cx=0, cy=0)
    .counterbore(hole_diameter=15, counterbore_diameter=23, counterbore_depth=6, cx=0, cy=0, through=True)
    .slope_cut(width=80, length=38, start_depth=0, end_depth=21.064, cx=76, cy=0, slope_axis="X")
    .threaded_hole(diameter=5, depth=40, cx=0, cy=20)
)
