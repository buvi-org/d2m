# Agent 022 Single Metal Part Requirements

Domain: toys, model-making, hobby robotics, tabletop games, and mechanical hobby kits

Each item below is one metal part only. Product assemblies and nonmetal components are explicitly out of scope.

## SMP-022-01 - Adjustable marble maze tile

Part name: Adjustable marble maze tile - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 13, "outer_diameter_mm": 66, "overall_length_mm": 76, "wall_minimum_mm": 26}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Adjustable marble maze tile'. The broader use case
is: A modular tabletop marble run set where users rearrange square tiles to create maze paths. The
chosen deliverable is only the metal body implied by: Machined maze tile with recessed tracks,
locating pins, gate slots, and underside connector pockets. All other product elements are external
reference items and must not be modeled. The part must perform this mechanical role: Guides a small
ball through channels with adjustable gates and junctions. It is intentionally included in the
SubCAD limit corpus because: Requires nested grooves, variable-depth channels, filleted
intersections, small alignment features, and functional clearances for moving inserts. The part is
made from low-carbon steel, ASTM A36 or equivalent using round bar stock. Start from one cut length
of round metal bar. Turn the outside, face both ends, bore the center, then mill secondary flats,
slots, and radial holes as needed. No separate inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 66 mm and length 76 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 13 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 23 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 22 mm wide over 68 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M6 holes through the top flat at X=25 mm and X=50 mm.
- split relief slit: Cut one full-length radial slit 4 mm wide from the outside to the axial bore on datum-B side.
- outside edge treatment: Break all outside circular edges with 1.0 mm chamfers and keep internal bore edges visibly chamfered.
- cross relief slot: Machine one transverse slot 6 mm wide across the top flat at X=38 mm, depth 6 mm.

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
- Do not broaden the requirement back into the full product idea named 'Adjustable marble maze tile'; this requirement is only for its chosen metal part.

---

## SMP-022-02 - Wind-up walking insect kit

Part name: Wind-up walking insect kit - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 39, "length_mm": 175, "width_mm": 40}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Wind-up walking insect kit'. The broader use case
is: A hobby mechanical toy kit assembled by children or model makers. The chosen deliverable is only
the metal body implied by: Central crank frame with axle bosses, cam slots, leg pivot holes, and
spring motor mounting points. All other product elements are external reference items and must not
be modeled. The part must perform this mechanical role: Converts spring-driven rotary motion into
alternating leg movement. It is intentionally included in the SubCAD limit corpus because: Tests
linked pivot geometry, mirrored but offset features, compact bearing surfaces, thin ribs, and
tolerance-sensitive rotating interfaces. The part is made from low-carbon steel, ASTM A36 or
equivalent using rectangular block stock. Start from one rectangular metal block or plate. Saw
oversize, face all datum sides, then machine the pockets, holes, slots, angled faces, grooves, and
edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 175 mm x 40 mm x 39 mm.
- mounting hole pattern: Drill two through holes diameter 8 mm on the length centerline at X=10 mm and X=165 mm, Y=20 mm.
- functional center feature: Machine a central obround slot 58 mm long x 16 mm wide through the part, centered at X=87 mm, Y=20 mm.
- top relief pocket: Mill a rectangular relief pocket 43 mm x 18 mm x 8 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Wind-up walking insect kit'; this requirement is only for its chosen metal part.

---

## SMP-022-03 - Mini desktop cable car model

Part name: Mini desktop cable car model - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"length_mm": 165, "thickness_mm": 5, "width_mm": 100}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Mini desktop cable car model'. The broader use case
is: A scale model-making kit for building a small suspended cable car display. The chosen
deliverable is only the metal body implied by: Machined trolley carriage with pulley forks, axle
holes, hanger bracket, and cabin attachment tabs. All other product elements are external reference
items and must not be modeled. The part must perform this mechanical role: Carries a tiny cabin
along a taut cord using grooved wheels. It is intentionally included in the SubCAD limit corpus
because: Combines curved wheel-clearance pockets, thin fork arms, coaxial holes, load-bearing
brackets, and constrained assembly interfaces. The part is made from low-carbon steel, ASTM A36 or
equivalent using sheet or plate stock. Start from one flat sheet or plate blank. Cut the outside
profile, machine holes, slots, pockets, lips, and relief features into that same piece. If bends are
called out, they are bends in the same sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 165 mm x 100 mm x 5 mm.
- mounting hole pattern: Drill two through holes diameter 8 mm on the length centerline at X=20 mm and X=145 mm, Y=50 mm.
- functional center feature: Machine a central obround slot 55 mm long x 10 mm wide through the part, centered at X=82 mm, Y=50 mm.
- top relief pocket: Mill a rectangular relief pocket 41 mm x 33 mm x 2 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Mini desktop cable car model'; this requirement is only for its chosen metal part.

---

## SMP-022-04 - Tabletop game rotating score dial

Part name: Tabletop game rotating score dial - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"length_mm": 230, "thickness_mm": 5, "width_mm": 145}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Tabletop game rotating score dial'. The broader use
case is: An accessory for board games that tracks points, turns, or resources. The chosen
deliverable is only the metal body implied by: Dial housing plate with concentric recesses, detent
pockets, viewing windows, and snap-fit axle posts. All other product elements are external reference
items and must not be modeled. The part must perform this mechanical role: Allows a player to rotate
numbered dials while keeping the selected value indexed. It is intentionally included in the SubCAD
limit corpus because: Tests concentric circular geometry, partial cutouts, repeated detent features,
layered moving parts, and visible alignment windows. The part is made from low-carbon steel, ASTM
A36 or equivalent using sheet or plate stock. Start from one flat sheet or plate blank. Cut the
outside profile, machine holes, slots, pockets, lips, and relief features into that same piece. If
bends are called out, they are bends in the same sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 230 mm x 145 mm x 5 mm.
- mounting hole pattern: Drill two through holes diameter 7 mm on the length centerline at X=29 mm and X=201 mm, Y=72 mm.
- functional center feature: Machine a central obround slot 76 mm long x 7 mm wide through the part, centered at X=115 mm, Y=72 mm.
- top relief pocket: Mill a rectangular relief pocket 57 mm x 48 mm x 2 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Tabletop game rotating score dial'; this requirement is only for its chosen metal part.

---

## SMP-022-05 - Hobby robot gripper claw

Part name: Hobby robot gripper claw - single metal part

Material: 6061-T6 aluminum (low mass with good machinability and stable flat features)

Envelope: `{"length_mm": 150, "thickness_mm": 11, "width_mm": 70}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Hobby robot gripper claw'. The broader use case is:
A small robotics kit end-effector for picking up lightweight classroom objects. The chosen
deliverable is only the metal body implied by: Machined gripper palm with servo pocket, linkage
pivots, finger stops, and mounting flange. All other product elements are external reference items
and must not be modeled. The part must perform this mechanical role: Opens and closes two fingers
using a servo-driven linkage. It is intentionally included in the SubCAD limit corpus because:
Requires precise servo geometry, nontrivial pivot spacing, mechanical travel limits, symmetric
linkage mounts, and compact clearance envelopes. The part is made from 6061-T6 aluminum using sheet
or plate stock. Start from one flat sheet or plate blank. Cut the outside profile, machine holes,
slots, pockets, lips, and relief features into that same piece. If bends are called out, they are
bends in the same sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 150 mm x 70 mm x 11 mm.
- mounting hole pattern: Drill two through holes diameter 6 mm on the length centerline at X=14 mm and X=136 mm, Y=35 mm.
- functional center feature: Machine a central obround slot 50 mm long x 14 mm wide through the part, centered at X=75 mm, Y=35 mm.
- top relief pocket: Mill a rectangular relief pocket 37 mm x 23 mm x 4 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Hobby robot gripper claw'; this requirement is only for its chosen metal part.

---

## SMP-022-06 - Snap-together model drawbridge

Part name: Snap-together model drawbridge - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 52, "length_mm": 155, "width_mm": 75}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Snap-together model drawbridge'. The broader use
case is: A mechanical scenery kit for tabletop terrain or educational bridge models. The chosen
deliverable is only the metal body implied by: Bridge hinge tower with bearing sockets, crank axle
supports, deck stops, and base connector slots. All other product elements are external reference
items and must not be modeled. The part must perform this mechanical role: Raises and lowers a small
bridge deck using side trunnions and a crank. It is intentionally included in the SubCAD limit
corpus because: Tests structural towers, aligned hinge bores, stop surfaces, assembly slots, and
parts that must represent both static and moving constraints. The part is made from low-carbon
steel, ASTM A36 or equivalent using rectangular block stock. Start from one rectangular metal block
or plate. Saw oversize, face all datum sides, then machine the pockets, holes, slots, angled faces,
grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 155 mm x 75 mm x 52 mm.
- mounting hole pattern: Drill two through holes diameter 8 mm on the length centerline at X=15 mm and X=140 mm, Y=37 mm.
- functional center feature: Machine a central obround slot 51 mm long x 18 mm wide through the part, centered at X=77 mm, Y=37 mm.
- top relief pocket: Mill a rectangular relief pocket 38 mm x 25 mm x 16 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Snap-together model drawbridge'; this requirement is only for its chosen metal part.

---

## SMP-022-07 - Programmable peg cam music box kit

Part name: Programmable peg cam music box kit - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 11, "outer_diameter_mm": 58, "overall_length_mm": 25, "wall_minimum_mm": 23}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Programmable peg cam music box kit'. The broader
use case is: A hands-on mechanical kit where users arrange pegs to trigger small levers or chimes.
The chosen deliverable is only the metal body implied by: Cylindrical cam drum with radial peg
holes, end bearing journals, indexing marks, and drive coupling. All other product elements are
external reference items and must not be modeled. The part must perform this mechanical role:
Rotates a drum with removable pegs that actuate followers in sequence. It is intentionally included
in the SubCAD limit corpus because: Challenges cylindrical feature placement, repeated radial hole
patterns, indexing references, rotational symmetry, and detachable component interfaces. The part is
made from low-carbon steel, ASTM A36 or equivalent using round bar stock. Start from one cut length
of round metal bar. Turn the outside, face both ends, bore the center, then mill secondary flats,
slots, and radial holes as needed. No separate inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 58 mm and length 25 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 11 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 21 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 19 mm wide over 17 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M4 holes through the top flat at X=8 mm and X=16 mm.
- split relief slit: Cut one full-length radial slit 2 mm wide from the outside to the axial bore on datum-B side.
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
- Do not broaden the requirement back into the full product idea named 'Programmable peg cam music box kit'; this requirement is only for its chosen metal part.

---

## SMP-022-08 - Miniature articulated crane model

Part name: Miniature articulated crane model - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 20, "length_mm": 210, "width_mm": 65}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Miniature articulated crane model'. The broader use
case is: A non-motorized model-making kit for constructing a small workshop crane. The chosen
deliverable is only the metal body implied by: Boom rail extrusion with hinge clevis, trolley
groove, stop blocks, and cable guide holes. All other product elements are external reference items
and must not be modeled. The part must perform this mechanical role: Allows a boom to pivot and a
hook carriage to slide along a short rail. It is intentionally included in the SubCAD limit corpus
because: Tests long slender parts, sliding-track profiles, hinge clevis geometry, end stops, and
mixed load-bearing and decorative detail. The part is made from low-carbon steel, ASTM A36 or
equivalent using rectangular block stock. Start from one rectangular metal block or plate. Saw
oversize, face all datum sides, then machine the pockets, holes, slots, angled faces, grooves, and
edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 210 mm x 65 mm x 20 mm.
- mounting hole pattern: Drill two through holes diameter 8 mm on the length centerline at X=13 mm and X=197 mm, Y=32 mm.
- functional center feature: Machine a central obround slot 70 mm long x 15 mm wide through the part, centered at X=105 mm, Y=32 mm.
- top relief pocket: Mill a rectangular relief pocket 52 mm x 21 mm x 1 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Miniature articulated crane model'; this requirement is only for its chosen metal part.

---

## SMP-022-09 - Magnetic tile hinge connector

Part name: Magnetic tile hinge connector - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 12, "outer_diameter_mm": 48, "overall_length_mm": 103, "wall_minimum_mm": 18}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Magnetic tile hinge connector'. The broader use
case is: An accessory for magnetic construction tiles used to build foldable geometric models. The
chosen deliverable is only the metal body implied by: Hinge connector block with magnet pockets,
interlocking knuckles, hinge pin bore, and panel seating lips. All other product elements are
external reference items and must not be modeled. The part must perform this mechanical role:
Connects two flat panels while allowing controlled angular rotation. It is intentionally included in
the SubCAD limit corpus because: Requires magnet retention cavities, alternating hinge knuckles,
coaxial bores, tight panel-fit features, and orientation-specific assembly details. The part is made
from low-carbon steel, ASTM A36 or equivalent using round bar stock. Start from one cut length of
round metal bar. Turn the outside, face both ends, bore the center, then mill secondary flats,
slots, and radial holes as needed. No separate inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 48 mm and length 103 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 12 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 22 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 16 mm wide over 95 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M6 holes through the top flat at X=34 mm and X=68 mm.
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
- Do not broaden the requirement back into the full product idea named 'Magnetic tile hinge connector'; this requirement is only for its chosen metal part.

---

## SMP-022-10 - Tabletop marble elevator module

Part name: Tabletop marble elevator module - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 58, "length_mm": 75, "width_mm": 70}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Tabletop marble elevator module'. The broader use
case is: A mechanical expansion module for a desktop marble machine or kinetic sculpture kit. The
chosen deliverable is only the metal body implied by: Ratchet lift wheel with marble pockets, pawl
teeth, axle hub, side clearance grooves, and crank interface. All other product elements are
external reference items and must not be modeled. The part must perform this mechanical role: Lifts
marbles one step at a time using a hand-cranked ratchet wheel. It is intentionally included in the
SubCAD limit corpus because: Tests compound rotational geometry, repeated pockets, asymmetric
ratchet teeth, functional clearances, and interaction between continuous curves and discrete
indexing features. The part is made from low-carbon steel, ASTM A36 or equivalent using rectangular
block stock. Start from one rectangular metal block or plate. Saw oversize, face all datum sides,
then machine the pockets, holes, slots, angled faces, grooves, and edge treatments into that same
solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 75 mm x 70 mm x 58 mm.
- mounting hole pattern: Drill two through holes diameter 11 mm on the length centerline at X=14 mm and X=61 mm, Y=35 mm.
- functional center feature: Machine a central obround slot 30 mm long x 17 mm wide through the part, centered at X=37 mm, Y=35 mm.
- top relief pocket: Mill a rectangular relief pocket 25 mm x 23 mm x 9 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- serrated contact edge: Cut 12 equal triangular serrations across the rear edge, each 3 mm deep.

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
- Do not broaden the requirement back into the full product idea named 'Tabletop marble elevator module'; this requirement is only for its chosen metal part.

---
