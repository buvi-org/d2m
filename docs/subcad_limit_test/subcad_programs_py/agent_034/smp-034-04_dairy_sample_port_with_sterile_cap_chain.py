# Requirement: SMP-034-04
# Source agent: 034
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_034_sanitary_food_processing_single_metal_parts.json
# Part: Dairy Sample Port With Sterile Cap Chain - single metal part
# Raw idea: Dairy Sample Port With Sterile Cap Chain
# Status: draft_unexecuted
#
# Coverage notes:
# - Created cylindrical round-bar stock at OD 95 mm x length 35 mm using material steel_1045.
# - Machine a centered through bore diameter 23 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
# - Added one axial counterbore-depth turn_id operation for the specified end counterbore size.
# - Added a shallow top pocket approximation for the longitudinal reference flat.
# - Added two threaded-hole placeholders at the specified axial stations.
# - Added a full-length slot placeholder for the split relief slit.
# - Applied a 1.0 mm chamfer operation for outside circular-edge treatment.
#
# Known gaps:
# - Requirement calls for 4140 alloy steel prehard; draft maps it to allowed SubCAD material steel_1045.
# - Requirement datum uses cylinder axis as X; Stock.cylindrical/turning operations are used as the closest axial representation and orientation should be reviewed after execution.
# - Bore mouth chamfers are covered only by the later general chamfer, not separate internal bore-mouth chamfers.
# - Add shallow concentric counterbores on both ends, diameter 33 mm x 3 mm deep. Counterbores are required on both ends; this draft can only express a generic/one-end axial ID enlargement without end selection.
# - Mill one longitudinal flat 31 mm wide over 27 mm of length, centered on the top side. A true milled tangent flat on cylindrical OD is approximated by a top pocket/flat cut.
# - Add two radial tapped M4 holes through the top flat at X=11 mm and X=23 mm. Exact radial orientation through the top flat is approximated with top-face threaded_hole operations.
# - Cut one full-length radial slit 3 mm wide from the outside to the axial bore on datum-B side. Exact radial slit from OD to axial bore is approximated as a full-depth top slot.
# - Internal bore-edge chamfers are not individually selected; general chamfer may not reach every required bore/counterbore mouth.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Radial and longitudinal secondary features on round stock are draft approximations until execution artifacts are inspected.

from subcad import Stock

part = (
    Stock.cylindrical(95, 35, material="steel_1045")
    .turn_id(diameter=23, depth=35)
    .turn_id(diameter=33, depth=3)
    .pocket(width=31, length=27, depth=2.6, cx=0, cy=0, corner_radius=0)
    .threaded_hole(diameter=4, depth=47.5, cx=-6.5, cy=0)
    .threaded_hole(diameter=4, depth=47.5, cx=5.5, cy=0)
    .slot(length=35, width=3, depth=95, cx=0, cy=0)
)
