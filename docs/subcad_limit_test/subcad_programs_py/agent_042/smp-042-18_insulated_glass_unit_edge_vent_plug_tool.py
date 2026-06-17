# Requirement: SMP-042-18
# Source agent: 042
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_042_glass_handling_hardware_single_metal_parts.json
# Part: Insulated Glass Unit Edge Vent Plug Tool - single metal part
# Raw idea: Insulated Glass Unit Edge Vent Plug Tool
# Status: draft_unexecuted
#
# Coverage notes:
# - cylindrical round-bar stock OD 40 mm x length 31 mm using steel_1045
# - centered axial through bore diameter 8 mm
# - concentric end counterbore diameter 18 mm x 3 mm deep from one accessible end
# - longitudinal milled flat proxy 13 mm wide over 23 mm length
# - two M5 radial tapped-hole placeholders at axial X=10 and X=20
# - full-length split relief slit placeholder width 6 mm
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
    Stock.cylindrical(40, 31, material="steel_1045")
    .mill_turn_setup(axis="Z")
    .turn_id(diameter=8, depth=31)
    .turn_id(diameter=18, depth=3)
    .pocket(width=13, length=23, depth=1.086, cx=0, cy=0)
    .threaded_hole(diameter=5, depth=20, cx=-5.5, cy=0)
    .threaded_hole(diameter=5, depth=20, cx=4.5, cy=0)
    .slot(length=31, width=6, depth=40, cx=0, cy=0, through=True)
)
