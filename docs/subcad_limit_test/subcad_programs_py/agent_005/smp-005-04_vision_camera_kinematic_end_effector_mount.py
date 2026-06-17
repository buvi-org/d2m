# Requirement: SMP-005-04
# Source agent: 005
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_005_robotics_automation_single_metal_parts.json
# Part: Vision Camera Kinematic End-Effector Mount - single metal part
# Raw idea: Vision Camera Kinematic End-Effector Mount
# Status: draft_unexecuted
#
# Coverage notes:
# - cylindrical round-bar stock OD 92 mm x length 110 mm using aluminum_6061
# - centered axial through bore diameter 30 mm
# - concentric end counterbore diameter 40 mm x 3 mm deep
# - longitudinal milled flat 30 mm wide over 102 mm length
# - two M6 radial tapped clamp holes at axial X=36 and X=73
# - full-length split relief slit width 4 mm
# - transverse cross relief slot width 6 mm at axial X=55, depth 9 mm
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
    Stock.cylindrical(92, 110, material="aluminum_6061")
    .mill_turn_setup(axis="Z")
    .turn_id(diameter=30, depth=110)
    .counterbore(hole_diameter=30, counterbore_diameter=40, counterbore_depth=3, cx=0, cy=0, through=True)
    .pocket(width=30, length=102, depth=2.514, cx=0, cy=0)
    .threaded_hole(diameter=6, depth=46, cx=-19, cy=0)
    .threaded_hole(diameter=6, depth=46, cx=18, cy=0)
    .slot(length=110, width=4, depth=92, cx=0, cy=0, through=True)
    .slot(length=92, width=6, depth=9, angle=90, cx=0, cy=0)
)
