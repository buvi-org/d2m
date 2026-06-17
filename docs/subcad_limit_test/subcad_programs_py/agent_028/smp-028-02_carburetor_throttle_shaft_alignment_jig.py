# Requirement: SMP-028-02
# Source agent: 028
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_028_small_engine_service_hardware_single_metal_parts.json
# Part: Carburetor Throttle Shaft Alignment Jig - single metal part
# Raw idea: Carburetor Throttle Shaft Alignment Jig
# Status: draft_unexecuted
#
# Coverage notes:
# - Created cylindrical round-bar stock at OD 72 mm x length 34 mm using material steel_a36.
# - Machine a centered through bore diameter 14 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
# - Added one axial counterbore-depth turn_id operation for the specified end counterbore size.
# - Added a shallow top pocket approximation for the longitudinal reference flat.
# - Added two threaded-hole placeholders at the specified axial stations.
# - Added a full-length slot placeholder for the split relief slit.
# - Applied a 1.0 mm chamfer operation for outside circular-edge treatment.
#
# Known gaps:
# - Requirement datum uses cylinder axis as X; Stock.cylindrical/turning operations are used as the closest axial representation and orientation should be reviewed after execution.
# - Bore mouth chamfers are covered only by the later general chamfer, not separate internal bore-mouth chamfers.
# - Add shallow concentric counterbores on both ends, diameter 24 mm x 3 mm deep. Counterbores are required on both ends; this draft can only express a generic/one-end axial ID enlargement without end selection.
# - Mill one longitudinal flat 24 mm wide over 26 mm of length, centered on the top side. A true milled tangent flat on cylindrical OD is approximated by a top pocket/flat cut.
# - Add two radial tapped M7 holes through the top flat at X=11 mm and X=22 mm. Exact radial orientation through the top flat is approximated with top-face threaded_hole operations.
# - Cut one full-length radial slit 4 mm wide from the outside to the axial bore on datum-B side. Exact radial slit from OD to axial bore is approximated as a full-depth top slot.
# - Internal bore-edge chamfers are not individually selected; general chamfer may not reach every required bore/counterbore mouth.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Radial and longitudinal secondary features on round stock are draft approximations until execution artifacts are inspected.

from subcad import Stock

part = (
    Stock.cylindrical(72, 34, material="steel_a36")
    .turn_id(diameter=14, depth=34)
    .turn_id(diameter=24, depth=3)
    .pocket(width=24, length=26, depth=2.059, cx=0, cy=0, corner_radius=0)
    .threaded_hole(diameter=7, depth=36, cx=-6, cy=0)
    .threaded_hole(diameter=7, depth=36, cx=5, cy=0)
    .slot(length=34, width=4, depth=72, cx=0, cy=0)
)
