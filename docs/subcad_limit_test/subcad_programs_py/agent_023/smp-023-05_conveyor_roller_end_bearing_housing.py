# Requirement: SMP-023-05
# Source agent: 023
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_023_warehouse_logistics_hardware_single_metal_parts.json
# Part: Conveyor Roller End Bearing Housing - single metal part
# Raw idea: Conveyor Roller End Bearing Housing
# Status: draft_unexecuted
#
# Coverage notes:
# - Base cylindrical stock OD 57 mm x length 63 mm.
# - Centered axial through bore diameter 19 mm through full length.
# - One concentric end counterbore diameter 29 mm x 3 mm deep represented.
# - Longitudinal top reference flat 19 mm wide over 55 mm represented as a top milled flat relief.
# - Two tapped M5 clamp holes at axial X=21 and X=42 represented on the top flat.
# - Full-length split relief slit 2 mm wide approximated as a through slot offset toward datum-B side.
# - Outside circular edge break represented with 1.0 mm chamfer operation.
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
    Stock.cylindrical(57, 63, material="steel_a36")
    .turn_id(diameter=19, depth=63)
    .counterbore(hole_diameter=19, counterbore_diameter=29, counterbore_depth=3, through=True)
    .pocket(length=55, width=19, depth=6.84, cx=0, cy=0, corner_radius=0)
    .threaded_hole(diameter=5, depth=28.5, cx=-10.5, cy=0)
    .threaded_hole(diameter=5, depth=28.5, cx=10.5, cy=0)
    .slot(length=63, width=2, depth=57, through=True, cx=0, cy=-14.25)
)
