# Requirement: SMP-026-01
# Source agent: 026
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_026_office_equipment_hardware_single_metal_parts.json
# Part: Printer Paper Tray Lift Cam - single metal part
# Raw idea: Printer Paper Tray Lift Cam
# Status: draft_unexecuted
#
# Coverage notes:
# - Base cylindrical stock OD 61 mm x length 87 mm.
# - Centered axial through bore diameter 12 mm through full length.
# - One concentric end counterbore diameter 22 mm x 3 mm deep represented.
# - Longitudinal top reference flat 20 mm wide over 79 mm represented as a top milled flat relief.
# - Two tapped M8 clamp holes at axial X=29 and X=58 represented on the top flat.
# - Full-length split relief slit 5 mm wide approximated as a through slot offset toward datum-B side.
# - Outside circular edge break represented with 1.0 mm chamfer operation.
#
# Known gaps:
# - Requirement specifies 4140 alloy steel; mapped to allowed SubCAD material key steel_1045.
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
    Stock.cylindrical(61, 87, material="steel_1045")
    .turn_id(diameter=12, depth=87)
    .counterbore(hole_diameter=12, counterbore_diameter=22, counterbore_depth=3, through=True)
    .pocket(length=79, width=20, depth=7.32, cx=0, cy=0, corner_radius=0)
    .threaded_hole(diameter=8, depth=30.5, cx=-14.5, cy=0)
    .threaded_hole(diameter=8, depth=30.5, cx=14.5, cy=0)
    .slot(length=87, width=5, depth=61, through=True, cx=0, cy=-15.25)
)
