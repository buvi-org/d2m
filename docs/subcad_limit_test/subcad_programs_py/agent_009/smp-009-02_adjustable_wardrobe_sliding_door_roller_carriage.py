# Requirement: SMP-009-02
# Source agent: 009
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_009_furniture_architectural_hardware_single_metal_parts.json
# Part: Adjustable Wardrobe Sliding Door Roller Carriage - single metal part
# Raw idea: Adjustable Wardrobe Sliding Door Roller Carriage
# Status: draft_unexecuted
#
# Coverage notes:
# - cylindrical round-bar stock OD 35 mm x length 115 mm using steel_a36
# - centered axial through bore diameter 8 mm
# - concentric end counterbore diameter 18 mm x 3 mm deep
# - longitudinal milled flat 11 mm wide over 107 mm length
# - two M5 radial tapped clamp holes at axial X=38 and X=76
# - full-length split relief slit width 3 mm
# - transverse cross relief slot width 5 mm at axial X=57, depth 3 mm
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
    Stock.cylindrical(35, 115, material="steel_a36")
    .mill_turn_setup(axis="Z")
    .turn_id(diameter=8, depth=115)
    .counterbore(hole_diameter=8, counterbore_diameter=18, counterbore_depth=3, cx=0, cy=0, through=True)
    .pocket(width=11, length=107, depth=0.887, cx=0, cy=0)
    .threaded_hole(diameter=5, depth=17.5, cx=-19.5, cy=0)
    .threaded_hole(diameter=5, depth=17.5, cx=18.5, cy=0)
    .slot(length=115, width=3, depth=35, cx=0, cy=0, through=True)
    .slot(length=35, width=5, depth=3, angle=90, cx=-0.5, cy=0)
)
