# Requirement: SMP-023-07
# Source agent: 023
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_023_warehouse_logistics_hardware_single_metal_parts.json
# Part: Modular Flow Rack Lane Divider Clamp - single metal part
# Raw idea: Modular Flow Rack Lane Divider Clamp
# Status: draft_unexecuted
#
# Coverage notes:
# - Base cylindrical stock OD 38 mm x length 118 mm.
# - Centered axial through bore diameter 8 mm through full length.
# - One concentric end counterbore diameter 18 mm x 3 mm deep represented.
# - Longitudinal top reference flat 12 mm wide over 110 mm represented as a top milled flat relief.
# - Two tapped M8 clamp holes at axial X=39 and X=78 represented on the top flat.
# - Full-length split relief slit 5 mm wide approximated as a through slot offset toward datum-B side.
# - Outside circular edge break represented with 1.0 mm chamfer operation.
# - Transverse relief slot 7 mm wide at X=59, depth 3 mm represented on top flat.
#
# Known gaps:
# - Bore-mouth 1.0 mm chamfers on both ends are noted but not separately selectable on the internal bore edges in this draft.
# - Requirement calls for counterbores on both ends; this draft models the accessible top/end counterbore only.
# - True longitudinal flat on a round bar side is approximated with a top-face pocket/flat operation.
# - Radial hole axis and intersection with cylindrical bore are approximated using top-face threaded_hole placement.
# - Exact radial slit from OD to axial bore on the cylindrical side is approximated as a top-face through slot.
# - Internal bore-edge chamfers are not separately modeled.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated directly from frozen Stage 2 requirement text; not executed or visually reviewed yet.
# - Coordinate conversion uses SubCAD centered stock coordinates while requirement text uses lower-left-near datum coordinates.

from subcad import Stock

part = (
    Stock.cylindrical(38, 118, material="steel_1045")
    .turn_id(diameter=8, depth=118)
    .counterbore(hole_diameter=8, counterbore_diameter=18, counterbore_depth=3, through=True)
    .pocket(length=110, width=12, depth=4.56, cx=0, cy=0, corner_radius=0)
    .threaded_hole(diameter=8, depth=19, cx=-20, cy=0)
    .threaded_hole(diameter=8, depth=19, cx=19, cy=0)
    .slot(length=118, width=5, depth=38, through=True, cx=0, cy=-9.5)
    .slot(length=28.5, width=7, depth=3, angle=90, cx=0, cy=0)
)
