# Requirement: SMP-040-16
# Source agent: 040
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_040_kiosk_payment_hardware_single_metal_parts.json
# Part: Reverse vending bottle entry throat - single metal part
# Raw idea: Reverse vending bottle entry throat
# Status: draft_unexecuted
#
# Coverage notes:
# - cylindrical round-bar stock OD 72 mm x length 80 mm using steel_1045
# - centered axial through bore diameter 14 mm
# - concentric end counterbore diameter 24 mm x 3 mm deep from one accessible end
# - longitudinal milled flat proxy 24 mm wide over 72 mm length
# - two M8 radial tapped-hole placeholders at axial X=26 and X=53
# - full-length split relief slit placeholder width 5 mm
# - 1.0 mm outside circular-edge chamfer pass
#
# Known gaps:
# - Requirement calls for 4140 alloy steel, prehard; allowed Stage 3 material keys do not include 4140, so this draft uses steel_1045 as the closest available steel key.
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
    Stock.cylindrical(72, 80, material="steel_1045")
    .mill_turn_setup(axis="Z")
    .turn_id(diameter=14, depth=80)
    .turn_id(diameter=24, depth=3)
    .pocket(width=24, length=72, depth=2.059, cx=0, cy=0)
    .threaded_hole(diameter=8, depth=36, cx=-14, cy=0)
    .threaded_hole(diameter=8, depth=36, cx=13, cy=0)
    .slot(length=80, width=5, depth=72, cx=0, cy=0, through=True)
)
