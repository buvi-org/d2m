# Requirement: SMP-023-09
# Source agent: 023
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_023_warehouse_logistics_hardware_single_metal_parts.json
# Part: Pallet Lift Table Scissor Link Plate - single metal part
# Raw idea: Pallet Lift Table Scissor Link Plate
# Status: draft_unexecuted
#
# Coverage notes:
# - Base cylindrical stock OD 73 mm x length 26 mm.
# - Centered axial through bore diameter 14 mm through full length.
# - One concentric end counterbore diameter 24 mm x 3 mm deep represented.
# - Longitudinal top reference flat 24 mm wide over 18 mm represented as a top milled flat relief.
# - Two tapped M8 clamp holes at axial X=8 and X=17 represented on the top flat.
# - Full-length split relief slit 6 mm wide approximated as a through slot offset toward datum-B side.
# - Outside circular edge break represented with 1.0 mm chamfer operation.
#
# Known gaps:
# - Bore-mouth 1.0 mm chamfers on both ends are noted but not separately selectable on the internal bore edges in this draft.
# - Requirement calls for counterbores on both ends; this draft models the accessible top/end counterbore only.
# - True longitudinal flat on a round bar side is approximated with a top-face pocket/flat operation.
# - Radial hole axis and intersection with cylindrical bore are approximated using top-face threaded_hole placement.
# - Exact radial slit from OD to axial bore on the cylindrical side is approximated as a top-face through slot.
# - Internal bore-edge chamfers are not separately modeled.
# - Opposed wrench flats leaving 65 mm across flats are not modeled; current draft keeps the cylindrical OD except for top-flat approximation.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated directly from frozen Stage 2 requirement text; not executed or visually reviewed yet.
# - Coordinate conversion uses SubCAD centered stock coordinates while requirement text uses lower-left-near datum coordinates.

from subcad import Stock

part = (
    Stock.cylindrical(73, 26, material="steel_a36")
    .turn_id(diameter=14, depth=26)
    .counterbore(hole_diameter=14, counterbore_diameter=24, counterbore_depth=3, through=True)
    .pocket(length=18, width=24, depth=8.76, cx=0, cy=0, corner_radius=0)
    .threaded_hole(diameter=8, depth=36.5, cx=-5, cy=0)
    .threaded_hole(diameter=8, depth=36.5, cx=4, cy=0)
    .slot(length=26, width=6, depth=73, through=True, cx=0, cy=-18.25)
)
