# Requirement: SMP-019-07
# Source agent: 019
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_019_renewable_energy_hardware_single_metal_parts.json
# Part: Ground-Mount Solar Pile Cap Plate - single metal part
# Raw idea: Ground-Mount Solar Pile Cap Plate
# Status: draft_unexecuted
#
# Coverage notes:
# - Base cylindrical stock OD 54 mm x length 100 mm.
# - Centered axial through bore diameter 13 mm through full length.
# - One concentric end counterbore diameter 23 mm x 3 mm deep represented.
# - Longitudinal top reference flat 18 mm wide over 92 mm represented as a top milled flat relief.
# - Two tapped M4 clamp holes at axial X=33 and X=66 represented on the top flat.
# - Full-length split relief slit 6 mm wide approximated as a through slot offset toward datum-B side.
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
    Stock.cylindrical(54, 100, material="steel_1045")
    .turn_id(diameter=13, depth=100)
    .counterbore(hole_diameter=13, counterbore_diameter=23, counterbore_depth=3, through=True)
    .pocket(length=92, width=18, depth=6.48, cx=0, cy=0, corner_radius=0)
    .threaded_hole(diameter=4, depth=27, cx=-17, cy=0)
    .threaded_hole(diameter=4, depth=27, cx=16, cy=0)
    .slot(length=100, width=6, depth=54, through=True, cx=0, cy=-13.5)
)
