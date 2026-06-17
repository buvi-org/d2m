# Requirement: SMP-009-10
# Source agent: 009
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_009_furniture_architectural_hardware_single_metal_parts.json
# Part: Flush Sliding Door Edge Pull Mechanism Cup - single metal part
# Raw idea: Flush Sliding Door Edge Pull Mechanism Cup
# Status: draft_unexecuted
#
# Coverage notes:
# - cylindrical round-bar stock OD 61 mm x length 34 mm using steel_a36
# - centered axial through bore diameter 12 mm
# - concentric end counterbore diameter 22 mm x 3 mm deep
# - longitudinal milled flat 20 mm wide over 26 mm length
# - two M6 radial tapped clamp holes at axial X=11 and X=22
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
    Stock.cylindrical(61, 34, material="steel_a36")
    .mill_turn_setup(axis="Z")
    .turn_id(diameter=12, depth=34)
    .counterbore(hole_diameter=12, counterbore_diameter=22, counterbore_depth=3, cx=0, cy=0, through=True)
    .pocket(width=20, length=26, depth=1.686, cx=0, cy=0)
    .threaded_hole(diameter=6, depth=30.5, cx=-6, cy=0)
    .threaded_hole(diameter=6, depth=30.5, cx=5, cy=0)
    .slot(length=34, width=3, depth=61, cx=0, cy=0, through=True)
)
