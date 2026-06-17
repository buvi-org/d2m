# Requirement: SMP-021-04
# Source agent: 021
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_021_education_lab_apparatus_single_metal_parts.json
# Part: Pendulum Length Adjustment Clamp - single metal part
# Raw idea: Pendulum Length Adjustment Clamp
# Status: draft_unexecuted
#
# Coverage notes:
# - Base cylindrical stock OD 63 mm x length 24 mm.
# - Centered axial through bore diameter 21 mm through full length.
# - One concentric end counterbore diameter 31 mm x 3 mm deep represented.
# - Longitudinal top reference flat 21 mm wide over 16 mm represented as a top milled flat relief.
# - Two tapped M6 clamp holes at axial X=8 and X=16 represented on the top flat.
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
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated directly from frozen Stage 2 requirement text; not executed or visually reviewed yet.
# - Coordinate conversion uses SubCAD centered stock coordinates while requirement text uses lower-left-near datum coordinates.

from subcad import Stock

part = (
    Stock.cylindrical(63, 24, material="steel_1045")
    .turn_id(diameter=21, depth=24)
    .counterbore(hole_diameter=21, counterbore_diameter=31, counterbore_depth=3, through=True)
    .pocket(length=16, width=21, depth=7.56, cx=0, cy=0, corner_radius=0)
    .threaded_hole(diameter=6, depth=31.5, cx=-4, cy=0)
    .threaded_hole(diameter=6, depth=31.5, cx=4, cy=0)
    .slot(length=24, width=6, depth=63, through=True, cx=0, cy=-15.75)
)
