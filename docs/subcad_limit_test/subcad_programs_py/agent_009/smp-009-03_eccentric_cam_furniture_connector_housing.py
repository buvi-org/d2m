# Requirement: SMP-009-03
# Source agent: 009
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_009_furniture_architectural_hardware_single_metal_parts.json
# Part: Eccentric Cam Furniture Connector Housing - single metal part
# Raw idea: Eccentric Cam Furniture Connector Housing
# Status: draft_unexecuted
#
# Coverage notes:
# - cylindrical round-bar stock OD 31 mm x length 105 mm using steel_4140
# - centered axial through bore diameter 10 mm
# - concentric end counterbore diameter 20 mm x 3 mm deep
# - longitudinal milled flat 10 mm wide over 97 mm length
# - two M7 radial tapped clamp holes at axial X=35 and X=70
# - full-length split relief slit width 2 mm
# - transverse cross relief slot width 4 mm at axial X=52, depth 3 mm
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
    Stock.cylindrical(31, 105, material="steel_4140")
    .mill_turn_setup(axis="Z")
    .turn_id(diameter=10, depth=105)
    .counterbore(hole_diameter=10, counterbore_diameter=20, counterbore_depth=3, cx=0, cy=0, through=True)
    .pocket(width=10, length=97, depth=0.829, cx=0, cy=0)
    .threaded_hole(diameter=7, depth=15.5, cx=-17.5, cy=0)
    .threaded_hole(diameter=7, depth=15.5, cx=17.5, cy=0)
    .slot(length=105, width=2, depth=31, cx=0, cy=0, through=True)
    .slot(length=31, width=4, depth=3, angle=90, cx=-0.5, cy=0)
)
