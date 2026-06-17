# Requirement: SMP-002-07
# Source agent: 002
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_002_mobility_hardware_single_metal_parts.json
# Part: E-bike mid-drive motor torque arm spline clamp - single metal part
# Raw idea: E-bike mid-drive motor torque arm spline clamp
# Status: draft_unexecuted
#
# Coverage notes:
# - cylindrical round-bar stock OD 67 mm x length 93 mm using steel_1045
# - centered axial through bore diameter 22 mm
# - concentric end counterbore diameter 32 mm x 3 mm deep
# - longitudinal milled flat 22 mm wide over 85 mm length
# - two M8 radial tapped clamp holes at axial X=31 and X=62
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
    Stock.cylindrical(67, 93, material="steel_1045")
    .mill_turn_setup(axis="Z")
    .turn_id(diameter=22, depth=93)
    .counterbore(hole_diameter=22, counterbore_diameter=32, counterbore_depth=3, cx=0, cy=0, through=True)
    .pocket(width=22, length=85, depth=1.857, cx=0, cy=0)
    .threaded_hole(diameter=8, depth=33.5, cx=-15.5, cy=0)
    .threaded_hole(diameter=8, depth=33.5, cx=15.5, cy=0)
    .slot(length=93, width=3, depth=67, cx=0, cy=0, through=True)
)
