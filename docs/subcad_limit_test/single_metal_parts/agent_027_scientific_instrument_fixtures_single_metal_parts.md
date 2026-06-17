# Agent 027 Single Metal Part Requirements

Domain: scientific instruments, spectroscopy/optics mounts, vacuum lab hardware, sample handling, and precision lab fixtures

Each item below is one metal part only. Product assemblies and nonmetal components are explicitly out of scope.

## SMP-027-01 - Kinematic Mirror Mount Flexure Plate

Part name: Kinematic Mirror Mount Flexure Plate - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"length_mm": 170, "thickness_mm": 6, "width_mm": 70}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Kinematic Mirror Mount Flexure Plate'. The broader
use case is: Optical spectroscopy beamline alignment for steering a laser into a monochromator or
interferometer. The chosen deliverable is only the metal body implied by: Machined monolithic
flexure plate with mirror pocket, thin hinge webs, actuator contact pads, and rear mounting bosses.
All other product elements are external reference items and must not be modeled. The part must
perform this mechanical role: Provides fine angular adjustment of a front mirror pad through three-
point kinematic support and elastic flexure compliance. It is intentionally included in the SubCAD
limit corpus because: Combines thin flexures, offset bosses, counterbores, mirror recesses, actuator
pads, symmetry, and tight clearances in one mechanically meaningful part. The part is made from low-
carbon steel, ASTM A36 or equivalent using sheet or plate stock. Start from one flat sheet or plate
blank. Cut the outside profile, machine holes, slots, pockets, lips, and relief features into that
same piece. If bends are called out, they are bends in the same sheet part, not separate welded
pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 170 mm x 70 mm x 6 mm.
- mounting hole pattern: Drill two through holes diameter 13 mm on the length centerline at X=14 mm and X=156 mm, Y=35 mm.
- functional center feature: Machine a central obround slot 56 mm long x 17 mm wide through the part, centered at X=85 mm, Y=35 mm.
- top relief pocket: Mill a rectangular relief pocket 42 mm x 23 mm x 3 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- counterbored seat: Add a central counterbore diameter 25 mm x 2 mm deep around the center feature.

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
- All required chamfers, reliefs, and edge treatments are visible in STEP and STL outputs.
- No extra parts, fasteners, hardware, labels, cosmetic meshes, or nonmetal components are present.
- Flat datums remain planar and usable; pockets or slots do not accidentally break unsupported walls.

Negative requirements:
- Represent exactly one metal part only.
- Do not model screws, nuts, springs, bushings, bearings, rubber pads, plastic covers, electronics, labels, handles, knobs, adhesives, weld beads, or separate inserts.
- Do not convert the part into an assembly or multiple bodies.
- Do not replace through holes, slots, pockets, grooves, flats, tapers, or chamfers with cosmetic markings.
- Do not omit datum-critical features just because they are small.
- Do not broaden the requirement back into the full product idea named 'Kinematic Mirror Mount Flexure Plate'; this requirement is only for its chosen metal part.

---

## SMP-027-02 - Vacuum Flange Optical Window Clamp Ring

Part name: Vacuum Flange Optical Window Clamp Ring - single metal part

Material: 1045 medium-carbon steel, normalized (durable wear surface for workshop loading)

Envelope: `{"length_mm": 190, "thickness_mm": 12, "width_mm": 80}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Vacuum Flange Optical Window Clamp Ring'. The
broader use case is: High-vacuum spectroscopy chamber with a removable fused silica or sapphire
viewport. The chosen deliverable is only the metal body implied by: Annular clamp ring with bolt
circle, stepped window recess, gasket groove, relief chamfers, and alignment notches. All other
product elements are external reference items and must not be modeled. The part must perform this
mechanical role: Compresses an optical window and gasket evenly against a vacuum flange while
preserving a clear optical aperture. It is intentionally included in the SubCAD limit corpus
because: Tests concentric circular features, annular grooves, bolt-pattern repetition, stepped
profiles, aperture constraints, and sealing-surface geometry. The part is made from 1045 medium-
carbon steel, normalized using sheet or plate stock. Start from one flat sheet or plate blank. Cut
the outside profile, machine holes, slots, pockets, lips, and relief features into that same piece.
If bends are called out, they are bends in the same sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 190 mm x 80 mm x 12 mm.
- mounting hole pattern: Drill two through holes diameter 11 mm on the length centerline at X=16 mm and X=174 mm, Y=40 mm.
- functional center feature: Machine a central obround slot 63 mm long x 16 mm wide through the part, centered at X=95 mm, Y=40 mm.
- top relief pocket: Mill a rectangular relief pocket 47 mm x 26 mm x 3 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- serrated contact edge: Cut 6 equal triangular serrations across the rear edge, each 2 mm deep.

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
- Do not broaden the requirement back into the full product idea named 'Vacuum Flange Optical Window Clamp Ring'; this requirement is only for its chosen metal part.

---

## SMP-027-03 - Cryogenic Sample Paddle Holder

Part name: Cryogenic Sample Paddle Holder - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"length_mm": 140, "thickness_mm": 5, "width_mm": 120}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Cryogenic Sample Paddle Holder'. The broader use
case is: Low-temperature optical or Raman spectroscopy stage for holding a small crystal, wafer
coupon, or thin sample. The chosen deliverable is only the metal body implied by: Small machined
copper sample holder with pocket, clamp screw bosses, thermal strap tabs, alignment slot, and
beveled optical clearance faces. All other product elements are external reference items and must
not be modeled. The part must perform this mechanical role: Secures a sample paddle thermally and
mechanically while allowing optical access from multiple angles. It is intentionally included in the
SubCAD limit corpus because: Requires mixed small-scale features, asymmetric cutouts, angled
reliefs, threaded-boss placement, and material-driven functional geometry. The part is made from
low-carbon steel, ASTM A36 or equivalent using sheet or plate stock. Start from one flat sheet or
plate blank. Cut the outside profile, machine holes, slots, pockets, lips, and relief features into
that same piece. If bends are called out, they are bends in the same sheet part, not separate welded
pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 140 mm x 120 mm x 5 mm.
- mounting hole pattern: Drill two through holes diameter 13 mm on the length centerline at X=24 mm and X=116 mm, Y=60 mm.
- functional center feature: Machine a central obround slot 46 mm long x 13 mm wide through the part, centered at X=70 mm, Y=60 mm.
- top relief pocket: Mill a rectangular relief pocket 35 mm x 40 mm x 1 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- machined angled reference face: Machine one top reference face at 24 degrees over the last 28 mm of length.
- side tapped hole: Tap one side hole M9 from the right long edge into the central pocket; hole axis is parallel to Y.

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
- Do not broaden the requirement back into the full product idea named 'Cryogenic Sample Paddle Holder'; this requirement is only for its chosen metal part.

---

## SMP-027-04 - Fiber Collimator V-Groove Alignment Block

Part name: Fiber Collimator V-Groove Alignment Block - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 8, "outer_diameter_mm": 29, "overall_length_mm": 65, "wall_minimum_mm": 10}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Fiber Collimator V-Groove Alignment Block'. The
broader use case is: Spectrometer input optics where a fiber ferrule must be aligned to a
collimating lens barrel. The chosen deliverable is only the metal body implied by: Rectangular
alignment block with precision V-groove, lens bore, split-clamp slit, cross holes, dowel pin holes,
and datum feet. All other product elements are external reference items and must not be modeled. The
part must perform this mechanical role: Locates a fiber ferrule and cylindrical lens housing on a
shared optical axis with clamp access. It is intentionally included in the SubCAD limit corpus
because: Tests V-shaped prismatic cuts, coaxial bores, clamp slots, orthogonal fastener holes, datum
surfaces, and alignment-critical relationships. The part is made from low-carbon steel, ASTM A36 or
equivalent using round bar stock. Start from one cut length of round metal bar. Turn the outside,
face both ends, bore the center, then mill secondary flats, slots, and radial holes as needed. No
separate inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 29 mm and length 65 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 8 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 18 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 9 mm wide over 57 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M7 holes through the top flat at X=21 mm and X=43 mm.
- split relief slit: Cut one full-length radial slit 6 mm wide from the outside to the axial bore on datum-B side.
- outside edge treatment: Break all outside circular edges with 1.0 mm chamfers and keep internal bore edges visibly chamfered.
- cross relief slot: Machine one transverse slot 8 mm wide across the top flat at X=32 mm, depth 2 mm.

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
- Do not broaden the requirement back into the full product idea named 'Fiber Collimator V-Groove Alignment Block'; this requirement is only for its chosen metal part.

---

## SMP-027-05 - Miniature Vacuum Feedthrough Bracket

Part name: Miniature Vacuum Feedthrough Bracket - single metal part

Material: AISI 316 stainless steel (corrosion resistance and cleanable metal surfaces)

Envelope: `{"length_mm": 125, "thickness_mm": 5, "width_mm": 100}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Miniature Vacuum Feedthrough Bracket'. The broader
use case is: Lab vacuum chamber carrying electrical or optical feedthrough connectors near a
spectroscopy sample stage. The chosen deliverable is only the metal body implied by: L-shaped
machined bracket with circular saddle, split clamp ears, mounting slots, cable relief channel, and
lightening pockets. All other product elements are external reference items and must not be modeled.
The part must perform this mechanical role: Supports a circular feedthrough body and routes strain-
relieved cables without interfering with nearby chamber hardware. It is intentionally included in
the SubCAD limit corpus because: Includes bracket orthogonality, partial cylindrical seats, slotted
holes, clamp ears, internal pockets, and cable-clearance geometry. The part is made from AISI 316
stainless steel using sheet or plate stock. Start from one flat sheet or plate blank. Cut the
outside profile, machine holes, slots, pockets, lips, and relief features into that same piece. If
bends are called out, they are bends in the same sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 125 mm x 100 mm x 5 mm.
- mounting hole pattern: Drill two through holes diameter 5 mm on the length centerline at X=20 mm and X=105 mm, Y=50 mm.
- functional center feature: Machine a central obround slot 41 mm long x 12 mm wide through the part, centered at X=62 mm, Y=50 mm.
- top relief pocket: Mill a rectangular relief pocket 31 mm x 33 mm x 2 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Miniature Vacuum Feedthrough Bracket'; this requirement is only for its chosen metal part.

---

## SMP-027-06 - Cuvette Carousel Indexing Plate

Part name: Cuvette Carousel Indexing Plate - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"length_mm": 210, "thickness_mm": 7, "width_mm": 80}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Cuvette Carousel Indexing Plate'. The broader use
case is: UV-visible spectroscopy accessory for presenting multiple square cuvettes to a fixed
optical beam. The chosen deliverable is only the metal body implied by: Circular carousel plate with
square cuvette pockets, radial optical windows, center bearing bore, detent holes, and engraved
index flats. All other product elements are external reference items and must not be modeled. The
part must perform this mechanical role: Holds several cuvettes at indexed angular positions while
exposing each optical path through clear side windows. It is intentionally included in the SubCAD
limit corpus because: Tests polar arrays, square pockets on a circular part, radial windows, central
bearing geometry, detent features, and repeated but orientation-sensitive cutouts. The part is made
from low-carbon steel, ASTM A36 or equivalent using sheet or plate stock. Start from one flat sheet
or plate blank. Cut the outside profile, machine holes, slots, pockets, lips, and relief features
into that same piece. If bends are called out, they are bends in the same sheet part, not separate
welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 210 mm x 80 mm x 7 mm.
- mounting hole pattern: Drill two through holes diameter 8 mm on the length centerline at X=16 mm and X=194 mm, Y=40 mm.
- functional center feature: Machine a central obround slot 70 mm long x 14 mm wide through the part, centered at X=105 mm, Y=40 mm.
- top relief pocket: Mill a rectangular relief pocket 52 mm x 26 mm x 2 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Cuvette Carousel Indexing Plate'; this requirement is only for its chosen metal part.

---

## SMP-027-07 - Adjustable Slit Jaw Carrier

Part name: Adjustable Slit Jaw Carrier - single metal part

Material: 6061-T6 aluminum (low mass with good machinability and stable flat features)

Envelope: `{"height_mm": 20, "length_mm": 100, "width_mm": 55}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Adjustable Slit Jaw Carrier'. The broader use case
is: Entrance or exit slit assembly for a monochromator, spectrograph, or beam-shaping optical
instrument. The chosen deliverable is only the metal body implied by: Machined jaw carrier with
blade ledge, screw slots, guide rail grooves, spring pocket, datum shoulder, and blade clamp holes.
All other product elements are external reference items and must not be modeled. The part must
perform this mechanical role: Carries one precision slit blade and allows controlled linear motion
relative to an opposing blade. It is intentionally included in the SubCAD limit corpus because:
Tests thin ledges, long guide features, precision shoulders, nested pockets, elongated slots, and
part geometry tied to motion constraints. The part is made from 6061-T6 aluminum using rectangular
block stock. Start from one rectangular metal block or plate. Saw oversize, face all datum sides,
then machine the pockets, holes, slots, angled faces, grooves, and edge treatments into that same
solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 100 mm x 55 mm x 20 mm.
- mounting hole pattern: Drill two through holes diameter 7 mm on the length centerline at X=11 mm and X=89 mm, Y=27 mm.
- functional center feature: Machine a central obround slot 33 mm long x 11 mm wide through the part, centered at X=50 mm, Y=27 mm.
- top relief pocket: Mill a rectangular relief pocket 25 mm x 18 mm x 5 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
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
- Do not broaden the requirement back into the full product idea named 'Adjustable Slit Jaw Carrier'; this requirement is only for its chosen metal part.

---

## SMP-027-08 - Microscope Objective Vacuum Adapter Nosepiece

Part name: Microscope Objective Vacuum Adapter Nosepiece - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 8, "outer_diameter_mm": 33, "overall_length_mm": 106, "wall_minimum_mm": 12}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Microscope Objective Vacuum Adapter Nosepiece'. The
broader use case is: Vacuum-compatible optical inspection chamber using a microscope objective
mounted through a custom adapter. The chosen deliverable is only the metal body implied by:
Cylindrical adapter body with external flange, internal stepped bore, thread relief, O-ring groove,
spanner flats, and vent holes. All other product elements are external reference items and must not
be modeled. The part must perform this mechanical role: Positions an objective lens at a fixed
working distance while sealing or shielding the chamber interface. It is intentionally included in
the SubCAD limit corpus because: Combines rotational geometry, stepped internal cavities, sealing
grooves, flats on cylinders, radial holes, and optical working-distance constraints. The part is
made from low-carbon steel, ASTM A36 or equivalent using round bar stock. Start from one cut length
of round metal bar. Turn the outside, face both ends, bore the center, then mill secondary flats,
slots, and radial holes as needed. No separate inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 33 mm and length 106 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 8 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 18 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 11 mm wide over 98 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M5 holes through the top flat at X=35 mm and X=70 mm.
- split relief slit: Cut one full-length radial slit 6 mm wide from the outside to the axial bore on datum-B side.
- outside edge treatment: Break all outside circular edges with 1.0 mm chamfers and keep internal bore edges visibly chamfered.
- opposed wrench flats: Mill two opposed flats across the outside, leaving 25 mm across flats over the middle third of the length.
- cross relief slot: Machine one transverse slot 8 mm wide across the top flat at X=53 mm, depth 3 mm.

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
- Do not broaden the requirement back into the full product idea named 'Microscope Objective Vacuum Adapter Nosepiece'; this requirement is only for its chosen metal part.

---

## SMP-027-09 - Precision Lab Jack Crosshead Block

Part name: Precision Lab Jack Crosshead Block - single metal part

Material: AISI 316 stainless steel (corrosion resistance and cleanable metal surfaces)

Envelope: `{"height_mm": 68, "length_mm": 120, "width_mm": 90}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Precision Lab Jack Crosshead Block'. The broader
use case is: Compact vertical positioning fixture for raising a sample holder or small optical
element under a beam path. The chosen deliverable is only the metal body implied by: Machined
crosshead block with lead screw nut pocket, twin guide-rod bores, top mounting grid, underside
clearance pocket, and anti-rotation keyway. All other product elements are external reference items
and must not be modeled. The part must perform this mechanical role: Transfers screw-driven motion
into guided vertical movement while maintaining parallelism and load support. It is intentionally
included in the SubCAD limit corpus because: Tests parallel bore alignment, central pocketing, grid-
pattern mounting holes, internal clearances, guide constraints, and load-path-driven shape. The part
is made from AISI 316 stainless steel using rectangular block stock. Start from one rectangular
metal block or plate. Saw oversize, face all datum sides, then machine the pockets, holes, slots,
angled faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 120 mm x 90 mm x 68 mm.
- mounting hole pattern: Drill two through holes diameter 8 mm on the length centerline at X=18 mm and X=102 mm, Y=45 mm.
- functional center feature: Machine a central obround slot 40 mm long x 8 mm wide through the part, centered at X=60 mm, Y=45 mm.
- top relief pocket: Mill a rectangular relief pocket 30 mm x 30 mm x 23 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Precision Lab Jack Crosshead Block'; this requirement is only for its chosen metal part.

---

## SMP-027-10 - Quartz Tube Furnace Sample Boat Fixture

Part name: Quartz Tube Furnace Sample Boat Fixture - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 10, "outer_diameter_mm": 43, "overall_length_mm": 98, "wall_minimum_mm": 16}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Quartz Tube Furnace Sample Boat Fixture'. The
broader use case is: Tube furnace or in-situ spectroscopy setup where a ceramic or metal sample boat
must be repeatably positioned inside a quartz tube. The chosen deliverable is only the metal body
implied by: Long narrow machined fixture rail with curved tube-contact feet, boat locating tabs,
vent slots, end stop, and thermocouple clip boss. All other product elements are external reference
items and must not be modeled. The part must perform this mechanical role: Cradles and locates a
sample boat while allowing gas flow and thermal expansion clearance. It is intentionally included in
the SubCAD limit corpus because: Tests elongated proportions, curved support surfaces, thin tabs,
slot arrays, asymmetric end features, and functional clearances for thermal and gas-flow behavior.
The part is made from low-carbon steel, ASTM A36 or equivalent using round bar stock. Start from one
cut length of round metal bar. Turn the outside, face both ends, bore the center, then mill
secondary flats, slots, and radial holes as needed. No separate inserts or fasteners are part of the
deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 43 mm and length 98 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 10 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 20 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 14 mm wide over 90 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M8 holes through the top flat at X=32 mm and X=65 mm.
- split relief slit: Cut one full-length radial slit 4 mm wide from the outside to the axial bore on datum-B side.
- outside edge treatment: Break all outside circular edges with 1.0 mm chamfers and keep internal bore edges visibly chamfered.
- cross relief slot: Machine one transverse slot 6 mm wide across the top flat at X=49 mm, depth 4 mm.

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
- Do not broaden the requirement back into the full product idea named 'Quartz Tube Furnace Sample Boat Fixture'; this requirement is only for its chosen metal part.

---
