# Requirement: SMP-002-06
# Source agent: 002
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_002_mobility_hardware_single_metal_parts.json
# Part: Folding bicycle handlebar latch cam - single metal part
# Raw idea: Folding bicycle handlebar latch cam
# Status: draft_unexecuted
#
# Coverage notes:
# - cylindrical round-bar stock OD 83 mm x length 43 mm using steel_a36
# - centered axial through bore diameter 16 mm
# - concentric end counterbore diameter 26 mm x 3 mm deep
# - longitudinal milled flat 27 mm wide over 35 mm length
# - two M7 radial tapped clamp holes at axial X=14 and X=28
# - full-length split relief slit width 5 mm
# - transverse cross relief slot width 7 mm at axial X=21, depth 8 mm
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
    Stock.cylindrical(83, 43, material="steel_a36")
    .mill_turn_setup(axis="Z")
    .turn_id(diameter=16, depth=43)
    .counterbore(hole_diameter=16, counterbore_diameter=26, counterbore_depth=3, cx=0, cy=0, through=True)
    .pocket(width=27, length=35, depth=2.257, cx=0, cy=0)
    .threaded_hole(diameter=7, depth=41.5, cx=-7.5, cy=0)
    .threaded_hole(diameter=7, depth=41.5, cx=6.5, cy=0)
    .slot(length=43, width=5, depth=83, cx=0, cy=0, through=True)
    .slot(length=83, width=7, depth=8, angle=90, cx=-0.5, cy=0)
)
