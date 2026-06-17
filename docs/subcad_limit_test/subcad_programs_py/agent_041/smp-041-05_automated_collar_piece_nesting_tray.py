# Requirement: SMP-041-05
# Source agent: 041
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_041_apparel_production_fixtures_single_metal_parts.json
# Part: Automated Collar Piece Nesting Tray - single metal part
# Raw idea: Automated Collar Piece Nesting Tray
# Status: draft_unexecuted
#
# Coverage notes:
# - cylindrical round-bar stock OD 40 mm x length 65 mm using steel_a36
# - centered axial through bore diameter 13 mm
# - concentric end counterbore diameter 23 mm x 3 mm deep from one accessible end
# - longitudinal milled flat proxy 13 mm wide over 57 mm length
# - two M7 radial tapped-hole placeholders at axial X=21 and X=43
# - full-length split relief slit placeholder width 4 mm
# - transverse relief slot proxy width 6 mm at axial X=32, depth 4 mm
# - 1.0 mm outside circular-edge chamfer pass
#
# Known gaps:
# - Transverse relief slot is represented as a top-face slot on cylindrical stock, not a fully oriented side mill operation.
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
    Stock.cylindrical(40, 65, material="steel_a36")
    .mill_turn_setup(axis="Z")
    .turn_id(diameter=13, depth=65)
    .turn_id(diameter=23, depth=3)
    .pocket(width=13, length=57, depth=1.086, cx=0, cy=0)
    .threaded_hole(diameter=7, depth=20, cx=-11.5, cy=0)
    .threaded_hole(diameter=7, depth=20, cx=10.5, cy=0)
    .slot(length=65, width=4, depth=40, cx=0, cy=0, through=True)
    .slot(length=40, width=6, depth=4, angle=90, cx=-0.5, cy=0)
)
