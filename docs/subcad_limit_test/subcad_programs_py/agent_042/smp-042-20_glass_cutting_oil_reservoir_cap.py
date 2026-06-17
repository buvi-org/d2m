# Requirement: SMP-042-20
# Source agent: 042
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_042_glass_handling_hardware_single_metal_parts.json
# Part: Glass Cutting Oil Reservoir Cap - single metal part
# Raw idea: Glass Cutting Oil Reservoir Cap
# Status: draft_unexecuted
#
# Coverage notes:
# - cylindrical round-bar stock OD 30 mm x length 58 mm using steel_a36
# - centered axial through bore diameter 8 mm
# - concentric end counterbore diameter 18 mm x 3 mm deep from one accessible end
# - longitudinal milled flat proxy 10 mm wide over 50 mm length
# - two M8 radial tapped-hole placeholders at axial X=19 and X=38
# - full-length split relief slit placeholder width 3 mm
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
    Stock.cylindrical(30, 58, material="steel_a36")
    .mill_turn_setup(axis="Z")
    .turn_id(diameter=8, depth=58)
    .turn_id(diameter=18, depth=3)
    .pocket(width=10, length=50, depth=0.858, cx=0, cy=0)
    .threaded_hole(diameter=8, depth=15, cx=-10, cy=0)
    .threaded_hole(diameter=8, depth=15, cx=9, cy=0)
    .slot(length=58, width=3, depth=30, cx=0, cy=0, through=True)
)
