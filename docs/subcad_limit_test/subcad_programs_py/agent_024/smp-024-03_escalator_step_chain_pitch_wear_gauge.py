# Requirement: SMP-024-03
# Source agent: 024
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_024_rail_transit_service_tools_single_metal_parts.json
# Part: Escalator Step Chain Pitch Wear Gauge - single metal part
# Raw idea: Escalator Step Chain Pitch Wear Gauge
# Status: draft_unexecuted
#
# Coverage notes:
# - Base cylindrical stock OD 45 mm x length 85 mm.
# - Centered axial through bore diameter 9 mm through full length.
# - One concentric end counterbore diameter 19 mm x 3 mm deep represented.
# - Longitudinal top reference flat 15 mm wide over 77 mm represented as a top milled flat relief.
# - Two tapped M5 clamp holes at axial X=28 and X=56 represented on the top flat.
# - Full-length split relief slit 2 mm wide approximated as a through slot offset toward datum-B side.
# - Outside circular edge break represented with 1.0 mm chamfer operation.
# - Transverse relief slot 4 mm wide at X=42, depth 4 mm represented on top flat.
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
    Stock.cylindrical(45, 85, material="steel_a36")
    .turn_id(diameter=9, depth=85)
    .counterbore(hole_diameter=9, counterbore_diameter=19, counterbore_depth=3, through=True)
    .pocket(length=77, width=15, depth=5.4, cx=0, cy=0, corner_radius=0)
    .threaded_hole(diameter=5, depth=22.5, cx=-14.5, cy=0)
    .threaded_hole(diameter=5, depth=22.5, cx=13.5, cy=0)
    .slot(length=85, width=2, depth=45, through=True, cx=0, cy=-11.25)
    .slot(length=33.75, width=4, depth=4, angle=90, cx=-0.5, cy=0)
)
