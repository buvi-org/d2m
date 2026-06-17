# Agent 011 Single Metal Part Requirements

Domain: industrial sensors, test instruments, measurement fixtures, and calibration hardware

Each item below is one metal part only. Product assemblies and nonmetal components are explicitly out of scope.

## SMP-011-01 - Flush-Mount Inductive Proximity Sensor Housing

Part name: Flush-Mount Inductive Proximity Sensor Housing - single metal part

Material: 4140 alloy steel, prehard (strong cylindrical metal part with threaded and slotted details)

Envelope: `{"axial_bore_diameter_mm": 27, "outer_diameter_mm": 83, "overall_length_mm": 115, "wall_minimum_mm": 28}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Flush-Mount Inductive Proximity Sensor Housing'.
The broader use case is: Rugged sensor body used on automated machine tools to detect carriage or
fixture position in oily environments. The chosen deliverable is only the metal body implied by:
Cylindrical stainless sensor barrel with external metric threads, hex flats, stepped internal bore,
front sensing lip, O-ring groove, and rear connector pocket. All other product elements are external
reference items and must not be modeled. The part must perform this mechanical role: Holds an
inductive sensing coil, connector insert, sealing features, and wrench flats while presenting a
precise threaded mounting interface. It is intentionally included in the SubCAD limit corpus
because: Combines coaxial turned geometry, external threading, wrench flats intersecting a cylinder,
sealing grooves, thin front lips, and nested internal bores. The part is made from 4140 alloy steel,
prehard using round bar stock. Start from one cut length of round metal bar. Turn the outside, face
both ends, bore the center, then mill secondary flats, slots, and radial holes as needed. No
separate inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 83 mm and length 115 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 27 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 37 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 27 mm wide over 107 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M7 holes through the top flat at X=38 mm and X=76 mm.
- split relief slit: Cut one full-length radial slit 4 mm wide from the outside to the axial bore on datum-B side.
- outside edge treatment: Break all outside circular edges with 1.0 mm chamfers and keep internal bore edges visibly chamfered.
- opposed wrench flats: Mill two opposed flats across the outside, leaving 75 mm across flats over the middle third of the length.

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
- Do not broaden the requirement back into the full product idea named 'Flush-Mount Inductive Proximity Sensor Housing'; this requirement is only for its chosen metal part.

---

## SMP-011-02 - Dial Indicator Magnetic Base Swivel Joint

Part name: Dial Indicator Magnetic Base Swivel Joint - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 31, "length_mm": 105, "width_mm": 35}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Dial Indicator Magnetic Base Swivel Joint'. The
broader use case is: Articulated positioning hardware for holding a dial indicator on inspection
tables or machine frames. The chosen deliverable is only the metal body implied by: Machined ball-
and-socket clamp yoke with split lugs, spherical seat, cross bolt bore, serrated friction faces, and
threaded arm mount. All other product elements are external reference items and must not be modeled.
The part must perform this mechanical role: Allows a metrology arm to pivot and lock at a chosen
angle without slipping under indicator load. It is intentionally included in the SubCAD limit corpus
because: Requires spherical contact surfaces, split clamp geometry, coaxial and offset bores, lug
symmetry, serrations, and assembly-critical clearances. The part is made from low-carbon steel, ASTM
A36 or equivalent using rectangular block stock. Start from one rectangular metal block or plate.
Saw oversize, face all datum sides, then machine the pockets, holes, slots, angled faces, grooves,
and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 105 mm x 35 mm x 31 mm.
- mounting hole pattern: Drill two through holes diameter 9 mm on the length centerline at X=10 mm and X=95 mm, Y=17 mm.
- functional center feature: Machine a central obround slot 35 mm long x 16 mm wide through the part, centered at X=52 mm, Y=17 mm.
- top relief pocket: Mill a rectangular relief pocket 26 mm x 18 mm x 6 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- serrated contact edge: Cut 11 equal triangular serrations across the rear edge, each 5 mm deep.
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
- The feature named 'serrated contact edge' is present with the stated size and position.
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
- Do not broaden the requirement back into the full product idea named 'Dial Indicator Magnetic Base Swivel Joint'; this requirement is only for its chosen metal part.

---

## SMP-011-03 - Portable Pressure Calibrator Manifold Block

Part name: Portable Pressure Calibrator Manifold Block - single metal part

Material: 1045 medium-carbon steel, normalized (durable wear surface for workshop loading)

Envelope: `{"height_mm": 23, "length_mm": 220, "width_mm": 115}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Portable Pressure Calibrator Manifold Block'. The
broader use case is: Bench or field calibration fixture for comparing pressure transmitters against
a reference gauge. The chosen deliverable is only the metal body implied by: Rectangular stainless
manifold block with intersecting drilled passages, multiple threaded ports, valve cavities,
chamfered edges, mounting feet, and engraved port pads. All other product elements are external
reference items and must not be modeled. The part must perform this mechanical role: Routes
pneumatic or hydraulic pressure between pump input, reference gauge, device under test, bleed valve,
and isolation valve. It is intentionally included in the SubCAD limit corpus because: Tests hidden
internal channel logic, orthogonal port placement, pipe-thread bosses, valve counterbores, sealing
faces, and manufacturable drilling paths. The part is made from 1045 medium-carbon steel, normalized
using rectangular block stock. Start from one rectangular metal block or plate. Saw oversize, face
all datum sides, then machine the pockets, holes, slots, angled faces, grooves, and edge treatments
into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 220 mm x 115 mm x 23 mm.
- mounting hole pattern: Drill two through holes diameter 7 mm on the length centerline at X=23 mm and X=197 mm, Y=57 mm.
- functional center feature: Machine a central obround slot 73 mm long x 18 mm wide through the part, centered at X=110 mm, Y=57 mm.
- top relief pocket: Mill a rectangular relief pocket 55 mm x 38 mm x 3 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- counterbored seat: Add a central counterbore diameter 26 mm x 6 mm deep around the center feature.
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
- The feature named 'counterbored seat' is present with the stated size and position.
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
- Do not broaden the requirement back into the full product idea named 'Portable Pressure Calibrator Manifold Block'; this requirement is only for its chosen metal part.

---

## SMP-011-04 - K-Type Thermocouple Compression Fitting Adapter

Part name: K-Type Thermocouple Compression Fitting Adapter - single metal part

Material: 6061-T6 aluminum (low mass with good machinability and stable flat features)

Envelope: `{"height_mm": 28, "length_mm": 155, "width_mm": 120}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'K-Type Thermocouple Compression Fitting Adapter'.
The broader use case is: Process instrumentation fitting used to mount a thermocouple probe into a
heated chamber or pipe wall. The chosen deliverable is only the metal body implied by: Hex-body
adapter with male pipe thread, tapered ferrule cone, through bore, rear compression nut interface,
wrench flats, and lead-in chamfers. All other product elements are external reference items and must
not be modeled. The part must perform this mechanical role: Compresses a ferrule around the probe
sheath while sealing into a threaded process port. It is intentionally included in the SubCAD limit
corpus because: Mixes tapered sealing cones, axial through holes, external process threads, hex-
prism-to-cylinder transitions, small clearances, and chamfered compression features. The part is
made from 6061-T6 aluminum using rectangular block stock. Start from one rectangular metal block or
plate. Saw oversize, face all datum sides, then machine the pockets, holes, slots, angled faces,
grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 155 mm x 120 mm x 28 mm.
- mounting hole pattern: Drill two through holes diameter 9 mm on the length centerline at X=24 mm and X=131 mm, Y=60 mm.
- functional center feature: Machine a central obround slot 51 mm long x 8 mm wide through the part, centered at X=77 mm, Y=60 mm.
- top relief pocket: Mill a rectangular relief pocket 38 mm x 40 mm x 13 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- machined angled reference face: Machine one top reference face at 22 degrees over the last 31 mm of length.
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
- Do not broaden the requirement back into the full product idea named 'K-Type Thermocouple Compression Fitting Adapter'; this requirement is only for its chosen metal part.

---

## SMP-011-05 - Laser Displacement Sensor Alignment Clamp

Part name: Laser Displacement Sensor Alignment Clamp - single metal part

Material: 1045 medium-carbon steel, normalized (durable wear surface for workshop loading)

Envelope: `{"height_mm": 27, "length_mm": 220, "width_mm": 40}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Laser Displacement Sensor Alignment Clamp'. The
broader use case is: Adjustable mount for aiming a compact laser triangulation sensor at a
production inspection target. The chosen deliverable is only the metal body implied by: Split
rectangular cradle with semicircular clamp bore, slotted adjustment arc, datum mounting face,
captive screw pockets, and relieved optical window opening. All other product elements are external
reference items and must not be modeled. The part must perform this mechanical role: Clamps the
sensor body and provides fine angular alignment while preserving optical clearance around the
emitter and receiver window. It is intentionally included in the SubCAD limit corpus because: Tests
partial cylindrical cuts through blocky geometry, curved slots, asymmetric reliefs, thin clamp
bridges, screw bosses, and datum-critical mounting surfaces. The part is made from 1045 medium-
carbon steel, normalized using rectangular block stock. Start from one rectangular metal block or
plate. Saw oversize, face all datum sides, then machine the pockets, holes, slots, angled faces,
grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 220 mm x 40 mm x 27 mm.
- mounting hole pattern: Drill two through holes diameter 7 mm on the length centerline at X=10 mm and X=210 mm, Y=20 mm.
- functional center feature: Machine a central obround slot 73 mm long x 8 mm wide through the part, centered at X=110 mm, Y=20 mm.
- top relief pocket: Mill a rectangular relief pocket 55 mm x 18 mm x 9 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
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
- Do not broaden the requirement back into the full product idea named 'Laser Displacement Sensor Alignment Clamp'; this requirement is only for its chosen metal part.

---

## SMP-011-06 - Calibration Weight Carrier Tray Insert

Part name: Calibration Weight Carrier Tray Insert - single metal part

Material: AISI 316 stainless steel (corrosion resistance and cleanable metal surfaces)

Envelope: `{"length_mm": 125, "thickness_mm": 7, "width_mm": 60}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Calibration Weight Carrier Tray Insert'. The
broader use case is: Precision storage and handling insert for certified mass standards used in
scale and balance calibration labs. The chosen deliverable is only the metal body implied by:
Machined aluminum tray insert with stepped circular pockets, soft-radius finger scoops, engraved
weight labels, dowel locating holes, and perimeter retaining ledge. All other product elements are
external reference items and must not be modeled. The part must perform this mechanical role:
Locates several cylindrical calibration weights without contact damage and provides finger access
for removal. It is intentionally included in the SubCAD limit corpus because: Includes repeated
pocket patterns with varying diameters, blended access cutouts, shallow engraving fields, ledges,
fillets, and ergonomic clearance geometry. The part is made from AISI 316 stainless steel using
sheet or plate stock. Start from one flat sheet or plate blank. Cut the outside profile, machine
holes, slots, pockets, lips, and relief features into that same piece. If bends are called out, they
are bends in the same sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 125 mm x 60 mm x 7 mm.
- mounting hole pattern: Drill two through holes diameter 10 mm on the length centerline at X=12 mm and X=113 mm, Y=30 mm.
- functional center feature: Machine a central obround slot 41 mm long x 8 mm wide through the part, centered at X=62 mm, Y=30 mm.
- top relief pocket: Mill a rectangular relief pocket 31 mm x 20 mm x 1 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- serrated contact edge: Cut 7 equal triangular serrations across the rear edge, each 3 mm deep.

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
- Do not broaden the requirement back into the full product idea named 'Calibration Weight Carrier Tray Insert'; this requirement is only for its chosen metal part.

---

## SMP-011-07 - Vibration Accelerometer Stud-Mount Adapter

Part name: Vibration Accelerometer Stud-Mount Adapter - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 53, "length_mm": 180, "width_mm": 105}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Vibration Accelerometer Stud-Mount Adapter'. The
broader use case is: Mechanical adapter used to mount an accelerometer onto curved motor housings or
bearing blocks during vibration testing. The chosen deliverable is only the metal body implied by:
Low-profile circular adapter puck with curved underside saddle, central threaded stud hole, top
precision pad, spanner holes, and anti-rotation flats. All other product elements are external
reference items and must not be modeled. The part must perform this mechanical role: Provides a flat
sensor mounting pad and a secure threaded connection to a non-flat machine surface. It is
intentionally included in the SubCAD limit corpus because: Challenges representation of concave
saddle surfaces, flat-to-curved transitions, threaded axial features, tool-access holes, and
orientation-specific mounting faces. The part is made from low-carbon steel, ASTM A36 or equivalent
using rectangular block stock. Start from one rectangular metal block or plate. Saw oversize, face
all datum sides, then machine the pockets, holes, slots, angled faces, grooves, and edge treatments
into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 180 mm x 105 mm x 53 mm.
- mounting hole pattern: Drill two through holes diameter 7 mm on the length centerline at X=21 mm and X=159 mm, Y=52 mm.
- functional center feature: Machine a central obround slot 60 mm long x 16 mm wide through the part, centered at X=90 mm, Y=52 mm.
- top relief pocket: Mill a rectangular relief pocket 45 mm x 35 mm x 10 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Vibration Accelerometer Stud-Mount Adapter'; this requirement is only for its chosen metal part.

---

## SMP-011-08 - Micrometer Calibration Step Gauge Block

Part name: Micrometer Calibration Step Gauge Block - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 24, "outer_diameter_mm": 73, "overall_length_mm": 49, "wall_minimum_mm": 24}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Micrometer Calibration Step Gauge Block'. The
broader use case is: Shop-floor reference artifact for checking outside micrometers and digital
calipers at several known distances. The chosen deliverable is only the metal body implied by:
Ground steel stepped gauge bar with ascending precision shoulders, relief grooves at step roots,
chamfered handling ends, serial-number pad, and case locating notch. All other product elements are
external reference items and must not be modeled. The part must perform this mechanical role:
Provides multiple precision step heights and measuring lands in one rigid calibration object. It is
intentionally included in the SubCAD limit corpus because: Tests exact stepped datum relationships,
sharp-but-relieved inside corners, tolerance-sensitive measuring faces, asymmetric notch placement,
and labeled nonfunctional surfaces. The part is made from low-carbon steel, ASTM A36 or equivalent
using round bar stock. Start from one cut length of round metal bar. Turn the outside, face both
ends, bore the center, then mill secondary flats, slots, and radial holes as needed. No separate
inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 73 mm and length 49 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 24 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 34 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 24 mm wide over 41 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M5 holes through the top flat at X=16 mm and X=32 mm.
- split relief slit: Cut one full-length radial slit 4 mm wide from the outside to the axial bore on datum-B side.
- outside edge treatment: Break all outside circular edges with 1.0 mm chamfers and keep internal bore edges visibly chamfered.
- cross relief slot: Machine one transverse slot 6 mm wide across the top flat at X=24 mm, depth 7 mm.

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
- Do not broaden the requirement back into the full product idea named 'Micrometer Calibration Step Gauge Block'; this requirement is only for its chosen metal part.

---

## SMP-011-09 - Conductivity Probe Flow Cell Body

Part name: Conductivity Probe Flow Cell Body - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 13, "outer_diameter_mm": 69, "overall_length_mm": 73, "wall_minimum_mm": 28}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Conductivity Probe Flow Cell Body'. The broader use
case is: Inline measurement cell for holding conductivity or pH probes in a controlled liquid sample
stream. The chosen deliverable is only the metal body implied by: Machined polymer or stainless flow
cell body with central flow chamber, angled probe port, inlet and outlet tube bosses, O-ring glands,
and transparent cover screw pattern. All other product elements are external reference items and
must not be modeled. The part must perform this mechanical role: Directs fluid past the sensing tip
while sealing threaded probe ports and tube connections. It is intentionally included in the SubCAD
limit corpus because: Combines angled intersecting bores, internal fluid cavity, sealing grooves,
raised tube bosses, cover fastener patterns, and asymmetric inspection geometry. The part is made
from low-carbon steel, ASTM A36 or equivalent using round bar stock. Start from one cut length of
round metal bar. Turn the outside, face both ends, bore the center, then mill secondary flats,
slots, and radial holes as needed. No separate inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 69 mm and length 73 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 13 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 23 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 23 mm wide over 65 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M4 holes through the top flat at X=24 mm and X=48 mm.
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
- Do not broaden the requirement back into the full product idea named 'Conductivity Probe Flow Cell Body'; this requirement is only for its chosen metal part.

---

## SMP-011-10 - Torque Sensor Reaction Arm Hub

Part name: Torque Sensor Reaction Arm Hub - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 11, "outer_diameter_mm": 33, "overall_length_mm": 92, "wall_minimum_mm": 11}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Torque Sensor Reaction Arm Hub'. The broader use
case is: Adapter hub for coupling a rotary torque transducer to a reaction arm during motor or
gearbox testing. The chosen deliverable is only the metal body implied by: Cylindrical hub with
keyed central bore, radial reaction-arm lug, bolt circle, split clamp slot, dowel holes, and
filleted torque-transfer shoulders. All other product elements are external reference items and must
not be modeled. The part must perform this mechanical role: Transfers torque reaction to a fixed arm
while keeping the sensor shaft concentric and accessible. It is intentionally included in the SubCAD
limit corpus because: Tests keyed bores, radial protrusions from rotational bodies, bolt-circle
patterns, clamp slots crossing round geometry, heavy fillets, and load-path-specific shape. The part
is made from low-carbon steel, ASTM A36 or equivalent using round bar stock. Start from one cut
length of round metal bar. Turn the outside, face both ends, bore the center, then mill secondary
flats, slots, and radial holes as needed. No separate inserts or fasteners are part of the
deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 33 mm and length 92 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 11 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 21 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 11 mm wide over 84 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M8 holes through the top flat at X=30 mm and X=61 mm.
- split relief slit: Cut one full-length radial slit 3 mm wide from the outside to the axial bore on datum-B side.
- outside edge treatment: Break all outside circular edges with 1.0 mm chamfers and keep internal bore edges visibly chamfered.
- cross relief slot: Machine one transverse slot 5 mm wide across the top flat at X=46 mm, depth 3 mm.

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
- Do not broaden the requirement back into the full product idea named 'Torque Sensor Reaction Arm Hub'; this requirement is only for its chosen metal part.

---
