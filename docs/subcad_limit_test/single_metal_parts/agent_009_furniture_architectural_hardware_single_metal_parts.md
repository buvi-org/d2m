# Agent 009 Single Metal Part Requirements

Domain: furniture hardware, adjustable fittings, architectural connectors, and door/window mechanisms

Each item below is one metal part only. Product assemblies and nonmetal components are explicitly out of scope.

## SMP-009-01 - Concealed Soft-Close Cabinet Hinge Cup

Part name: Concealed Soft-Close Cabinet Hinge Cup - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 54, "length_mm": 215, "width_mm": 70}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Concealed Soft-Close Cabinet Hinge Cup'. The
broader use case is: Kitchen and wardrobe cabinetry with hidden European-style hinges. The chosen
deliverable is only the metal body implied by: Machined hinge cup body with mounting ears, pivot
bores, damper pocket, and countersunk screw holes. All other product elements are external reference
items and must not be modeled. The part must perform this mechanical role: Houses the hinge pivot
and damping insert inside a recessed cup mounted in the cabinet door. It is intentionally included
in the SubCAD limit corpus because: Combines cylindrical recesses, thin flanges, coaxial hinge
features, countersinks, asymmetric pockets, and tight clearances in a compact part. The part is made
from low-carbon steel, ASTM A36 or equivalent using rectangular block stock. Start from one
rectangular metal block or plate. Saw oversize, face all datum sides, then machine the pockets,
holes, slots, angled faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 215 mm x 70 mm x 54 mm.
- mounting hole pattern: Drill two through holes diameter 11 mm on the length centerline at X=14 mm and X=201 mm, Y=35 mm.
- functional center feature: Machine a central obround slot 71 mm long x 18 mm wide through the part, centered at X=107 mm, Y=35 mm.
- top relief pocket: Mill a rectangular relief pocket 53 mm x 23 mm x 14 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- side tapped hole: Tap one side hole M4 from the right long edge into the central pocket; hole axis is parallel to Y.

Tolerances:
- Overall envelope dimensions: +/-0.20 mm.
- Hole diameters and slot widths: +/-0.10 mm.
- Hole and slot center positions from datums B and C: +/-0.15 mm.
- Pocket depths and relief depths: +/-0.10 mm.
- Nonfunctional chamfers and radii: +/-0.30 mm.

Acceptance checklist:
- The output contains one continuous metal solid representing one part.
- The stock family, material intent, envelope dimensions, and datum orientation match this requirement.
- The feature named 'single rectangular metal body' is present with the stated size and position.
- The feature named 'mounting hole pattern' is present with the stated size and position.
- The feature named 'functional center feature' is present with the stated size and position.
- The feature named 'top relief pocket' is present with the stated size and position.
- The feature named 'edge chamfers' is present with the stated size and position.
- The feature named 'side tapped hole' is present with the stated size and position.
- All required chamfers, reliefs, and edge treatments are visible in STEP and STL outputs.
- No extra parts, fasteners, hardware, labels, cosmetic meshes, or nonmetal components are present.
- Flat datums remain planar and usable; pockets or slots do not accidentally break unsupported walls.

Negative requirements:
- Represent exactly one metal part only.
- Do not model screws, nuts, springs, bushings, bearings, rubber pads, plastic covers, electronics, labels, handles, knobs, adhesives, weld beads, or separate inserts.
- Do not convert the part into an assembly or multiple bodies.
- Do not replace through holes, slots, pockets, grooves, flats, tapers, or chamfers with cosmetic markings.
- Do not omit datum-critical features just because they are small.
- Do not broaden the requirement back into the full product idea named 'Concealed Soft-Close Cabinet Hinge Cup'; this requirement is only for its chosen metal part.

---

## SMP-009-02 - Adjustable Wardrobe Sliding Door Roller Carriage

Part name: Adjustable Wardrobe Sliding Door Roller Carriage - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 8, "outer_diameter_mm": 35, "overall_length_mm": 115, "wall_minimum_mm": 13}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Adjustable Wardrobe Sliding Door Roller Carriage'.
The broader use case is: Top-hung or bottom-running sliding wardrobe door systems. The chosen
deliverable is only the metal body implied by: Roller carriage block with axle bosses, threaded
height-adjuster seat, guide slot, and door attachment interface. All other product elements are
external reference items and must not be modeled. The part must perform this mechanical role:
Supports a sliding door on rollers while allowing height and alignment adjustment after
installation. It is intentionally included in the SubCAD limit corpus because: Requires nested wheel
clearances, offset axle geometry, threaded adjustment features, slots, bosses, and load-bearing wall
thickness changes. The part is made from low-carbon steel, ASTM A36 or equivalent using round bar
stock. Start from one cut length of round metal bar. Turn the outside, face both ends, bore the
center, then mill secondary flats, slots, and radial holes as needed. No separate inserts or
fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 35 mm and length 115 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 8 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 18 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 11 mm wide over 107 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M5 holes through the top flat at X=38 mm and X=76 mm.
- split relief slit: Cut one full-length radial slit 3 mm wide from the outside to the axial bore on datum-B side.
- outside edge treatment: Break all outside circular edges with 1.0 mm chamfers and keep internal bore edges visibly chamfered.
- cross relief slot: Machine one transverse slot 5 mm wide across the top flat at X=57 mm, depth 3 mm.

Tolerances:
- Outside diameter and axial bore diameter: +/-0.05 mm.
- Concentricity of bore to outer diameter: within 0.05 mm TIR.
- Milled flats and slots: +/-0.15 mm unless otherwise specified.
- Nonfunctional chamfers: +/-0.3 mm.

Acceptance checklist:
- The output contains one continuous metal solid representing one part.
- The stock family, material intent, envelope dimensions, and datum orientation match this requirement.
- The feature named 'single cylindrical body' is present with the stated size and position.
- The feature named 'axial through bore' is present with the stated size and position.
- The feature named 'end counterbores' is present with the stated size and position.
- The feature named 'milled reference flat' is present with the stated size and position.
- The feature named 'radial clamp holes' is present with the stated size and position.
- The feature named 'split relief slit' is present with the stated size and position.
- The feature named 'outside edge treatment' is present with the stated size and position.
- The feature named 'cross relief slot' is present with the stated size and position.
- All required chamfers, reliefs, and edge treatments are visible in STEP and STL outputs.
- No extra parts, fasteners, hardware, labels, cosmetic meshes, or nonmetal components are present.
- Round features are coaxial unless the requirement explicitly says they are radial or offset.

Negative requirements:
- Represent exactly one metal part only.
- Do not model screws, nuts, springs, bushings, bearings, rubber pads, plastic covers, electronics, labels, handles, knobs, adhesives, weld beads, or separate inserts.
- Do not convert the part into an assembly or multiple bodies.
- Do not replace through holes, slots, pockets, grooves, flats, tapers, or chamfers with cosmetic markings.
- Do not omit datum-critical features just because they are small.
- Do not broaden the requirement back into the full product idea named 'Adjustable Wardrobe Sliding Door Roller Carriage'; this requirement is only for its chosen metal part.

---

## SMP-009-03 - Eccentric Cam Furniture Connector Housing

Part name: Eccentric Cam Furniture Connector Housing - single metal part

Material: 4140 alloy steel, prehard (strong cylindrical metal part with threaded and slotted details)

Envelope: `{"axial_bore_diameter_mm": 10, "outer_diameter_mm": 31, "overall_length_mm": 105, "wall_minimum_mm": 10}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Eccentric Cam Furniture Connector Housing'. The
broader use case is: Flat-pack furniture panels joined by cam-and-dowel fasteners. The chosen
deliverable is only the metal body implied by: Round cam connector housing with eccentric drive
cavity, dowel-entry throat, screwdriver slot, and retention lip. All other product elements are
external reference items and must not be modeled. The part must perform this mechanical role:
Captures a rotating cam that pulls a dowel head inward to clamp two panels together. It is
intentionally included in the SubCAD limit corpus because: Tests eccentric internal geometry,
interrupted circular profiles, shallow drive features, undercut-like retention forms, and precise
panel-facing datum surfaces. The part is made from 4140 alloy steel, prehard using round bar stock.
Start from one cut length of round metal bar. Turn the outside, face both ends, bore the center,
then mill secondary flats, slots, and radial holes as needed. No separate inserts or fasteners are
part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 31 mm and length 105 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 10 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 20 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 10 mm wide over 97 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M7 holes through the top flat at X=35 mm and X=70 mm.
- split relief slit: Cut one full-length radial slit 2 mm wide from the outside to the axial bore on datum-B side.
- outside edge treatment: Break all outside circular edges with 1.0 mm chamfers and keep internal bore edges visibly chamfered.
- cross relief slot: Machine one transverse slot 4 mm wide across the top flat at X=52 mm, depth 3 mm.

Tolerances:
- Outside diameter and axial bore diameter: +/-0.05 mm.
- Concentricity of bore to outer diameter: within 0.05 mm TIR.
- Milled flats and slots: +/-0.15 mm unless otherwise specified.
- Nonfunctional chamfers: +/-0.3 mm.

Acceptance checklist:
- The output contains one continuous metal solid representing one part.
- The stock family, material intent, envelope dimensions, and datum orientation match this requirement.
- The feature named 'single cylindrical body' is present with the stated size and position.
- The feature named 'axial through bore' is present with the stated size and position.
- The feature named 'end counterbores' is present with the stated size and position.
- The feature named 'milled reference flat' is present with the stated size and position.
- The feature named 'radial clamp holes' is present with the stated size and position.
- The feature named 'split relief slit' is present with the stated size and position.
- The feature named 'outside edge treatment' is present with the stated size and position.
- The feature named 'cross relief slot' is present with the stated size and position.
- All required chamfers, reliefs, and edge treatments are visible in STEP and STL outputs.
- No extra parts, fasteners, hardware, labels, cosmetic meshes, or nonmetal components are present.
- Round features are coaxial unless the requirement explicitly says they are radial or offset.

Negative requirements:
- Represent exactly one metal part only.
- Do not model screws, nuts, springs, bushings, bearings, rubber pads, plastic covers, electronics, labels, handles, knobs, adhesives, weld beads, or separate inserts.
- Do not convert the part into an assembly or multiple bodies.
- Do not replace through holes, slots, pockets, grooves, flats, tapers, or chamfers with cosmetic markings.
- Do not omit datum-critical features just because they are small.
- Do not broaden the requirement back into the full product idea named 'Eccentric Cam Furniture Connector Housing'; this requirement is only for its chosen metal part.

---

## SMP-009-04 - Adjustable Glass Shelf Support Pin

Part name: Adjustable Glass Shelf Support Pin - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 21, "outer_diameter_mm": 85, "overall_length_mm": 64, "wall_minimum_mm": 32}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Adjustable Glass Shelf Support Pin'. The broader
use case is: Display cabinets and wall units with movable glass shelves. The chosen deliverable is
only the metal body implied by: Stepped shelf pin with threaded leveling stem, flattened glass pad,
rubber insert recess, and locking shoulder. All other product elements are external reference items
and must not be modeled. The part must perform this mechanical role: Supports a glass shelf while
providing fine leveling and anti-slip retention. It is intentionally included in the SubCAD limit
corpus because: Mixes turned cylindrical sections with flats, small recesses, threaded regions, pad
geometry, and contact surfaces that must align to a shelf plane. The part is made from low-carbon
steel, ASTM A36 or equivalent using round bar stock. Start from one cut length of round metal bar.
Turn the outside, face both ends, bore the center, then mill secondary flats, slots, and radial
holes as needed. No separate inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 85 mm and length 64 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 21 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 31 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 28 mm wide over 56 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M4 holes through the top flat at X=21 mm and X=42 mm.
- split relief slit: Cut one full-length radial slit 2 mm wide from the outside to the axial bore on datum-B side.
- outside edge treatment: Break all outside circular edges with 1.0 mm chamfers and keep internal bore edges visibly chamfered.
- opposed wrench flats: Mill two opposed flats across the outside, leaving 77 mm across flats over the middle third of the length.

Tolerances:
- Outside diameter and axial bore diameter: +/-0.05 mm.
- Concentricity of bore to outer diameter: within 0.05 mm TIR.
- Milled flats and slots: +/-0.15 mm unless otherwise specified.
- Nonfunctional chamfers: +/-0.3 mm.

Acceptance checklist:
- The output contains one continuous metal solid representing one part.
- The stock family, material intent, envelope dimensions, and datum orientation match this requirement.
- The feature named 'single cylindrical body' is present with the stated size and position.
- The feature named 'axial through bore' is present with the stated size and position.
- The feature named 'end counterbores' is present with the stated size and position.
- The feature named 'milled reference flat' is present with the stated size and position.
- The feature named 'radial clamp holes' is present with the stated size and position.
- The feature named 'split relief slit' is present with the stated size and position.
- The feature named 'outside edge treatment' is present with the stated size and position.
- The feature named 'opposed wrench flats' is present with the stated size and position.
- All required chamfers, reliefs, and edge treatments are visible in STEP and STL outputs.
- No extra parts, fasteners, hardware, labels, cosmetic meshes, or nonmetal components are present.
- Round features are coaxial unless the requirement explicitly says they are radial or offset.

Negative requirements:
- Represent exactly one metal part only.
- Do not model screws, nuts, springs, bushings, bearings, rubber pads, plastic covers, electronics, labels, handles, knobs, adhesives, weld beads, or separate inserts.
- Do not convert the part into an assembly or multiple bodies.
- Do not replace through holes, slots, pockets, grooves, flats, tapers, or chamfers with cosmetic markings.
- Do not omit datum-critical features just because they are small.
- Do not broaden the requirement back into the full product idea named 'Adjustable Glass Shelf Support Pin'; this requirement is only for its chosen metal part.

---

## SMP-009-05 - Architectural Curtain Wall T-Slot Anchor Clamp

Part name: Architectural Curtain Wall T-Slot Anchor Clamp - single metal part

Material: 1045 medium-carbon steel, normalized (durable wear surface for workshop loading)

Envelope: `{"height_mm": 69, "length_mm": 155, "width_mm": 95}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Architectural Curtain Wall T-Slot Anchor Clamp'.
The broader use case is: Aluminum curtain wall framing used to secure panels or mullion accessories.
The chosen deliverable is only the metal body implied by: T-slot anchor clamp with tapered wedge
face, threaded boss, anti-rotation tabs, and bearing shoulders. All other product elements are
external reference items and must not be modeled. The part must perform this mechanical role: Slides
into an extrusion channel and clamps against the slot lips when tightened. It is intentionally
included in the SubCAD limit corpus because: Tests channel-specific geometry, wedge angles, slot
engagement lips, asymmetric anti-rotation features, and threaded load paths. The part is made from
1045 medium-carbon steel, normalized using rectangular block stock. Start from one rectangular metal
block or plate. Saw oversize, face all datum sides, then machine the pockets, holes, slots, angled
faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 155 mm x 95 mm x 69 mm.
- mounting hole pattern: Drill two through holes diameter 10 mm on the length centerline at X=19 mm and X=136 mm, Y=47 mm.
- functional center feature: Machine a central obround slot 51 mm long x 18 mm wide through the part, centered at X=77 mm, Y=47 mm.
- top relief pocket: Mill a rectangular relief pocket 38 mm x 31 mm x 5 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- machined angled reference face: Machine one top reference face at 12 degrees over the last 31 mm of length.
- side tapped hole: Tap one side hole M5 from the right long edge into the central pocket; hole axis is parallel to Y.

Tolerances:
- Overall envelope dimensions: +/-0.20 mm.
- Hole diameters and slot widths: +/-0.10 mm.
- Hole and slot center positions from datums B and C: +/-0.15 mm.
- Pocket depths and relief depths: +/-0.10 mm.
- Nonfunctional chamfers and radii: +/-0.30 mm.

Acceptance checklist:
- The output contains one continuous metal solid representing one part.
- The stock family, material intent, envelope dimensions, and datum orientation match this requirement.
- The feature named 'single rectangular metal body' is present with the stated size and position.
- The feature named 'mounting hole pattern' is present with the stated size and position.
- The feature named 'functional center feature' is present with the stated size and position.
- The feature named 'top relief pocket' is present with the stated size and position.
- The feature named 'edge chamfers' is present with the stated size and position.
- The feature named 'machined angled reference face' is present with the stated size and position.
- The feature named 'side tapped hole' is present with the stated size and position.
- All required chamfers, reliefs, and edge treatments are visible in STEP and STL outputs.
- No extra parts, fasteners, hardware, labels, cosmetic meshes, or nonmetal components are present.
- Flat datums remain planar and usable; pockets or slots do not accidentally break unsupported walls.

Negative requirements:
- Represent exactly one metal part only.
- Do not model screws, nuts, springs, bushings, bearings, rubber pads, plastic covers, electronics, labels, handles, knobs, adhesives, weld beads, or separate inserts.
- Do not convert the part into an assembly or multiple bodies.
- Do not replace through holes, slots, pockets, grooves, flats, tapers, or chamfers with cosmetic markings.
- Do not omit datum-critical features just because they are small.
- Do not broaden the requirement back into the full product idea named 'Architectural Curtain Wall T-Slot Anchor Clamp'; this requirement is only for its chosen metal part.

---

## SMP-009-06 - Pivot Door Bottom Bearing Shoe

Part name: Pivot Door Bottom Bearing Shoe - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 15, "outer_diameter_mm": 47, "overall_length_mm": 90, "wall_minimum_mm": 16}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Pivot Door Bottom Bearing Shoe'. The broader use
case is: Heavy frameless or timber pivot doors in architectural interiors. The chosen deliverable is
only the metal body implied by: Bearing shoe block with vertical spindle bore, thrust washer recess,
door-edge mounting holes, and alignment datum faces. All other product elements are external
reference items and must not be modeled. The part must perform this mechanical role: Supports the
lower pivot spindle and transfers door weight into the floor-mounted pivot assembly. It is
intentionally included in the SubCAD limit corpus because: Requires deep bores, concentric bearing
seats, countersunk fasteners, thick-to-thin transitions, and accurately related mounting and pivot
axes. The part is made from low-carbon steel, ASTM A36 or equivalent using round bar stock. Start
from one cut length of round metal bar. Turn the outside, face both ends, bore the center, then mill
secondary flats, slots, and radial holes as needed. No separate inserts or fasteners are part of the
deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 47 mm and length 90 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 15 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 25 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 15 mm wide over 82 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M6 holes through the top flat at X=30 mm and X=60 mm.
- split relief slit: Cut one full-length radial slit 3 mm wide from the outside to the axial bore on datum-B side.
- outside edge treatment: Break all outside circular edges with 1.0 mm chamfers and keep internal bore edges visibly chamfered.

Tolerances:
- Outside diameter and axial bore diameter: +/-0.05 mm.
- Concentricity of bore to outer diameter: within 0.05 mm TIR.
- Milled flats and slots: +/-0.15 mm unless otherwise specified.
- Nonfunctional chamfers: +/-0.3 mm.

Acceptance checklist:
- The output contains one continuous metal solid representing one part.
- The stock family, material intent, envelope dimensions, and datum orientation match this requirement.
- The feature named 'single cylindrical body' is present with the stated size and position.
- The feature named 'axial through bore' is present with the stated size and position.
- The feature named 'end counterbores' is present with the stated size and position.
- The feature named 'milled reference flat' is present with the stated size and position.
- The feature named 'radial clamp holes' is present with the stated size and position.
- The feature named 'split relief slit' is present with the stated size and position.
- The feature named 'outside edge treatment' is present with the stated size and position.
- All required chamfers, reliefs, and edge treatments are visible in STEP and STL outputs.
- No extra parts, fasteners, hardware, labels, cosmetic meshes, or nonmetal components are present.
- Round features are coaxial unless the requirement explicitly says they are radial or offset.

Negative requirements:
- Represent exactly one metal part only.
- Do not model screws, nuts, springs, bushings, bearings, rubber pads, plastic covers, electronics, labels, handles, knobs, adhesives, weld beads, or separate inserts.
- Do not convert the part into an assembly or multiple bodies.
- Do not replace through holes, slots, pockets, grooves, flats, tapers, or chamfers with cosmetic markings.
- Do not omit datum-critical features just because they are small.
- Do not broaden the requirement back into the full product idea named 'Pivot Door Bottom Bearing Shoe'; this requirement is only for its chosen metal part.

---

## SMP-009-07 - Tilt-and-Turn Window Locking Cam Keeper

Part name: Tilt-and-Turn Window Locking Cam Keeper - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 62, "length_mm": 205, "width_mm": 70}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Tilt-and-Turn Window Locking Cam Keeper'. The
broader use case is: European-style tilt-and-turn window perimeter locking systems. The chosen
deliverable is only the metal body implied by: Frame-mounted keeper with ramped cam entry, captive
locking pocket, slotted adjustment holes, and raised wear pads. All other product elements are
external reference items and must not be modeled. The part must perform this mechanical role:
Receives a mushroom cam from the sash hardware and locks it against the window frame. It is
intentionally included in the SubCAD limit corpus because: Tests ramped contact surfaces, partial
pockets, elongated mounting slots, small reliefs, and geometry tied to the path of a rotating
locking cam. The part is made from low-carbon steel, ASTM A36 or equivalent using rectangular block
stock. Start from one rectangular metal block or plate. Saw oversize, face all datum sides, then
machine the pockets, holes, slots, angled faces, grooves, and edge treatments into that same solid
piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 205 mm x 70 mm x 62 mm.
- mounting hole pattern: Drill two through holes diameter 5 mm on the length centerline at X=14 mm and X=191 mm, Y=35 mm.
- functional center feature: Machine a central obround slot 68 mm long x 12 mm wide through the part, centered at X=102 mm, Y=35 mm.
- top relief pocket: Mill a rectangular relief pocket 51 mm x 23 mm x 3 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- integral hook lip: Leave an integral hook lip on one short end, projecting 13 mm and undercut 2 mm for registration.

Tolerances:
- Overall envelope dimensions: +/-0.20 mm.
- Hole diameters and slot widths: +/-0.10 mm.
- Hole and slot center positions from datums B and C: +/-0.15 mm.
- Pocket depths and relief depths: +/-0.10 mm.
- Nonfunctional chamfers and radii: +/-0.30 mm.

Acceptance checklist:
- The output contains one continuous metal solid representing one part.
- The stock family, material intent, envelope dimensions, and datum orientation match this requirement.
- The feature named 'single rectangular metal body' is present with the stated size and position.
- The feature named 'mounting hole pattern' is present with the stated size and position.
- The feature named 'functional center feature' is present with the stated size and position.
- The feature named 'top relief pocket' is present with the stated size and position.
- The feature named 'edge chamfers' is present with the stated size and position.
- The feature named 'integral hook lip' is present with the stated size and position.
- All required chamfers, reliefs, and edge treatments are visible in STEP and STL outputs.
- No extra parts, fasteners, hardware, labels, cosmetic meshes, or nonmetal components are present.
- Flat datums remain planar and usable; pockets or slots do not accidentally break unsupported walls.

Negative requirements:
- Represent exactly one metal part only.
- Do not model screws, nuts, springs, bushings, bearings, rubber pads, plastic covers, electronics, labels, handles, knobs, adhesives, weld beads, or separate inserts.
- Do not convert the part into an assembly or multiple bodies.
- Do not replace through holes, slots, pockets, grooves, flats, tapers, or chamfers with cosmetic markings.
- Do not omit datum-critical features just because they are small.
- Do not broaden the requirement back into the full product idea named 'Tilt-and-Turn Window Locking Cam Keeper'; this requirement is only for its chosen metal part.

---

## SMP-009-08 - Concealed Door Closer Arm Linkage Block

Part name: Concealed Door Closer Arm Linkage Block - single metal part

Material: 4140 alloy steel, prehard (strong cylindrical metal part with threaded and slotted details)

Envelope: `{"axial_bore_diameter_mm": 17, "outer_diameter_mm": 53, "overall_length_mm": 118, "wall_minimum_mm": 18}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Concealed Door Closer Arm Linkage Block'. The
broader use case is: Concealed overhead door closers used in commercial doors. The chosen
deliverable is only the metal body implied by: Linkage block with cross pin bore, sliding shoe
interface, arm clevis pocket, and lubrication groove. All other product elements are external
reference items and must not be modeled. The part must perform this mechanical role: Connects the
closer arm to a sliding track while allowing pivoting motion under spring load. It is intentionally
included in the SubCAD limit corpus because: Combines clevis-style geometry, precision pin bores,
sliding contact faces, grooves, filleted load paths, and clearance for angular movement. The part is
made from 4140 alloy steel, prehard using round bar stock. Start from one cut length of round metal
bar. Turn the outside, face both ends, bore the center, then mill secondary flats, slots, and radial
holes as needed. No separate inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 53 mm and length 118 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 17 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 27 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 17 mm wide over 110 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M5 holes through the top flat at X=39 mm and X=78 mm.
- split relief slit: Cut one full-length radial slit 5 mm wide from the outside to the axial bore on datum-B side.
- outside edge treatment: Break all outside circular edges with 1.0 mm chamfers and keep internal bore edges visibly chamfered.

Tolerances:
- Outside diameter and axial bore diameter: +/-0.05 mm.
- Concentricity of bore to outer diameter: within 0.05 mm TIR.
- Milled flats and slots: +/-0.15 mm unless otherwise specified.
- Nonfunctional chamfers: +/-0.3 mm.

Acceptance checklist:
- The output contains one continuous metal solid representing one part.
- The stock family, material intent, envelope dimensions, and datum orientation match this requirement.
- The feature named 'single cylindrical body' is present with the stated size and position.
- The feature named 'axial through bore' is present with the stated size and position.
- The feature named 'end counterbores' is present with the stated size and position.
- The feature named 'milled reference flat' is present with the stated size and position.
- The feature named 'radial clamp holes' is present with the stated size and position.
- The feature named 'split relief slit' is present with the stated size and position.
- The feature named 'outside edge treatment' is present with the stated size and position.
- All required chamfers, reliefs, and edge treatments are visible in STEP and STL outputs.
- No extra parts, fasteners, hardware, labels, cosmetic meshes, or nonmetal components are present.
- Round features are coaxial unless the requirement explicitly says they are radial or offset.

Negative requirements:
- Represent exactly one metal part only.
- Do not model screws, nuts, springs, bushings, bearings, rubber pads, plastic covers, electronics, labels, handles, knobs, adhesives, weld beads, or separate inserts.
- Do not convert the part into an assembly or multiple bodies.
- Do not replace through holes, slots, pockets, grooves, flats, tapers, or chamfers with cosmetic markings.
- Do not omit datum-critical features just because they are small.
- Do not broaden the requirement back into the full product idea named 'Concealed Door Closer Arm Linkage Block'; this requirement is only for its chosen metal part.

---

## SMP-009-09 - Adjustable Stair Handrail Glass Clamp

Part name: Adjustable Stair Handrail Glass Clamp - single metal part

Material: 1045 medium-carbon steel, normalized (durable wear surface for workshop loading)

Envelope: `{"height_mm": 26, "length_mm": 205, "width_mm": 45}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Adjustable Stair Handrail Glass Clamp'. The broader
use case is: Architectural glass balustrades with mounted handrail supports. The chosen deliverable
is only the metal body implied by: Clamp body half with glass pad recess, handrail saddle boss,
adjustment screw seat, and alignment ribs. All other product elements are external reference items
and must not be modeled. The part must perform this mechanical role: Clamps onto a glass panel and
provides an adjustable saddle for a round or oval handrail. It is intentionally included in the
SubCAD limit corpus because: Tests curved saddle geometry, pad pockets, split-clamp interfaces,
threaded adjustment seats, and multiple functional surfaces at different angles. The part is made
from 1045 medium-carbon steel, normalized using rectangular block stock. Start from one rectangular
metal block or plate. Saw oversize, face all datum sides, then machine the pockets, holes, slots,
angled faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 205 mm x 45 mm x 26 mm.
- mounting hole pattern: Drill two through holes diameter 13 mm on the length centerline at X=10 mm and X=195 mm, Y=22 mm.
- functional center feature: Machine a central obround slot 68 mm long x 13 mm wide through the part, centered at X=102 mm, Y=22 mm.
- top relief pocket: Mill a rectangular relief pocket 51 mm x 18 mm x 6 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- machined angled reference face: Machine one top reference face at 16 degrees over the last 41 mm of length.
- side tapped hole: Tap one side hole M6 from the right long edge into the central pocket; hole axis is parallel to Y.

Tolerances:
- Overall envelope dimensions: +/-0.20 mm.
- Hole diameters and slot widths: +/-0.10 mm.
- Hole and slot center positions from datums B and C: +/-0.15 mm.
- Pocket depths and relief depths: +/-0.10 mm.
- Nonfunctional chamfers and radii: +/-0.30 mm.

Acceptance checklist:
- The output contains one continuous metal solid representing one part.
- The stock family, material intent, envelope dimensions, and datum orientation match this requirement.
- The feature named 'single rectangular metal body' is present with the stated size and position.
- The feature named 'mounting hole pattern' is present with the stated size and position.
- The feature named 'functional center feature' is present with the stated size and position.
- The feature named 'top relief pocket' is present with the stated size and position.
- The feature named 'edge chamfers' is present with the stated size and position.
- The feature named 'machined angled reference face' is present with the stated size and position.
- The feature named 'side tapped hole' is present with the stated size and position.
- All required chamfers, reliefs, and edge treatments are visible in STEP and STL outputs.
- No extra parts, fasteners, hardware, labels, cosmetic meshes, or nonmetal components are present.
- Flat datums remain planar and usable; pockets or slots do not accidentally break unsupported walls.

Negative requirements:
- Represent exactly one metal part only.
- Do not model screws, nuts, springs, bushings, bearings, rubber pads, plastic covers, electronics, labels, handles, knobs, adhesives, weld beads, or separate inserts.
- Do not convert the part into an assembly or multiple bodies.
- Do not replace through holes, slots, pockets, grooves, flats, tapers, or chamfers with cosmetic markings.
- Do not omit datum-critical features just because they are small.
- Do not broaden the requirement back into the full product idea named 'Adjustable Stair Handrail Glass Clamp'; this requirement is only for its chosen metal part.

---

## SMP-009-10 - Flush Sliding Door Edge Pull Mechanism Cup

Part name: Flush Sliding Door Edge Pull Mechanism Cup - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 12, "outer_diameter_mm": 61, "overall_length_mm": 34, "wall_minimum_mm": 24}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Flush Sliding Door Edge Pull Mechanism Cup'. The
broader use case is: Pocket doors and flush sliding interior doors. The chosen deliverable is only
the metal body implied by: Recessed edge-pull cup with curved finger cavity, pivot pin bosses, tab
clearance pocket, and countersunk fixing holes. All other product elements are external reference
items and must not be modeled. The part must perform this mechanical role: Provides a recessed
finger pull and houses a small pivoting tab that can be pulled from the door edge. It is
intentionally included in the SubCAD limit corpus because: Requires sculpted ergonomic recesses,
thin edge flanges, pin bosses, internal clearance volumes, countersinks, and door-edge mounting
constraints. The part is made from low-carbon steel, ASTM A36 or equivalent using round bar stock.
Start from one cut length of round metal bar. Turn the outside, face both ends, bore the center,
then mill secondary flats, slots, and radial holes as needed. No separate inserts or fasteners are
part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 61 mm and length 34 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 12 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 22 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 20 mm wide over 26 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M6 holes through the top flat at X=11 mm and X=22 mm.
- split relief slit: Cut one full-length radial slit 3 mm wide from the outside to the axial bore on datum-B side.
- outside edge treatment: Break all outside circular edges with 1.0 mm chamfers and keep internal bore edges visibly chamfered.

Tolerances:
- Outside diameter and axial bore diameter: +/-0.05 mm.
- Concentricity of bore to outer diameter: within 0.05 mm TIR.
- Milled flats and slots: +/-0.15 mm unless otherwise specified.
- Nonfunctional chamfers: +/-0.3 mm.

Acceptance checklist:
- The output contains one continuous metal solid representing one part.
- The stock family, material intent, envelope dimensions, and datum orientation match this requirement.
- The feature named 'single cylindrical body' is present with the stated size and position.
- The feature named 'axial through bore' is present with the stated size and position.
- The feature named 'end counterbores' is present with the stated size and position.
- The feature named 'milled reference flat' is present with the stated size and position.
- The feature named 'radial clamp holes' is present with the stated size and position.
- The feature named 'split relief slit' is present with the stated size and position.
- The feature named 'outside edge treatment' is present with the stated size and position.
- All required chamfers, reliefs, and edge treatments are visible in STEP and STL outputs.
- No extra parts, fasteners, hardware, labels, cosmetic meshes, or nonmetal components are present.
- Round features are coaxial unless the requirement explicitly says they are radial or offset.

Negative requirements:
- Represent exactly one metal part only.
- Do not model screws, nuts, springs, bushings, bearings, rubber pads, plastic covers, electronics, labels, handles, knobs, adhesives, weld beads, or separate inserts.
- Do not convert the part into an assembly or multiple bodies.
- Do not replace through holes, slots, pockets, grooves, flats, tapers, or chamfers with cosmetic markings.
- Do not omit datum-critical features just because they are small.
- Do not broaden the requirement back into the full product idea named 'Flush Sliding Door Edge Pull Mechanism Cup'; this requirement is only for its chosen metal part.

---
