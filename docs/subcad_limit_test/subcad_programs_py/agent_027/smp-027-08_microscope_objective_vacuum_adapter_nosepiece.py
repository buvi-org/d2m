# Requirement: SMP-027-08
# Source agent: 027
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_027_scientific_instrument_fixtures_single_metal_parts.json
# Part: Microscope Objective Vacuum Adapter Nosepiece - single metal part
# Raw idea: Microscope Objective Vacuum Adapter Nosepiece
# Status: draft_unexecuted
#
# Coverage notes:
# - Base cylindrical stock OD 33 mm x length 106 mm.
# - Centered axial through bore diameter 8 mm through full length.
# - One concentric end counterbore diameter 18 mm x 3 mm deep represented.
# - Longitudinal top reference flat 11 mm wide over 98 mm represented as a top milled flat relief.
# - Two tapped M5 clamp holes at axial X=35 and X=70 represented on the top flat.
# - Full-length split relief slit 6 mm wide approximated as a through slot offset toward datum-B side.
# - Outside circular edge break represented with 1.0 mm chamfer operation.
# - Transverse relief slot 8 mm wide at X=53, depth 3 mm represented on top flat.
#
# Known gaps:
# - Bore-mouth 1.0 mm chamfers on both ends are noted but not separately selectable on the internal bore edges in this draft.
# - Requirement calls for counterbores on both ends; this draft models the accessible top/end counterbore only.
# - True longitudinal flat on a round bar side is approximated with a top-face pocket/flat operation.
# - Radial hole axis and intersection with cylindrical bore are approximated using top-face threaded_hole placement.
# - Exact radial slit from OD to axial bore on the cylindrical side is approximated as a top-face through slot.
# - Internal bore-edge chamfers are not separately modeled.
# - Opposed wrench flats leaving 25 mm across flats are not modeled; current draft keeps the cylindrical OD except for top-flat approximation.
# - Global chamfer operation removed from executable .py because current SubCAD chamfering fails on many complex generated solids; chamfers remain a requirement gap until targeted edge chamfer support is reliable.
#
# Review notes:
# - Draft generated directly from frozen Stage 2 requirement text; not executed or visually reviewed yet.
# - Coordinate conversion uses SubCAD centered stock coordinates while requirement text uses lower-left-near datum coordinates.

from subcad import Stock

part = (
    Stock.cylindrical(33, 106, material="steel_a36")
    .turn_id(diameter=8, depth=106)
    .counterbore(hole_diameter=8, counterbore_diameter=18, counterbore_depth=3, through=True)
    .pocket(length=98, width=11, depth=3.96, cx=0, cy=0, corner_radius=0)
    .threaded_hole(diameter=5, depth=16.5, cx=-18, cy=0)
    .threaded_hole(diameter=5, depth=16.5, cx=17, cy=0)
    .slot(length=106, width=6, depth=33, through=True, cx=0, cy=-8.25)
    .slot(length=24.75, width=8, depth=3, angle=90, cx=0, cy=0)
)
