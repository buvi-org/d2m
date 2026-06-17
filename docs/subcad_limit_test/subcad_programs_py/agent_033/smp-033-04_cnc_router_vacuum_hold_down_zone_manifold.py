# Requirement: SMP-033-04
# Source agent: 033
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_033_woodworking_machines_single_metal_parts.json
# Part: CNC router vacuum hold-down zone manifold - single metal part
# Raw idea: CNC router vacuum hold-down zone manifold
# Status: draft_unexecuted
#
# Coverage notes:
# - Created cylindrical round-bar stock at OD 55 mm x length 108 mm using material steel_a36.
# - Machine a centered through bore diameter 18 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
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
# - Add shallow concentric counterbores on both ends, diameter 28 mm x 3 mm deep. Counterbores are required on both ends; this draft can only express a generic/one-end axial ID enlargement without end selection.
# - Mill one longitudinal flat 18 mm wide over 100 mm of length, centered on the top side. A true milled tangent flat on cylindrical OD is approximated by a top pocket/flat cut.
# - Add two radial tapped M5 holes through the top flat at X=36 mm and X=72 mm. Exact radial orientation through the top flat is approximated with top-face threaded_hole operations.
# - Cut one full-length radial slit 6 mm wide from the outside to the axial bore on datum-B side. Exact radial slit from OD to axial bore is approximated as a full-depth top slot.
# - Internal bore-edge chamfers are not individually selected; general chamfer may not reach every required bore/counterbore mouth.
# - Mill two opposed flats across the outside, leaving 47 mm across flats over the middle third of the length. True opposed flats with two-sided OD removal are approximated by one top pocket/flat.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Radial and longitudinal secondary features on round stock are draft approximations until execution artifacts are inspected.

from subcad import Stock

part = (
    Stock.cylindrical(55, 108, material="steel_a36")
    .turn_id(diameter=18, depth=108)
    .turn_id(diameter=28, depth=3)
    .pocket(width=18, length=100, depth=1.514, cx=0, cy=0, corner_radius=0)
    .threaded_hole(diameter=5, depth=27.5, cx=-18, cy=0)
    .threaded_hole(diameter=5, depth=27.5, cx=18, cy=0)
    .slot(length=108, width=6, depth=55, cx=0, cy=0)
    .pocket(width=47, length=36, depth=4, cx=0, cy=0, corner_radius=0)
)
