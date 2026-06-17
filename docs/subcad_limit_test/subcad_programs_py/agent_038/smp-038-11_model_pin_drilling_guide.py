# Requirement: SMP-038-11
# Source agent: 038
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_038_dental_lab_fixtures_single_metal_parts.json
# Part: Model Pin Drilling Guide - single metal part
# Raw idea: Model Pin Drilling Guide
# Status: draft_unexecuted
#
# Coverage notes:
# - Created cylindrical stock OD 58 x length 97 mm in stainless_316.
# - Machined centered axial through bore diameter 14 mm along the full length using turn_id.
# - Modeled one concentric end counterbore diameter 24 mm x 3 mm deep.
# - Added an approximate transverse groove for the cross relief slot width 8 mm and depth 5 mm.
# - Applied 1.0 mm general chamfer operation to outside circular edges where supported.
#
# Known gaps:
# - Bore-mouth 1.0 mm x 45 degree chamfers are not individually represented; only a general chamfer operation is included.
# - Requirement calls for counterbores on both ends; current SubCAD chain models only one accessible end counterbore.
# - Cross relief slot placement on a milled longitudinal flat is approximate because this cylindrical draft does not establish that side flat as a machinable setup plane.
# - Longitudinal milled reference flat on the cylinder side is not represented exactly by current top/end-face fluent operations.
# - Radial tapped M4 holes at axial X=32 and X=64 mm through the top flat are not represented; top-face threaded_hole does not express radial side drilling on the cylindrical surface.
# - Full-length radial split relief slit from OD to bore is not represented exactly.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft cylindrical program is not executed; check whether Stock.cylindrical axis/orientation matches the requirement datum during Stage 4.

from subcad import Stock

part = (
    Stock.cylindrical(58, 97, material="stainless_316")
    .turn_id(diameter=14, depth=97)
    .counterbore(hole_diameter=14, counterbore_diameter=24, counterbore_depth=3, cx=0, cy=0)
    .groove(length=58, width=8, depth=5, cx=0, cy=-0.5)
)
