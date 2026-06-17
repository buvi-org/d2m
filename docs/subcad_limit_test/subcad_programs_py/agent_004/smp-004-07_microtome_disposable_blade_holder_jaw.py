# Requirement: SMP-004-07
# Source agent: 004
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_004_medical_lab_dental_hardware_single_metal_parts.json
# Part: Microtome Disposable Blade Holder Jaw - single metal part
# Raw idea: Microtome Disposable Blade Holder Jaw
# Status: draft_unexecuted
#
# Coverage notes:
# - cylindrical round-bar stock OD 40 mm x length 48 mm using stainless_316
# - centered axial through bore diameter 13 mm
# - concentric end counterbore diameter 23 mm x 3 mm deep
# - longitudinal milled flat 13 mm wide over 40 mm length
# - two M8 radial tapped clamp holes at axial X=16 and X=32
# - full-length split relief slit width 5 mm
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
    Stock.cylindrical(40, 48, material="stainless_316")
    .mill_turn_setup(axis="Z")
    .turn_id(diameter=13, depth=48)
    .counterbore(hole_diameter=13, counterbore_diameter=23, counterbore_depth=3, cx=0, cy=0, through=True)
    .pocket(width=13, length=40, depth=1.086, cx=0, cy=0)
    .threaded_hole(diameter=8, depth=20, cx=-8, cy=0)
    .threaded_hole(diameter=8, depth=20, cx=8, cy=0)
    .slot(length=48, width=5, depth=40, cx=0, cy=0, through=True)
)
