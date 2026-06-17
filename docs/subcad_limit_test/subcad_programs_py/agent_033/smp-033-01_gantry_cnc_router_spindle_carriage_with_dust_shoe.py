# Requirement: SMP-033-01
# Source agent: 033
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_033_woodworking_machines_single_metal_parts.json
# Part: Gantry CNC router spindle carriage with dust shoe - single metal part
# Raw idea: Gantry CNC router spindle carriage with dust shoe
# Status: draft_unexecuted
#
# Coverage notes:
# - Created cylindrical round-bar stock at OD 29 mm x length 93 mm using material steel_a36.
# - Machine a centered through bore diameter 8 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
# - Added one axial counterbore-depth turn_id operation for the specified end counterbore size.
# - Added a shallow top pocket approximation for the longitudinal reference flat.
# - Added two threaded-hole placeholders at the specified axial stations.
# - Added a full-length slot placeholder for the split relief slit.
# - Applied a 1.0 mm chamfer operation for outside circular-edge treatment.
# - Added a middle-length flat-cut placeholder for opposed wrench flats.
#
# Known gaps:
# - Requirement datum uses cylinder axis as X; Stock.cylindrical/turning operations are used as the closest axial representation and orientation should be reviewed after execution.
# - Bore mouth chamfers are covered only by the later general chamfer, not separate internal bore-mouth chamfers.
# - Add shallow concentric counterbores on both ends, diameter 18 mm x 3 mm deep. Counterbores are required on both ends; this draft can only express a generic/one-end axial ID enlargement without end selection.
# - Mill one longitudinal flat 9 mm wide over 85 mm of length, centered on the top side. A true milled tangent flat on cylindrical OD is approximated by a top pocket/flat cut.
# - Add two radial tapped M8 holes through the top flat at X=31 mm and X=62 mm. Exact radial orientation through the top flat is approximated with top-face threaded_hole operations.
# - Cut one full-length radial slit 3 mm wide from the outside to the axial bore on datum-B side. Exact radial slit from OD to axial bore is approximated as a full-depth top slot.
# - Internal bore-edge chamfers are not individually selected; general chamfer may not reach every required bore/counterbore mouth.
# - Mill two opposed flats across the outside, leaving 22 mm across flats over the middle third of the length. True opposed flats with two-sided OD removal are approximated by one top pocket/flat.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Radial and longitudinal secondary features on round stock are draft approximations until execution artifacts are inspected.

from subcad import Stock

part = (
    Stock.cylindrical(29, 93, material="steel_a36")
    .turn_id(diameter=8, depth=93)
    .turn_id(diameter=18, depth=3)
    .pocket(width=9, length=85, depth=0.716, cx=0, cy=0, corner_radius=0)
    .threaded_hole(diameter=8, depth=14.5, cx=-15.5, cy=0)
    .threaded_hole(diameter=8, depth=14.5, cx=15.5, cy=0)
    .slot(length=93, width=3, depth=29, cx=0, cy=0)
    .pocket(width=22, length=31, depth=3.5, cx=0, cy=0, corner_radius=0)
)
