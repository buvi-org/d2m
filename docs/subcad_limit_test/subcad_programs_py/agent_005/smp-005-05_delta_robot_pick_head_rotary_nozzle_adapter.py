# Requirement: SMP-005-05
# Source agent: 005
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_005_robotics_automation_single_metal_parts.json
# Part: Delta Robot Pick Head Rotary Nozzle Adapter - single metal part
# Raw idea: Delta Robot Pick Head Rotary Nozzle Adapter
# Status: draft_unexecuted
#
# Coverage notes:
# - cylindrical round-bar stock OD 74 mm x length 33 mm using aluminum_6061
# - centered axial through bore diameter 24 mm
# - concentric end counterbore diameter 34 mm x 3 mm deep
# - longitudinal milled flat 24 mm wide over 25 mm length
# - two M8 radial tapped clamp holes at axial X=11 and X=22
# - full-length split relief slit width 5 mm
# - opposed wrench flats leaving 66 mm across flats over middle third
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
    Stock.cylindrical(74, 33, material="aluminum_6061")
    .mill_turn_setup(axis="Z")
    .turn_id(diameter=24, depth=33)
    .counterbore(hole_diameter=24, counterbore_diameter=34, counterbore_depth=3, cx=0, cy=0, through=True)
    .pocket(width=24, length=25, depth=2, cx=0, cy=0)
    .threaded_hole(diameter=8, depth=37, cx=-5.5, cy=0)
    .threaded_hole(diameter=8, depth=37, cx=5.5, cy=0)
    .slot(length=33, width=5, depth=74, cx=0, cy=0, through=True)
    .pocket(width=74, length=11, depth=4, cx=0, cy=0, face_selector=">Z")
    .pocket(width=74, length=11, depth=4, cx=0, cy=0, face_selector="<Z")
)
