# Agent 008 Single Metal Part Requirements

Domain: camera, audio, and creator-equipment rigging hardware

Each item below is one metal part only. Product assemblies and nonmetal components are explicitly out of scope.

## SMP-008-01 - Cage-Mounted HDMI Cable Clamp With Captive Wedge

Part name: Cage-Mounted HDMI Cable Clamp With Captive Wedge - single metal part

Material: 6061-T6 aluminum (low mass with good machinability and stable flat features)

Envelope: `{"height_mm": 63, "length_mm": 180, "width_mm": 35}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Cage-Mounted HDMI Cable Clamp With Captive Wedge'.
The broader use case is: A compact clamp for mirrorless camera cages that secures a full-size or
micro-HDMI cable near the camera body during handheld video work. The chosen deliverable is only the
metal body implied by: Machined aluminum clamp body with stepped cable channel, cage mounting slot,
captive wedge pocket, and thumbscrew bore. All other product elements are external reference items
and must not be modeled. The part must perform this mechanical role: Prevent cable strain and
accidental unplugging while allowing quick cable removal without detaching the camera cage. It is
intentionally included in the SubCAD limit corpus because: Combines small asymmetric features,
stepped channels, counterbores, sliding wedge geometry, rounded cable reliefs, and tight clearances
around threaded hardware. The part is made from 6061-T6 aluminum using rectangular block stock.
Start from one rectangular metal block or plate. Saw oversize, face all datum sides, then machine
the pockets, holes, slots, angled faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 180 mm x 35 mm x 63 mm.
- mounting hole pattern: Drill two through holes diameter 8 mm on the length centerline at X=10 mm and X=170 mm, Y=17 mm.
- functional center feature: Machine a central obround slot 60 mm long x 14 mm wide through the part, centered at X=90 mm, Y=17 mm.
- top relief pocket: Mill a rectangular relief pocket 45 mm x 18 mm x 27 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- serrated contact edge: Cut 7 equal triangular serrations across the rear edge, each 5 mm deep.
- machined angled reference face: Machine one top reference face at 18 degrees over the last 36 mm of length.
- counterbored seat: Add a central counterbore diameter 22 mm x 6 mm deep around the center feature.
- side tapped hole: Tap one side hole M10 from the right long edge into the central pocket; hole axis is parallel to Y.

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
- Do not broaden the requirement back into the full product idea named 'Cage-Mounted HDMI Cable Clamp With Captive Wedge'; this requirement is only for its chosen metal part.

---

## SMP-008-02 - Dual Cold-Shoe Audio Receiver Bridge

Part name: Dual Cold-Shoe Audio Receiver Bridge - single metal part

Material: 6061-T6 aluminum (low mass with good machinability and stable flat features)

Envelope: `{"height_mm": 38, "length_mm": 195, "width_mm": 115}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Dual Cold-Shoe Audio Receiver Bridge'. The broader
use case is: A camera-top accessory bridge for mounting two compact wireless microphone receivers
above a cinema or mirrorless camera cage. The chosen deliverable is only the metal body implied by:
Machined bridge bar with two cold-shoe rails, center cage-mount slot, cable clearance scallops, and
end-stop lips. All other product elements are external reference items and must not be modeled. The
part must perform this mechanical role: Hold two receivers side by side while leaving clearance for
screen tilt, cables, and top-handle operation. It is intentionally included in the SubCAD limit
corpus because: Requires accurate rail profiles, repeated but mirrored mounting features, undercut-
like lips, slot placement, and clearance cutouts tied to real accessory envelopes. The part is made
from 6061-T6 aluminum using rectangular block stock. Start from one rectangular metal block or
plate. Saw oversize, face all datum sides, then machine the pockets, holes, slots, angled faces,
grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 195 mm x 115 mm x 38 mm.
- mounting hole pattern: Drill two through holes diameter 5 mm on the length centerline at X=23 mm and X=172 mm, Y=57 mm.
- functional center feature: Machine a central obround slot 65 mm long x 11 mm wide through the part, centered at X=97 mm, Y=57 mm.
- top relief pocket: Mill a rectangular relief pocket 48 mm x 38 mm x 1 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Dual Cold-Shoe Audio Receiver Bridge'; this requirement is only for its chosen metal part.

---

## SMP-008-03 - Low-Profile NATO Rail Microphone Shock Mount Base

Part name: Low-Profile NATO Rail Microphone Shock Mount Base - single metal part

Material: 6061-T6 aluminum (low mass with good machinability and stable flat features)

Envelope: `{"height_mm": 70, "length_mm": 140, "width_mm": 70}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Low-Profile NATO Rail Microphone Shock Mount Base'.
The broader use case is: A base adapter that lets a small shotgun microphone shock mount slide onto
a camera cage NATO rail. The chosen deliverable is only the metal body implied by: Machined NATO
clamp block with dovetail jaw profile, locking screw boss, microphone mount boss, and relief
pockets. All other product elements are external reference items and must not be modeled. The part
must perform this mechanical role: Provide fast repositioning of a microphone while locking securely
to a standard camera rig rail. It is intentionally included in the SubCAD limit corpus because:
Tests standardized rail geometry, angled clamping faces, screw-axis alignment, raised bosses,
weight-reducing pockets, and functional interference constraints. The part is made from 6061-T6
aluminum using rectangular block stock. Start from one rectangular metal block or plate. Saw
oversize, face all datum sides, then machine the pockets, holes, slots, angled faces, grooves, and
edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 140 mm x 70 mm x 70 mm.
- mounting hole pattern: Drill two through holes diameter 13 mm on the length centerline at X=14 mm and X=126 mm, Y=35 mm.
- functional center feature: Machine a central obround slot 46 mm long x 16 mm wide through the part, centered at X=70 mm, Y=35 mm.
- top relief pocket: Mill a rectangular relief pocket 35 mm x 23 mm x 17 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- dovetail slide form: Machine a straight dovetail groove on the top face, length 116 mm, throat 14 mm, included angle 60 degrees.
- machined angled reference face: Machine one top reference face at 17 degrees over the last 28 mm of length.
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
- The feature named 'dovetail slide form' is present with the stated size and position.
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
- Do not broaden the requirement back into the full product idea named 'Low-Profile NATO Rail Microphone Shock Mount Base'; this requirement is only for its chosen metal part.

---

## SMP-008-04 - Articulating Monitor Rosette Knuckle

Part name: Articulating Monitor Rosette Knuckle - single metal part

Material: 6061-T6 aluminum (low mass with good machinability and stable flat features)

Envelope: `{"height_mm": 65, "length_mm": 205, "width_mm": 65}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Articulating Monitor Rosette Knuckle'. The broader
use case is: A machined center joint for a field monitor arm used on camera rigs, positioned between
two short adjustable arms. The chosen deliverable is only the metal body implied by: Circular
rosette knuckle with radial teeth, central through-bore, side arm clevis ears, and recessed washer
seat. All other product elements are external reference items and must not be modeled. The part must
perform this mechanical role: Allow a monitor to rotate and lock at repeatable angles without
slipping during movement. It is intentionally included in the SubCAD limit corpus because:
Challenges CAD representation with radial tooth arrays, circular symmetry, clevis geometry, coaxial
bores, recesses, and load-bearing mating surfaces. The part is made from 6061-T6 aluminum using
rectangular block stock. Start from one rectangular metal block or plate. Saw oversize, face all
datum sides, then machine the pockets, holes, slots, angled faces, grooves, and edge treatments into
that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 205 mm x 65 mm x 65 mm.
- mounting hole pattern: Drill two through holes diameter 13 mm on the length centerline at X=13 mm and X=192 mm, Y=32 mm.
- functional center feature: Machine a central obround slot 68 mm long x 12 mm wide through the part, centered at X=102 mm, Y=32 mm.
- top relief pocket: Mill a rectangular relief pocket 51 mm x 21 mm x 29 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Articulating Monitor Rosette Knuckle'; this requirement is only for its chosen metal part.

---

## SMP-008-05 - Boom Pole Quick-Release Recorder Cradle

Part name: Boom Pole Quick-Release Recorder Cradle - single metal part

Material: 1045 medium-carbon steel, normalized (durable wear surface for workshop loading)

Envelope: `{"axial_bore_diameter_mm": 14, "outer_diameter_mm": 71, "overall_length_mm": 105, "wall_minimum_mm": 28}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Boom Pole Quick-Release Recorder Cradle'. The
broader use case is: A clamp-on holder for attaching a small field audio recorder to a boom pole
during documentary sound recording. The chosen deliverable is only the metal body implied by: Curved
machined cradle with cylindrical pole clamp saddle, recorder backplate, strap slots, and angled
viewing offset. All other product elements are external reference items and must not be modeled. The
part must perform this mechanical role: Secure the recorder at a readable angle while isolating it
from rotation around the pole. It is intentionally included in the SubCAD limit corpus because:
Mixes cylindrical grip surfaces, angled planar mounting, strap pass-through slots, filleted
transitions, and ergonomic offsets in one compact part. The part is made from 1045 medium-carbon
steel, normalized using round bar stock. Start from one cut length of round metal bar. Turn the
outside, face both ends, bore the center, then mill secondary flats, slots, and radial holes as
needed. No separate inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 71 mm and length 105 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 14 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 24 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 23 mm wide over 97 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M8 holes through the top flat at X=35 mm and X=70 mm.
- split relief slit: Cut one full-length radial slit 6 mm wide from the outside to the axial bore on datum-B side.
- outside edge treatment: Break all outside circular edges with 1.0 mm chamfers and keep internal bore edges visibly chamfered.
- cross relief slot: Machine one transverse slot 8 mm wide across the top flat at X=52 mm, depth 7 mm.

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
- Do not broaden the requirement back into the full product idea named 'Boom Pole Quick-Release Recorder Cradle'; this requirement is only for its chosen metal part.

---

## SMP-008-06 - Camera Cage Side Handle ARRI-Locating Mount Block

Part name: Camera Cage Side Handle ARRI-Locating Mount Block - single metal part

Material: 6061-T6 aluminum (low mass with good machinability and stable flat features)

Envelope: `{"axial_bore_diameter_mm": 8, "outer_diameter_mm": 39, "overall_length_mm": 98, "wall_minimum_mm": 15}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Camera Cage Side Handle ARRI-Locating Mount Block'.
The broader use case is: A side-handle interface block for attaching a wooden or aluminum grip to a
cinema camera cage using ARRI-style locating pins. The chosen deliverable is only the metal body
implied by: Machined mount block with central threaded bore, two locating pin holes, handle tenon
pocket, and contoured finger-side chamfers. All other product elements are external reference items
and must not be modeled. The part must perform this mechanical role: Prevent handle twist while
transferring hand loads into the camera cage. It is intentionally included in the SubCAD limit
corpus because: Tests precise hole patterns, anti-rotation features, pocketed mating geometry,
chamfer orientation, and structural massing around high-load fasteners. The part is made from
6061-T6 aluminum using round bar stock. Start from one cut length of round metal bar. Turn the
outside, face both ends, bore the center, then mill secondary flats, slots, and radial holes as
needed. No separate inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 39 mm and length 98 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 8 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 18 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 13 mm wide over 90 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M5 holes through the top flat at X=32 mm and X=65 mm.
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
- Do not broaden the requirement back into the full product idea named 'Camera Cage Side Handle ARRI-Locating Mount Block'; this requirement is only for its chosen metal part.

---

## SMP-008-07 - V-Mount Battery Plate Offset Spacer With Cable Tunnel

Part name: V-Mount Battery Plate Offset Spacer With Cable Tunnel - single metal part

Material: 6061-T6 aluminum (low mass with good machinability and stable flat features)

Envelope: `{"length_mm": 215, "thickness_mm": 10, "width_mm": 65}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'V-Mount Battery Plate Offset Spacer With Cable
Tunnel'. The broader use case is: An offset spacer used between a V-mount battery plate and a
compact cinema camera rig to improve clearance for rear ports. The chosen deliverable is only the
metal body implied by: Machined spacer block with staggered mounting holes, internal cable tunnel,
rear plate bosses, and side-access cutout. All other product elements are external reference items
and must not be modeled. The part must perform this mechanical role: Move the battery plate backward
and upward while routing power cables through a protected internal path. It is intentionally
included in the SubCAD limit corpus because: Includes non-coplanar mounting interfaces, hidden
passage geometry, offset hole patterns, weight relief, and cable bend-radius constraints. The part
is made from 6061-T6 aluminum using sheet or plate stock. Start from one flat sheet or plate blank.
Cut the outside profile, machine holes, slots, pockets, lips, and relief features into that same
piece. If bends are called out, they are bends in the same sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 215 mm x 65 mm x 10 mm.
- mounting hole pattern: Drill two through holes diameter 13 mm on the length centerline at X=13 mm and X=202 mm, Y=32 mm.
- functional center feature: Machine a central obround slot 71 mm long x 17 mm wide through the part, centered at X=107 mm, Y=32 mm.
- top relief pocket: Mill a rectangular relief pocket 53 mm x 21 mm x 3 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'V-Mount Battery Plate Offset Spacer With Cable Tunnel'; this requirement is only for its chosen metal part.

---

## SMP-008-08 - Overhead Desk Camera Arm Clamp Head

Part name: Overhead Desk Camera Arm Clamp Head - single metal part

Material: 6061-T6 aluminum (low mass with good machinability and stable flat features)

Envelope: `{"axial_bore_diameter_mm": 20, "outer_diameter_mm": 61, "overall_length_mm": 40, "wall_minimum_mm": 20}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Overhead Desk Camera Arm Clamp Head'. The broader
use case is: A clamp head for a creator desk rig that holds a vertical camera arm above a work
surface for top-down filming. The chosen deliverable is only the metal body implied by: Machined
clamp head with desk-clamp interface flange, vertical post bore, split-clamp slot, pinch screw
bosses, and anti-rotation keyway. All other product elements are external reference items and must
not be modeled. The part must perform this mechanical role: Lock a round or square vertical post to
the desk-edge clamp while resisting rotation and sag. It is intentionally included in the SubCAD
limit corpus because: Tests split clamp mechanics, large bores through compact geometry, keyways,
flange transitions, screw bosses, and perpendicular load paths. The part is made from 6061-T6
aluminum using round bar stock. Start from one cut length of round metal bar. Turn the outside, face
both ends, bore the center, then mill secondary flats, slots, and radial holes as needed. No
separate inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 61 mm and length 40 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 20 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 30 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 20 mm wide over 32 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M5 holes through the top flat at X=13 mm and X=26 mm.
- split relief slit: Cut one full-length radial slit 6 mm wide from the outside to the axial bore on datum-B side.
- outside edge treatment: Break all outside circular edges with 1.0 mm chamfers and keep internal bore edges visibly chamfered.
- cross relief slot: Machine one transverse slot 8 mm wide across the top flat at X=20 mm, depth 6 mm.

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
- Do not broaden the requirement back into the full product idea named 'Overhead Desk Camera Arm Clamp Head'; this requirement is only for its chosen metal part.

---

## SMP-008-09 - Lens Support Yoke for 15mm Rod Rig

Part name: Lens Support Yoke for 15mm Rod Rig - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 68, "length_mm": 80, "width_mm": 60}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Lens Support Yoke for 15mm Rod Rig'. The broader
use case is: A support yoke that mounts to standard 15mm rods and cradles a heavy cinema lens
beneath the barrel. The chosen deliverable is only the metal body implied by: Machined yoke body
with twin rod bores, vertical adjustment slot, curved lens saddle, and locking screw lands. All
other product elements are external reference items and must not be modeled. The part must perform
this mechanical role: Transfer lens weight into the rod system while allowing height adjustment for
different lens diameters. It is intentionally included in the SubCAD limit corpus because: Combines
parallel precision bores, curved support surfaces, slotted vertical adjustment, symmetric structure,
and contact geometry for cylindrical lenses. The part is made from low-carbon steel, ASTM A36 or
equivalent using rectangular block stock. Start from one rectangular metal block or plate. Saw
oversize, face all datum sides, then machine the pockets, holes, slots, angled faces, grooves, and
edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 80 mm x 60 mm x 68 mm.
- mounting hole pattern: Drill two through holes diameter 12 mm on the length centerline at X=12 mm and X=68 mm, Y=30 mm.
- functional center feature: Machine a central obround slot 30 mm long x 16 mm wide through the part, centered at X=40 mm, Y=30 mm.
- top relief pocket: Mill a rectangular relief pocket 25 mm x 20 mm x 11 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
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
- Do not broaden the requirement back into the full product idea named 'Lens Support Yoke for 15mm Rod Rig'; this requirement is only for its chosen metal part.

---

## SMP-008-10 - Creator Light Stand Cable-Managed Ball Head Adapter

Part name: Creator Light Stand Cable-Managed Ball Head Adapter - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 67, "length_mm": 85, "width_mm": 80}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Creator Light Stand Cable-Managed Ball Head
Adapter'. The broader use case is: A compact adapter between a small LED panel ball head and a light
stand, designed for studio creators who need tidy power routing. The chosen deliverable is only the
metal body implied by: Machined adapter puck with threaded stand socket, raised ball-head boss,
radial cable groove, clamp screw hole, and knurled grip perimeter. All other product elements are
external reference items and must not be modeled. The part must perform this mechanical role: Adapt
stand threads to a ball head while guiding the light power cable through a protected side channel.
It is intentionally included in the SubCAD limit corpus because: Requires concentric threaded
features, radial cable routing, perimeter grip texture, raised bosses, and small-scale clearances
around fastening hardware. The part is made from low-carbon steel, ASTM A36 or equivalent using
rectangular block stock. Start from one rectangular metal block or plate. Saw oversize, face all
datum sides, then machine the pockets, holes, slots, angled faces, grooves, and edge treatments into
that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 85 mm x 80 mm x 67 mm.
- mounting hole pattern: Drill two through holes diameter 5 mm on the length centerline at X=16 mm and X=69 mm, Y=40 mm.
- functional center feature: Machine a central obround slot 30 mm long x 13 mm wide through the part, centered at X=42 mm, Y=40 mm.
- top relief pocket: Mill a rectangular relief pocket 25 mm x 26 mm x 19 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
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
- Do not broaden the requirement back into the full product idea named 'Creator Light Stand Cable-Managed Ball Head Adapter'; this requirement is only for its chosen metal part.

---
