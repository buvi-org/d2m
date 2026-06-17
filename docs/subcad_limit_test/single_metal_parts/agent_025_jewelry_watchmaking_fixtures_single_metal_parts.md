# Agent 025 Single Metal Part Requirements

Domain: jewelry tools, watchmaking fixtures, clock mechanisms, small precision repair jigs, and wearable hardware

Each item below is one metal part only. Product assemblies and nonmetal components are explicitly out of scope.

## SMP-025-01 - Ring Shank Ovalizing Mandrel Block

Part name: Ring Shank Ovalizing Mandrel Block - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 27, "length_mm": 120, "width_mm": 85}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Ring Shank Ovalizing Mandrel Block'. The broader
use case is: Jewelry bench tool for reshaping distorted ring bands before sizing or solder repair.
The chosen deliverable is only the metal body implied by: Hardened steel mandrel block with stepped
oval profiles, relief slots, and clamp-reference flats. All other product elements are external
reference items and must not be modeled. The part must perform this mechanical role: Holds a ring
shank against a controlled oval mandrel profile while side pressure is applied through guide faces.
It is intentionally included in the SubCAD limit corpus because: Requires smooth non-circular
profiles, stepped size transitions, precise symmetry, edge reliefs, and functional datum surfaces.
The part is made from low-carbon steel, ASTM A36 or equivalent using rectangular block stock. Start
from one rectangular metal block or plate. Saw oversize, face all datum sides, then machine the
pockets, holes, slots, angled faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 120 mm x 85 mm x 27 mm.
- mounting hole pattern: Drill two through holes diameter 7 mm on the length centerline at X=17 mm and X=103 mm, Y=42 mm.
- functional center feature: Machine a central obround slot 40 mm long x 15 mm wide through the part, centered at X=60 mm, Y=42 mm.
- top relief pocket: Mill a rectangular relief pocket 30 mm x 28 mm x 10 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- serrated contact edge: Cut 5 equal triangular serrations across the rear edge, each 4 mm deep.

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
- Do not broaden the requirement back into the full product idea named 'Ring Shank Ovalizing Mandrel Block'; this requirement is only for its chosen metal part.

---

## SMP-025-02 - Watch Balance Staff Pivot Burnishing Jig

Part name: Watch Balance Staff Pivot Burnishing Jig - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 58, "length_mm": 100, "width_mm": 75}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Watch Balance Staff Pivot Burnishing Jig'. The
broader use case is: Watchmaking fixture used during restoration of mechanical watch balance
assemblies. The chosen deliverable is only the metal body implied by: Miniature V-block carriage
with opposed jewel-like support seats and micro-adjustable stop geometry. All other product elements
are external reference items and must not be modeled. The part must perform this mechanical role:
Supports a balance staff at a fixed axis while exposing tiny pivots for controlled burnishing or
polishing. It is intentionally included in the SubCAD limit corpus because: Tests tiny coaxial
features, V-grooves, shallow cups, delicate clearances, and constrained tool-access openings. The
part is made from low-carbon steel, ASTM A36 or equivalent using rectangular block stock. Start from
one rectangular metal block or plate. Saw oversize, face all datum sides, then machine the pockets,
holes, slots, angled faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 100 mm x 75 mm x 58 mm.
- mounting hole pattern: Drill two through holes diameter 13 mm on the length centerline at X=15 mm and X=85 mm, Y=37 mm.
- functional center feature: Machine a central obround slot 33 mm long x 9 mm wide through the part, centered at X=50 mm, Y=37 mm.
- top relief pocket: Mill a rectangular relief pocket 25 mm x 25 mm x 7 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- centered V-groove: Cut a 90 degree V-groove along the full X length on the top face, groove mouth 37 mm wide and depth 19 mm.

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
- The feature named 'centered V-groove' is present with the stated size and position.
- All required chamfers, reliefs, and edge treatments are visible in STEP and STL outputs.
- No extra parts, fasteners, hardware, labels, cosmetic meshes, or nonmetal components are present.
- Flat datums remain planar and usable; pockets or slots do not accidentally break unsupported walls.

Negative requirements:
- Represent exactly one metal part only.
- Do not model screws, nuts, springs, bushings, bearings, rubber pads, plastic covers, electronics, labels, handles, knobs, adhesives, weld beads, or separate inserts.
- Do not convert the part into an assembly or multiple bodies.
- Do not replace through holes, slots, pockets, grooves, flats, tapers, or chamfers with cosmetic markings.
- Do not omit datum-critical features just because they are small.
- Do not broaden the requirement back into the full product idea named 'Watch Balance Staff Pivot Burnishing Jig'; this requirement is only for its chosen metal part.

---

## SMP-025-03 - Clock Gear Depthing Gauge Frame

Part name: Clock Gear Depthing Gauge Frame - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 65, "length_mm": 80, "width_mm": 40}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Clock Gear Depthing Gauge Frame'. The broader use
case is: Clock repair fixture for setting correct center distance between meshing gears before
bushing plates. The chosen deliverable is only the metal body implied by: Slotted gauge frame with
parallel arbor channels, clamp lands, engraved scale recesses, and pivot bores. All other product
elements are external reference items and must not be modeled. The part must perform this mechanical
role: Lets two clock arbors be positioned and locked so gear mesh depth can be inspected. It is
intentionally included in the SubCAD limit corpus because: Combines long slots, coaxial bore pairs,
linear adjustability, scale features, and thin rigid frame geometry. The part is made from low-
carbon steel, ASTM A36 or equivalent using rectangular block stock. Start from one rectangular metal
block or plate. Saw oversize, face all datum sides, then machine the pockets, holes, slots, angled
faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 80 mm x 40 mm x 65 mm.
- mounting hole pattern: Drill two through holes diameter 9 mm on the length centerline at X=10 mm and X=70 mm, Y=20 mm.
- functional center feature: Machine a central obround slot 30 mm long x 7 mm wide through the part, centered at X=40 mm, Y=20 mm.
- top relief pocket: Mill a rectangular relief pocket 25 mm x 18 mm x 8 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Clock Gear Depthing Gauge Frame'; this requirement is only for its chosen metal part.

---

## SMP-025-04 - Bracelet Link Pin Press Anvil

Part name: Bracelet Link Pin Press Anvil - single metal part

Material: 1045 medium-carbon steel, normalized (durable wear surface for workshop loading)

Envelope: `{"axial_bore_diameter_mm": 28, "outer_diameter_mm": 84, "overall_length_mm": 68, "wall_minimum_mm": 28}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Bracelet Link Pin Press Anvil'. The broader use
case is: Wearable hardware repair tool for resizing metal watch bracelets and jewelry chain links.
The chosen deliverable is only the metal body implied by: Replaceable steel anvil with stepped link
channels, pin-exit holes, chamfered entry guides, and underside locating boss. All other product
elements are external reference items and must not be modeled. The part must perform this mechanical
role: Supports bracelet links while a press pin drives out friction-fit or split pins without
deforming the link. It is intentionally included in the SubCAD limit corpus because: Requires nested
channels, small through-holes, chamfers, offsets for asymmetric links, and robust part orientation.
The part is made from 1045 medium-carbon steel, normalized using round bar stock. Start from one cut
length of round metal bar. Turn the outside, face both ends, bore the center, then mill secondary
flats, slots, and radial holes as needed. No separate inserts or fasteners are part of the
deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 84 mm and length 68 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 28 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 38 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 28 mm wide over 60 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M5 holes through the top flat at X=22 mm and X=45 mm.
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
- Do not broaden the requirement back into the full product idea named 'Bracelet Link Pin Press Anvil'; this requirement is only for its chosen metal part.

---

## SMP-025-05 - Micro Screw Slot Dressing Holder

Part name: Micro Screw Slot Dressing Holder - single metal part

Material: 6061-T6 aluminum (low mass with good machinability and stable flat features)

Envelope: `{"length_mm": 230, "thickness_mm": 11, "width_mm": 50}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Micro Screw Slot Dressing Holder'. The broader use
case is: Precision repair jig for refinishing damaged screw heads from watches, eyeglasses, and
small instruments. The chosen deliverable is only the metal body implied by: Threaded holding plate
with counterbored screw nests, screwdriver clearance windows, and indexing edge stops. All other
product elements are external reference items and must not be modeled. The part must perform this
mechanical role: Captures tiny screws at a repeatable height so the slot can be filed or polished
squarely. It is intentionally included in the SubCAD limit corpus because: Tests miniature threads,
counterbores, thin webs, slot alignment, and repeated small feature patterns. The part is made from
6061-T6 aluminum using sheet or plate stock. Start from one flat sheet or plate blank. Cut the
outside profile, machine holes, slots, pockets, lips, and relief features into that same piece. If
bends are called out, they are bends in the same sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 230 mm x 50 mm x 11 mm.
- mounting hole pattern: Drill two through holes diameter 11 mm on the length centerline at X=10 mm and X=220 mm, Y=25 mm.
- functional center feature: Machine a central obround slot 76 mm long x 15 mm wide through the part, centered at X=115 mm, Y=25 mm.
- top relief pocket: Mill a rectangular relief pocket 57 mm x 18 mm x 1 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- counterbored seat: Add a central counterbore diameter 23 mm x 3 mm deep around the center feature.
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
- Do not broaden the requirement back into the full product idea named 'Micro Screw Slot Dressing Holder'; this requirement is only for its chosen metal part.

---

## SMP-025-06 - Gem Setting Prong Equalizer Plate

Part name: Gem Setting Prong Equalizer Plate - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"length_mm": 165, "thickness_mm": 11, "width_mm": 80}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Gem Setting Prong Equalizer Plate'. The broader use
case is: Jewelry setting tool for aligning and checking prong spacing around round or oval stones.
The chosen deliverable is only the metal body implied by: Circular hardened plate with concentric
stone seats, radial prong channels, and tapered access notches. All other product elements are
external reference items and must not be modeled. The part must perform this mechanical role:
Provides radial reference grooves that help bend prongs evenly before final stone tightening. It is
intentionally included in the SubCAD limit corpus because: Challenges radial arrays, concentric
shallow pockets, tapered slots, compound symmetry, and fine edge transitions. The part is made from
low-carbon steel, ASTM A36 or equivalent using sheet or plate stock. Start from one flat sheet or
plate blank. Cut the outside profile, machine holes, slots, pockets, lips, and relief features into
that same piece. If bends are called out, they are bends in the same sheet part, not separate welded
pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 165 mm x 80 mm x 11 mm.
- mounting hole pattern: Drill two through holes diameter 7 mm on the length centerline at X=16 mm and X=149 mm, Y=40 mm.
- functional center feature: Machine a central obround slot 55 mm long x 15 mm wide through the part, centered at X=82 mm, Y=40 mm.
- top relief pocket: Mill a rectangular relief pocket 41 mm x 26 mm x 3 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- machined angled reference face: Machine one top reference face at 26 degrees over the last 33 mm of length.

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
- Do not broaden the requirement back into the full product idea named 'Gem Setting Prong Equalizer Plate'; this requirement is only for its chosen metal part.

---

## SMP-025-07 - Pocket Watch Case Hinge Alignment Jig

Part name: Pocket Watch Case Hinge Alignment Jig - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 30, "length_mm": 155, "width_mm": 80}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Pocket Watch Case Hinge Alignment Jig'. The broader
use case is: Restoration fixture for repairing hinged pocket watch cases and lids. The chosen
deliverable is only the metal body implied by: Curved support saddle with adjustable hinge-axis
cradle, clamp pads, and clearance cutouts for case lips. All other product elements are external
reference items and must not be modeled. The part must perform this mechanical role: Holds case body
and lid hinge knuckles coaxially while a replacement hinge pin is fitted. It is intentionally
included in the SubCAD limit corpus because: Requires curved support surfaces, offset hinge-axis
references, organic clearance pockets, and mixed cylindrical/planar datums. The part is made from
low-carbon steel, ASTM A36 or equivalent using rectangular block stock. Start from one rectangular
metal block or plate. Saw oversize, face all datum sides, then machine the pockets, holes, slots,
angled faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 155 mm x 80 mm x 30 mm.
- mounting hole pattern: Drill two through holes diameter 7 mm on the length centerline at X=16 mm and X=139 mm, Y=40 mm.
- functional center feature: Machine a central obround slot 51 mm long x 17 mm wide through the part, centered at X=77 mm, Y=40 mm.
- top relief pocket: Mill a rectangular relief pocket 38 mm x 26 mm x 15 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Pocket Watch Case Hinge Alignment Jig'; this requirement is only for its chosen metal part.

---

## SMP-025-08 - Earring Post Soldering Heat Sink Clamp

Part name: Earring Post Soldering Heat Sink Clamp - single metal part

Material: 1045 medium-carbon steel, normalized (durable wear surface for workshop loading)

Envelope: `{"axial_bore_diameter_mm": 15, "outer_diameter_mm": 46, "overall_length_mm": 45, "wall_minimum_mm": 15}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Earring Post Soldering Heat Sink Clamp'. The
broader use case is: Jewelry repair tool for replacing or straightening earring posts without
overheating decorative fronts. The chosen deliverable is only the metal body implied by: Copper
clamp jaw with shallow domed cavities, post clearance slot, alignment pins, and textured grip lands.
All other product elements are external reference items and must not be modeled. The part must
perform this mechanical role: Clamps the ornament face while exposing the post base and drawing heat
away during soldering. It is intentionally included in the SubCAD limit corpus because: Tests
thermal-mass geometry, shallow concave surfaces, narrow slots, paired alignment features, and
ergonomic exterior shaping. The part is made from 1045 medium-carbon steel, normalized using round
bar stock. Start from one cut length of round metal bar. Turn the outside, face both ends, bore the
center, then mill secondary flats, slots, and radial holes as needed. No separate inserts or
fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 46 mm and length 45 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 15 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 25 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 15 mm wide over 37 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M7 holes through the top flat at X=15 mm and X=30 mm.
- split relief slit: Cut one full-length radial slit 6 mm wide from the outside to the axial bore on datum-B side.
- outside edge treatment: Break all outside circular edges with 1.0 mm chamfers and keep internal bore edges visibly chamfered.
- cross relief slot: Machine one transverse slot 8 mm wide across the top flat at X=22 mm, depth 4 mm.

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
- Do not broaden the requirement back into the full product idea named 'Earring Post Soldering Heat Sink Clamp'; this requirement is only for its chosen metal part.

---

## SMP-025-09 - Clock Escapement Pallet Fork Setting Fixture

Part name: Clock Escapement Pallet Fork Setting Fixture - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"length_mm": 90, "thickness_mm": 11, "width_mm": 70}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Clock Escapement Pallet Fork Setting Fixture'. The
broader use case is: Clock mechanism repair fixture for adjusting pallet geometry relative to an
escape wheel. The chosen deliverable is only the metal body implied by: Precision fixture plate with
arbor jewel seats, angular reference slots, removable stop bosses, and curved inspection window. All
other product elements are external reference items and must not be modeled. The part must perform
this mechanical role: Positions a pallet arbor and reference escape-wheel arc so lock and drop can
be checked. It is intentionally included in the SubCAD limit corpus because: Combines angular datum
geometry, arc-shaped windows, small bearing seats, modular locating bosses, and mechanism-clearance
modeling. The part is made from low-carbon steel, ASTM A36 or equivalent using sheet or plate stock.
Start from one flat sheet or plate blank. Cut the outside profile, machine holes, slots, pockets,
lips, and relief features into that same piece. If bends are called out, they are bends in the same
sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 90 mm x 70 mm x 11 mm.
- mounting hole pattern: Drill two through holes diameter 11 mm on the length centerline at X=14 mm and X=76 mm, Y=35 mm.
- functional center feature: Machine a central obround slot 30 mm long x 7 mm wide through the part, centered at X=45 mm, Y=35 mm.
- top relief pocket: Mill a rectangular relief pocket 25 mm x 23 mm x 4 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Clock Escapement Pallet Fork Setting Fixture'; this requirement is only for its chosen metal part.

---

## SMP-025-10 - Wearable Sensor Strap Lug Drill Guide

Part name: Wearable Sensor Strap Lug Drill Guide - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 9, "outer_diameter_mm": 29, "overall_length_mm": 63, "wall_minimum_mm": 10}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Wearable Sensor Strap Lug Drill Guide'. The broader
use case is: Wearable hardware fabrication jig for drilling consistent spring-bar or screw-bar holes
in custom strap lugs. The chosen deliverable is only the metal body implied by: U-shaped drill guide
body with hardened bushing bore, lug-spacing bridge, case-radius relief, and clamp screw pads. All
other product elements are external reference items and must not be modeled. The part must perform
this mechanical role: Locates a drill bushing across paired lugs so holes remain coaxial and
correctly spaced from the case body. It is intentionally included in the SubCAD limit corpus
because: Tests U-channel geometry, coaxial transverse bores, replaceable bushing pockets, curved
reliefs, and tolerance-critical mirrored features. The part is made from low-carbon steel, ASTM A36
or equivalent using round bar stock. Start from one cut length of round metal bar. Turn the outside,
face both ends, bore the center, then mill secondary flats, slots, and radial holes as needed. No
separate inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 29 mm and length 63 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 9 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 19 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 9 mm wide over 55 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M8 holes through the top flat at X=21 mm and X=42 mm.
- split relief slit: Cut one full-length radial slit 6 mm wide from the outside to the axial bore on datum-B side.
- outside edge treatment: Break all outside circular edges with 1.0 mm chamfers and keep internal bore edges visibly chamfered.
- cross relief slot: Machine one transverse slot 8 mm wide across the top flat at X=31 mm, depth 2 mm.

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
- Do not broaden the requirement back into the full product idea named 'Wearable Sensor Strap Lug Drill Guide'; this requirement is only for its chosen metal part.

---
