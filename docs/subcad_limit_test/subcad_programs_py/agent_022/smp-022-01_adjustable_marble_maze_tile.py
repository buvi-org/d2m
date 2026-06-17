# Requirement: SMP-022-01
# Source agent: 022
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_022_toys_hobby_mechanisms_single_metal_parts.json
# Part: Adjustable marble maze tile - single metal part
# Raw idea: Adjustable marble maze tile
# Status: draft_unexecuted
#
# Coverage notes:
# - Base cylindrical stock OD 66 mm x length 76 mm.
# - Centered axial through bore diameter 13 mm through full length.
# - One concentric end counterbore diameter 23 mm x 3 mm deep represented.
# - Longitudinal top reference flat 22 mm wide over 68 mm represented as a top milled flat relief.
# - Two tapped M6 clamp holes at axial X=25 and X=50 represented on the top flat.
# - Full-length split relief slit 4 mm wide approximated as a through slot offset toward datum-B side.
# - Outside circular edge break represented with 1.0 mm chamfer operation.
# - Transverse relief slot 6 mm wide at X=38, depth 6 mm represented on top flat.
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
    Stock.cylindrical(66, 76, material="steel_a36")
    .turn_id(diameter=13, depth=76)
    .counterbore(hole_diameter=13, counterbore_diameter=23, counterbore_depth=3, through=True)
    .pocket(length=68, width=22, depth=7.92, cx=0, cy=0, corner_radius=0)
    .threaded_hole(diameter=6, depth=33, cx=-13, cy=0)
    .threaded_hole(diameter=6, depth=33, cx=12, cy=0)
    .slot(length=76, width=4, depth=66, through=True, cx=0, cy=-16.5)
    .slot(length=49.5, width=6, depth=6, angle=90, cx=0, cy=0)
)
