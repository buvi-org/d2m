# Requirement: SMP-041-19
# Source agent: 041
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_041_apparel_production_fixtures_single_metal_parts.json
# Part: Conveyorized Garment Sleeve Turner - single metal part
# Raw idea: Conveyorized Garment Sleeve Turner
# Status: draft_unexecuted
#
# Coverage notes:
# - cylindrical round-bar stock OD 56 mm x length 110 mm using steel_a36
# - centered axial through bore diameter 14 mm
# - concentric end counterbore diameter 24 mm x 3 mm deep from one accessible end
# - longitudinal milled flat proxy 18 mm wide over 102 mm length
# - two M4 radial tapped-hole placeholders at axial X=36 and X=73
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
    Stock.cylindrical(56, 110, material="steel_a36")
    .mill_turn_setup(axis="Z")
    .turn_id(diameter=14, depth=110)
    .turn_id(diameter=24, depth=3)
    .pocket(width=18, length=102, depth=1.486, cx=0, cy=0)
    .threaded_hole(diameter=4, depth=28, cx=-19, cy=0)
    .threaded_hole(diameter=4, depth=28, cx=18, cy=0)
    .slot(length=110, width=2, depth=56, cx=0, cy=0, through=True)
)
