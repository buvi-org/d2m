# Requirement: SMP-007-10
# Source agent: 007
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_007_consumer_electronics_single_metal_parts.json
# Part: E-Reader Waterproof Port Service Plug Frame - single metal part
# Raw idea: E-Reader Waterproof Port Service Plug Frame
# Status: draft_unexecuted
#
# Coverage notes:
# - cylindrical round-bar stock OD 78 mm x length 112 mm using steel_4140
# - centered axial through bore diameter 26 mm
# - concentric end counterbore diameter 36 mm x 3 mm deep
# - longitudinal milled flat 26 mm wide over 104 mm length
# - two M7 radial tapped clamp holes at axial X=37 and X=74
# - full-length split relief slit width 6 mm
# - transverse cross relief slot width 8 mm at axial X=56, depth 7 mm
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
    Stock.cylindrical(78, 112, material="steel_4140")
    .mill_turn_setup(axis="Z")
    .turn_id(diameter=26, depth=112)
    .counterbore(hole_diameter=26, counterbore_diameter=36, counterbore_depth=3, cx=0, cy=0, through=True)
    .pocket(width=26, length=104, depth=2.23, cx=0, cy=0)
    .threaded_hole(diameter=7, depth=39, cx=-19, cy=0)
    .threaded_hole(diameter=7, depth=39, cx=18, cy=0)
    .slot(length=112, width=6, depth=78, cx=0, cy=0, through=True)
    .slot(length=78, width=8, depth=7, angle=90, cx=0, cy=0)
)
