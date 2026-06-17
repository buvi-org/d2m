# Requirement: SMP-041-16
# Source agent: 041
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_041_apparel_production_fixtures_single_metal_parts.json
# Part: Apparel Fixture Quick-Change Baseplate - single metal part
# Raw idea: Apparel Fixture Quick-Change Baseplate
# Status: draft_unexecuted
#
# Coverage notes:
# - cylindrical round-bar stock OD 60 mm x length 54 mm using steel_1045
# - centered axial through bore diameter 20 mm
# - concentric end counterbore diameter 30 mm x 3 mm deep from one accessible end
# - longitudinal milled flat proxy 20 mm wide over 46 mm length
# - two M5 radial tapped-hole placeholders at axial X=18 and X=36
# - full-length split relief slit placeholder width 4 mm
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
    Stock.cylindrical(60, 54, material="steel_1045")
    .mill_turn_setup(axis="Z")
    .turn_id(diameter=20, depth=54)
    .turn_id(diameter=30, depth=3)
    .pocket(width=20, length=46, depth=1.716, cx=0, cy=0)
    .threaded_hole(diameter=5, depth=30, cx=-9, cy=0)
    .threaded_hole(diameter=5, depth=30, cx=9, cy=0)
    .slot(length=54, width=4, depth=60, cx=0, cy=0, through=True)
)
