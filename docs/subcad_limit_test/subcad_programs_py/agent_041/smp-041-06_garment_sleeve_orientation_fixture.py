# Requirement: SMP-041-06
# Source agent: 041
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_041_apparel_production_fixtures_single_metal_parts.json
# Part: Garment Sleeve Orientation Fixture - single metal part
# Raw idea: Garment Sleeve Orientation Fixture
# Status: draft_unexecuted
#
# Coverage notes:
# - cylindrical round-bar stock OD 94 mm x length 80 mm using aluminum_6061
# - centered axial through bore diameter 23 mm
# - concentric end counterbore diameter 33 mm x 3 mm deep from one accessible end
# - longitudinal milled flat proxy 31 mm wide over 72 mm length
# - two M4 radial tapped-hole placeholders at axial X=26 and X=53
# - full-length split relief slit placeholder width 6 mm
# - opposed wrench flat proxy over middle third, target across-flats 86 mm
# - 1.0 mm outside circular-edge chamfer pass
#
# Known gaps:
# - Two opposed wrench flats are approximated with one top pocket operation; the opposite flat is not separately oriented.
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
    Stock.cylindrical(94, 80, material="aluminum_6061")
    .mill_turn_setup(axis="Z")
    .turn_id(diameter=23, depth=80)
    .turn_id(diameter=33, depth=3)
    .pocket(width=31, length=72, depth=2.629, cx=0, cy=0)
    .threaded_hole(diameter=4, depth=47, cx=-14, cy=0)
    .threaded_hole(diameter=4, depth=47, cx=13, cy=0)
    .slot(length=80, width=6, depth=94, cx=0, cy=0, through=True)
    .pocket(width=94, length=26.667, depth=4, cx=0, cy=0)
)
