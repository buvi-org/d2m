# Requirement: SMP-037-23
# Source agent: 037
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_037_construction_tools_single_metal_parts.json
# Part: Chalk line corner wrap guide - single metal part
# Raw idea: Chalk line corner wrap guide
# Status: draft_unexecuted
#
# Coverage notes:
# - Created cylindrical stock OD 50 x length 105 mm in steel_a36.
# - Machined centered axial through bore diameter 12 mm along the full length using turn_id.
# - Modeled one concentric end counterbore diameter 22 mm x 3 mm deep.
# - Added an approximate transverse groove for the cross relief slot width 6 mm and depth 5 mm.
# - Applied 1.0 mm general chamfer operation to outside circular edges where supported.
#
# Known gaps:
# - Bore-mouth 1.0 mm x 45 degree chamfers are not individually represented; only a general chamfer operation is included.
# - Requirement calls for counterbores on both ends; current SubCAD chain models only one accessible end counterbore.
# - Cross relief slot placement on a milled longitudinal flat is approximate because this cylindrical draft does not establish that side flat as a machinable setup plane.
# - Longitudinal milled reference flat on the cylinder side is not represented exactly by current top/end-face fluent operations.
# - Radial tapped M7 holes at axial X=35 and X=70 mm through the top flat are not represented; top-face threaded_hole does not express radial side drilling on the cylindrical surface.
# - Full-length radial split relief slit from OD to bore is not represented exactly.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft cylindrical program is not executed; check whether Stock.cylindrical axis/orientation matches the requirement datum during Stage 4.

from subcad import Stock

part = (
    Stock.cylindrical(50, 105, material="steel_a36")
    .turn_id(diameter=12, depth=105)
    .counterbore(hole_diameter=12, counterbore_diameter=22, counterbore_depth=3, cx=0, cy=0)
    .groove(length=50, width=6, depth=5, cx=0, cy=-0.5)
)
