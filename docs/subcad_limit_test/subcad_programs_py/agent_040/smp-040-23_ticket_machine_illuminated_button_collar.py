# Requirement: SMP-040-23
# Source agent: 040
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_040_kiosk_payment_hardware_single_metal_parts.json
# Part: Ticket machine illuminated button collar - single metal part
# Raw idea: Ticket machine illuminated button collar
# Status: draft_unexecuted
#
# Coverage notes:
# - cylindrical round-bar stock OD 49 mm x length 117 mm using steel_a36
# - centered axial through bore diameter 9 mm
# - concentric end counterbore diameter 19 mm x 3 mm deep from one accessible end
# - longitudinal milled flat proxy 16 mm wide over 109 mm length
# - two M4 radial tapped-hole placeholders at axial X=39 and X=78
# - full-length split relief slit placeholder width 5 mm
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
    Stock.cylindrical(49, 117, material="steel_a36")
    .mill_turn_setup(axis="Z")
    .turn_id(diameter=9, depth=117)
    .turn_id(diameter=19, depth=3)
    .pocket(width=16, length=109, depth=1.343, cx=0, cy=0)
    .threaded_hole(diameter=4, depth=24.5, cx=-19.5, cy=0)
    .threaded_hole(diameter=4, depth=24.5, cx=19.5, cy=0)
    .slot(length=117, width=5, depth=49, cx=0, cy=0, through=True)
)
