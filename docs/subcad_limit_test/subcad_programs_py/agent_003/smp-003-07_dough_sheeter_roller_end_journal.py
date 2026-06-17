# Requirement: SMP-003-07
# Source agent: 003
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_003_kitchen_food_mechanisms_single_metal_parts.json
# Part: Dough Sheeter Roller End Journal - single metal part
# Raw idea: Dough Sheeter Roller End Journal
# Status: draft_unexecuted
#
# Coverage notes:
# - cylindrical round-bar stock OD 38 mm x length 75 mm using steel_4140
# - centered axial through bore diameter 12 mm
# - concentric end counterbore diameter 22 mm x 3 mm deep
# - longitudinal milled flat 12 mm wide over 67 mm length
# - two M6 radial tapped clamp holes at axial X=25 and X=50
# - full-length split relief slit width 4 mm
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
    Stock.cylindrical(38, 75, material="steel_4140")
    .mill_turn_setup(axis="Z")
    .turn_id(diameter=12, depth=75)
    .counterbore(hole_diameter=12, counterbore_diameter=22, counterbore_depth=3, cx=0, cy=0, through=True)
    .pocket(width=12, length=67, depth=0.972, cx=0, cy=0)
    .threaded_hole(diameter=6, depth=19, cx=-12.5, cy=0)
    .threaded_hole(diameter=6, depth=19, cx=12.5, cy=0)
    .slot(length=75, width=4, depth=38, cx=0, cy=0, through=True)
)
