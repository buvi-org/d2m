# Agent 033 Single Metal Part Requirements

Domain: CNC router, woodworking machine, saw, planer, and dust-collection hardware

Each item below is one metal part only. Product assemblies and nonmetal components are explicitly out of scope.

## SMP-033-01 - Gantry CNC router spindle carriage with dust shoe

Part name: Gantry CNC router spindle carriage with dust shoe - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 8, "outer_diameter_mm": 29, "overall_length_mm": 93, "wall_minimum_mm": 10}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Gantry CNC router spindle carriage with dust shoe'.
The broader use case is: A moving spindle assembly used on a gantry-style CNC router for sheet
goods, cabinet panels, and nested woodworking operations. The chosen deliverable is only the metal
body implied by: Layered carriage plate carrying linear blocks, spindle clamp, Z-axis slide, and
dust-shoe mount. All other product elements are external reference items and must not be modeled.
The part must perform this mechanical role: Holds the router spindle, guides vertical travel, and
surrounds the cutting area with a brush-backed dust shoe. It is intentionally included in the SubCAD
limit corpus because: Combines flat plates, rail interfaces, clamp geometry, nested openings, and a
partially transparent accessory region without needing exact machine dimensions. The part is made
from low-carbon steel, ASTM A36 or equivalent using round bar stock. Start from one cut length of
round metal bar. Turn the outside, face both ends, bore the center, then mill secondary flats,
slots, and radial holes as needed. No separate inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 29 mm and length 93 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 8 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 18 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 9 mm wide over 85 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M8 holes through the top flat at X=31 mm and X=62 mm.
- split relief slit: Cut one full-length radial slit 3 mm wide from the outside to the axial bore on datum-B side.
- outside edge treatment: Break all outside circular edges with 1.0 mm chamfers and keep internal bore edges visibly chamfered.
- opposed wrench flats: Mill two opposed flats across the outside, leaving 22 mm across flats over the middle third of the length.

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
- Do not broaden the requirement back into the full product idea named 'Gantry CNC router spindle carriage with dust shoe'; this requirement is only for its chosen metal part.

---

## SMP-033-02 - Tilting table saw blade guard and riving knife bracket

Part name: Tilting table saw blade guard and riving knife bracket - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"length_mm": 140, "thickness_mm": 6, "width_mm": 105}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Tilting table saw blade guard and riving knife
bracket'. The broader use case is: A safety hardware assembly mounted behind the blade area of a
woodworking table saw. The chosen deliverable is only the metal body implied by: Curved bracket with
slotted adjustment holes, hinge ears, and a narrow knife-like plate. All other product elements are
external reference items and must not be modeled. The part must perform this mechanical role:
Supports a riving knife, holds a pivoting blade guard, and keeps alignment with the blade path
during cutting adjustments. It is intentionally included in the SubCAD limit corpus because: Tests
thin safety plates, curved guards, pivot lugs, clearance slots, and feature placement around an
implied rotating blade envelope. The part is made from low-carbon steel, ASTM A36 or equivalent
using sheet or plate stock. Start from one flat sheet or plate blank. Cut the outside profile,
machine holes, slots, pockets, lips, and relief features into that same piece. If bends are called
out, they are bends in the same sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 140 mm x 105 mm x 6 mm.
- mounting hole pattern: Drill two through holes diameter 8 mm on the length centerline at X=21 mm and X=119 mm, Y=52 mm.
- functional center feature: Machine a central obround slot 46 mm long x 8 mm wide through the part, centered at X=70 mm, Y=52 mm.
- top relief pocket: Mill a rectangular relief pocket 35 mm x 35 mm x 1 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Tilting table saw blade guard and riving knife bracket'; this requirement is only for its chosen metal part.

---

## SMP-033-03 - Planer cutterhead chip hood with hose outlet

Part name: Planer cutterhead chip hood with hose outlet - single metal part

Material: 4140 alloy steel, prehard (strong cylindrical metal part with threaded and slotted details)

Envelope: `{"axial_bore_diameter_mm": 12, "outer_diameter_mm": 36, "overall_length_mm": 64, "wall_minimum_mm": 12}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Planer cutterhead chip hood with hose outlet'. The
broader use case is: A dust and chip extraction hood fitted over the cutterhead area of a thickness
planer. The chosen deliverable is only the metal body implied by: Swept hood shell with rectangular
intake mouth, rounded transition, and cylindrical outlet collar. All other product elements are
external reference items and must not be modeled. The part must perform this mechanical role:
Captures high-volume shavings from the cutterhead and routes them toward a dust-collection hose. It
is intentionally included in the SubCAD limit corpus because: Challenges representation of smooth
transitions between rectangular and round openings, hollow shell intent, flange details, and
directional flow geometry. The part is made from 4140 alloy steel, prehard using round bar stock.
Start from one cut length of round metal bar. Turn the outside, face both ends, bore the center,
then mill secondary flats, slots, and radial holes as needed. No separate inserts or fasteners are
part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 36 mm and length 64 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 12 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 22 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 12 mm wide over 56 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M5 holes through the top flat at X=21 mm and X=42 mm.
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
- Do not broaden the requirement back into the full product idea named 'Planer cutterhead chip hood with hose outlet'; this requirement is only for its chosen metal part.

---

## SMP-033-04 - CNC router vacuum hold-down zone manifold

Part name: CNC router vacuum hold-down zone manifold - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 18, "outer_diameter_mm": 55, "overall_length_mm": 108, "wall_minimum_mm": 18}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'CNC router vacuum hold-down zone manifold'. The
broader use case is: A manifold plate used under a CNC router spoilboard to distribute vacuum to
selectable cutting zones. The chosen deliverable is only the metal body implied by: Flat manifold
body with branching channels, gasket grooves, valve pockets, and port collars. All other product
elements are external reference items and must not be modeled. The part must perform this mechanical
role: Routes vacuum from a main inlet to multiple gated channels so wood sheets stay fixed during
machining. It is intentionally included in the SubCAD limit corpus because: Tests internal routing,
repeated sealed zones, shallow grooves, planar layouts, and the distinction between visible surface
features and hidden flow paths. The part is made from low-carbon steel, ASTM A36 or equivalent using
round bar stock. Start from one cut length of round metal bar. Turn the outside, face both ends,
bore the center, then mill secondary flats, slots, and radial holes as needed. No separate inserts
or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 55 mm and length 108 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 18 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 28 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 18 mm wide over 100 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M5 holes through the top flat at X=36 mm and X=72 mm.
- split relief slit: Cut one full-length radial slit 6 mm wide from the outside to the axial bore on datum-B side.
- outside edge treatment: Break all outside circular edges with 1.0 mm chamfers and keep internal bore edges visibly chamfered.
- opposed wrench flats: Mill two opposed flats across the outside, leaving 47 mm across flats over the middle third of the length.

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
- Do not broaden the requirement back into the full product idea named 'CNC router vacuum hold-down zone manifold'; this requirement is only for its chosen metal part.

---

## SMP-033-05 - Sliding compound miter saw fence extension stop

Part name: Sliding compound miter saw fence extension stop - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 10, "outer_diameter_mm": 42, "overall_length_mm": 102, "wall_minimum_mm": 16}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Sliding compound miter saw fence extension stop'.
The broader use case is: An adjustable stop and fence extension accessory for repeat cuts on a
sliding compound miter saw station. The chosen deliverable is only the metal body implied by:
Extruded rail-like fence body with sliding stop block, pivoting flag, and clamp knob boss. All other
product elements are external reference items and must not be modeled. The part must perform this
mechanical role: Extends the saw fence and provides a flip-down stop for repeatable woodworking
cuts. It is intentionally included in the SubCAD limit corpus because: Exercises long prismatic
rails, movable accessory blocks, hinge-like stop features, knobs, and repeatable profile details
without fixed length requirements. The part is made from low-carbon steel, ASTM A36 or equivalent
using round bar stock. Start from one cut length of round metal bar. Turn the outside, face both
ends, bore the center, then mill secondary flats, slots, and radial holes as needed. No separate
inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 42 mm and length 102 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 10 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 20 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 14 mm wide over 94 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M6 holes through the top flat at X=34 mm and X=68 mm.
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
- Do not broaden the requirement back into the full product idea named 'Sliding compound miter saw fence extension stop'; this requirement is only for its chosen metal part.

---

## SMP-033-06 - Cyclone dust separator inlet and cone body

Part name: Cyclone dust separator inlet and cone body - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 15, "outer_diameter_mm": 79, "overall_length_mm": 99, "wall_minimum_mm": 32}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Cyclone dust separator inlet and cone body'. The
broader use case is: A compact cyclone separator mounted between woodworking machines and a shop
dust collector. The chosen deliverable is only the metal body implied by: Tapered cyclone cone with
tangential inlet, top outlet tube, and bin-mounting flange. All other product elements are external
reference items and must not be modeled. The part must perform this mechanical role: Spins dust-
laden air so chips fall into a collection bin before air continues to the vacuum system. It is
intentionally included in the SubCAD limit corpus because: Tests conical bodies, tangential
cylindrical intersections, hollow airflow features, flange bolt patterns, and non-orthogonal
relationships. The part is made from low-carbon steel, ASTM A36 or equivalent using round bar stock.
Start from one cut length of round metal bar. Turn the outside, face both ends, bore the center,
then mill secondary flats, slots, and radial holes as needed. No separate inserts or fasteners are
part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 79 mm and length 99 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 15 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 25 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 26 mm wide over 91 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M5 holes through the top flat at X=33 mm and X=66 mm.
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
- Do not broaden the requirement back into the full product idea named 'Cyclone dust separator inlet and cone body'; this requirement is only for its chosen metal part.

---

## SMP-033-07 - Jointer planer adjustable outfeed table hinge support

Part name: Jointer planer adjustable outfeed table hinge support - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 42, "length_mm": 95, "width_mm": 85}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Jointer planer adjustable outfeed table hinge
support'. The broader use case is: A support bracket for fine alignment of a jointer or planer
outfeed table relative to the cutterhead. The chosen deliverable is only the metal body implied by:
Heavy side casting with hinge barrel, locking boss, ribbing, and adjustment screw pads. All other
product elements are external reference items and must not be modeled. The part must perform this
mechanical role: Allows the table to pivot and lock while maintaining a stable coplanar reference
surface for boards. It is intentionally included in the SubCAD limit corpus because: Combines cast-
looking ribs, hinge cylinders, flat reference faces, threaded adjuster locations, and load-bearing
asymmetry. The part is made from low-carbon steel, ASTM A36 or equivalent using rectangular block
stock. Start from one rectangular metal block or plate. Saw oversize, face all datum sides, then
machine the pockets, holes, slots, angled faces, grooves, and edge treatments into that same solid
piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 95 mm x 85 mm x 42 mm.
- mounting hole pattern: Drill two through holes diameter 5 mm on the length centerline at X=17 mm and X=78 mm, Y=42 mm.
- functional center feature: Machine a central obround slot 31 mm long x 18 mm wide through the part, centered at X=47 mm, Y=42 mm.
- top relief pocket: Mill a rectangular relief pocket 25 mm x 28 mm x 12 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Jointer planer adjustable outfeed table hinge support'; this requirement is only for its chosen metal part.

---

## SMP-033-08 - Band saw lower wheel cover with dust port

Part name: Band saw lower wheel cover with dust port - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"length_mm": 145, "thickness_mm": 5, "width_mm": 105}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Band saw lower wheel cover with dust port'. The
broader use case is: A removable lower enclosure panel for a woodworking band saw. The chosen
deliverable is only the metal body implied by: Curved cover panel with recessed wheel bulge, latch
bosses, hinge tabs, and angled dust port. All other product elements are external reference items
and must not be modeled. The part must perform this mechanical role: Covers the lower wheel area,
provides access for blade changes, and connects to dust extraction near the lower guide path. It is
intentionally included in the SubCAD limit corpus because: Tests shallow domed surfaces, door-like
hardware, wheel clearance volumes, asymmetric ports, and cover-panel thickness. The part is made
from low-carbon steel, ASTM A36 or equivalent using sheet or plate stock. Start from one flat sheet
or plate blank. Cut the outside profile, machine holes, slots, pockets, lips, and relief features
into that same piece. If bends are called out, they are bends in the same sheet part, not separate
welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 145 mm x 105 mm x 5 mm.
- mounting hole pattern: Drill two through holes diameter 12 mm on the length centerline at X=21 mm and X=124 mm, Y=52 mm.
- functional center feature: Machine a central obround slot 48 mm long x 7 mm wide through the part, centered at X=72 mm, Y=52 mm.
- top relief pocket: Mill a rectangular relief pocket 36 mm x 35 mm x 1 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- machined angled reference face: Machine one top reference face at 40 degrees over the last 29 mm of length.

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
- Do not broaden the requirement back into the full product idea named 'Band saw lower wheel cover with dust port'; this requirement is only for its chosen metal part.

---

## SMP-033-09 - CNC router automatic tool setter puck mount

Part name: CNC router automatic tool setter puck mount - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 22, "length_mm": 100, "width_mm": 90}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'CNC router automatic tool setter puck mount'. The
broader use case is: A fixed probing accessory installed on a CNC router bed for measuring tool
length during woodworking jobs. The chosen deliverable is only the metal body implied by: Low-
profile puck holder with circular contact recess, cable strain relief, mounting ears, and protective
lip. All other product elements are external reference items and must not be modeled. The part must
perform this mechanical role: Presents a repeatable contact surface for the router bit and protects
probe wiring from chips and dust. It is intentionally included in the SubCAD limit corpus because:
Exercises small fixture geometry, concentric circular features, cable-routing detail, protected
contact zones, and mixed rounded and flat forms. The part is made from low-carbon steel, ASTM A36 or
equivalent using rectangular block stock. Start from one rectangular metal block or plate. Saw
oversize, face all datum sides, then machine the pockets, holes, slots, angled faces, grooves, and
edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 100 mm x 90 mm x 22 mm.
- mounting hole pattern: Drill two through holes diameter 7 mm on the length centerline at X=18 mm and X=82 mm, Y=45 mm.
- functional center feature: Machine a central obround slot 33 mm long x 15 mm wide through the part, centered at X=50 mm, Y=45 mm.
- top relief pocket: Mill a rectangular relief pocket 25 mm x 30 mm x 6 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'CNC router automatic tool setter puck mount'; this requirement is only for its chosen metal part.

---

## SMP-033-10 - Router table lift crank plate and motor clamp

Part name: Router table lift crank plate and motor clamp - single metal part

Material: 1045 medium-carbon steel, normalized (durable wear surface for workshop loading)

Envelope: `{"length_mm": 175, "thickness_mm": 3, "width_mm": 120}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Router table lift crank plate and motor clamp'. The
broader use case is: A lift mechanism installed under a router table to raise and lower a
woodworking router motor. The chosen deliverable is only the metal body implied by: Motor clamp ring
carried by a lift plate with guide posts, crank socket, and lead-screw support boss. All other
product elements are external reference items and must not be modeled. The part must perform this
mechanical role: Clamps the router motor and converts crank adjustment into controlled vertical
movement. It is intentionally included in the SubCAD limit corpus because: Tests split-ring clamp
intent, aligned guide structures, screw-driven motion features, circular motor clearance, and
layered mechanical packaging. The part is made from 1045 medium-carbon steel, normalized using sheet
or plate stock. Start from one flat sheet or plate blank. Cut the outside profile, machine holes,
slots, pockets, lips, and relief features into that same piece. If bends are called out, they are
bends in the same sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 175 mm x 120 mm x 3 mm.
- mounting hole pattern: Drill two through holes diameter 7 mm on the length centerline at X=24 mm and X=151 mm, Y=60 mm.
- functional center feature: Machine a central obround slot 58 mm long x 17 mm wide through the part, centered at X=87 mm, Y=60 mm.
- top relief pocket: Mill a rectangular relief pocket 43 mm x 40 mm x 1 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Router table lift crank plate and motor clamp'; this requirement is only for its chosen metal part.

---
