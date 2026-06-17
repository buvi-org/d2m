# Requirement: SMP-002-10
# Source agent: 002
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_002_mobility_hardware_single_metal_parts.json
# Part: Manual wheelchair quick-release caster fork crown - single metal part
# Raw idea: Manual wheelchair quick-release caster fork crown
# Status: draft_unexecuted
#
# Coverage notes:
# - cylindrical round-bar stock OD 56 mm x length 53 mm using steel_a36
# - centered axial through bore diameter 14 mm
# - concentric end counterbore diameter 24 mm x 3 mm deep
# - longitudinal milled flat 18 mm wide over 45 mm length
# - two M8 radial tapped clamp holes at axial X=17 and X=35
# - full-length split relief slit width 2 mm
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
    Stock.cylindrical(56, 53, material="steel_a36")
    .mill_turn_setup(axis="Z")
    .turn_id(diameter=14, depth=53)
    .counterbore(hole_diameter=14, counterbore_diameter=24, counterbore_depth=3, cx=0, cy=0, through=True)
    .pocket(width=18, length=45, depth=1.486, cx=0, cy=0)
    .threaded_hole(diameter=8, depth=28, cx=-9.5, cy=0)
    .threaded_hole(diameter=8, depth=28, cx=8.5, cy=0)
    .slot(length=53, width=2, depth=56, cx=0, cy=0, through=True)
)
