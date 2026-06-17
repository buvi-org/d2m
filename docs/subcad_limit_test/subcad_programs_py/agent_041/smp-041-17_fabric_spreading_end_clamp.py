# Requirement: SMP-041-17
# Source agent: 041
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_041_apparel_production_fixtures_single_metal_parts.json
# Part: Fabric Spreading End Clamp - single metal part
# Raw idea: Fabric Spreading End Clamp
# Status: draft_unexecuted
#
# Coverage notes:
# - cylindrical round-bar stock OD 57 mm x length 59 mm using steel_1045
# - centered axial through bore diameter 11 mm
# - concentric end counterbore diameter 21 mm x 3 mm deep from one accessible end
# - longitudinal milled flat proxy 19 mm wide over 51 mm length
# - two M7 radial tapped-hole placeholders at axial X=19 and X=39
# - full-length split relief slit placeholder width 6 mm
# - 1.0 mm outside circular-edge chamfer pass
#
# Known gaps:
# - Requirement datum uses cylinder axis as X; Stock.cylindrical/turning operations use the native cylindrical axis and should be orientation-reviewed after execution.
# - Counterbores are required on both ends; this draft only expresses a generic one-end axial ID enlargement without end selection.
# - True tangent flat on cylindrical OD is approximated by a rectangular top pocket/chord cut.
# - Radial tapped holes through the top flat are approximated with top-face threaded_hole operations.
# - Split slit from outside to axial bore is approximated by a full top-face slot.
# - Internal bore-mouth chamfers are not separately targeted; only the later general chamfer is included.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated from frozen Stage 2 requirement and not executed or visually compared yet.
# - Rectangular/sheet X/Y feature placement uses drill_at/slot_at/pocket_at datum offsets from the lower-left requirement origin where applicable.

from subcad import Stock

part = (
    Stock.cylindrical(57, 59, material="steel_1045")
    .mill_turn_setup(axis="Z")
    .turn_id(diameter=11, depth=59)
    .turn_id(diameter=21, depth=3)
    .pocket(width=19, length=51, depth=1.63, cx=0, cy=0)
    .threaded_hole(diameter=7, depth=28.5, cx=-10.5, cy=0)
    .threaded_hole(diameter=7, depth=28.5, cx=9.5, cy=0)
    .slot(length=59, width=6, depth=57, cx=0, cy=0, through=True)
)
