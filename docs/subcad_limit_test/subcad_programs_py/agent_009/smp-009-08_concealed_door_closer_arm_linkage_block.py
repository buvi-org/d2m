# Requirement: SMP-009-08
# Source agent: 009
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_009_furniture_architectural_hardware_single_metal_parts.json
# Part: Concealed Door Closer Arm Linkage Block - single metal part
# Raw idea: Concealed Door Closer Arm Linkage Block
# Status: draft_unexecuted
#
# Coverage notes:
# - cylindrical round-bar stock OD 53 mm x length 118 mm using steel_4140
# - centered axial through bore diameter 17 mm
# - concentric end counterbore diameter 27 mm x 3 mm deep
# - longitudinal milled flat 17 mm wide over 110 mm length
# - two M5 radial tapped clamp holes at axial X=39 and X=78
# - full-length split relief slit width 5 mm
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
    Stock.cylindrical(53, 118, material="steel_4140")
    .mill_turn_setup(axis="Z")
    .turn_id(diameter=17, depth=118)
    .counterbore(hole_diameter=17, counterbore_diameter=27, counterbore_depth=3, cx=0, cy=0, through=True)
    .pocket(width=17, length=110, depth=1.4, cx=0, cy=0)
    .threaded_hole(diameter=5, depth=26.5, cx=-20, cy=0)
    .threaded_hole(diameter=5, depth=26.5, cx=19, cy=0)
    .slot(length=118, width=5, depth=53, cx=0, cy=0, through=True)
)
