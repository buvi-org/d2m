# Requirement: SMP-035-04
# Source agent: 035
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_035_electronics_manufacturing_single_metal_parts.json
# Part: Pogo-Pin Programming Fixture for Panelized PCBs - single metal part
# Raw idea: Pogo-Pin Programming Fixture for Panelized PCBs
# Status: draft_unexecuted
#
# Coverage notes:
# - Created cylindrical round-bar stock at OD 31 mm x length 29 mm using material steel_a36.
# - Machine a centered through bore diameter 8 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
# - Added one axial counterbore-depth turn_id operation for the specified end counterbore size.
# - Added a shallow top pocket approximation for the longitudinal reference flat.
# - Added two threaded-hole placeholders at the specified axial stations.
# - Added a full-length slot placeholder for the split relief slit.
# - Applied a 1.0 mm chamfer operation for outside circular-edge treatment.
# - Machine one transverse slot 4 mm wide across the top flat at X=14 mm, depth 3 mm.
#
# Known gaps:
# - Requirement datum uses cylinder axis as X; Stock.cylindrical/turning operations are used as the closest axial representation and orientation should be reviewed after execution.
# - Bore mouth chamfers are covered only by the later general chamfer, not separate internal bore-mouth chamfers.
# - Add shallow concentric counterbores on both ends, diameter 18 mm x 3 mm deep. Counterbores are required on both ends; this draft can only express a generic/one-end axial ID enlargement without end selection.
# - Mill one longitudinal flat 10 mm wide over 21 mm of length, centered on the top side. A true milled tangent flat on cylindrical OD is approximated by a top pocket/flat cut.
# - Add two radial tapped M5 holes through the top flat at X=9 mm and X=19 mm. Exact radial orientation through the top flat is approximated with top-face threaded_hole operations.
# - Cut one full-length radial slit 2 mm wide from the outside to the axial bore on datum-B side. Exact radial slit from OD to axial bore is approximated as a full-depth top slot.
# - Internal bore-edge chamfers are not individually selected; general chamfer may not reach every required bore/counterbore mouth.
# - Cross relief slot is approximated as a transverse top slot on cylindrical stock.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Radial and longitudinal secondary features on round stock are draft approximations until execution artifacts are inspected.

from subcad import Stock

part = (
    Stock.cylindrical(31, 29, material="steel_a36")
    .turn_id(diameter=8, depth=29)
    .turn_id(diameter=18, depth=3)
    .pocket(width=10, length=21, depth=0.829, cx=0, cy=0, corner_radius=0)
    .threaded_hole(diameter=5, depth=15.5, cx=-5.5, cy=0)
    .threaded_hole(diameter=5, depth=15.5, cx=4.5, cy=0)
    .slot(length=29, width=2, depth=31, cx=0, cy=0)
    .slot(length=31, width=4, depth=3, angle=90, cx=-0.5, cy=0)
)
