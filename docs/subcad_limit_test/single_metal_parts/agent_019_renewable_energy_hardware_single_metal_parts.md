# Agent 019 Single Metal Part Requirements

Domain: renewable energy, solar mounting, wind measurement, battery storage, and electrical infrastructure hardware

Each item below is one metal part only. Product assemblies and nonmetal components are explicitly out of scope.

## SMP-019-01 - Adjustable Solar Rail Mid-Clamp Body

Part name: Adjustable Solar Rail Mid-Clamp Body - single metal part

Material: 1045 medium-carbon steel, normalized (durable wear surface for workshop loading)

Envelope: `{"height_mm": 47, "length_mm": 80, "width_mm": 80}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Adjustable Solar Rail Mid-Clamp Body'. The broader
use case is: Rooftop photovoltaic panel mounting systems using aluminum rails and framed solar
modules. The chosen deliverable is only the metal body implied by: CNC-machined aluminum mid-clamp
block with stepped contact faces, bolt clearance slot, and serrated underside. All other product
elements are external reference items and must not be modeled. The part must perform this mechanical
role: Clamp adjacent solar panel frames to a mounting rail while allowing small frame-height
variations. It is intentionally included in the SubCAD limit corpus because: Requires asymmetric
steps, functional serrations, bolt-slot geometry, frame-contact surfaces, and clear distinction
between clamping faces and clearance regions. The part is made from 1045 medium-carbon steel,
normalized using rectangular block stock. Start from one rectangular metal block or plate. Saw
oversize, face all datum sides, then machine the pockets, holes, slots, angled faces, grooves, and
edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 80 mm x 80 mm x 47 mm.
- mounting hole pattern: Drill two through holes diameter 13 mm on the length centerline at X=16 mm and X=64 mm, Y=40 mm.
- functional center feature: Machine a central obround slot 30 mm long x 10 mm wide through the part, centered at X=40 mm, Y=40 mm.
- top relief pocket: Mill a rectangular relief pocket 25 mm x 26 mm x 10 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- serrated contact edge: Cut 8 equal triangular serrations across the rear edge, each 4 mm deep.

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
- The feature named 'serrated contact edge' is present with the stated size and position.
- All required chamfers, reliefs, and edge treatments are visible in STEP and STL outputs.
- No extra parts, fasteners, hardware, labels, cosmetic meshes, or nonmetal components are present.
- Flat datums remain planar and usable; pockets or slots do not accidentally break unsupported walls.

Negative requirements:
- Represent exactly one metal part only.
- Do not model screws, nuts, springs, bushings, bearings, rubber pads, plastic covers, electronics, labels, handles, knobs, adhesives, weld beads, or separate inserts.
- Do not convert the part into an assembly or multiple bodies.
- Do not replace through holes, slots, pockets, grooves, flats, tapers, or chamfers with cosmetic markings.
- Do not omit datum-critical features just because they are small.
- Do not broaden the requirement back into the full product idea named 'Adjustable Solar Rail Mid-Clamp Body'; this requirement is only for its chosen metal part.

---

## SMP-019-02 - Wind Mast Anemometer Boom Bracket

Part name: Wind Mast Anemometer Boom Bracket - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"length_mm": 145, "thickness_mm": 4, "width_mm": 60}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Wind Mast Anemometer Boom Bracket'. The broader use
case is: Meteorological towers used for wind-resource assessment before turbine installation. The
chosen deliverable is only the metal body implied by: Machined split clamp bracket with semicircular
mast bore, boom socket, cross-bolt holes, and anti-rotation ribs. All other product elements are
external reference items and must not be modeled. The part must perform this mechanical role: Hold a
horizontal sensor boom at a fixed offset from a round mast while resisting rotation under wind
loading. It is intentionally included in the SubCAD limit corpus because: Combines cylindrical
clamping geometry, perpendicular socket features, split-line details, ribbing, and multiple fastener
axes. The part is made from low-carbon steel, ASTM A36 or equivalent using sheet or plate stock.
Start from one flat sheet or plate blank. Cut the outside profile, machine holes, slots, pockets,
lips, and relief features into that same piece. If bends are called out, they are bends in the same
sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 145 mm x 60 mm x 4 mm.
- mounting hole pattern: Drill two through holes diameter 8 mm on the length centerline at X=12 mm and X=133 mm, Y=30 mm.
- functional center feature: Machine a central obround slot 48 mm long x 7 mm wide through the part, centered at X=72 mm, Y=30 mm.
- top relief pocket: Mill a rectangular relief pocket 36 mm x 20 mm x 1 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.

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
- All required chamfers, reliefs, and edge treatments are visible in STEP and STL outputs.
- No extra parts, fasteners, hardware, labels, cosmetic meshes, or nonmetal components are present.
- Flat datums remain planar and usable; pockets or slots do not accidentally break unsupported walls.

Negative requirements:
- Represent exactly one metal part only.
- Do not model screws, nuts, springs, bushings, bearings, rubber pads, plastic covers, electronics, labels, handles, knobs, adhesives, weld beads, or separate inserts.
- Do not convert the part into an assembly or multiple bodies.
- Do not replace through holes, slots, pockets, grooves, flats, tapers, or chamfers with cosmetic markings.
- Do not omit datum-critical features just because they are small.
- Do not broaden the requirement back into the full product idea named 'Wind Mast Anemometer Boom Bracket'; this requirement is only for its chosen metal part.

---

## SMP-019-03 - Battery Rack Seismic Foot Anchor

Part name: Battery Rack Seismic Foot Anchor - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"length_mm": 180, "thickness_mm": 9, "width_mm": 130}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Battery Rack Seismic Foot Anchor'. The broader use
case is: Grid-scale lithium battery storage cabinets mounted in seismic-rated equipment rooms. The
chosen deliverable is only the metal body implied by: Thick steel base foot plate with slotted
anchor holes, raised rack pad, gusset interfaces, and chamfered corners. All other product elements
are external reference items and must not be modeled. The part must perform this mechanical role:
Anchor a battery rack frame to concrete while distributing load and allowing minor alignment
adjustment. It is intentionally included in the SubCAD limit corpus because: Tests plate thickness,
slots, raised bosses, load-bearing pads, chamfers, and orientation-specific mounting surfaces. The
part is made from low-carbon steel, ASTM A36 or equivalent using sheet or plate stock. Start from
one flat sheet or plate blank. Cut the outside profile, machine holes, slots, pockets, lips, and
relief features into that same piece. If bends are called out, they are bends in the same sheet
part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 180 mm x 130 mm x 9 mm.
- mounting hole pattern: Drill two through holes diameter 10 mm on the length centerline at X=26 mm and X=154 mm, Y=65 mm.
- functional center feature: Machine a central obround slot 60 mm long x 17 mm wide through the part, centered at X=90 mm, Y=65 mm.
- top relief pocket: Mill a rectangular relief pocket 45 mm x 43 mm x 2 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.

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
- All required chamfers, reliefs, and edge treatments are visible in STEP and STL outputs.
- No extra parts, fasteners, hardware, labels, cosmetic meshes, or nonmetal components are present.
- Flat datums remain planar and usable; pockets or slots do not accidentally break unsupported walls.

Negative requirements:
- Represent exactly one metal part only.
- Do not model screws, nuts, springs, bushings, bearings, rubber pads, plastic covers, electronics, labels, handles, knobs, adhesives, weld beads, or separate inserts.
- Do not convert the part into an assembly or multiple bodies.
- Do not replace through holes, slots, pockets, grooves, flats, tapers, or chamfers with cosmetic markings.
- Do not omit datum-critical features just because they are small.
- Do not broaden the requirement back into the full product idea named 'Battery Rack Seismic Foot Anchor'; this requirement is only for its chosen metal part.

---

## SMP-019-04 - Solar Tracker Torque Tube Saddle

Part name: Solar Tracker Torque Tube Saddle - single metal part

Material: 1045 medium-carbon steel, normalized (durable wear surface for workshop loading)

Envelope: `{"axial_bore_diameter_mm": 25, "outer_diameter_mm": 77, "overall_length_mm": 66, "wall_minimum_mm": 26}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Solar Tracker Torque Tube Saddle'. The broader use
case is: Single-axis solar tracker systems supporting long rows of photovoltaic modules. The chosen
deliverable is only the metal body implied by: Machined saddle block with concave tube seat, side
keeper flanges, bolt holes, and drain relief channels. All other product elements are external
reference items and must not be modeled. The part must perform this mechanical role: Cradle and
locate a rectangular or round torque tube on a rotating support post. It is intentionally included
in the SubCAD limit corpus because: Requires curved seating surfaces, flange constraints, drainage
cutouts, bolt patterns, and structural mass distribution. The part is made from 1045 medium-carbon
steel, normalized using round bar stock. Start from one cut length of round metal bar. Turn the
outside, face both ends, bore the center, then mill secondary flats, slots, and radial holes as
needed. No separate inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 77 mm and length 66 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 25 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 35 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 25 mm wide over 58 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M8 holes through the top flat at X=22 mm and X=44 mm.
- split relief slit: Cut one full-length radial slit 6 mm wide from the outside to the axial bore on datum-B side.
- outside edge treatment: Break all outside circular edges with 1.0 mm chamfers and keep internal bore edges visibly chamfered.
- cross relief slot: Machine one transverse slot 8 mm wide across the top flat at X=33 mm, depth 7 mm.

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
- Do not broaden the requirement back into the full product idea named 'Solar Tracker Torque Tube Saddle'; this requirement is only for its chosen metal part.

---

## SMP-019-05 - Cable Tray Expansion Joint Slider

Part name: Cable Tray Expansion Joint Slider - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"length_mm": 100, "thickness_mm": 9, "width_mm": 90}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Cable Tray Expansion Joint Slider'. The broader use
case is: Outdoor electrical infrastructure carrying power cables across temperature-varying solar or
battery sites. The chosen deliverable is only the metal body implied by: Machined sliding splice
plate with elongated guide slots, stop shoulders, low-friction bearing lands, and fastener bosses.
All other product elements are external reference items and must not be modeled. The part must
perform this mechanical role: Allow controlled longitudinal expansion between cable tray sections
while maintaining lateral alignment. It is intentionally included in the SubCAD limit corpus
because: Tests sliding interfaces, long slots, travel stops, paired symmetry, and surfaces that must
remain parallel and coplanar. The part is made from low-carbon steel, ASTM A36 or equivalent using
sheet or plate stock. Start from one flat sheet or plate blank. Cut the outside profile, machine
holes, slots, pockets, lips, and relief features into that same piece. If bends are called out, they
are bends in the same sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 100 mm x 90 mm x 9 mm.
- mounting hole pattern: Drill two through holes diameter 10 mm on the length centerline at X=18 mm and X=82 mm, Y=45 mm.
- functional center feature: Machine a central obround slot 33 mm long x 16 mm wide through the part, centered at X=50 mm, Y=45 mm.
- top relief pocket: Mill a rectangular relief pocket 25 mm x 30 mm x 2 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.

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
- All required chamfers, reliefs, and edge treatments are visible in STEP and STL outputs.
- No extra parts, fasteners, hardware, labels, cosmetic meshes, or nonmetal components are present.
- Flat datums remain planar and usable; pockets or slots do not accidentally break unsupported walls.

Negative requirements:
- Represent exactly one metal part only.
- Do not model screws, nuts, springs, bushings, bearings, rubber pads, plastic covers, electronics, labels, handles, knobs, adhesives, weld beads, or separate inserts.
- Do not convert the part into an assembly or multiple bodies.
- Do not replace through holes, slots, pockets, grooves, flats, tapers, or chamfers with cosmetic markings.
- Do not omit datum-critical features just because they are small.
- Do not broaden the requirement back into the full product idea named 'Cable Tray Expansion Joint Slider'; this requirement is only for its chosen metal part.

---

## SMP-019-06 - Wind Vane Tail Hub Adapter

Part name: Wind Vane Tail Hub Adapter - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 18, "outer_diameter_mm": 74, "overall_length_mm": 65, "wall_minimum_mm": 28}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Wind Vane Tail Hub Adapter'. The broader use case
is: Mechanical wind direction sensors mounted on remote weather stations. The chosen deliverable is
only the metal body implied by: Small machined hub with vertical shaft bore, radial vane slot, set-
screw holes, and alignment datum notch. All other product elements are external reference items and
must not be modeled. The part must perform this mechanical role: Connect a lightweight vane tail to
a vertical sensor shaft with precise angular alignment. It is intentionally included in the SubCAD
limit corpus because: Uses intersecting bores, thin slots, set-screw geometry, datum features, and
rotational alignment details. The part is made from low-carbon steel, ASTM A36 or equivalent using
round bar stock. Start from one cut length of round metal bar. Turn the outside, face both ends,
bore the center, then mill secondary flats, slots, and radial holes as needed. No separate inserts
or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 74 mm and length 65 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 18 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 28 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 24 mm wide over 57 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M4 holes through the top flat at X=21 mm and X=43 mm.
- split relief slit: Cut one full-length radial slit 3 mm wide from the outside to the axial bore on datum-B side.
- outside edge treatment: Break all outside circular edges with 1.0 mm chamfers and keep internal bore edges visibly chamfered.
- cross relief slot: Machine one transverse slot 5 mm wide across the top flat at X=32 mm, depth 7 mm.

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
- Do not broaden the requirement back into the full product idea named 'Wind Vane Tail Hub Adapter'; this requirement is only for its chosen metal part.

---

## SMP-019-07 - Ground-Mount Solar Pile Cap Plate

Part name: Ground-Mount Solar Pile Cap Plate - single metal part

Material: 4140 alloy steel, prehard (strong cylindrical metal part with threaded and slotted details)

Envelope: `{"axial_bore_diameter_mm": 13, "outer_diameter_mm": 54, "overall_length_mm": 100, "wall_minimum_mm": 20}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Ground-Mount Solar Pile Cap Plate'. The broader use
case is: Utility-scale ground-mounted solar arrays installed on driven steel piles. The chosen
deliverable is only the metal body implied by: Weldment-derived machined cap plate with pile saddle
radius, angled mounting face, bolt pattern, and stiffening webs. All other product elements are
external reference items and must not be modeled. The part must perform this mechanical role:
Provide a bolted interface between a vertical pile and an angled racking support member. It is
intentionally included in the SubCAD limit corpus because: Tests angled planes, curved saddle
contact, bolt-hole arrays, web-like reinforcement, and non-orthogonal part relationships. The part
is made from 4140 alloy steel, prehard using round bar stock. Start from one cut length of round
metal bar. Turn the outside, face both ends, bore the center, then mill secondary flats, slots, and
radial holes as needed. No separate inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 54 mm and length 100 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 13 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 23 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 18 mm wide over 92 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M4 holes through the top flat at X=33 mm and X=66 mm.
- split relief slit: Cut one full-length radial slit 6 mm wide from the outside to the axial bore on datum-B side.
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
- Do not broaden the requirement back into the full product idea named 'Ground-Mount Solar Pile Cap Plate'; this requirement is only for its chosen metal part.

---

## SMP-019-08 - Battery Module Compression End Plate

Part name: Battery Module Compression End Plate - single metal part

Material: 1045 medium-carbon steel, normalized (durable wear surface for workshop loading)

Envelope: `{"length_mm": 235, "thickness_mm": 6, "width_mm": 100}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Battery Module Compression End Plate'. The broader
use case is: Battery storage packs where prismatic cells are mechanically compressed inside a module
frame. The chosen deliverable is only the metal body implied by: Machined aluminum end plate with
tie-rod holes, recessed cell contact field, perimeter rail pockets, and edge stiffeners. All other
product elements are external reference items and must not be modeled. The part must perform this
mechanical role: Apply even compression across a cell stack while tying into side rails and tie
rods. It is intentionally included in the SubCAD limit corpus because: Requires large flat datum
surfaces, recessed fields, repeated hole patterns, rail pockets, and stiffness-driven geometry. The
part is made from 1045 medium-carbon steel, normalized using sheet or plate stock. Start from one
flat sheet or plate blank. Cut the outside profile, machine holes, slots, pockets, lips, and relief
features into that same piece. If bends are called out, they are bends in the same sheet part, not
separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 235 mm x 100 mm x 6 mm.
- mounting hole pattern: Drill two through holes diameter 11 mm on the length centerline at X=20 mm and X=215 mm, Y=50 mm.
- functional center feature: Machine a central obround slot 78 mm long x 15 mm wide through the part, centered at X=117 mm, Y=50 mm.
- top relief pocket: Mill a rectangular relief pocket 58 mm x 33 mm x 3 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.

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
- All required chamfers, reliefs, and edge treatments are visible in STEP and STL outputs.
- No extra parts, fasteners, hardware, labels, cosmetic meshes, or nonmetal components are present.
- Flat datums remain planar and usable; pockets or slots do not accidentally break unsupported walls.

Negative requirements:
- Represent exactly one metal part only.
- Do not model screws, nuts, springs, bushings, bearings, rubber pads, plastic covers, electronics, labels, handles, knobs, adhesives, weld beads, or separate inserts.
- Do not convert the part into an assembly or multiple bodies.
- Do not replace through holes, slots, pockets, grooves, flats, tapers, or chamfers with cosmetic markings.
- Do not omit datum-critical features just because they are small.
- Do not broaden the requirement back into the full product idea named 'Battery Module Compression End Plate'; this requirement is only for its chosen metal part.

---

## SMP-019-09 - Substation Busbar Support Clamp

Part name: Substation Busbar Support Clamp - single metal part

Material: 1045 medium-carbon steel, normalized (durable wear surface for workshop loading)

Envelope: `{"axial_bore_diameter_mm": 23, "outer_diameter_mm": 70, "overall_length_mm": 44, "wall_minimum_mm": 23}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Substation Busbar Support Clamp'. The broader use
case is: Electrical substations using rigid aluminum or copper busbars supported on insulators. The
chosen deliverable is only the metal body implied by: Machined clamp saddle with rectangular busbar
channel, insulated spacer pocket, cap-screw holes, and rounded corona-safe edges. All other product
elements are external reference items and must not be modeled. The part must perform this mechanical
role: Mechanically retain a rectangular busbar while allowing thermal movement and maintaining
clearance. It is intentionally included in the SubCAD limit corpus because: Tests rectangular
channels, clearance gaps, spacer pockets, rounded edge requirements, and functional electrical-
mechanical constraints. The part is made from 1045 medium-carbon steel, normalized using round bar
stock. Start from one cut length of round metal bar. Turn the outside, face both ends, bore the
center, then mill secondary flats, slots, and radial holes as needed. No separate inserts or
fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 70 mm and length 44 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 23 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 33 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 23 mm wide over 36 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M6 holes through the top flat at X=14 mm and X=29 mm.
- split relief slit: Cut one full-length radial slit 4 mm wide from the outside to the axial bore on datum-B side.
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
- Do not broaden the requirement back into the full product idea named 'Substation Busbar Support Clamp'; this requirement is only for its chosen metal part.

---

## SMP-019-10 - Solar Inverter Skid Lifting Lug

Part name: Solar Inverter Skid Lifting Lug - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 35, "length_mm": 150, "width_mm": 60}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Solar Inverter Skid Lifting Lug'. The broader use
case is: Mechanical skids carrying solar inverters, transformers, or battery power conversion
equipment. The chosen deliverable is only the metal body implied by: Thick machined lifting lug with
large shackle hole, base bolt pattern, load-spreading fillets, and orientation marking recess. All
other product elements are external reference items and must not be modeled. The part must perform
this mechanical role: Provide a certified lifting point for moving a heavy electrical skid during
installation. It is intentionally included in the SubCAD limit corpus because: Requires high-load
geometry, large through-hole features, generous fillets, base interface definition, and clear force-
path representation. The part is made from low-carbon steel, ASTM A36 or equivalent using
rectangular block stock. Start from one rectangular metal block or plate. Saw oversize, face all
datum sides, then machine the pockets, holes, slots, angled faces, grooves, and edge treatments into
that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 150 mm x 60 mm x 35 mm.
- mounting hole pattern: Drill two through holes diameter 10 mm on the length centerline at X=12 mm and X=138 mm, Y=30 mm.
- functional center feature: Machine a central obround slot 50 mm long x 8 mm wide through the part, centered at X=75 mm, Y=30 mm.
- top relief pocket: Mill a rectangular relief pocket 37 mm x 20 mm x 14 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.

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
- All required chamfers, reliefs, and edge treatments are visible in STEP and STL outputs.
- No extra parts, fasteners, hardware, labels, cosmetic meshes, or nonmetal components are present.
- Flat datums remain planar and usable; pockets or slots do not accidentally break unsupported walls.

Negative requirements:
- Represent exactly one metal part only.
- Do not model screws, nuts, springs, bushings, bearings, rubber pads, plastic covers, electronics, labels, handles, knobs, adhesives, weld beads, or separate inserts.
- Do not convert the part into an assembly or multiple bodies.
- Do not replace through holes, slots, pockets, grooves, flats, tapers, or chamfers with cosmetic markings.
- Do not omit datum-critical features just because they are small.
- Do not broaden the requirement back into the full product idea named 'Solar Inverter Skid Lifting Lug'; this requirement is only for its chosen metal part.

---
