# Requirement: SMP-030-08
# Source agent: 030
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_030_appliance_repair_hardware_single_metal_parts.json
# Part: Dryer Drum Roller Axle Support Bracket - single metal part
# Raw idea: Dryer Drum Roller Axle Support Bracket
# Status: draft_unexecuted
#
# Coverage notes:
# - Created cylindrical round-bar stock at OD 69 mm x length 43 mm using material steel_a36.
# - Machine a centered through bore diameter 23 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
# - Added one axial counterbore-depth turn_id operation for the specified end counterbore size.
# - Added a shallow top pocket approximation for the longitudinal reference flat.
# - Added two threaded-hole placeholders at the specified axial stations.
# - Added a full-length slot placeholder for the split relief slit.
# - Applied a 1.0 mm chamfer operation for outside circular-edge treatment.
# - Machine one transverse slot 5 mm wide across the top flat at X=21 mm, depth 6 mm.
#
# Known gaps:
# - Requirement datum uses cylinder axis as X; Stock.cylindrical/turning operations are used as the closest axial representation and orientation should be reviewed after execution.
# - Bore mouth chamfers are covered only by the later general chamfer, not separate internal bore-mouth chamfers.
# - Add shallow concentric counterbores on both ends, diameter 33 mm x 3 mm deep. Counterbores are required on both ends; this draft can only express a generic/one-end axial ID enlargement without end selection.
# - Mill one longitudinal flat 23 mm wide over 35 mm of length, centered on the top side. A true milled tangent flat on cylindrical OD is approximated by a top pocket/flat cut.
# - Add two radial tapped M7 holes through the top flat at X=14 mm and X=28 mm. Exact radial orientation through the top flat is approximated with top-face threaded_hole operations.
# - Cut one full-length radial slit 3 mm wide from the outside to the axial bore on datum-B side. Exact radial slit from OD to axial bore is approximated as a full-depth top slot.
# - Internal bore-edge chamfers are not individually selected; general chamfer may not reach every required bore/counterbore mouth.
# - Cross relief slot is approximated as a transverse top slot on cylindrical stock.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Radial and longitudinal secondary features on round stock are draft approximations until execution artifacts are inspected.

from subcad import Stock

part = (
    Stock.cylindrical(69, 43, material="steel_a36")
    .turn_id(diameter=23, depth=43)
    .turn_id(diameter=33, depth=3)
    .pocket(width=23, length=35, depth=1.973, cx=0, cy=0, corner_radius=0)
    .threaded_hole(diameter=7, depth=34.5, cx=-7.5, cy=0)
    .threaded_hole(diameter=7, depth=34.5, cx=6.5, cy=0)
    .slot(length=43, width=3, depth=69, cx=0, cy=0)
    .slot(length=69, width=5, depth=6, angle=90, cx=-0.5, cy=0)
)
