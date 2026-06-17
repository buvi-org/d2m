# Requirement: SMP-022-09
# Source agent: 022
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_022_toys_hobby_mechanisms_single_metal_parts.json
# Part: Magnetic tile hinge connector - single metal part
# Raw idea: Magnetic tile hinge connector
# Status: draft_unexecuted
#
# Coverage notes:
# - Base cylindrical stock OD 48 mm x length 103 mm.
# - Centered axial through bore diameter 12 mm through full length.
# - One concentric end counterbore diameter 22 mm x 3 mm deep represented.
# - Longitudinal top reference flat 16 mm wide over 95 mm represented as a top milled flat relief.
# - Two tapped M6 clamp holes at axial X=34 and X=68 represented on the top flat.
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
    Stock.cylindrical(48, 103, material="steel_a36")
    .turn_id(diameter=12, depth=103)
    .counterbore(hole_diameter=12, counterbore_diameter=22, counterbore_depth=3, through=True)
    .pocket(length=95, width=16, depth=5.76, cx=0, cy=0, corner_radius=0)
    .threaded_hole(diameter=6, depth=24, cx=-17.5, cy=0)
    .threaded_hole(diameter=6, depth=24, cx=16.5, cy=0)
    .slot(length=103, width=3, depth=48, through=True, cx=0, cy=-12)
)
