# Requirement: SMP-003-09
# Source agent: 003
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_003_kitchen_food_mechanisms_single_metal_parts.json
# Part: Grain Mill Fluted Feed Roller - single metal part
# Raw idea: Grain Mill Fluted Feed Roller
# Status: draft_unexecuted
#
# Coverage notes:
# - cylindrical round-bar stock OD 89 mm x length 32 mm using steel_4140
# - centered axial through bore diameter 29 mm
# - concentric end counterbore diameter 39 mm x 3 mm deep
# - longitudinal milled flat 29 mm wide over 24 mm length
# - two M5 radial tapped clamp holes at axial X=10 and X=21
# - full-length split relief slit width 3 mm
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
    Stock.cylindrical(89, 32, material="steel_4140")
    .mill_turn_setup(axis="Z")
    .turn_id(diameter=29, depth=32)
    .counterbore(hole_diameter=29, counterbore_diameter=39, counterbore_depth=3, cx=0, cy=0, through=True)
    .pocket(width=29, length=24, depth=2.429, cx=0, cy=0)
    .threaded_hole(diameter=5, depth=44.5, cx=-6, cy=0)
    .threaded_hole(diameter=5, depth=44.5, cx=5, cy=0)
    .slot(length=32, width=3, depth=89, cx=0, cy=0, through=True)
)
