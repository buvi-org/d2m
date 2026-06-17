# Requirement: SMP-038-24
# Source agent: 038
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_038_dental_lab_fixtures_single_metal_parts.json
# Part: Orthodontic Appliance Soldering Jig - single metal part
# Raw idea: Orthodontic Appliance Soldering Jig
# Status: draft_unexecuted
#
# Coverage notes:
# - Created cylindrical stock OD 89 x length 51 mm in steel_a36.
# - Machined centered axial through bore diameter 17 mm along the full length using turn_id.
# - Modeled one concentric end counterbore diameter 27 mm x 3 mm deep.
# - Added an approximate transverse groove for the cross relief slot width 5 mm and depth 8 mm.
# - Applied 1.0 mm general chamfer operation to outside circular edges where supported.
#
# Known gaps:
# - Bore-mouth 1.0 mm x 45 degree chamfers are not individually represented; only a general chamfer operation is included.
# - Requirement calls for counterbores on both ends; current SubCAD chain models only one accessible end counterbore.
# - Cross relief slot placement on a milled longitudinal flat is approximate because this cylindrical draft does not establish that side flat as a machinable setup plane.
# - Longitudinal milled reference flat on the cylinder side is not represented exactly by current top/end-face fluent operations.
# - Radial tapped M8 holes at axial X=17 and X=34 mm through the top flat are not represented; top-face threaded_hole does not express radial side drilling on the cylindrical surface.
# - Full-length radial split relief slit from OD to bore is not represented exactly.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft cylindrical program is not executed; check whether Stock.cylindrical axis/orientation matches the requirement datum during Stage 4.

from subcad import Stock

part = (
    Stock.cylindrical(89, 51, material="steel_a36")
    .turn_id(diameter=17, depth=51)
    .counterbore(hole_diameter=17, counterbore_diameter=27, counterbore_depth=3, cx=0, cy=0)
    .groove(length=89, width=5, depth=8, cx=0, cy=-0.5)
)
