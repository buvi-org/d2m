# Requirement: SMP-002-03
# Source agent: 002
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_002_mobility_hardware_single_metal_parts.json
# Part: Cargo bicycle adjustable kickstand yoke - single metal part
# Raw idea: Cargo bicycle adjustable kickstand yoke
# Status: draft_unexecuted
#
# Coverage notes:
# - cylindrical round-bar stock OD 53 mm x length 45 mm using steel_a36
# - centered axial through bore diameter 17 mm
# - concentric end counterbore diameter 27 mm x 3 mm deep
# - longitudinal milled flat 17 mm wide over 37 mm length
# - two M4 radial tapped clamp holes at axial X=15 and X=30
# - full-length split relief slit width 2 mm
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
    Stock.cylindrical(53, 45, material="steel_a36")
    .mill_turn_setup(axis="Z")
    .turn_id(diameter=17, depth=45)
    .counterbore(hole_diameter=17, counterbore_diameter=27, counterbore_depth=3, cx=0, cy=0, through=True)
    .pocket(width=17, length=37, depth=1.4, cx=0, cy=0)
    .threaded_hole(diameter=4, depth=26.5, cx=-7.5, cy=0)
    .threaded_hole(diameter=4, depth=26.5, cx=7.5, cy=0)
    .slot(length=45, width=2, depth=53, cx=0, cy=0, through=True)
)
