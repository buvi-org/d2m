# Requirement: SMP-029-06
# Source agent: 029
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_029_pet_veterinary_hardware_single_metal_parts.json
# Part: Quiet Nail Grinder Depth Guard - single metal part
# Raw idea: Quiet Nail Grinder Depth Guard
# Status: draft_unexecuted
#
# Coverage notes:
# - Created cylindrical round-bar stock at OD 44 mm x length 85 mm using material steel_1045.
# - Machine a centered through bore diameter 11 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
# - Added one axial counterbore-depth turn_id operation for the specified end counterbore size.
# - Added a shallow top pocket approximation for the longitudinal reference flat.
# - Added two threaded-hole placeholders at the specified axial stations.
# - Added a full-length slot placeholder for the split relief slit.
# - Applied a 1.0 mm chamfer operation for outside circular-edge treatment.
#
# Known gaps:
# - Requirement datum uses cylinder axis as X; Stock.cylindrical/turning operations are used as the closest axial representation and orientation should be reviewed after execution.
# - Bore mouth chamfers are covered only by the later general chamfer, not separate internal bore-mouth chamfers.
# - Add shallow concentric counterbores on both ends, diameter 21 mm x 3 mm deep. Counterbores are required on both ends; this draft can only express a generic/one-end axial ID enlargement without end selection.
# - Mill one longitudinal flat 14 mm wide over 77 mm of length, centered on the top side. A true milled tangent flat on cylindrical OD is approximated by a top pocket/flat cut.
# - Add two radial tapped M5 holes through the top flat at X=28 mm and X=56 mm. Exact radial orientation through the top flat is approximated with top-face threaded_hole operations.
# - Cut one full-length radial slit 2 mm wide from the outside to the axial bore on datum-B side. Exact radial slit from OD to axial bore is approximated as a full-depth top slot.
# - Internal bore-edge chamfers are not individually selected; general chamfer may not reach every required bore/counterbore mouth.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Radial and longitudinal secondary features on round stock are draft approximations until execution artifacts are inspected.

from subcad import Stock

part = (
    Stock.cylindrical(44, 85, material="steel_1045")
    .turn_id(diameter=11, depth=85)
    .turn_id(diameter=21, depth=3)
    .pocket(width=14, length=77, depth=1.143, cx=0, cy=0, corner_radius=0)
    .threaded_hole(diameter=5, depth=22, cx=-14.5, cy=0)
    .threaded_hole(diameter=5, depth=22, cx=13.5, cy=0)
    .slot(length=85, width=2, depth=44, cx=0, cy=0)
)
