# Requirement: SMP-006-01
# Source agent: 006
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_006_automotive_service_tools_single_metal_parts.json
# Part: Brake Caliper Piston Wind-Back Adapter - single metal part
# Raw idea: Brake Caliper Piston Wind-Back Adapter
# Status: draft_unexecuted
#
# Coverage notes:
# - cylindrical round-bar stock OD 72 mm x length 88 mm using steel_a36
# - centered axial through bore diameter 24 mm
# - concentric end counterbore diameter 34 mm x 3 mm deep
# - longitudinal milled flat 24 mm wide over 80 mm length
# - two M6 radial tapped clamp holes at axial X=29 and X=58
# - full-length split relief slit width 4 mm
# - transverse cross relief slot width 6 mm at axial X=44, depth 7 mm
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
    Stock.cylindrical(72, 88, material="steel_a36")
    .mill_turn_setup(axis="Z")
    .turn_id(diameter=24, depth=88)
    .counterbore(hole_diameter=24, counterbore_diameter=34, counterbore_depth=3, cx=0, cy=0, through=True)
    .pocket(width=24, length=80, depth=2.059, cx=0, cy=0)
    .threaded_hole(diameter=6, depth=36, cx=-15, cy=0)
    .threaded_hole(diameter=6, depth=36, cx=14, cy=0)
    .slot(length=88, width=4, depth=72, cx=0, cy=0, through=True)
    .slot(length=72, width=6, depth=7, angle=90, cx=0, cy=0)
)
