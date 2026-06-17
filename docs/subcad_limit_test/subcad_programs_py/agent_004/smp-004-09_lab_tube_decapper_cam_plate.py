# Requirement: SMP-004-09
# Source agent: 004
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_004_medical_lab_dental_hardware_single_metal_parts.json
# Part: Lab Tube Decapper Cam Plate - single metal part
# Raw idea: Lab Tube Decapper Cam Plate
# Status: draft_unexecuted
#
# Coverage notes:
# - cylindrical round-bar stock OD 83 mm x length 75 mm using stainless_316
# - centered axial through bore diameter 16 mm
# - concentric end counterbore diameter 26 mm x 3 mm deep
# - longitudinal milled flat 27 mm wide over 67 mm length
# - two M5 radial tapped clamp holes at axial X=25 and X=50
# - full-length split relief slit width 6 mm
# - transverse cross relief slot width 8 mm at axial X=37, depth 8 mm
# - 1.0 mm outside edge chamfer pass
#
# Known gaps:
# - requirement datum says cylinder axis is X; Stock.cylindrical is used with its native cylinder axis for this draft
# - counterbores called from one accessible face; opposite-end counterbore remains an approximation
# - milled cylindrical flat is approximated by a rectangular top pocket/chord cut
# - radial tapped holes through a top flat are represented as top-face threaded holes at matching axial offsets
# - slit from outside to axial bore is approximated by a full top-face through slot
# - internal bore mouth chamfers are noted but not separately modeled with targeted bore-edge selections
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.

from subcad import Stock

part = (
    Stock.cylindrical(83, 75, material="stainless_316")
    .mill_turn_setup(axis="Z")
    .turn_id(diameter=16, depth=75)
    .counterbore(hole_diameter=16, counterbore_diameter=26, counterbore_depth=3, cx=0, cy=0, through=True)
    .pocket(width=27, length=67, depth=2.257, cx=0, cy=0)
    .threaded_hole(diameter=5, depth=41.5, cx=-12.5, cy=0)
    .threaded_hole(diameter=5, depth=41.5, cx=12.5, cy=0)
    .slot(length=75, width=6, depth=83, cx=0, cy=0, through=True)
    .slot(length=83, width=8, depth=8, angle=90, cx=-0.5, cy=0)
)
