# Requirement: SMP-037-05
# Source agent: 037
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_037_construction_tools_single_metal_parts.json
# Part: Concrete edge screed rail bracket - single metal part
# Raw idea: Concrete edge screed rail bracket
# Status: draft_unexecuted
#
# Coverage notes:
# - Created cylindrical stock OD 48 x length 90 mm in stainless_316.
# - Machined centered axial through bore diameter 9 mm along the full length using turn_id.
# - Modeled one concentric end counterbore diameter 19 mm x 3 mm deep.
# - Added an approximate transverse groove for the cross relief slot width 5 mm and depth 4 mm.
# - Applied 1.0 mm general chamfer operation to outside circular edges where supported.
#
# Known gaps:
# - Bore-mouth 1.0 mm x 45 degree chamfers are not individually represented; only a general chamfer operation is included.
# - Requirement calls for counterbores on both ends; current SubCAD chain models only one accessible end counterbore.
# - Cross relief slot placement on a milled longitudinal flat is approximate because this cylindrical draft does not establish that side flat as a machinable setup plane.
# - Longitudinal milled reference flat on the cylinder side is not represented exactly by current top/end-face fluent operations.
# - Radial tapped M6 holes at axial X=30 and X=60 mm through the top flat are not represented; top-face threaded_hole does not express radial side drilling on the cylindrical surface.
# - Full-length radial split relief slit from OD to bore is not represented exactly.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft cylindrical program is not executed; check whether Stock.cylindrical axis/orientation matches the requirement datum during Stage 4.

from subcad import Stock

part = (
    Stock.cylindrical(48, 90, material="stainless_316")
    .turn_id(diameter=9, depth=90)
    .counterbore(hole_diameter=9, counterbore_diameter=19, counterbore_depth=3, cx=0, cy=0)
    .groove(length=48, width=5, depth=4, cx=0, cy=0)
)
