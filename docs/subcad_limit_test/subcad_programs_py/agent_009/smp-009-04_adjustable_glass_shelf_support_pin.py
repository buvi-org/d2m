# Requirement: SMP-009-04
# Source agent: 009
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_009_furniture_architectural_hardware_single_metal_parts.json
# Part: Adjustable Glass Shelf Support Pin - single metal part
# Raw idea: Adjustable Glass Shelf Support Pin
# Status: draft_unexecuted
#
# Coverage notes:
# - cylindrical round-bar stock OD 85 mm x length 64 mm using steel_a36
# - centered axial through bore diameter 21 mm
# - concentric end counterbore diameter 31 mm x 3 mm deep
# - longitudinal milled flat 28 mm wide over 56 mm length
# - two M4 radial tapped clamp holes at axial X=21 and X=42
# - full-length split relief slit width 2 mm
# - opposed wrench flats leaving 77 mm across flats over middle third
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
    Stock.cylindrical(85, 64, material="steel_a36")
    .mill_turn_setup(axis="Z")
    .turn_id(diameter=21, depth=64)
    .counterbore(hole_diameter=21, counterbore_diameter=31, counterbore_depth=3, cx=0, cy=0, through=True)
    .pocket(width=28, length=56, depth=2.372, cx=0, cy=0)
    .threaded_hole(diameter=4, depth=42.5, cx=-11, cy=0)
    .threaded_hole(diameter=4, depth=42.5, cx=10, cy=0)
    .slot(length=64, width=2, depth=85, cx=0, cy=0, through=True)
    .pocket(width=85, length=21.333, depth=4, cx=0, cy=0, face_selector=">Z")
    .pocket(width=85, length=21.333, depth=4, cx=0, cy=0, face_selector="<Z")
)
