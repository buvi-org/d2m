# Requirement: SMP-025-04
# Source agent: 025
# Source requirements file: docs/subcad_limit_test/single_metal_parts/agent_025_jewelry_watchmaking_fixtures_single_metal_parts.json
# Part: Bracelet Link Pin Press Anvil - single metal part
# Raw idea: Bracelet Link Pin Press Anvil
# Status: draft_unexecuted
#
# Coverage notes:
# - Base cylindrical stock OD 84 mm x length 68 mm.
# - Centered axial through bore diameter 28 mm through full length.
# - One concentric end counterbore diameter 38 mm x 3 mm deep represented.
# - Longitudinal top reference flat 28 mm wide over 60 mm represented as a top milled flat relief.
# - Two tapped M5 clamp holes at axial X=22 and X=45 represented on the top flat.
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
    Stock.cylindrical(84, 68, material="steel_1045")
    .turn_id(diameter=28, depth=68)
    .counterbore(hole_diameter=28, counterbore_diameter=38, counterbore_depth=3, through=True)
    .pocket(length=60, width=28, depth=10.08, cx=0, cy=0, corner_radius=0)
    .threaded_hole(diameter=5, depth=42, cx=-12, cy=0)
    .threaded_hole(diameter=5, depth=42, cx=11, cy=0)
    .slot(length=68, width=6, depth=84, through=True, cx=0, cy=-21)
)
