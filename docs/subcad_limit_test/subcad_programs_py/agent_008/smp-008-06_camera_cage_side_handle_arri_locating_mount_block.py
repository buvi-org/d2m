# Requirement: SMP-008-06
# Source agent: 008
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_008_creator_rigging_hardware_single_metal_parts.json
# Part: Camera Cage Side Handle ARRI-Locating Mount Block - single metal part
# Raw idea: Camera Cage Side Handle ARRI-Locating Mount Block
# Status: draft_unexecuted
#
# Coverage notes:
# - cylindrical round-bar stock OD 39 mm x length 98 mm using aluminum_6061
# - centered axial through bore diameter 8 mm
# - concentric end counterbore diameter 18 mm x 3 mm deep
# - longitudinal milled flat 13 mm wide over 90 mm length
# - two M5 radial tapped clamp holes at axial X=32 and X=65
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
    Stock.cylindrical(39, 98, material="aluminum_6061")
    .mill_turn_setup(axis="Z")
    .turn_id(diameter=8, depth=98)
    .counterbore(hole_diameter=8, counterbore_diameter=18, counterbore_depth=3, cx=0, cy=0, through=True)
    .pocket(width=13, length=90, depth=1.115, cx=0, cy=0)
    .threaded_hole(diameter=5, depth=19.5, cx=-17, cy=0)
    .threaded_hole(diameter=5, depth=19.5, cx=16, cy=0)
    .slot(length=98, width=4, depth=39, cx=0, cy=0, through=True)
)
