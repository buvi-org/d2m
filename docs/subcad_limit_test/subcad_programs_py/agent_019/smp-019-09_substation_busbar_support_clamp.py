# Requirement: SMP-019-09
# Source agent: 019
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_019_renewable_energy_hardware_single_metal_parts.json
# Part: Substation Busbar Support Clamp - single metal part
# Raw idea: Substation Busbar Support Clamp
# Status: draft_unexecuted
#
# Coverage notes:
# - Base cylindrical stock OD 70 mm x length 44 mm.
# - Centered axial through bore diameter 23 mm through full length.
# - One concentric end counterbore diameter 33 mm x 3 mm deep represented.
# - Longitudinal top reference flat 23 mm wide over 36 mm represented as a top milled flat relief.
# - Two tapped M6 clamp holes at axial X=14 and X=29 represented on the top flat.
# - Full-length split relief slit 4 mm wide approximated as a through slot offset toward datum-B side.
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
    Stock.cylindrical(70, 44, material="steel_1045")
    .turn_id(diameter=23, depth=44)
    .counterbore(hole_diameter=23, counterbore_diameter=33, counterbore_depth=3, through=True)
    .pocket(length=36, width=23, depth=8.4, cx=0, cy=0, corner_radius=0)
    .threaded_hole(diameter=6, depth=35, cx=-8, cy=0)
    .threaded_hole(diameter=6, depth=35, cx=7, cy=0)
    .slot(length=44, width=4, depth=70, through=True, cx=0, cy=-17.5)
)
