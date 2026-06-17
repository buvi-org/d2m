# Requirement: SMP-006-03
# Source agent: 006
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_006_automotive_service_tools_single_metal_parts.json
# Part: CV Boot Clamp Crimping Anvil - single metal part
# Raw idea: CV Boot Clamp Crimping Anvil
# Status: draft_unexecuted
#
# Coverage notes:
# - cylindrical round-bar stock OD 90 mm x length 101 mm using steel_1045
# - centered axial through bore diameter 30 mm
# - concentric end counterbore diameter 40 mm x 3 mm deep
# - longitudinal milled flat 30 mm wide over 93 mm length
# - two M6 radial tapped clamp holes at axial X=33 and X=67
# - full-length split relief slit width 5 mm
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
    Stock.cylindrical(90, 101, material="steel_1045")
    .mill_turn_setup(axis="Z")
    .turn_id(diameter=30, depth=101)
    .counterbore(hole_diameter=30, counterbore_diameter=40, counterbore_depth=3, cx=0, cy=0, through=True)
    .pocket(width=30, length=93, depth=2.574, cx=0, cy=0)
    .threaded_hole(diameter=6, depth=45, cx=-17.5, cy=0)
    .threaded_hole(diameter=6, depth=45, cx=16.5, cy=0)
    .slot(length=101, width=5, depth=90, cx=0, cy=0, through=True)
)
