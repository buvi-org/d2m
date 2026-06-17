# Requirement: SMP-001-08
# Source agent: 001
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_001_workshop_fixtures_single_metal_parts.json
# Part: Small Rotary Table Centering Plug - single metal part
# Raw idea: Small Rotary Table Centering Plug
# Status: draft_unexecuted
#
# Coverage notes:
# - cylindrical round-bar stock OD 72 mm x length 110 mm using steel_1045
# - centered axial through bore diameter 18 mm
# - concentric end counterbore diameter 28 mm x 3 mm deep
# - longitudinal milled flat 24 mm wide over 102 mm length
# - two M7 radial tapped clamp holes at axial X=36 and X=73
# - full-length split relief slit width 6 mm
# - opposed wrench flats leaving 64 mm across flats over middle third
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
    Stock.cylindrical(72, 110, material="steel_1045")
    .mill_turn_setup(axis="Z")
    .turn_id(diameter=18, depth=110)
    .counterbore(hole_diameter=18, counterbore_diameter=28, counterbore_depth=3, cx=0, cy=0, through=True)
    .pocket(width=24, length=102, depth=2.059, cx=0, cy=0)
    .threaded_hole(diameter=7, depth=36, cx=-19, cy=0)
    .threaded_hole(diameter=7, depth=36, cx=18, cy=0)
    .slot(length=110, width=6, depth=72, cx=0, cy=0, through=True)
    .pocket(width=72, length=36.667, depth=4, cx=0, cy=0, face_selector=">Z")
    .pocket(width=72, length=36.667, depth=4, cx=0, cy=0, face_selector="<Z")
)
