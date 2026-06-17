# Requirement: SMP-003-04
# Source agent: 003
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_003_kitchen_food_mechanisms_single_metal_parts.json
# Part: Stand Mixer Planetary Gear Carrier - single metal part
# Raw idea: Stand Mixer Planetary Gear Carrier
# Status: draft_unexecuted
#
# Coverage notes:
# - cylindrical round-bar stock OD 64 mm x length 117 mm using steel_a36
# - centered axial through bore diameter 21 mm
# - concentric end counterbore diameter 31 mm x 3 mm deep
# - longitudinal milled flat 21 mm wide over 109 mm length
# - two M6 radial tapped clamp holes at axial X=39 and X=78
# - full-length split relief slit width 3 mm
# - transverse cross relief slot width 5 mm at axial X=58, depth 6 mm
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
    Stock.cylindrical(64, 117, material="steel_a36")
    .mill_turn_setup(axis="Z")
    .turn_id(diameter=21, depth=117)
    .counterbore(hole_diameter=21, counterbore_diameter=31, counterbore_depth=3, cx=0, cy=0, through=True)
    .pocket(width=21, length=109, depth=1.772, cx=0, cy=0)
    .threaded_hole(diameter=6, depth=32, cx=-19.5, cy=0)
    .threaded_hole(diameter=6, depth=32, cx=19.5, cy=0)
    .slot(length=117, width=3, depth=64, cx=0, cy=0, through=True)
    .slot(length=64, width=5, depth=6, angle=90, cx=-0.5, cy=0)
)
