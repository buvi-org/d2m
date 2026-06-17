# Requirement: SMP-004-02
# Source agent: 004
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_004_medical_lab_dental_hardware_single_metal_parts.json
# Part: Benchtop Centrifuge Rotor Adapter - single metal part
# Raw idea: Benchtop Centrifuge Rotor Adapter
# Status: draft_unexecuted
#
# Coverage notes:
# - cylindrical round-bar stock OD 86 mm x length 44 mm using steel_a36
# - centered axial through bore diameter 17 mm
# - concentric end counterbore diameter 27 mm x 3 mm deep
# - longitudinal milled flat 28 mm wide over 36 mm length
# - two M7 radial tapped clamp holes at axial X=14 and X=29
# - full-length split relief slit width 5 mm
# - transverse cross relief slot width 7 mm at axial X=22, depth 8 mm
# - opposed wrench flats leaving 78 mm across flats over middle third
# - 1.0 mm outside edge chamfer pass
#
# Known gaps:
# - requirement datum says cylinder axis is X; Stock.cylindrical is used with its native cylinder axis for this draft
# - counterbores called from one accessible face; opposite-end counterbore remains an approximation
# - milled cylindrical flat is approximated by a rectangular top pocket/chord cut
# - radial tapped holes through a top flat are represented as top-face threaded holes at matching axial offsets
# - slit from outside to axial bore is approximated by a full top-face through slot
# - opposed wrench flats use top/bottom pocket proxies on a cylindrical stock
# - internal bore mouth chamfers are noted but not separately modeled with targeted bore-edge selections
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.

from subcad import Stock

part = (
    Stock.cylindrical(86, 44, material="steel_a36")
    .mill_turn_setup(axis="Z")
    .turn_id(diameter=17, depth=44)
    .counterbore(hole_diameter=17, counterbore_diameter=27, counterbore_depth=3, cx=0, cy=0, through=True)
    .pocket(width=28, length=36, depth=2.343, cx=0, cy=0)
    .threaded_hole(diameter=7, depth=43, cx=-8, cy=0)
    .threaded_hole(diameter=7, depth=43, cx=7, cy=0)
    .slot(length=44, width=5, depth=86, cx=0, cy=0, through=True)
    .slot(length=86, width=7, depth=8, angle=90, cx=0, cy=0)
    .pocket(width=86, length=14.667, depth=4, cx=0, cy=0, face_selector=">Z")
    .pocket(width=86, length=14.667, depth=4, cx=0, cy=0, face_selector="<Z")
)
