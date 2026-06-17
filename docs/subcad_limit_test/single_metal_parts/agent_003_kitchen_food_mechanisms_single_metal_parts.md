# Agent 003 Single Metal Part Requirements

Domain: kitchen appliances and food-processing mechanisms

Each item below is one metal part only. Product assemblies and nonmetal components are explicitly out of scope.

## SMP-003-01 - Conical Burr Coffee Grinder Adjustment Collar

Part name: Conical Burr Coffee Grinder Adjustment Collar - single metal part

Material: 1045 medium-carbon steel, normalized (durable wear surface for workshop loading)

Envelope: `{"axial_bore_diameter_mm": 22, "outer_diameter_mm": 89, "overall_length_mm": 54, "wall_minimum_mm": 33}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Conical Burr Coffee Grinder Adjustment Collar'. The
broader use case is: Manual or electric burr coffee grinder used for espresso-to-French-press grind
adjustment. The chosen deliverable is only the metal body implied by: Threaded stepped adjustment
collar with detent pockets and burr mounting lands. All other product elements are external
reference items and must not be modeled. The part must perform this mechanical role: Holds and
indexes the upper conical burr while allowing fine axial position changes. It is intentionally
included in the SubCAD limit corpus because: Combines internal threads, concentric stepped bores,
radial detent features, tight coaxial references, and small repeated pockets around a circular body.
The part is made from 1045 medium-carbon steel, normalized using round bar stock. Start from one cut
length of round metal bar. Turn the outside, face both ends, bore the center, then mill secondary
flats, slots, and radial holes as needed. No separate inserts or fasteners are part of the
deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 89 mm and length 54 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 22 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 32 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 29 mm wide over 46 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M5 holes through the top flat at X=18 mm and X=36 mm.
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
- Do not broaden the requirement back into the full product idea named 'Conical Burr Coffee Grinder Adjustment Collar'; this requirement is only for its chosen metal part.

---

## SMP-003-02 - Meat Grinder Feed Auger

Part name: Meat Grinder Feed Auger - single metal part

Material: 1045 medium-carbon steel, normalized (durable wear surface for workshop loading)

Envelope: `{"height_mm": 27, "length_mm": 175, "width_mm": 105}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Meat Grinder Feed Auger'. The broader use case is:
Countertop meat grinder or mixer attachment for sausage and ground meat preparation. The chosen
deliverable is only the metal body implied by: Tapered helical auger screw with drive coupling and
front knife pilot. All other product elements are external reference items and must not be modeled.
The part must perform this mechanical role: Draws meat from the hopper and compresses it toward the
cutting knife and extrusion plate. It is intentionally included in the SubCAD limit corpus because:
Requires continuous helical flights, changing pitch or diameter, blended root fillets, keyed drive
geometry, and a functional transition from screw body to shaft. The part is made from 1045 medium-
carbon steel, normalized using rectangular block stock. Start from one rectangular metal block or
plate. Saw oversize, face all datum sides, then machine the pockets, holes, slots, angled faces,
grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 175 mm x 105 mm x 27 mm.
- mounting hole pattern: Drill two through holes diameter 8 mm on the length centerline at X=21 mm and X=154 mm, Y=52 mm.
- functional center feature: Machine a central obround slot 58 mm long x 16 mm wide through the part, centered at X=87 mm, Y=52 mm.
- top relief pocket: Mill a rectangular relief pocket 43 mm x 35 mm x 4 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- machined angled reference face: Machine one top reference face at 31 degrees over the last 35 mm of length.
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
- Do not broaden the requirement back into the full product idea named 'Meat Grinder Feed Auger'; this requirement is only for its chosen metal part.

---

## SMP-003-03 - Citrus Juicer Reamer Cone

Part name: Citrus Juicer Reamer Cone - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 54, "length_mm": 110, "width_mm": 70}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Citrus Juicer Reamer Cone'. The broader use case
is: Lever or motorized citrus juicer for oranges, lemons, and grapefruit. The chosen deliverable is
only the metal body implied by: Ribbed tapered reamer cone with central hub and drainage channels.
All other product elements are external reference items and must not be modeled. The part must
perform this mechanical role: Ruptures citrus segments while guiding juice downward and retaining
pulp. It is intentionally included in the SubCAD limit corpus because: Tests radial rib repetition
on a curved tapered surface, alternating grooves, smooth lofted cone geometry, and blended drain
paths. The part is made from low-carbon steel, ASTM A36 or equivalent using rectangular block stock.
Start from one rectangular metal block or plate. Saw oversize, face all datum sides, then machine
the pockets, holes, slots, angled faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 110 mm x 70 mm x 54 mm.
- mounting hole pattern: Drill two through holes diameter 12 mm on the length centerline at X=14 mm and X=96 mm, Y=35 mm.
- functional center feature: Machine a central obround slot 36 mm long x 8 mm wide through the part, centered at X=55 mm, Y=35 mm.
- top relief pocket: Mill a rectangular relief pocket 27 mm x 23 mm x 22 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- machined angled reference face: Machine one top reference face at 11 degrees over the last 22 mm of length.

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
- Do not broaden the requirement back into the full product idea named 'Citrus Juicer Reamer Cone'; this requirement is only for its chosen metal part.

---

## SMP-003-04 - Stand Mixer Planetary Gear Carrier

Part name: Stand Mixer Planetary Gear Carrier - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 21, "outer_diameter_mm": 64, "overall_length_mm": 117, "wall_minimum_mm": 21}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Stand Mixer Planetary Gear Carrier'. The broader
use case is: Kitchen stand mixer head that drives beaters in a planetary mixing motion. The chosen
deliverable is only the metal body implied by: Planet carrier hub with offset shaft bosses, bearing
seats, and gear clearance pockets. All other product elements are external reference items and must
not be modeled. The part must perform this mechanical role: Supports rotating gear elements so the
beater shaft orbits while spinning. It is intentionally included in the SubCAD limit corpus because:
Includes eccentric axes, precise bearing bores, multiple concentric and nonconcentric features, gear
relief cutouts, and load-bearing filleted bosses. The part is made from low-carbon steel, ASTM A36
or equivalent using round bar stock. Start from one cut length of round metal bar. Turn the outside,
face both ends, bore the center, then mill secondary flats, slots, and radial holes as needed. No
separate inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 64 mm and length 117 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 21 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 31 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 21 mm wide over 109 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M6 holes through the top flat at X=39 mm and X=78 mm.
- split relief slit: Cut one full-length radial slit 3 mm wide from the outside to the axial bore on datum-B side.
- outside edge treatment: Break all outside circular edges with 1.0 mm chamfers and keep internal bore edges visibly chamfered.
- cross relief slot: Machine one transverse slot 5 mm wide across the top flat at X=58 mm, depth 6 mm.

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
- Do not broaden the requirement back into the full product idea named 'Stand Mixer Planetary Gear Carrier'; this requirement is only for its chosen metal part.

---

## SMP-003-05 - Pasta Roller Thickness Cam

Part name: Pasta Roller Thickness Cam - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 22, "outer_diameter_mm": 90, "overall_length_mm": 52, "wall_minimum_mm": 34}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Pasta Roller Thickness Cam'. The broader use case
is: Hand-cranked or motorized pasta roller used to progressively thin dough sheets. The chosen
deliverable is only the metal body implied by: Multi-lobed eccentric cam disk with selector notches
and shaft bore. All other product elements are external reference items and must not be modeled. The
part must perform this mechanical role: Shifts roller spacing through indexed thickness settings. It
is intentionally included in the SubCAD limit corpus because: Tests noncircular cam profiles,
angular indexing, asymmetric lobes, shaft flats, and dimensionally meaningful offset geometry. The
part is made from low-carbon steel, ASTM A36 or equivalent using round bar stock. Start from one cut
length of round metal bar. Turn the outside, face both ends, bore the center, then mill secondary
flats, slots, and radial holes as needed. No separate inserts or fasteners are part of the
deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 90 mm and length 52 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 22 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 32 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 30 mm wide over 44 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M8 holes through the top flat at X=17 mm and X=34 mm.
- split relief slit: Cut one full-length radial slit 2 mm wide from the outside to the axial bore on datum-B side.
- outside edge treatment: Break all outside circular edges with 1.0 mm chamfers and keep internal bore edges visibly chamfered.
- opposed wrench flats: Mill two opposed flats across the outside, leaving 82 mm across flats over the middle third of the length.

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
- Do not broaden the requirement back into the full product idea named 'Pasta Roller Thickness Cam'; this requirement is only for its chosen metal part.

---

## SMP-003-06 - Mandoline Slicer Thickness Ramp Carriage

Part name: Mandoline Slicer Thickness Ramp Carriage - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 62, "length_mm": 80, "width_mm": 70}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Mandoline Slicer Thickness Ramp Carriage'. The
broader use case is: Adjustable mandoline slicer for vegetables such as potatoes, cucumbers, and
carrots. The chosen deliverable is only the metal body implied by: Sliding ramp carriage with angled
guide rails, blade clearance slot, and locking teeth. All other product elements are external
reference items and must not be modeled. The part must perform this mechanical role: Raises or
lowers the food deck relative to the blade to set slice thickness. It is intentionally included in
the SubCAD limit corpus because: Combines angled reference planes, long slots, rack-like teeth,
shallow ramps, and clearance geometry tied to a cutting edge. The part is made from low-carbon
steel, ASTM A36 or equivalent using rectangular block stock. Start from one rectangular metal block
or plate. Saw oversize, face all datum sides, then machine the pockets, holes, slots, angled faces,
grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 80 mm x 70 mm x 62 mm.
- mounting hole pattern: Drill two through holes diameter 7 mm on the length centerline at X=14 mm and X=66 mm, Y=35 mm.
- functional center feature: Machine a central obround slot 30 mm long x 18 mm wide through the part, centered at X=40 mm, Y=35 mm.
- top relief pocket: Mill a rectangular relief pocket 25 mm x 23 mm x 1 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- serrated contact edge: Cut 9 equal triangular serrations across the rear edge, each 2 mm deep.
- machined angled reference face: Machine one top reference face at 34 degrees over the last 18 mm of length.

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
- Do not broaden the requirement back into the full product idea named 'Mandoline Slicer Thickness Ramp Carriage'; this requirement is only for its chosen metal part.

---

## SMP-003-07 - Dough Sheeter Roller End Journal

Part name: Dough Sheeter Roller End Journal - single metal part

Material: 4140 alloy steel, prehard (strong cylindrical metal part with threaded and slotted details)

Envelope: `{"axial_bore_diameter_mm": 12, "outer_diameter_mm": 38, "overall_length_mm": 75, "wall_minimum_mm": 13}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Dough Sheeter Roller End Journal'. The broader use
case is: Small bakery dough sheeter or countertop laminator for pastry dough. The chosen deliverable
is only the metal body implied by: Stepped roller end journal with bearing seats, keyway, retaining
groove, and taper transition. All other product elements are external reference items and must not
be modeled. The part must perform this mechanical role: Supports a heavy roller while transmitting
torque and maintaining alignment. It is intentionally included in the SubCAD limit corpus because:
Tests precision stepped shafts, grooves, keyways, chamfers, bearing shoulders, and transitions
between cylindrical sections with different tolerance roles. The part is made from 4140 alloy steel,
prehard using round bar stock. Start from one cut length of round metal bar. Turn the outside, face
both ends, bore the center, then mill secondary flats, slots, and radial holes as needed. No
separate inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 38 mm and length 75 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 12 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 22 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 12 mm wide over 67 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M6 holes through the top flat at X=25 mm and X=50 mm.
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
- Do not broaden the requirement back into the full product idea named 'Dough Sheeter Roller End Journal'; this requirement is only for its chosen metal part.

---

## SMP-003-08 - Food Processor Bowl Bayonet Lock Ring

Part name: Food Processor Bowl Bayonet Lock Ring - single metal part

Material: AISI 316 stainless steel (corrosion resistance and cleanable metal surfaces)

Envelope: `{"height_mm": 62, "length_mm": 120, "width_mm": 45}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Food Processor Bowl Bayonet Lock Ring'. The broader
use case is: Food processor bowl interface that twists onto the motor base before operation. The
chosen deliverable is only the metal body implied by: Circular bayonet lock ring with ramped lugs,
stop blocks, and interlock actuator tab. All other product elements are external reference items and
must not be modeled. The part must perform this mechanical role: Locks the bowl mechanically and
aligns safety interlock features. It is intentionally included in the SubCAD limit corpus because:
Requires circumferential locking ramps, interrupted ring geometry, repeated but directional lugs,
undercut-like stops, and functional angular travel constraints. The part is made from AISI 316
stainless steel using rectangular block stock. Start from one rectangular metal block or plate. Saw
oversize, face all datum sides, then machine the pockets, holes, slots, angled faces, grooves, and
edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 120 mm x 45 mm x 62 mm.
- mounting hole pattern: Drill two through holes diameter 9 mm on the length centerline at X=10 mm and X=110 mm, Y=22 mm.
- functional center feature: Machine a central obround slot 40 mm long x 17 mm wide through the part, centered at X=60 mm, Y=22 mm.
- top relief pocket: Mill a rectangular relief pocket 30 mm x 18 mm x 31 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Food Processor Bowl Bayonet Lock Ring'; this requirement is only for its chosen metal part.

---

## SMP-003-09 - Grain Mill Fluted Feed Roller

Part name: Grain Mill Fluted Feed Roller - single metal part

Material: 4140 alloy steel, prehard (strong cylindrical metal part with threaded and slotted details)

Envelope: `{"axial_bore_diameter_mm": 29, "outer_diameter_mm": 89, "overall_length_mm": 32, "wall_minimum_mm": 30}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Grain Mill Fluted Feed Roller'. The broader use
case is: Home grain mill or oat flaker feeding kernels into crushing or milling rollers. The chosen
deliverable is only the metal body implied by: Cylindrical feed roller with axial flutes, knurled
grip zones, and keyed shaft ends. All other product elements are external reference items and must
not be modeled. The part must perform this mechanical role: Grips and meters grain into the milling
gap. It is intentionally included in the SubCAD limit corpus because: Tests repeated flutes around a
cylinder, shallow concave groove profiles, shaft-to-roller transitions, rotational symmetry, and
manufacturable texture-like geometry. The part is made from 4140 alloy steel, prehard using round
bar stock. Start from one cut length of round metal bar. Turn the outside, face both ends, bore the
center, then mill secondary flats, slots, and radial holes as needed. No separate inserts or
fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 89 mm and length 32 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 29 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 39 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 29 mm wide over 24 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M5 holes through the top flat at X=10 mm and X=21 mm.
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
- Do not broaden the requirement back into the full product idea named 'Grain Mill Fluted Feed Roller'; this requirement is only for its chosen metal part.

---

## SMP-003-10 - Rotary Cheese Grater Drum

Part name: Rotary Cheese Grater Drum - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 21, "outer_diameter_mm": 63, "overall_length_mm": 75, "wall_minimum_mm": 21}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Rotary Cheese Grater Drum'. The broader use case
is: Handheld rotary grater for hard cheese, chocolate, or nuts. The chosen deliverable is only the
metal body implied by: Perforated cylindrical grater drum with raised cutting lips and end drive
socket. All other product elements are external reference items and must not be modeled. The part
must perform this mechanical role: Cuts food against a fixed pressure plate as the drum rotates. It
is intentionally included in the SubCAD limit corpus because: Challenges CAD representation with
patterned holes on a curved surface, directional cutting protrusions, thin-wall cylinder
constraints, rolled-edge rims, and a nonround drive interface. The part is made from low-carbon
steel, ASTM A36 or equivalent using round bar stock. Start from one cut length of round metal bar.
Turn the outside, face both ends, bore the center, then mill secondary flats, slots, and radial
holes as needed. No separate inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 63 mm and length 75 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 21 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 31 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 21 mm wide over 67 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M8 holes through the top flat at X=25 mm and X=50 mm.
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
- Do not broaden the requirement back into the full product idea named 'Rotary Cheese Grater Drum'; this requirement is only for its chosen metal part.

---
