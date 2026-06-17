# Requirement: SMP-031-07
# Source agent: 031
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_031_pumps_rotating_equipment_single_metal_parts.json
# Part: Rotating Equipment Shaft Alignment Target Bracket - single metal part
# Raw idea: Rotating Equipment Shaft Alignment Target Bracket
# Status: draft_unexecuted
#
# Coverage notes:
# - Created cylindrical round-bar stock at OD 79 mm x length 119 mm using material steel_a36.
# - Machine a centered through bore diameter 15 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
# - Added one axial counterbore-depth turn_id operation for the specified end counterbore size.
# - Added a shallow top pocket approximation for the longitudinal reference flat.
# - Added two threaded-hole placeholders at the specified axial stations.
# - Added a full-length slot placeholder for the split relief slit.
# - Applied a 1.0 mm chamfer operation for outside circular-edge treatment.
#
# Known gaps:
# - Requirement datum uses cylinder axis as X; Stock.cylindrical/turning operations are used as the closest axial representation and orientation should be reviewed after execution.
# - Bore mouth chamfers are covered only by the later general chamfer, not separate internal bore-mouth chamfers.
# - Add shallow concentric counterbores on both ends, diameter 25 mm x 3 mm deep. Counterbores are required on both ends; this draft can only express a generic/one-end axial ID enlargement without end selection.
# - Mill one longitudinal flat 26 mm wide over 111 mm of length, centered on the top side. A true milled tangent flat on cylindrical OD is approximated by a top pocket/flat cut.
# - Add two radial tapped M6 holes through the top flat at X=39 mm and X=79 mm. Exact radial orientation through the top flat is approximated with top-face threaded_hole operations.
# - Cut one full-length radial slit 2 mm wide from the outside to the axial bore on datum-B side. Exact radial slit from OD to axial bore is approximated as a full-depth top slot.
# - Internal bore-edge chamfers are not individually selected; general chamfer may not reach every required bore/counterbore mouth.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Radial and longitudinal secondary features on round stock are draft approximations until execution artifacts are inspected.

from subcad import Stock

part = (
    Stock.cylindrical(79, 119, material="steel_a36")
    .turn_id(diameter=15, depth=119)
    .turn_id(diameter=25, depth=3)
    .pocket(width=26, length=111, depth=2.201, cx=0, cy=0, corner_radius=0)
    .threaded_hole(diameter=6, depth=39.5, cx=-20.5, cy=0)
    .threaded_hole(diameter=6, depth=39.5, cx=19.5, cy=0)
    .slot(length=119, width=2, depth=79, cx=0, cy=0)
)
