# Requirement: SMP-030-09
# Source agent: 030
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_030_appliance_repair_hardware_single_metal_parts.json
# Part: Washer Suspension Rod Calibration Clamp - single metal part
# Raw idea: Washer Suspension Rod Calibration Clamp
# Status: draft_unexecuted
#
# Coverage notes:
# - Created cylindrical round-bar stock at OD 87 mm x length 84 mm using material steel_1045.
# - Machine a centered through bore diameter 17 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
# - Added one axial counterbore-depth turn_id operation for the specified end counterbore size.
# - Added a shallow top pocket approximation for the longitudinal reference flat.
# - Added two threaded-hole placeholders at the specified axial stations.
# - Added a full-length slot placeholder for the split relief slit.
# - Applied a 1.0 mm chamfer operation for outside circular-edge treatment.
#
# Known gaps:
# - Requirement datum uses cylinder axis as X; Stock.cylindrical/turning operations are used as the closest axial representation and orientation should be reviewed after execution.
# - Bore mouth chamfers are covered only by the later general chamfer, not separate internal bore-mouth chamfers.
# - Add shallow concentric counterbores on both ends, diameter 27 mm x 3 mm deep. Counterbores are required on both ends; this draft can only express a generic/one-end axial ID enlargement without end selection.
# - Mill one longitudinal flat 29 mm wide over 76 mm of length, centered on the top side. A true milled tangent flat on cylindrical OD is approximated by a top pocket/flat cut.
# - Add two radial tapped M4 holes through the top flat at X=28 mm and X=56 mm. Exact radial orientation through the top flat is approximated with top-face threaded_hole operations.
# - Cut one full-length radial slit 4 mm wide from the outside to the axial bore on datum-B side. Exact radial slit from OD to axial bore is approximated as a full-depth top slot.
# - Internal bore-edge chamfers are not individually selected; general chamfer may not reach every required bore/counterbore mouth.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Radial and longitudinal secondary features on round stock are draft approximations until execution artifacts are inspected.

from subcad import Stock

part = (
    Stock.cylindrical(87, 84, material="steel_1045")
    .turn_id(diameter=17, depth=84)
    .turn_id(diameter=27, depth=3)
    .pocket(width=29, length=76, depth=2.488, cx=0, cy=0, corner_radius=0)
    .threaded_hole(diameter=4, depth=43.5, cx=-14, cy=0)
    .threaded_hole(diameter=4, depth=43.5, cx=14, cy=0)
    .slot(length=84, width=4, depth=87, cx=0, cy=0)
)
