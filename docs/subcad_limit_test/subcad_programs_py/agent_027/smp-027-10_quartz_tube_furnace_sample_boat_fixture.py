# Requirement: SMP-027-10
# Source agent: 027
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_027_scientific_instrument_fixtures_single_metal_parts.json
# Part: Quartz Tube Furnace Sample Boat Fixture - single metal part
# Raw idea: Quartz Tube Furnace Sample Boat Fixture
# Status: draft_unexecuted
#
# Coverage notes:
# - Base cylindrical stock OD 43 mm x length 98 mm.
# - Centered axial through bore diameter 10 mm through full length.
# - One concentric end counterbore diameter 20 mm x 3 mm deep represented.
# - Longitudinal top reference flat 14 mm wide over 90 mm represented as a top milled flat relief.
# - Two tapped M8 clamp holes at axial X=32 and X=65 represented on the top flat.
# - Full-length split relief slit 4 mm wide approximated as a through slot offset toward datum-B side.
# - Outside circular edge break represented with 1.0 mm chamfer operation.
# - Transverse relief slot 6 mm wide at X=49, depth 4 mm represented on top flat.
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
    Stock.cylindrical(43, 98, material="steel_a36")
    .turn_id(diameter=10, depth=98)
    .counterbore(hole_diameter=10, counterbore_diameter=20, counterbore_depth=3, through=True)
    .pocket(length=90, width=14, depth=5.16, cx=0, cy=0, corner_radius=0)
    .threaded_hole(diameter=8, depth=21.5, cx=-17, cy=0)
    .threaded_hole(diameter=8, depth=21.5, cx=16, cy=0)
    .slot(length=98, width=4, depth=43, through=True, cx=0, cy=-10.75)
    .slot(length=32.25, width=6, depth=4, angle=90, cx=0, cy=0)
)
