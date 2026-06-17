# Requirement: SMP-006-06
# Source agent: 006
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_006_automotive_service_tools_single_metal_parts.json
# Part: Strut Knuckle Spreader Wedge - single metal part
# Raw idea: Strut Knuckle Spreader Wedge
# Status: draft_unexecuted
#
# Coverage notes:
# - cylindrical round-bar stock OD 77 mm x length 110 mm using steel_1045
# - centered axial through bore diameter 19 mm
# - concentric end counterbore diameter 29 mm x 3 mm deep
# - longitudinal milled flat 25 mm wide over 102 mm length
# - two M8 radial tapped clamp holes at axial X=36 and X=73
# - full-length split relief slit width 6 mm
# - opposed wrench flats leaving 69 mm across flats over middle third
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
    Stock.cylindrical(77, 110, material="steel_1045")
    .mill_turn_setup(axis="Z")
    .turn_id(diameter=19, depth=110)
    .counterbore(hole_diameter=19, counterbore_diameter=29, counterbore_depth=3, cx=0, cy=0, through=True)
    .pocket(width=25, length=102, depth=2.086, cx=0, cy=0)
    .threaded_hole(diameter=8, depth=38.5, cx=-19, cy=0)
    .threaded_hole(diameter=8, depth=38.5, cx=18, cy=0)
    .slot(length=110, width=6, depth=77, cx=0, cy=0, through=True)
    .pocket(width=77, length=36.667, depth=4, cx=0, cy=0, face_selector=">Z")
    .pocket(width=77, length=36.667, depth=4, cx=0, cy=0, face_selector="<Z")
)
