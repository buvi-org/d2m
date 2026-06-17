# Requirement: SMP-027-04
# Source agent: 027
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_027_scientific_instrument_fixtures_single_metal_parts.json
# Part: Fiber Collimator V-Groove Alignment Block - single metal part
# Raw idea: Fiber Collimator V-Groove Alignment Block
# Status: draft_unexecuted
#
# Coverage notes:
# - Base cylindrical stock OD 29 mm x length 65 mm.
# - Centered axial through bore diameter 8 mm through full length.
# - One concentric end counterbore diameter 18 mm x 3 mm deep represented.
# - Longitudinal top reference flat 9 mm wide over 57 mm represented as a top milled flat relief.
# - Two tapped M7 clamp holes at axial X=21 and X=43 represented on the top flat.
# - Full-length split relief slit 6 mm wide approximated as a through slot offset toward datum-B side.
# - Outside circular edge break represented with 1.0 mm chamfer operation.
# - Transverse relief slot 8 mm wide at X=32, depth 2 mm represented on top flat.
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
    Stock.cylindrical(29, 65, material="steel_a36")
    .turn_id(diameter=8, depth=65)
    .counterbore(hole_diameter=8, counterbore_diameter=18, counterbore_depth=3, through=True)
    .pocket(length=57, width=9, depth=3.48, cx=0, cy=0, corner_radius=0)
    .threaded_hole(diameter=7, depth=14.5, cx=-11.5, cy=0)
    .threaded_hole(diameter=7, depth=14.5, cx=10.5, cy=0)
    .slot(length=65, width=6, depth=29, through=True, cx=0, cy=-7.25)
    .slot(length=21.75, width=8, depth=2, angle=90, cx=-0.5, cy=0)
)
