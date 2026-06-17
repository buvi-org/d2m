# Requirement: SMP-039-24
# Source agent: 039
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_039_marine_service_hardware_single_metal_parts.json
# Part: Impeller Vane Preload Sleeve - single metal part
# Raw idea: Impeller Vane Preload Sleeve
# Status: draft_unexecuted
#
# Coverage notes:
# - Created cylindrical stock OD 30 x length 74 mm in steel_a36.
# - Machined centered axial through bore diameter 8 mm along the full length using turn_id.
# - Modeled one concentric end counterbore diameter 18 mm x 3 mm deep.
# - Applied 1.0 mm general chamfer operation to outside circular edges where supported.
#
# Known gaps:
# - Bore-mouth 1.0 mm x 45 degree chamfers are not individually represented; only a general chamfer operation is included.
# - Requirement calls for counterbores on both ends; current SubCAD chain models only one accessible end counterbore.
# - Longitudinal milled reference flat on the cylinder side is not represented exactly by current top/end-face fluent operations.
# - Radial tapped M8 holes at axial X=24 and X=49 mm through the top flat are not represented; top-face threaded_hole does not express radial side drilling on the cylindrical surface.
# - Full-length radial split relief slit from OD to bore is not represented exactly.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft cylindrical program is not executed; check whether Stock.cylindrical axis/orientation matches the requirement datum during Stage 4.

from subcad import Stock

part = (
    Stock.cylindrical(30, 74, material="steel_a36")
    .turn_id(diameter=8, depth=74)
    .counterbore(hole_diameter=8, counterbore_diameter=18, counterbore_depth=3, cx=0, cy=0)
)
