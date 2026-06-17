# Requirement: SMP-040-26
# Source agent: 040
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_040_kiosk_payment_hardware_single_metal_parts.json
# Part: Self-checkout kiosk bag hook bracket - single metal part
# Raw idea: Self-checkout kiosk bag hook bracket
# Status: draft_unexecuted
#
# Coverage notes:
# - cylindrical round-bar stock OD 39 mm x length 42 mm using aluminum_6061
# - centered axial through bore diameter 8 mm
# - concentric end counterbore diameter 18 mm x 3 mm deep from one accessible end
# - longitudinal milled flat proxy 13 mm wide over 34 mm length
# - two M6 radial tapped-hole placeholders at axial X=14 and X=28
# - full-length split relief slit placeholder width 2 mm
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
    Stock.cylindrical(39, 42, material="aluminum_6061")
    .mill_turn_setup(axis="Z")
    .turn_id(diameter=8, depth=42)
    .turn_id(diameter=18, depth=3)
    .pocket(width=13, length=34, depth=1.115, cx=0, cy=0)
    .threaded_hole(diameter=6, depth=19.5, cx=-7, cy=0)
    .threaded_hole(diameter=6, depth=19.5, cx=7, cy=0)
    .slot(length=42, width=2, depth=39, cx=0, cy=0, through=True)
)
