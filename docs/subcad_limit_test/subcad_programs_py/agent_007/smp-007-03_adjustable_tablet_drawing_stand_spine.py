# Requirement: SMP-007-03
# Source agent: 007
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_007_consumer_electronics_single_metal_parts.json
# Part: Adjustable Tablet Drawing Stand Spine - single metal part
# Raw idea: Adjustable Tablet Drawing Stand Spine
# Status: draft_unexecuted
#
# Coverage notes:
# - cylindrical round-bar stock OD 79 mm x length 64 mm using steel_4140
# - centered axial through bore diameter 15 mm
# - concentric end counterbore diameter 25 mm x 3 mm deep
# - longitudinal milled flat 26 mm wide over 56 mm length
# - two M5 radial tapped clamp holes at axial X=21 and X=42
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
    Stock.cylindrical(79, 64, material="steel_4140")
    .mill_turn_setup(axis="Z")
    .turn_id(diameter=15, depth=64)
    .counterbore(hole_diameter=15, counterbore_diameter=25, counterbore_depth=3, cx=0, cy=0, through=True)
    .pocket(width=26, length=56, depth=2.201, cx=0, cy=0)
    .threaded_hole(diameter=5, depth=39.5, cx=-11, cy=0)
    .threaded_hole(diameter=5, depth=39.5, cx=10, cy=0)
    .slot(length=64, width=3, depth=79, cx=0, cy=0, through=True)
)
