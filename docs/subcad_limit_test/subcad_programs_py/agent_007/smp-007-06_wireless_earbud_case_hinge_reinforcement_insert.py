# Requirement: SMP-007-06
# Source agent: 007
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_007_consumer_electronics_single_metal_parts.json
# Part: Wireless Earbud Case Hinge Reinforcement Insert - single metal part
# Raw idea: Wireless Earbud Case Hinge Reinforcement Insert
# Status: draft_unexecuted
#
# Coverage notes:
# - cylindrical round-bar stock OD 50 mm x length 113 mm using steel_4140
# - centered axial through bore diameter 16 mm
# - concentric end counterbore diameter 26 mm x 3 mm deep
# - longitudinal milled flat 16 mm wide over 105 mm length
# - two M4 radial tapped clamp holes at axial X=37 and X=75
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
    Stock.cylindrical(50, 113, material="steel_4140")
    .mill_turn_setup(axis="Z")
    .turn_id(diameter=16, depth=113)
    .counterbore(hole_diameter=16, counterbore_diameter=26, counterbore_depth=3, cx=0, cy=0, through=True)
    .pocket(width=16, length=105, depth=1.315, cx=0, cy=0)
    .threaded_hole(diameter=4, depth=25, cx=-19.5, cy=0)
    .threaded_hole(diameter=4, depth=25, cx=18.5, cy=0)
    .slot(length=113, width=3, depth=50, cx=0, cy=0, through=True)
)
