# Requirement: SMP-021-05
# Source agent: 021
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_021_education_lab_apparatus_single_metal_parts.json
# Part: Force Table Pulley Mount - single metal part
# Raw idea: Force Table Pulley Mount
# Status: draft_unexecuted
#
# Coverage notes:
# - Base cylindrical stock OD 75 mm x length 59 mm.
# - Centered axial through bore diameter 15 mm through full length.
# - One concentric end counterbore diameter 25 mm x 3 mm deep represented.
# - Longitudinal top reference flat 25 mm wide over 51 mm represented as a top milled flat relief.
# - Two tapped M7 clamp holes at axial X=19 and X=39 represented on the top flat.
# - Full-length split relief slit 3 mm wide approximated as a through slot offset toward datum-B side.
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
    Stock.cylindrical(75, 59, material="stainless_316")
    .turn_id(diameter=15, depth=59)
    .counterbore(hole_diameter=15, counterbore_diameter=25, counterbore_depth=3, through=True)
    .pocket(length=51, width=25, depth=9, cx=0, cy=0, corner_radius=0)
    .threaded_hole(diameter=7, depth=37.5, cx=-10.5, cy=0)
    .threaded_hole(diameter=7, depth=37.5, cx=9.5, cy=0)
    .slot(length=59, width=3, depth=75, through=True, cx=0, cy=-18.75)
)
