# Requirement: SMP-005-06
# Source agent: 005
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_005_robotics_automation_single_metal_parts.json
# Part: Automated Screwdriver Floating Nosepiece - single metal part
# Raw idea: Automated Screwdriver Floating Nosepiece
# Status: draft_unexecuted
#
# Coverage notes:
# - cylindrical round-bar stock OD 79 mm x length 104 mm using aluminum_6061
# - centered axial through bore diameter 15 mm
# - concentric end counterbore diameter 25 mm x 3 mm deep
# - longitudinal milled flat 26 mm wide over 96 mm length
# - two M5 radial tapped clamp holes at axial X=34 and X=69
# - full-length split relief slit width 2 mm
# - transverse cross relief slot width 4 mm at axial X=52, depth 7 mm
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
    Stock.cylindrical(79, 104, material="aluminum_6061")
    .mill_turn_setup(axis="Z")
    .turn_id(diameter=15, depth=104)
    .counterbore(hole_diameter=15, counterbore_diameter=25, counterbore_depth=3, cx=0, cy=0, through=True)
    .pocket(width=26, length=96, depth=2.201, cx=0, cy=0)
    .threaded_hole(diameter=5, depth=39.5, cx=-18, cy=0)
    .threaded_hole(diameter=5, depth=39.5, cx=17, cy=0)
    .slot(length=104, width=2, depth=79, cx=0, cy=0, through=True)
    .slot(length=79, width=4, depth=7, angle=90, cx=0, cy=0)
)
