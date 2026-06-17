# Requirement: SMP-001-04
# Source agent: 001
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_001_workshop_fixtures_single_metal_parts.json
# Part: Lathe Carriage Dial Indicator Holder - single metal part
# Raw idea: Lathe Carriage Dial Indicator Holder
# Status: draft_unexecuted
#
# Coverage notes:
# - cylindrical round-bar stock OD 79 mm x length 35 mm using steel_1045
# - centered axial through bore diameter 26 mm
# - concentric end counterbore diameter 36 mm x 3 mm deep
# - longitudinal milled flat 26 mm wide over 27 mm length
# - two M8 radial tapped clamp holes at axial X=11 and X=23
# - full-length split relief slit width 3 mm
# - transverse cross relief slot width 5 mm at axial X=17, depth 7 mm
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
    Stock.cylindrical(79, 35, material="steel_1045")
    .mill_turn_setup(axis="Z")
    .turn_id(diameter=26, depth=35)
    .counterbore(hole_diameter=26, counterbore_diameter=36, counterbore_depth=3, cx=0, cy=0, through=True)
    .pocket(width=26, length=27, depth=2.201, cx=0, cy=0)
    .threaded_hole(diameter=8, depth=39.5, cx=-6.5, cy=0)
    .threaded_hole(diameter=8, depth=39.5, cx=5.5, cy=0)
    .slot(length=35, width=3, depth=79, cx=0, cy=0, through=True)
    .slot(length=79, width=5, depth=7, angle=90, cx=-0.5, cy=0)
)
