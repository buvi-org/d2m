# Requirement: SMP-004-08
# Source agent: 004
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_004_medical_lab_dental_hardware_single_metal_parts.json
# Part: Orthodontic Wire Bending Turret - single metal part
# Raw idea: Orthodontic Wire Bending Turret
# Status: draft_unexecuted
#
# Coverage notes:
# - cylindrical round-bar stock OD 82 mm x length 78 mm using steel_a36
# - centered axial through bore diameter 27 mm
# - concentric end counterbore diameter 37 mm x 3 mm deep
# - longitudinal milled flat 27 mm wide over 70 mm length
# - two M5 radial tapped clamp holes at axial X=26 and X=52
# - full-length split relief slit width 4 mm
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
    Stock.cylindrical(82, 78, material="steel_a36")
    .mill_turn_setup(axis="Z")
    .turn_id(diameter=27, depth=78)
    .counterbore(hole_diameter=27, counterbore_diameter=37, counterbore_depth=3, cx=0, cy=0, through=True)
    .pocket(width=27, length=70, depth=2.286, cx=0, cy=0)
    .threaded_hole(diameter=5, depth=41, cx=-13, cy=0)
    .threaded_hole(diameter=5, depth=41, cx=13, cy=0)
    .slot(length=78, width=4, depth=82, cx=0, cy=0, through=True)
)
