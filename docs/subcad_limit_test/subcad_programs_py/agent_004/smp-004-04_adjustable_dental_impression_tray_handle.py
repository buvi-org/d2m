# Requirement: SMP-004-04
# Source agent: 004
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_004_medical_lab_dental_hardware_single_metal_parts.json
# Part: Adjustable Dental Impression Tray Handle - single metal part
# Raw idea: Adjustable Dental Impression Tray Handle
# Status: draft_unexecuted
#
# Coverage notes:
# - cylindrical round-bar stock OD 71 mm x length 95 mm using stainless_316
# - centered axial through bore diameter 23 mm
# - concentric end counterbore diameter 33 mm x 3 mm deep
# - longitudinal milled flat 23 mm wide over 87 mm length
# - two M7 radial tapped clamp holes at axial X=31 and X=63
# - full-length split relief slit width 3 mm
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
    Stock.cylindrical(71, 95, material="stainless_316")
    .mill_turn_setup(axis="Z")
    .turn_id(diameter=23, depth=95)
    .counterbore(hole_diameter=23, counterbore_diameter=33, counterbore_depth=3, cx=0, cy=0, through=True)
    .pocket(width=23, length=87, depth=1.914, cx=0, cy=0)
    .threaded_hole(diameter=7, depth=35.5, cx=-16.5, cy=0)
    .threaded_hole(diameter=7, depth=35.5, cx=15.5, cy=0)
    .slot(length=95, width=3, depth=71, cx=0, cy=0, through=True)
)
