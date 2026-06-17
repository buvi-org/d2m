# Requirement: SMP-041-22
# Source agent: 041
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_041_apparel_production_fixtures_single_metal_parts.json
# Part: Zipper Tape Feed Cassette - single metal part
# Raw idea: Zipper Tape Feed Cassette
# Status: draft_unexecuted
#
# Coverage notes:
# - cylindrical round-bar stock OD 67 mm x length 34 mm using steel_a36
# - centered axial through bore diameter 22 mm
# - concentric end counterbore diameter 32 mm x 3 mm deep from one accessible end
# - longitudinal milled flat proxy 22 mm wide over 26 mm length
# - two M8 radial tapped-hole placeholders at axial X=11 and X=22
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
    Stock.cylindrical(67, 34, material="steel_a36")
    .mill_turn_setup(axis="Z")
    .turn_id(diameter=22, depth=34)
    .turn_id(diameter=32, depth=3)
    .pocket(width=22, length=26, depth=1.857, cx=0, cy=0)
    .threaded_hole(diameter=8, depth=33.5, cx=-6, cy=0)
    .threaded_hole(diameter=8, depth=33.5, cx=5, cy=0)
    .slot(length=34, width=6, depth=67, cx=0, cy=0, through=True)
)
