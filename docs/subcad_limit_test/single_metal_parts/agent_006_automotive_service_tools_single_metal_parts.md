# Agent 006 Single Metal Part Requirements

Domain: automotive service tools, inspection aids, brackets, jigs, and repair hardware

Each item below is one metal part only. Product assemblies and nonmetal components are explicitly out of scope.

## SMP-006-01 - Brake Caliper Piston Wind-Back Adapter

Part name: Brake Caliper Piston Wind-Back Adapter - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 24, "outer_diameter_mm": 72, "overall_length_mm": 88, "wall_minimum_mm": 24}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Brake Caliper Piston Wind-Back Adapter'. The
broader use case is: Automotive brake service tool used when retracting rear brake caliper pistons
with integrated parking brake mechanisms. The chosen deliverable is only the metal body implied by:
Cylindrical adapter puck with opposing drive lugs, central square-drive socket, chamfered rim, and
relief grooves. All other product elements are external reference items and must not be modeled. The
part must perform this mechanical role: Engages the piston face slots while transmitting axial
pressure and rotation from a service wrench or press tool. It is intentionally included in the
SubCAD limit corpus because: Requires precise coaxial features, raised lugs on a circular face,
socket geometry, chamfers, and functional clearances between shallow and deep features. The part is
made from low-carbon steel, ASTM A36 or equivalent using round bar stock. Start from one cut length
of round metal bar. Turn the outside, face both ends, bore the center, then mill secondary flats,
slots, and radial holes as needed. No separate inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 72 mm and length 88 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 24 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 34 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 24 mm wide over 80 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M6 holes through the top flat at X=29 mm and X=58 mm.
- split relief slit: Cut one full-length radial slit 4 mm wide from the outside to the axial bore on datum-B side.
- outside edge treatment: Break all outside circular edges with 1.0 mm chamfers and keep internal bore edges visibly chamfered.
- cross relief slot: Machine one transverse slot 6 mm wide across the top flat at X=44 mm, depth 7 mm.

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
- Do not broaden the requirement back into the full product idea named 'Brake Caliper Piston Wind-Back Adapter'; this requirement is only for its chosen metal part.

---

## SMP-006-02 - Oxygen Sensor Offset Wrench Head

Part name: Oxygen Sensor Offset Wrench Head - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 51, "length_mm": 105, "width_mm": 70}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Oxygen Sensor Offset Wrench Head'. The broader use
case is: Exhaust repair tool for removing oxygen sensors in tight engine bays without disconnecting
the wiring harness first. The chosen deliverable is only the metal body implied by: Offset crowfoot-
style wrench head with hex bore, open cable slot, square-drive boss, and reinforced curved neck. All
other product elements are external reference items and must not be modeled. The part must perform
this mechanical role: Grips the hex body of an oxygen sensor while leaving a side slot for the
sensor wire to pass through. It is intentionally included in the SubCAD limit corpus because:
Combines interrupted hex geometry, asymmetric openings, load-bearing transitions, bosses, and
nontrivial wall thickness constraints. The part is made from low-carbon steel, ASTM A36 or
equivalent using rectangular block stock. Start from one rectangular metal block or plate. Saw
oversize, face all datum sides, then machine the pockets, holes, slots, angled faces, grooves, and
edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 105 mm x 70 mm x 51 mm.
- mounting hole pattern: Drill two through holes diameter 6 mm on the length centerline at X=14 mm and X=91 mm, Y=35 mm.
- functional center feature: Machine a central obround slot 35 mm long x 9 mm wide through the part, centered at X=52 mm, Y=35 mm.
- top relief pocket: Mill a rectangular relief pocket 26 mm x 23 mm x 17 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Oxygen Sensor Offset Wrench Head'; this requirement is only for its chosen metal part.

---

## SMP-006-03 - CV Boot Clamp Crimping Anvil

Part name: CV Boot Clamp Crimping Anvil - single metal part

Material: 1045 medium-carbon steel, normalized (durable wear surface for workshop loading)

Envelope: `{"axial_bore_diameter_mm": 30, "outer_diameter_mm": 90, "overall_length_mm": 101, "wall_minimum_mm": 30}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'CV Boot Clamp Crimping Anvil'. The broader use case
is: Drivetrain service fixture used to crimp ear-style CV boot clamps consistently during axle
repair. The chosen deliverable is only the metal body implied by: Small hardened anvil block with
contoured saddle, clamp-ear pocket, jaw guide channels, and mounting holes. All other product
elements are external reference items and must not be modeled. The part must perform this mechanical
role: Supports the clamp ear and guides plier jaws so the crimp closes to a repeatable height
without damaging the boot. It is intentionally included in the SubCAD limit corpus because: Tests
concave saddles, small radiused pockets, parallel guide features, compact hole placement, and
service-clearance-driven geometry. The part is made from 1045 medium-carbon steel, normalized using
round bar stock. Start from one cut length of round metal bar. Turn the outside, face both ends,
bore the center, then mill secondary flats, slots, and radial holes as needed. No separate inserts
or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 90 mm and length 101 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 30 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 40 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 30 mm wide over 93 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M6 holes through the top flat at X=33 mm and X=67 mm.
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
- Do not broaden the requirement back into the full product idea named 'CV Boot Clamp Crimping Anvil'; this requirement is only for its chosen metal part.

---

## SMP-006-04 - Wheel Stud Press Support Cup

Part name: Wheel Stud Press Support Cup - single metal part

Material: 1045 medium-carbon steel, normalized (durable wear surface for workshop loading)

Envelope: `{"length_mm": 255, "thickness_mm": 5, "width_mm": 100}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Wheel Stud Press Support Cup'. The broader use case
is: Hub repair hardware used with a shop press or C-clamp tool to remove and install wheel studs
without bending the hub flange. The chosen deliverable is only the metal body implied by: Thick
annular cup with stepped bore, relieved side window, flange contact face, and anti-slip outer flats.
All other product elements are external reference items and must not be modeled. The part must
perform this mechanical role: Supports the hub around the stud head while leaving clearance for the
stud to pass through during pressing. It is intentionally included in the SubCAD limit corpus
because: Includes nested cylindrical bores, stepped internal cavities, side cutouts, thick-section
proportions, and datum-critical bearing surfaces. The part is made from 1045 medium-carbon steel,
normalized using sheet or plate stock. Start from one flat sheet or plate blank. Cut the outside
profile, machine holes, slots, pockets, lips, and relief features into that same piece. If bends are
called out, they are bends in the same sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 255 mm x 100 mm x 5 mm.
- mounting hole pattern: Drill two through holes diameter 8 mm on the length centerline at X=20 mm and X=235 mm, Y=50 mm.
- functional center feature: Machine a central obround slot 85 mm long x 13 mm wide through the part, centered at X=127 mm, Y=50 mm.
- top relief pocket: Mill a rectangular relief pocket 63 mm x 33 mm x 2 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- serrated contact edge: Cut 10 equal triangular serrations across the rear edge, each 2 mm deep.

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
- Do not broaden the requirement back into the full product idea named 'Wheel Stud Press Support Cup'; this requirement is only for its chosen metal part.

---

## SMP-006-05 - Tie Rod End Taper Inspection Gauge

Part name: Tie Rod End Taper Inspection Gauge - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 19, "outer_diameter_mm": 77, "overall_length_mm": 80, "wall_minimum_mm": 29}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Tie Rod End Taper Inspection Gauge'. The broader
use case is: Steering inspection aid for checking whether a tie rod end taper or steering knuckle
bore is worn beyond acceptable fit. The chosen deliverable is only the metal body implied by:
Machined tapered plug gauge with shoulder stop, engraved depth bands, knurled grip section, and flat
reference face. All other product elements are external reference items and must not be modeled. The
part must perform this mechanical role: Provides reference taper surfaces and depth marks to compare
seating depth and contact pattern. It is intentionally included in the SubCAD limit corpus because:
Tests tapered solids, shoulder transitions, engraved or recessed markings, mixed grip textures, and
tolerance-sensitive reference surfaces. The part is made from low-carbon steel, ASTM A36 or
equivalent using round bar stock. Start from one cut length of round metal bar. Turn the outside,
face both ends, bore the center, then mill secondary flats, slots, and radial holes as needed. No
separate inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 77 mm and length 80 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 19 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 29 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 25 mm wide over 72 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M5 holes through the top flat at X=26 mm and X=53 mm.
- split relief slit: Cut one full-length radial slit 2 mm wide from the outside to the axial bore on datum-B side.
- outside edge treatment: Break all outside circular edges with 1.0 mm chamfers and keep internal bore edges visibly chamfered.
- opposed wrench flats: Mill two opposed flats across the outside, leaving 69 mm across flats over the middle third of the length.

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
- Do not broaden the requirement back into the full product idea named 'Tie Rod End Taper Inspection Gauge'; this requirement is only for its chosen metal part.

---

## SMP-006-06 - Strut Knuckle Spreader Wedge

Part name: Strut Knuckle Spreader Wedge - single metal part

Material: 1045 medium-carbon steel, normalized (durable wear surface for workshop loading)

Envelope: `{"axial_bore_diameter_mm": 19, "outer_diameter_mm": 77, "overall_length_mm": 110, "wall_minimum_mm": 29}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Strut Knuckle Spreader Wedge'. The broader use case
is: Suspension service tool for opening the clamping slot on MacPherson strut knuckles during strut
removal. The chosen deliverable is only the metal body implied by: Tapered wedge with rounded nose,
stop shoulder, wrench flats, and shallow retention groove. All other product elements are external
reference items and must not be modeled. The part must perform this mechanical role: Slides into the
knuckle slot and expands it a controlled amount without over-spreading or gouging the casting. It is
intentionally included in the SubCAD limit corpus because: Uses tapered prismatic geometry, rounded
leading surfaces, functional stops, flats on angled bodies, and stress-aware transitions. The part
is made from 1045 medium-carbon steel, normalized using round bar stock. Start from one cut length
of round metal bar. Turn the outside, face both ends, bore the center, then mill secondary flats,
slots, and radial holes as needed. No separate inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 77 mm and length 110 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 19 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 29 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 25 mm wide over 102 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M8 holes through the top flat at X=36 mm and X=73 mm.
- split relief slit: Cut one full-length radial slit 6 mm wide from the outside to the axial bore on datum-B side.
- outside edge treatment: Break all outside circular edges with 1.0 mm chamfers and keep internal bore edges visibly chamfered.
- opposed wrench flats: Mill two opposed flats across the outside, leaving 69 mm across flats over the middle third of the length.

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
- Do not broaden the requirement back into the full product idea named 'Strut Knuckle Spreader Wedge'; this requirement is only for its chosen metal part.

---

## SMP-006-07 - Brake Rotor Runout Indicator Clamp

Part name: Brake Rotor Runout Indicator Clamp - single metal part

Material: 1045 medium-carbon steel, normalized (durable wear surface for workshop loading)

Envelope: `{"height_mm": 17, "length_mm": 200, "width_mm": 85}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Brake Rotor Runout Indicator Clamp'. The broader
use case is: Brake inspection aid for mounting a dial indicator to a suspension upright or caliper
bracket when measuring rotor runout. The chosen deliverable is only the metal body implied by: Split
clamp block with V-groove jaw, cross-bolt slot, indicator stem bore, and perpendicular locking screw
boss. All other product elements are external reference items and must not be modeled. The part must
perform this mechanical role: Clamps to an irregular service location and provides a rigid
adjustable mount for an indicator stem. It is intentionally included in the SubCAD limit corpus
because: Challenges representation of split bodies, V-grooves, intersecting bores, clamp slots,
bosses, and perpendicular fastening features. The part is made from 1045 medium-carbon steel,
normalized using rectangular block stock. Start from one rectangular metal block or plate. Saw
oversize, face all datum sides, then machine the pockets, holes, slots, angled faces, grooves, and
edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 200 mm x 85 mm x 17 mm.
- mounting hole pattern: Drill two through holes diameter 8 mm on the length centerline at X=17 mm and X=183 mm, Y=42 mm.
- functional center feature: Machine a central obround slot 66 mm long x 18 mm wide through the part, centered at X=100 mm, Y=42 mm.
- top relief pocket: Mill a rectangular relief pocket 50 mm x 28 mm x 7 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- centered V-groove: Cut a 90 degree V-groove along the full X length on the top face, groove mouth 42 mm wide and depth 5 mm.
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
- The feature named 'centered V-groove' is present with the stated size and position.
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
- Do not broaden the requirement back into the full product idea named 'Brake Rotor Runout Indicator Clamp'; this requirement is only for its chosen metal part.

---

## SMP-006-08 - Fuel Injector Puller Bridge

Part name: Fuel Injector Puller Bridge - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 49, "length_mm": 95, "width_mm": 70}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Fuel Injector Puller Bridge'. The broader use case
is: Engine service jig for extracting stuck fuel injectors from a cylinder head without prying
against fragile plastic or aluminum surfaces. The chosen deliverable is only the metal body implied
by: Rigid bridge bar with arched center clearance, adjustable foot pads, threaded pull-screw boss,
and elongated mounting slots. All other product elements are external reference items and must not
be modeled. The part must perform this mechanical role: Spans across nearby head features and guides
a pull screw aligned with the injector axis. It is intentionally included in the SubCAD limit corpus
because: Combines arched relief geometry, slots, threaded boss placement, planar support feet, and
alignment-critical central features. The part is made from low-carbon steel, ASTM A36 or equivalent
using rectangular block stock. Start from one rectangular metal block or plate. Saw oversize, face
all datum sides, then machine the pockets, holes, slots, angled faces, grooves, and edge treatments
into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 95 mm x 70 mm x 49 mm.
- mounting hole pattern: Drill two through holes diameter 9 mm on the length centerline at X=14 mm and X=81 mm, Y=35 mm.
- functional center feature: Machine a central obround slot 31 mm long x 12 mm wide through the part, centered at X=47 mm, Y=35 mm.
- top relief pocket: Mill a rectangular relief pocket 25 mm x 23 mm x 11 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Fuel Injector Puller Bridge'; this requirement is only for its chosen metal part.

---

## SMP-006-09 - Exhaust Hanger Removal Fork

Part name: Exhaust Hanger Removal Fork - single metal part

Material: 1045 medium-carbon steel, normalized (durable wear surface for workshop loading)

Envelope: `{"height_mm": 24, "length_mm": 190, "width_mm": 85}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Exhaust Hanger Removal Fork'. The broader use case
is: Exhaust service hand tool for pushing rubber exhaust isolators off welded hanger rods. The
chosen deliverable is only the metal body implied by: Forked pry head with semicircular rod notch,
broad curved pusher face, offset handle socket, and reinforced ribs. All other product elements are
external reference items and must not be modeled. The part must perform this mechanical role:
Captures the hanger rod while applying force to the rubber isolator face without tearing it. It is
intentionally included in the SubCAD limit corpus because: Tests forked negative spaces, curved
contact faces, socket-to-head offsets, ribbed reinforcement, and ergonomic service geometry. The
part is made from 1045 medium-carbon steel, normalized using rectangular block stock. Start from one
rectangular metal block or plate. Saw oversize, face all datum sides, then machine the pockets,
holes, slots, angled faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 190 mm x 85 mm x 24 mm.
- mounting hole pattern: Drill two through holes diameter 10 mm on the length centerline at X=17 mm and X=173 mm, Y=42 mm.
- functional center feature: Machine a central obround slot 63 mm long x 11 mm wide through the part, centered at X=95 mm, Y=42 mm.
- top relief pocket: Mill a rectangular relief pocket 47 mm x 28 mm x 6 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Exhaust Hanger Removal Fork'; this requirement is only for its chosen metal part.

---

## SMP-006-10 - Door Hinge Pin Alignment Jig

Part name: Door Hinge Pin Alignment Jig - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 12, "outer_diameter_mm": 60, "overall_length_mm": 53, "wall_minimum_mm": 24}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Door Hinge Pin Alignment Jig'. The broader use case
is: Body repair jig used when replacing worn door hinge pins and bushings on vehicles with heavy
doors. The chosen deliverable is only the metal body implied by: Clamp-on alignment block with dual
hinge-barrel saddles, guide bushing bore, tightening screw pads, and datum shoulders. All other
product elements are external reference items and must not be modeled. The part must perform this
mechanical role: Holds the hinge leaves coaxial while guiding a replacement pin or reamer through
both hinge barrels. It is intentionally included in the SubCAD limit corpus because: Requires
coaxial guide features, paired saddles, clamp pads, shoulders, and constrained access geometry tied
to a real repair workflow. The part is made from low-carbon steel, ASTM A36 or equivalent using
round bar stock. Start from one cut length of round metal bar. Turn the outside, face both ends,
bore the center, then mill secondary flats, slots, and radial holes as needed. No separate inserts
or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 60 mm and length 53 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 12 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 22 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 20 mm wide over 45 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M5 holes through the top flat at X=17 mm and X=35 mm.
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
- Do not broaden the requirement back into the full product idea named 'Door Hinge Pin Alignment Jig'; this requirement is only for its chosen metal part.

---
