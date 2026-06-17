# Agent 014 Single Metal Part Requirements

Domain: musical instrument hardware, stage equipment, pedals, stands, and tuning mechanisms

Each item below is one metal part only. Product assemblies and nonmetal components are explicitly out of scope.

## SMP-014-01 - Locking Tremolo Saddle Micro-Adjuster

Part name: Locking Tremolo Saddle Micro-Adjuster - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 46, "length_mm": 90, "width_mm": 80}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Locking Tremolo Saddle Micro-Adjuster'. The broader
use case is: Electric guitar floating tremolo bridge hardware The chosen deliverable is only the
metal body implied by: Machined saddle block with captive screw channel, string witness groove,
clamp face, and radiused bridge contact underside All other product elements are external reference
items and must not be modeled. The part must perform this mechanical role: Allows fine string
intonation adjustment while clamping the saddle against vibrational movement It is intentionally
included in the SubCAD limit corpus because: Combines angled string paths, small threaded adjustment
features, asymmetric bearing surfaces, and precise contact geometry in one compact part The part is
made from low-carbon steel, ASTM A36 or equivalent using rectangular block stock. Start from one
rectangular metal block or plate. Saw oversize, face all datum sides, then machine the pockets,
holes, slots, angled faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 90 mm x 80 mm x 46 mm.
- mounting hole pattern: Drill two through holes diameter 9 mm on the length centerline at X=16 mm and X=74 mm, Y=40 mm.
- functional center feature: Machine a central obround slot 30 mm long x 9 mm wide through the part, centered at X=45 mm, Y=40 mm.
- top relief pocket: Mill a rectangular relief pocket 25 mm x 26 mm x 2 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- machined angled reference face: Machine one top reference face at 18 degrees over the last 18 mm of length.
- side tapped hole: Tap one side hole M8 from the right long edge into the central pocket; hole axis is parallel to Y.

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
- Do not broaden the requirement back into the full product idea named 'Locking Tremolo Saddle Micro-Adjuster'; this requirement is only for its chosen metal part.

---

## SMP-014-02 - Kick Drum Pedal Cam Hub

Part name: Kick Drum Pedal Cam Hub - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 63, "length_mm": 105, "width_mm": 90}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Kick Drum Pedal Cam Hub'. The broader use case is:
Bass drum pedal drive mechanism The chosen deliverable is only the metal body implied by: Eccentric
machined cam hub with axle bore, chain anchor slot, set-screw flats, and variable-radius outer
profile All other product elements are external reference items and must not be modeled. The part
must perform this mechanical role: Converts footboard motion into beater rotation with a non-linear
response curve It is intentionally included in the SubCAD limit corpus because: Requires
representing non-circular curves, offset bores, clamping details, and functional clearance around a
rotating assembly The part is made from low-carbon steel, ASTM A36 or equivalent using rectangular
block stock. Start from one rectangular metal block or plate. Saw oversize, face all datum sides,
then machine the pockets, holes, slots, angled faces, grooves, and edge treatments into that same
solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 105 mm x 90 mm x 63 mm.
- mounting hole pattern: Drill two through holes diameter 9 mm on the length centerline at X=18 mm and X=87 mm, Y=45 mm.
- functional center feature: Machine a central obround slot 35 mm long x 8 mm wide through the part, centered at X=52 mm, Y=45 mm.
- top relief pocket: Mill a rectangular relief pocket 26 mm x 30 mm x 8 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- side tapped hole: Tap one side hole M7 from the right long edge into the central pocket; hole axis is parallel to Y.

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
- Do not broaden the requirement back into the full product idea named 'Kick Drum Pedal Cam Hub'; this requirement is only for its chosen metal part.

---

## SMP-014-03 - Hi-Hat Clutch Lock Collar

Part name: Hi-Hat Clutch Lock Collar - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 17, "outer_diameter_mm": 53, "overall_length_mm": 99, "wall_minimum_mm": 18}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Hi-Hat Clutch Lock Collar'. The broader use case
is: Drum kit hi-hat cymbal stand The chosen deliverable is only the metal body implied by: Knurled
cylindrical collar with split clamp, cross screw boss, stepped felt seat, and central rod bore All
other product elements are external reference items and must not be modeled. The part must perform
this mechanical role: Locks the top cymbal to the pull rod while allowing controlled felt
compression It is intentionally included in the SubCAD limit corpus because: Tests concentric
stepped geometry, split clamp gaps, knurl-like grip surfaces, and small fastener bosses The part is
made from low-carbon steel, ASTM A36 or equivalent using round bar stock. Start from one cut length
of round metal bar. Turn the outside, face both ends, bore the center, then mill secondary flats,
slots, and radial holes as needed. No separate inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 53 mm and length 99 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 17 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 27 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 17 mm wide over 91 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M5 holes through the top flat at X=33 mm and X=66 mm.
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
- Do not broaden the requirement back into the full product idea named 'Hi-Hat Clutch Lock Collar'; this requirement is only for its chosen metal part.

---

## SMP-014-04 - Pedalboard Quick-Release Rail Clamp

Part name: Pedalboard Quick-Release Rail Clamp - single metal part

Material: 1045 medium-carbon steel, normalized (durable wear surface for workshop loading)

Envelope: `{"length_mm": 230, "thickness_mm": 3, "width_mm": 85}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Pedalboard Quick-Release Rail Clamp'. The broader
use case is: Modular guitar effects pedalboard mounting system The chosen deliverable is only the
metal body implied by: Low-profile machined clamp shoe with dovetail rail engagement, eccentric
locking tab, and pedal flange capture lip All other product elements are external reference items
and must not be modeled. The part must perform this mechanical role: Secures an effects pedal to a
slotted rail without permanent adhesive or hook-and-loop material It is intentionally included in
the SubCAD limit corpus because: Involves undercuts, dovetail interfaces, low-clearance sliding
features, and geometry tied to repeated user adjustment The part is made from 1045 medium-carbon
steel, normalized using sheet or plate stock. Start from one flat sheet or plate blank. Cut the
outside profile, machine holes, slots, pockets, lips, and relief features into that same piece. If
bends are called out, they are bends in the same sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 230 mm x 85 mm x 3 mm.
- mounting hole pattern: Drill two through holes diameter 7 mm on the length centerline at X=17 mm and X=213 mm, Y=42 mm.
- functional center feature: Machine a central obround slot 76 mm long x 17 mm wide through the part, centered at X=115 mm, Y=42 mm.
- top relief pocket: Mill a rectangular relief pocket 57 mm x 28 mm x 1 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- dovetail slide form: Machine a straight dovetail groove on the top face, length 206 mm, throat 17 mm, included angle 60 degrees.

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
- The feature named 'dovetail slide form' is present with the stated size and position.
- All required chamfers, reliefs, and edge treatments are visible in STEP and STL outputs.
- No extra parts, fasteners, hardware, labels, cosmetic meshes, or nonmetal components are present.
- Flat datums remain planar and usable; pockets or slots do not accidentally break unsupported walls.

Negative requirements:
- Represent exactly one metal part only.
- Do not model screws, nuts, springs, bushings, bearings, rubber pads, plastic covers, electronics, labels, handles, knobs, adhesives, weld beads, or separate inserts.
- Do not convert the part into an assembly or multiple bodies.
- Do not replace through holes, slots, pockets, grooves, flats, tapers, or chamfers with cosmetic markings.
- Do not omit datum-critical features just because they are small.
- Do not broaden the requirement back into the full product idea named 'Pedalboard Quick-Release Rail Clamp'; this requirement is only for its chosen metal part.

---

## SMP-014-05 - Mic Stand Boom Angle Rosette Joint

Part name: Mic Stand Boom Angle Rosette Joint - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 60, "length_mm": 125, "width_mm": 70}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Mic Stand Boom Angle Rosette Joint'. The broader
use case is: Adjustable microphone boom stand The chosen deliverable is only the metal body implied
by: Toothed rosette hinge disk with central pivot bore, radial locking teeth, compression washer
seat, and boom socket boss All other product elements are external reference items and must not be
modeled. The part must perform this mechanical role: Locks a boom arm at repeatable angular
positions without slipping under microphone weight It is intentionally included in the SubCAD limit
corpus because: Tests radial tooth arrays, circular symmetry with localized bosses, mating friction
surfaces, and load-bearing hinge geometry The part is made from low-carbon steel, ASTM A36 or
equivalent using rectangular block stock. Start from one rectangular metal block or plate. Saw
oversize, face all datum sides, then machine the pockets, holes, slots, angled faces, grooves, and
edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 125 mm x 70 mm x 60 mm.
- mounting hole pattern: Drill two through holes diameter 11 mm on the length centerline at X=14 mm and X=111 mm, Y=35 mm.
- functional center feature: Machine a central obround slot 41 mm long x 10 mm wide through the part, centered at X=62 mm, Y=35 mm.
- top relief pocket: Mill a rectangular relief pocket 31 mm x 23 mm x 13 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- serrated contact edge: Cut 6 equal triangular serrations across the rear edge, each 3 mm deep.
- machined angled reference face: Machine one top reference face at 25 degrees over the last 25 mm of length.

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
- The feature named 'machined angled reference face' is present with the stated size and position.
- All required chamfers, reliefs, and edge treatments are visible in STEP and STL outputs.
- No extra parts, fasteners, hardware, labels, cosmetic meshes, or nonmetal components are present.
- Flat datums remain planar and usable; pockets or slots do not accidentally break unsupported walls.

Negative requirements:
- Represent exactly one metal part only.
- Do not model screws, nuts, springs, bushings, bearings, rubber pads, plastic covers, electronics, labels, handles, knobs, adhesives, weld beads, or separate inserts.
- Do not convert the part into an assembly or multiple bodies.
- Do not replace through holes, slots, pockets, grooves, flats, tapers, or chamfers with cosmetic markings.
- Do not omit datum-critical features just because they are small.
- Do not broaden the requirement back into the full product idea named 'Mic Stand Boom Angle Rosette Joint'; this requirement is only for its chosen metal part.

---

## SMP-014-06 - Violin Fine Tuner Lever Body

Part name: Violin Fine Tuner Lever Body - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 32, "length_mm": 80, "width_mm": 80}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Violin Fine Tuner Lever Body'. The broader use case
is: String fine tuner mounted on a violin tailpiece The chosen deliverable is only the metal body
implied by: Miniature lever frame with string hook, pivot ears, screw contact pad, and tailpiece
mounting saddle All other product elements are external reference items and must not be modeled. The
part must perform this mechanical role: Transfers screw motion into small string tension changes for
precise pitch tuning It is intentionally included in the SubCAD limit corpus because: Requires tiny
functional features, curved string contact paths, pivot geometry, and tight spatial relationships
between interacting mechanisms The part is made from low-carbon steel, ASTM A36 or equivalent using
rectangular block stock. Start from one rectangular metal block or plate. Saw oversize, face all
datum sides, then machine the pockets, holes, slots, angled faces, grooves, and edge treatments into
that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 80 mm x 80 mm x 32 mm.
- mounting hole pattern: Drill two through holes diameter 11 mm on the length centerline at X=16 mm and X=64 mm, Y=40 mm.
- functional center feature: Machine a central obround slot 30 mm long x 12 mm wide through the part, centered at X=40 mm, Y=40 mm.
- top relief pocket: Mill a rectangular relief pocket 25 mm x 26 mm x 6 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- integral hook lip: Leave an integral hook lip on one short end, projecting 15 mm and undercut 5 mm for registration.
- side tapped hole: Tap one side hole M7 from the right long edge into the central pocket; hole axis is parallel to Y.

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
- Do not broaden the requirement back into the full product idea named 'Violin Fine Tuner Lever Body'; this requirement is only for its chosen metal part.

---

## SMP-014-07 - Cymbal Stand Memory Lock

Part name: Cymbal Stand Memory Lock - single metal part

Material: 4140 alloy steel, prehard (strong cylindrical metal part with threaded and slotted details)

Envelope: `{"axial_bore_diameter_mm": 13, "outer_diameter_mm": 66, "overall_length_mm": 112, "wall_minimum_mm": 26}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Cymbal Stand Memory Lock'. The broader use case is:
Stage drum hardware stand height positioning The chosen deliverable is only the metal body implied
by: Split ring collar with hinged lug, indexed orientation notch, thumb-screw boss, and internal
tube relief groove All other product elements are external reference items and must not be modeled.
The part must perform this mechanical role: Clamps around a stand tube to preserve repeatable height
and orientation during setup It is intentionally included in the SubCAD limit corpus because: Tests
split circular bodies, hinge-and-clamp features, ergonomic screw placement, and internal cylindrical
fit constraints The part is made from 4140 alloy steel, prehard using round bar stock. Start from
one cut length of round metal bar. Turn the outside, face both ends, bore the center, then mill
secondary flats, slots, and radial holes as needed. No separate inserts or fasteners are part of the
deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 66 mm and length 112 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 13 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 23 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 22 mm wide over 104 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M6 holes through the top flat at X=37 mm and X=74 mm.
- split relief slit: Cut one full-length radial slit 3 mm wide from the outside to the axial bore on datum-B side.
- outside edge treatment: Break all outside circular edges with 1.0 mm chamfers and keep internal bore edges visibly chamfered.
- cross relief slot: Machine one transverse slot 5 mm wide across the top flat at X=56 mm, depth 6 mm.

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
- Do not broaden the requirement back into the full product idea named 'Cymbal Stand Memory Lock'; this requirement is only for its chosen metal part.

---

## SMP-014-08 - Expression Pedal Rocker Pivot Block

Part name: Expression Pedal Rocker Pivot Block - single metal part

Material: 1045 medium-carbon steel, normalized (durable wear surface for workshop loading)

Envelope: `{"height_mm": 64, "length_mm": 170, "width_mm": 105}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Expression Pedal Rocker Pivot Block'. The broader
use case is: Guitar or synthesizer expression pedal enclosure The chosen deliverable is only the
metal body implied by: Machined pivot block with dual bearing bores, rocker stop faces, sensor
linkage slot, and enclosure mounting feet All other product elements are external reference items
and must not be modeled. The part must perform this mechanical role: Supports smooth rocker motion
and transfers position to an internal sensor linkage It is intentionally included in the SubCAD
limit corpus because: Combines aligned bearing geometry, motion stops, linkage clearance, and
structural mounting surfaces in a compact mechanism The part is made from 1045 medium-carbon steel,
normalized using rectangular block stock. Start from one rectangular metal block or plate. Saw
oversize, face all datum sides, then machine the pockets, holes, slots, angled faces, grooves, and
edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 170 mm x 105 mm x 64 mm.
- mounting hole pattern: Drill two through holes diameter 8 mm on the length centerline at X=21 mm and X=149 mm, Y=52 mm.
- functional center feature: Machine a central obround slot 56 mm long x 9 mm wide through the part, centered at X=85 mm, Y=52 mm.
- top relief pocket: Mill a rectangular relief pocket 42 mm x 35 mm x 23 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Expression Pedal Rocker Pivot Block'; this requirement is only for its chosen metal part.

---

## SMP-014-09 - Keyboard Stand Telescoping Tube Latch

Part name: Keyboard Stand Telescoping Tube Latch - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 10, "outer_diameter_mm": 42, "overall_length_mm": 75, "wall_minimum_mm": 16}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Keyboard Stand Telescoping Tube Latch'. The broader
use case is: Collapsible stage keyboard stand The chosen deliverable is only the metal body implied
by: Spring-loaded latch housing with plunger bore, angled thumb pad, tube saddle radius, and detent
pin guide All other product elements are external reference items and must not be modeled. The part
must perform this mechanical role: Locks telescoping support tubes at selectable width or height
settings It is intentionally included in the SubCAD limit corpus because: Requires nested
cylindrical interfaces, spring/plunger accommodation, ergonomic external shape, and precise
alignment with repeated adjustment holes The part is made from low-carbon steel, ASTM A36 or
equivalent using round bar stock. Start from one cut length of round metal bar. Turn the outside,
face both ends, bore the center, then mill secondary flats, slots, and radial holes as needed. No
separate inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 42 mm and length 75 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 10 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 20 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 14 mm wide over 67 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M5 holes through the top flat at X=25 mm and X=50 mm.
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
- Do not broaden the requirement back into the full product idea named 'Keyboard Stand Telescoping Tube Latch'; this requirement is only for its chosen metal part.

---

## SMP-014-10 - Guitar Tuning Machine Worm Gear Bracket

Part name: Guitar Tuning Machine Worm Gear Bracket - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 12, "outer_diameter_mm": 48, "overall_length_mm": 82, "wall_minimum_mm": 18}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Guitar Tuning Machine Worm Gear Bracket'. The
broader use case is: Open-gear guitar headstock tuning machine The chosen deliverable is only the
metal body implied by: Machined tuner bracket with two raised bearing towers, worm shaft bores,
string post clearance pocket, and screw mounting ears All other product elements are external
reference items and must not be modeled. The part must perform this mechanical role: Holds the worm
shaft in alignment with the string post gear while mounting to the headstock It is intentionally
included in the SubCAD limit corpus because: Tests multi-axis alignment, small bearing supports,
gear clearance pockets, thin mounting tabs, and ornamental yet functional hardware geometry The part
is made from low-carbon steel, ASTM A36 or equivalent using round bar stock. Start from one cut
length of round metal bar. Turn the outside, face both ends, bore the center, then mill secondary
flats, slots, and radial holes as needed. No separate inserts or fasteners are part of the
deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 48 mm and length 82 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 12 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 22 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 16 mm wide over 74 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M6 holes through the top flat at X=27 mm and X=54 mm.
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
- Do not broaden the requirement back into the full product idea named 'Guitar Tuning Machine Worm Gear Bracket'; this requirement is only for its chosen metal part.

---
