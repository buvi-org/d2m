# Requirement: SMP-001-05
# Source agent: 001
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_001_workshop_fixtures_single_metal_parts.json
# Part: Quick-Change Toolpost Boring Bar Sleeve - single metal part
# Raw idea: Quick-Change Toolpost Boring Bar Sleeve
# Status: draft_unexecuted
#
# Coverage notes:
# - cylindrical round-bar stock OD 72 mm x length 40 mm using steel_1045
# - centered axial through bore diameter 18 mm
# - concentric end counterbore diameter 28 mm x 3 mm deep
# - longitudinal milled flat 24 mm wide over 32 mm length
# - two M8 radial tapped clamp holes at axial X=13 and X=26
# - full-length split relief slit width 2 mm
# - transverse cross relief slot width 4 mm at axial X=20, depth 7 mm
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
    Stock.cylindrical(72, 40, material="steel_1045")
    .mill_turn_setup(axis="Z")
    .turn_id(diameter=18, depth=40)
    .counterbore(hole_diameter=18, counterbore_diameter=28, counterbore_depth=3, cx=0, cy=0, through=True)
    .pocket(width=24, length=32, depth=2.059, cx=0, cy=0)
    .threaded_hole(diameter=8, depth=36, cx=-7, cy=0)
    .threaded_hole(diameter=8, depth=36, cx=6, cy=0)
    .slot(length=40, width=2, depth=72, cx=0, cy=0, through=True)
    .slot(length=72, width=4, depth=7, angle=90, cx=0, cy=0)
    .pocket(width=72, length=13.333, depth=4, cx=0, cy=0, face_selector=">Z")
    .pocket(width=72, length=13.333, depth=4, cx=0, cy=0, face_selector="<Z")
)
