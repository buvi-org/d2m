# Requirement: SMP-039-19
# Source agent: 039
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_039_marine_service_hardware_single_metal_parts.json
# Part: Marine Hose Clamp Torque Access Driver - single metal part
# Raw idea: Marine Hose Clamp Torque Access Driver
# Status: draft_unexecuted
#
# Coverage notes:
# - Created cylindrical stock OD 47 x length 95 mm in stainless_316.
# - Machined centered axial through bore diameter 15 mm along the full length using turn_id.
# - Modeled one concentric end counterbore diameter 25 mm x 3 mm deep.
# - Applied 1.0 mm general chamfer operation to outside circular edges where supported.
#
# Known gaps:
# - Bore-mouth 1.0 mm x 45 degree chamfers are not individually represented; only a general chamfer operation is included.
# - Requirement calls for counterbores on both ends; current SubCAD chain models only one accessible end counterbore.
# - Longitudinal milled reference flat on the cylinder side is not represented exactly by current top/end-face fluent operations.
# - Radial tapped M5 holes at axial X=31 and X=63 mm through the top flat are not represented; top-face threaded_hole does not express radial side drilling on the cylindrical surface.
# - Full-length radial split relief slit from OD to bore is not represented exactly.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft cylindrical program is not executed; check whether Stock.cylindrical axis/orientation matches the requirement datum during Stage 4.

from subcad import Stock

part = (
    Stock.cylindrical(47, 95, material="stainless_316")
    .turn_id(diameter=15, depth=95)
    .counterbore(hole_diameter=15, counterbore_diameter=25, counterbore_depth=3, cx=0, cy=0)
)
