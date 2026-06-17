# Requirement: SMP-008-05
# Source agent: 008
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_008_creator_rigging_hardware_single_metal_parts.json
# Part: Boom Pole Quick-Release Recorder Cradle - single metal part
# Raw idea: Boom Pole Quick-Release Recorder Cradle
# Status: draft_unexecuted
#
# Coverage notes:
# - cylindrical round-bar stock OD 71 mm x length 105 mm using steel_1045
# - centered axial through bore diameter 14 mm
# - concentric end counterbore diameter 24 mm x 3 mm deep
# - longitudinal milled flat 23 mm wide over 97 mm length
# - two M8 radial tapped clamp holes at axial X=35 and X=70
# - full-length split relief slit width 6 mm
# - transverse cross relief slot width 8 mm at axial X=52, depth 7 mm
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
    Stock.cylindrical(71, 105, material="steel_1045")
    .mill_turn_setup(axis="Z")
    .turn_id(diameter=14, depth=105)
    .counterbore(hole_diameter=14, counterbore_diameter=24, counterbore_depth=3, cx=0, cy=0, through=True)
    .pocket(width=23, length=97, depth=1.914, cx=0, cy=0)
    .threaded_hole(diameter=8, depth=35.5, cx=-17.5, cy=0)
    .threaded_hole(diameter=8, depth=35.5, cx=17.5, cy=0)
    .slot(length=105, width=6, depth=71, cx=0, cy=0, through=True)
    .slot(length=71, width=8, depth=7, angle=90, cx=-0.5, cy=0)
)
