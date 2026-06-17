# Requirement: SMP-003-01
# Source agent: 003
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_003_kitchen_food_mechanisms_single_metal_parts.json
# Part: Conical Burr Coffee Grinder Adjustment Collar - single metal part
# Raw idea: Conical Burr Coffee Grinder Adjustment Collar
# Status: draft_unexecuted
#
# Coverage notes:
# - cylindrical round-bar stock OD 89 mm x length 54 mm using steel_1045
# - centered axial through bore diameter 22 mm
# - concentric end counterbore diameter 32 mm x 3 mm deep
# - longitudinal milled flat 29 mm wide over 46 mm length
# - two M5 radial tapped clamp holes at axial X=18 and X=36
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
    Stock.cylindrical(89, 54, material="steel_1045")
    .mill_turn_setup(axis="Z")
    .turn_id(diameter=22, depth=54)
    .counterbore(hole_diameter=22, counterbore_diameter=32, counterbore_depth=3, cx=0, cy=0, through=True)
    .pocket(width=29, length=46, depth=2.429, cx=0, cy=0)
    .threaded_hole(diameter=5, depth=44.5, cx=-9, cy=0)
    .threaded_hole(diameter=5, depth=44.5, cx=9, cy=0)
    .slot(length=54, width=5, depth=89, cx=0, cy=0, through=True)
)
