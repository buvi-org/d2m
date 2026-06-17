# Requirement: SMP-009-06
# Source agent: 009
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_009_furniture_architectural_hardware_single_metal_parts.json
# Part: Pivot Door Bottom Bearing Shoe - single metal part
# Raw idea: Pivot Door Bottom Bearing Shoe
# Status: draft_unexecuted
#
# Coverage notes:
# - cylindrical round-bar stock OD 47 mm x length 90 mm using steel_a36
# - centered axial through bore diameter 15 mm
# - concentric end counterbore diameter 25 mm x 3 mm deep
# - longitudinal milled flat 15 mm wide over 82 mm length
# - two M6 radial tapped clamp holes at axial X=30 and X=60
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
    Stock.cylindrical(47, 90, material="steel_a36")
    .mill_turn_setup(axis="Z")
    .turn_id(diameter=15, depth=90)
    .counterbore(hole_diameter=15, counterbore_diameter=25, counterbore_depth=3, cx=0, cy=0, through=True)
    .pocket(width=15, length=82, depth=1.229, cx=0, cy=0)
    .threaded_hole(diameter=6, depth=23.5, cx=-15, cy=0)
    .threaded_hole(diameter=6, depth=23.5, cx=15, cy=0)
    .slot(length=90, width=3, depth=47, cx=0, cy=0, through=True)
)
