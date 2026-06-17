# Requirement: SMP-030-10
# Source agent: 030
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_030_appliance_repair_hardware_single_metal_parts.json
# Part: Refrigerator Compressor Foot Leveling Spacer - single metal part
# Raw idea: Refrigerator Compressor Foot Leveling Spacer
# Status: draft_unexecuted
#
# Coverage notes:
# - Created cylindrical round-bar stock at OD 49 mm x length 41 mm using material steel_1045.
# - Machine a centered through bore diameter 12 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
# - Added one axial counterbore-depth turn_id operation for the specified end counterbore size.
# - Added a shallow top pocket approximation for the longitudinal reference flat.
# - Added two threaded-hole placeholders at the specified axial stations.
# - Added a full-length slot placeholder for the split relief slit.
# - Applied a 1.0 mm chamfer operation for outside circular-edge treatment.
# - Machine one transverse slot 4 mm wide across the top flat at X=20 mm, depth 4 mm.
#
# Known gaps:
# - Requirement datum uses cylinder axis as X; Stock.cylindrical/turning operations are used as the closest axial representation and orientation should be reviewed after execution.
# - Bore mouth chamfers are covered only by the later general chamfer, not separate internal bore-mouth chamfers.
# - Add shallow concentric counterbores on both ends, diameter 22 mm x 3 mm deep. Counterbores are required on both ends; this draft can only express a generic/one-end axial ID enlargement without end selection.
# - Mill one longitudinal flat 16 mm wide over 33 mm of length, centered on the top side. A true milled tangent flat on cylindrical OD is approximated by a top pocket/flat cut.
# - Add two radial tapped M8 holes through the top flat at X=13 mm and X=27 mm. Exact radial orientation through the top flat is approximated with top-face threaded_hole operations.
# - Cut one full-length radial slit 2 mm wide from the outside to the axial bore on datum-B side. Exact radial slit from OD to axial bore is approximated as a full-depth top slot.
# - Internal bore-edge chamfers are not individually selected; general chamfer may not reach every required bore/counterbore mouth.
# - Cross relief slot is approximated as a transverse top slot on cylindrical stock.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Radial and longitudinal secondary features on round stock are draft approximations until execution artifacts are inspected.

from subcad import Stock

part = (
    Stock.cylindrical(49, 41, material="steel_1045")
    .turn_id(diameter=12, depth=41)
    .turn_id(diameter=22, depth=3)
    .pocket(width=16, length=33, depth=1.343, cx=0, cy=0, corner_radius=0)
    .threaded_hole(diameter=8, depth=24.5, cx=-7.5, cy=0)
    .threaded_hole(diameter=8, depth=24.5, cx=6.5, cy=0)
    .slot(length=41, width=2, depth=49, cx=0, cy=0)
    .slot(length=49, width=4, depth=4, angle=90, cx=-0.5, cy=0)
)
