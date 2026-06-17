# Agent 002 Single Metal Part Requirements

Domain: bicycle, scooter, and light mobility hardware

Each item below is one metal part only. Product assemblies and nonmetal components are explicitly out of scope.

## SMP-002-01 - Bicycle thru-axle chain tensioner dropout insert

Part name: Bicycle thru-axle chain tensioner dropout insert - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 36, "length_mm": 105, "width_mm": 105}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Bicycle thru-axle chain tensioner dropout insert'.
The broader use case is: Single-speed or internally geared bicycle frame with sliding rear dropouts
The chosen deliverable is only the metal body implied by: Machined dropout insert with axle bore,
adjustment screw seat, guide rails, and clamp faces All other product elements are external
reference items and must not be modeled. The part must perform this mechanical role: Provides
precise fore-aft axle adjustment while maintaining wheel alignment under pedaling load It is
intentionally included in the SubCAD limit corpus because: Requires coaxial axle geometry, sliding
contact faces, threaded adjustment features, asymmetric reliefs, and tight relationships between
clamping and alignment surfaces The part is made from low-carbon steel, ASTM A36 or equivalent using
rectangular block stock. Start from one rectangular metal block or plate. Saw oversize, face all
datum sides, then machine the pockets, holes, slots, angled faces, grooves, and edge treatments into
that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 105 mm x 105 mm x 36 mm.
- mounting hole pattern: Drill two through holes diameter 9 mm on the length centerline at X=21 mm and X=84 mm, Y=52 mm.
- functional center feature: Machine a central obround slot 35 mm long x 11 mm wide through the part, centered at X=52 mm, Y=52 mm.
- top relief pocket: Mill a rectangular relief pocket 26 mm x 35 mm x 15 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Bicycle thru-axle chain tensioner dropout insert'; this requirement is only for its chosen metal part.

---

## SMP-002-02 - Electric scooter folding stem hinge knuckle

Part name: Electric scooter folding stem hinge knuckle - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 64, "length_mm": 110, "width_mm": 90}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Electric scooter folding stem hinge knuckle'. The
broader use case is: Commuter electric scooter with a folding handlebar stem The chosen deliverable
is only the metal body implied by: Machined hinge knuckle with interlocking ears, pivot bore, latch
pocket, stop faces, and cable clearance channel All other product elements are external reference
items and must not be modeled. The part must perform this mechanical role: Allows the stem to fold
for storage while locking rigidly during riding It is intentionally included in the SubCAD limit
corpus because: Combines hinge articulation geometry, nested forked features, hard stop surfaces,
nontrivial pockets, and clearance routing in a compact safety-critical part The part is made from
low-carbon steel, ASTM A36 or equivalent using rectangular block stock. Start from one rectangular
metal block or plate. Saw oversize, face all datum sides, then machine the pockets, holes, slots,
angled faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 110 mm x 90 mm x 64 mm.
- mounting hole pattern: Drill two through holes diameter 11 mm on the length centerline at X=18 mm and X=92 mm, Y=45 mm.
- functional center feature: Machine a central obround slot 36 mm long x 17 mm wide through the part, centered at X=55 mm, Y=45 mm.
- top relief pocket: Mill a rectangular relief pocket 27 mm x 30 mm x 18 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Electric scooter folding stem hinge knuckle'; this requirement is only for its chosen metal part.

---

## SMP-002-03 - Cargo bicycle adjustable kickstand yoke

Part name: Cargo bicycle adjustable kickstand yoke - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 17, "outer_diameter_mm": 53, "overall_length_mm": 45, "wall_minimum_mm": 18}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Cargo bicycle adjustable kickstand yoke'. The
broader use case is: Long-tail or front-loader cargo bicycle needing a stable center stand The
chosen deliverable is only the metal body implied by: Machined yoke block with paired leg sockets,
cross-pin bores, frame interface bosses, and angular stop shoulders All other product elements are
external reference items and must not be modeled. The part must perform this mechanical role:
Connects twin kickstand legs to the frame and lets their stance width or angle be tuned It is
intentionally included in the SubCAD limit corpus because: Tests mirrored but angled sockets, load-
bearing bosses, intersecting holes, repeated pin features, and geometry that must communicate stance
and mechanical limits The part is made from low-carbon steel, ASTM A36 or equivalent using round bar
stock. Start from one cut length of round metal bar. Turn the outside, face both ends, bore the
center, then mill secondary flats, slots, and radial holes as needed. No separate inserts or
fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 53 mm and length 45 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 17 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 27 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 17 mm wide over 37 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M4 holes through the top flat at X=15 mm and X=30 mm.
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
- Do not broaden the requirement back into the full product idea named 'Cargo bicycle adjustable kickstand yoke'; this requirement is only for its chosen metal part.

---

## SMP-002-04 - Bicycle disc brake flat-mount adapter with cooling fins

Part name: Bicycle disc brake flat-mount adapter with cooling fins - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 41, "length_mm": 205, "width_mm": 105}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Bicycle disc brake flat-mount adapter with cooling
fins'. The broader use case is: Road or gravel bicycle adapting a caliper to a larger rotor size The
chosen deliverable is only the metal body implied by: Machined brake adapter with stepped mounting
pads, through holes, counterbores, rotor-clearance arch, and integral fins All other product
elements are external reference items and must not be modeled. The part must perform this mechanical
role: Offsets the brake caliper to the correct rotor radius while adding heat-dissipating surface
area It is intentionally included in the SubCAD limit corpus because: Requires precise hole spacing,
parallel datum surfaces, curved clearance envelopes, thin repeated fin geometry, and functional
offsets The part is made from low-carbon steel, ASTM A36 or equivalent using rectangular block
stock. Start from one rectangular metal block or plate. Saw oversize, face all datum sides, then
machine the pockets, holes, slots, angled faces, grooves, and edge treatments into that same solid
piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 205 mm x 105 mm x 41 mm.
- mounting hole pattern: Drill two through holes diameter 8 mm on the length centerline at X=21 mm and X=184 mm, Y=52 mm.
- functional center feature: Machine a central obround slot 68 mm long x 12 mm wide through the part, centered at X=102 mm, Y=52 mm.
- top relief pocket: Mill a rectangular relief pocket 51 mm x 35 mm x 18 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- serrated contact edge: Cut 11 equal triangular serrations across the rear edge, each 3 mm deep.
- counterbored seat: Add a central counterbore diameter 20 mm x 6 mm deep around the center feature.

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
- The feature named 'counterbored seat' is present with the stated size and position.
- All required chamfers, reliefs, and edge treatments are visible in STEP and STL outputs.
- No extra parts, fasteners, hardware, labels, cosmetic meshes, or nonmetal components are present.
- Flat datums remain planar and usable; pockets or slots do not accidentally break unsupported walls.

Negative requirements:
- Represent exactly one metal part only.
- Do not model screws, nuts, springs, bushings, bearings, rubber pads, plastic covers, electronics, labels, handles, knobs, adhesives, weld beads, or separate inserts.
- Do not convert the part into an assembly or multiple bodies.
- Do not replace through holes, slots, pockets, grooves, flats, tapers, or chamfers with cosmetic markings.
- Do not omit datum-critical features just because they are small.
- Do not broaden the requirement back into the full product idea named 'Bicycle disc brake flat-mount adapter with cooling fins'; this requirement is only for its chosen metal part.

---

## SMP-002-05 - Scooter rear suspension rocker link

Part name: Scooter rear suspension rocker link - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 29, "length_mm": 180, "width_mm": 110}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Scooter rear suspension rocker link'. The broader
use case is: Light electric scooter with compact rear swingarm suspension The chosen deliverable is
only the metal body implied by: Machined rocker link with three bearing bores, offset lobes, spacer
bosses, and weight-relief pockets All other product elements are external reference items and must
not be modeled. The part must perform this mechanical role: Transfers motion from the rear swingarm
to a small shock absorber with defined leverage ratio It is intentionally included in the SubCAD
limit corpus because: Tests multi-axis pivot relationships, organic but machinable link profiles,
boss thickness transitions, pocketing, and bearing-seat precision The part is made from low-carbon
steel, ASTM A36 or equivalent using rectangular block stock. Start from one rectangular metal block
or plate. Saw oversize, face all datum sides, then machine the pockets, holes, slots, angled faces,
grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 180 mm x 110 mm x 29 mm.
- mounting hole pattern: Drill two through holes diameter 10 mm on the length centerline at X=22 mm and X=158 mm, Y=55 mm.
- functional center feature: Machine a central obround slot 60 mm long x 17 mm wide through the part, centered at X=90 mm, Y=55 mm.
- top relief pocket: Mill a rectangular relief pocket 45 mm x 36 mm x 14 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Scooter rear suspension rocker link'; this requirement is only for its chosen metal part.

---

## SMP-002-06 - Folding bicycle handlebar latch cam

Part name: Folding bicycle handlebar latch cam - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 16, "outer_diameter_mm": 83, "overall_length_mm": 43, "wall_minimum_mm": 33}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Folding bicycle handlebar latch cam'. The broader
use case is: Folding bicycle handlepost latch mechanism The chosen deliverable is only the metal
body implied by: Machined eccentric cam lever with pivot bore, cam surface, finger relief, and
latch-pin contact pad All other product elements are external reference items and must not be
modeled. The part must perform this mechanical role: Applies over-center clamping force to secure
the folding handlebar post It is intentionally included in the SubCAD limit corpus because: Requires
eccentric surfaces, smooth cam profiles, ergonomic lever shaping, contact patches, and clear
representation of over-center locking geometry The part is made from low-carbon steel, ASTM A36 or
equivalent using round bar stock. Start from one cut length of round metal bar. Turn the outside,
face both ends, bore the center, then mill secondary flats, slots, and radial holes as needed. No
separate inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 83 mm and length 43 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 16 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 26 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 27 mm wide over 35 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M7 holes through the top flat at X=14 mm and X=28 mm.
- split relief slit: Cut one full-length radial slit 5 mm wide from the outside to the axial bore on datum-B side.
- outside edge treatment: Break all outside circular edges with 1.0 mm chamfers and keep internal bore edges visibly chamfered.
- cross relief slot: Machine one transverse slot 7 mm wide across the top flat at X=21 mm, depth 8 mm.

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
- Do not broaden the requirement back into the full product idea named 'Folding bicycle handlebar latch cam'; this requirement is only for its chosen metal part.

---

## SMP-002-07 - E-bike mid-drive motor torque arm spline clamp

Part name: E-bike mid-drive motor torque arm spline clamp - single metal part

Material: 1045 medium-carbon steel, normalized (durable wear surface for workshop loading)

Envelope: `{"axial_bore_diameter_mm": 22, "outer_diameter_mm": 67, "overall_length_mm": 93, "wall_minimum_mm": 22}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'E-bike mid-drive motor torque arm spline clamp'.
The broader use case is: Retrofitted or modular e-bike mid-drive system mounted near the bottom
bracket The chosen deliverable is only the metal body implied by: Machined split clamp arm with
spline-like bore features, pinch bolt ears, offset arm, and frame contact pad All other product
elements are external reference items and must not be modeled. The part must perform this mechanical
role: Resists motor reaction torque by clamping around a splined or keyed interface and tying into
the frame It is intentionally included in the SubCAD limit corpus because: Tests internal keyed
geometry, split-clamp behavior, bolt ear symmetry, torque-load path clarity, and blended transitions
from circular clamp to structural arm The part is made from 1045 medium-carbon steel, normalized
using round bar stock. Start from one cut length of round metal bar. Turn the outside, face both
ends, bore the center, then mill secondary flats, slots, and radial holes as needed. No separate
inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 67 mm and length 93 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 22 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 32 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 22 mm wide over 85 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M8 holes through the top flat at X=31 mm and X=62 mm.
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
- Do not broaden the requirement back into the full product idea named 'E-bike mid-drive motor torque arm spline clamp'; this requirement is only for its chosen metal part.

---

## SMP-002-08 - Recumbent trike steering bellcrank

Part name: Recumbent trike steering bellcrank - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 51, "length_mm": 180, "width_mm": 100}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Recumbent trike steering bellcrank'. The broader
use case is: Light mobility recumbent tricycle with under-seat indirect steering The chosen
deliverable is only the metal body implied by: Machined bellcrank with central bearing boss, two
offset linkage holes, tapered arms, and angular indexing marks All other product elements are
external reference items and must not be modeled. The part must perform this mechanical role:
Converts handlebar linkage movement into tie-rod motion for front wheel steering It is intentionally
included in the SubCAD limit corpus because: Requires accurate angular relationships, multiple pivot
centers, non-rectilinear arm shapes, bearing features, and clear mechanical intent through linkage
geometry The part is made from low-carbon steel, ASTM A36 or equivalent using rectangular block
stock. Start from one rectangular metal block or plate. Saw oversize, face all datum sides, then
machine the pockets, holes, slots, angled faces, grooves, and edge treatments into that same solid
piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 180 mm x 100 mm x 51 mm.
- mounting hole pattern: Drill two through holes diameter 9 mm on the length centerline at X=20 mm and X=160 mm, Y=50 mm.
- functional center feature: Machine a central obround slot 60 mm long x 11 mm wide through the part, centered at X=90 mm, Y=50 mm.
- top relief pocket: Mill a rectangular relief pocket 45 mm x 33 mm x 23 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- machined angled reference face: Machine one top reference face at 28 degrees over the last 36 mm of length.

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
- All required chamfers, reliefs, and edge treatments are visible in STEP and STL outputs.
- No extra parts, fasteners, hardware, labels, cosmetic meshes, or nonmetal components are present.
- Flat datums remain planar and usable; pockets or slots do not accidentally break unsupported walls.

Negative requirements:
- Represent exactly one metal part only.
- Do not model screws, nuts, springs, bushings, bearings, rubber pads, plastic covers, electronics, labels, handles, knobs, adhesives, weld beads, or separate inserts.
- Do not convert the part into an assembly or multiple bodies.
- Do not replace through holes, slots, pockets, grooves, flats, tapers, or chamfers with cosmetic markings.
- Do not omit datum-critical features just because they are small.
- Do not broaden the requirement back into the full product idea named 'Recumbent trike steering bellcrank'; this requirement is only for its chosen metal part.

---

## SMP-002-09 - Bicycle dynamo hub wire-exit strain relief cap

Part name: Bicycle dynamo hub wire-exit strain relief cap - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"length_mm": 175, "thickness_mm": 10, "width_mm": 60}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Bicycle dynamo hub wire-exit strain relief cap'.
The broader use case is: Touring bicycle front hub with integrated dynamo wiring The chosen
deliverable is only the metal body implied by: Machined protective cap with hub-interface bore, wire
channel, clamp screw boss, curved outer shield, and anti-rotation tab All other product elements are
external reference items and must not be modeled. The part must perform this mechanical role:
Protects the electrical connector and guides the wire away from the spinning hub and spokes It is
intentionally included in the SubCAD limit corpus because: Tests small protective shell geometry,
internal channels, anti-rotation features, screw bosses, and spatial clearance around rotating
bicycle components The part is made from low-carbon steel, ASTM A36 or equivalent using sheet or
plate stock. Start from one flat sheet or plate blank. Cut the outside profile, machine holes,
slots, pockets, lips, and relief features into that same piece. If bends are called out, they are
bends in the same sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 175 mm x 60 mm x 10 mm.
- mounting hole pattern: Drill two through holes diameter 8 mm on the length centerline at X=12 mm and X=163 mm, Y=30 mm.
- functional center feature: Machine a central obround slot 58 mm long x 17 mm wide through the part, centered at X=87 mm, Y=30 mm.
- top relief pocket: Mill a rectangular relief pocket 43 mm x 20 mm x 3 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Bicycle dynamo hub wire-exit strain relief cap'; this requirement is only for its chosen metal part.

---

## SMP-002-10 - Manual wheelchair quick-release caster fork crown

Part name: Manual wheelchair quick-release caster fork crown - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 14, "outer_diameter_mm": 56, "overall_length_mm": 53, "wall_minimum_mm": 21}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Manual wheelchair quick-release caster fork crown'.
The broader use case is: Lightweight manual wheelchair or adaptive mobility chair The chosen
deliverable is only the metal body implied by: Machined caster crown block with vertical stem bore,
transverse release-pin hole, stepped height-index grooves, and fork lug interfaces All other product
elements are external reference items and must not be modeled. The part must perform this mechanical
role: Holds the front caster fork and enables quick removal or height adjustment It is intentionally
included in the SubCAD limit corpus because: Combines vertical and transverse precision holes,
indexed adjustment features, fork interface geometry, compact load paths, and accessibility-focused
mechanical detail The part is made from low-carbon steel, ASTM A36 or equivalent using round bar
stock. Start from one cut length of round metal bar. Turn the outside, face both ends, bore the
center, then mill secondary flats, slots, and radial holes as needed. No separate inserts or
fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 56 mm and length 53 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 14 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 24 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 18 mm wide over 45 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M8 holes through the top flat at X=17 mm and X=35 mm.
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
- Do not broaden the requirement back into the full product idea named 'Manual wheelchair quick-release caster fork crown'; this requirement is only for its chosen metal part.

---
