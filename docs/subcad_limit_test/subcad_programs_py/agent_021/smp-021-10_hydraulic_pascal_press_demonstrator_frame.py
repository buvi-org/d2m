# Requirement: SMP-021-10
# Source agent: 021
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_021_education_lab_apparatus_single_metal_parts.json
# Part: Hydraulic Pascal Press Demonstrator Frame - single metal part
# Raw idea: Hydraulic Pascal Press Demonstrator Frame
# Status: draft_unexecuted
#
# Coverage notes:
# - Base cylindrical stock OD 57 mm x length 119 mm.
# - Centered axial through bore diameter 14 mm through full length.
# - One concentric end counterbore diameter 24 mm x 3 mm deep represented.
# - Longitudinal top reference flat 19 mm wide over 111 mm represented as a top milled flat relief.
# - Two tapped M7 clamp holes at axial X=39 and X=79 represented on the top flat.
# - Full-length split relief slit 5 mm wide approximated as a through slot offset toward datum-B side.
# - Outside circular edge break represented with 1.0 mm chamfer operation.
# - Transverse relief slot 7 mm wide at X=59, depth 5 mm represented on top flat.
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
    Stock.cylindrical(57, 119, material="steel_1045")
    .turn_id(diameter=14, depth=119)
    .counterbore(hole_diameter=14, counterbore_diameter=24, counterbore_depth=3, through=True)
    .pocket(length=111, width=19, depth=6.84, cx=0, cy=0, corner_radius=0)
    .threaded_hole(diameter=7, depth=28.5, cx=-20.5, cy=0)
    .threaded_hole(diameter=7, depth=28.5, cx=19.5, cy=0)
    .slot(length=119, width=5, depth=57, through=True, cx=0, cy=-14.25)
    .slot(length=42.75, width=7, depth=5, angle=90, cx=-0.5, cy=0)
)
