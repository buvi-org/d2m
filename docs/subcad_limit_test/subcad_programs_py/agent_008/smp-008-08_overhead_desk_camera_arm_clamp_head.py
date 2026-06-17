# Requirement: SMP-008-08
# Source agent: 008
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_008_creator_rigging_hardware_single_metal_parts.json
# Part: Overhead Desk Camera Arm Clamp Head - single metal part
# Raw idea: Overhead Desk Camera Arm Clamp Head
# Status: draft_unexecuted
#
# Coverage notes:
# - cylindrical round-bar stock OD 61 mm x length 40 mm using aluminum_6061
# - centered axial through bore diameter 20 mm
# - concentric end counterbore diameter 30 mm x 3 mm deep
# - longitudinal milled flat 20 mm wide over 32 mm length
# - two M5 radial tapped clamp holes at axial X=13 and X=26
# - full-length split relief slit width 6 mm
# - transverse cross relief slot width 8 mm at axial X=20, depth 6 mm
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
    Stock.cylindrical(61, 40, material="aluminum_6061")
    .mill_turn_setup(axis="Z")
    .turn_id(diameter=20, depth=40)
    .counterbore(hole_diameter=20, counterbore_diameter=30, counterbore_depth=3, cx=0, cy=0, through=True)
    .pocket(width=20, length=32, depth=1.686, cx=0, cy=0)
    .threaded_hole(diameter=5, depth=30.5, cx=-7, cy=0)
    .threaded_hole(diameter=5, depth=30.5, cx=6, cy=0)
    .slot(length=40, width=6, depth=61, cx=0, cy=0, through=True)
    .slot(length=61, width=8, depth=6, angle=90, cx=0, cy=0)
)
