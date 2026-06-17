# Requirement: SMP-003-05
# Source agent: 003
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_003_kitchen_food_mechanisms_single_metal_parts.json
# Part: Pasta Roller Thickness Cam - single metal part
# Raw idea: Pasta Roller Thickness Cam
# Status: draft_unexecuted
#
# Coverage notes:
# - cylindrical round-bar stock OD 90 mm x length 52 mm using steel_a36
# - centered axial through bore diameter 22 mm
# - concentric end counterbore diameter 32 mm x 3 mm deep
# - longitudinal milled flat 30 mm wide over 44 mm length
# - two M8 radial tapped clamp holes at axial X=17 and X=34
# - full-length split relief slit width 2 mm
# - opposed wrench flats leaving 82 mm across flats over middle third
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
    Stock.cylindrical(90, 52, material="steel_a36")
    .mill_turn_setup(axis="Z")
    .turn_id(diameter=22, depth=52)
    .counterbore(hole_diameter=22, counterbore_diameter=32, counterbore_depth=3, cx=0, cy=0, through=True)
    .pocket(width=30, length=44, depth=2.574, cx=0, cy=0)
    .threaded_hole(diameter=8, depth=45, cx=-9, cy=0)
    .threaded_hole(diameter=8, depth=45, cx=8, cy=0)
    .slot(length=52, width=2, depth=90, cx=0, cy=0, through=True)
    .pocket(width=90, length=17.333, depth=4, cx=0, cy=0, face_selector=">Z")
    .pocket(width=90, length=17.333, depth=4, cx=0, cy=0, face_selector="<Z")
)
