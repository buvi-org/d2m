# Requirement: SMP-001-10
# Source agent: 001
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_001_workshop_fixtures_single_metal_parts.json
# Part: Tap Guide Block With Interchangeable Bushings - single metal part
# Raw idea: Tap Guide Block With Interchangeable Bushings
# Status: draft_unexecuted
#
# Coverage notes:
# - cylindrical round-bar stock OD 40 mm x length 91 mm using steel_1045
# - centered axial through bore diameter 8 mm
# - concentric end counterbore diameter 18 mm x 3 mm deep
# - longitudinal milled flat 13 mm wide over 83 mm length
# - two M7 radial tapped clamp holes at axial X=30 and X=60
# - full-length split relief slit width 6 mm
# - transverse cross relief slot width 8 mm at axial X=45, depth 4 mm
# - opposed wrench flats leaving 32 mm across flats over middle third
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
    Stock.cylindrical(40, 91, material="steel_1045")
    .mill_turn_setup(axis="Z")
    .turn_id(diameter=8, depth=91)
    .counterbore(hole_diameter=8, counterbore_diameter=18, counterbore_depth=3, cx=0, cy=0, through=True)
    .pocket(width=13, length=83, depth=1.086, cx=0, cy=0)
    .threaded_hole(diameter=7, depth=20, cx=-15.5, cy=0)
    .threaded_hole(diameter=7, depth=20, cx=14.5, cy=0)
    .slot(length=91, width=6, depth=40, cx=0, cy=0, through=True)
    .slot(length=40, width=8, depth=4, angle=90, cx=-0.5, cy=0)
    .pocket(width=40, length=30.333, depth=4, cx=0, cy=0, face_selector=">Z")
    .pocket(width=40, length=30.333, depth=4, cx=0, cy=0, face_selector="<Z")
)
