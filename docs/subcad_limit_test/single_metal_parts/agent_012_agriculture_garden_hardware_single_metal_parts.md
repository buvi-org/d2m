# Agent 012 Single Metal Part Requirements

Domain: agriculture, garden equipment, irrigation fittings, pruning tools, and small farm hardware

Each item below is one metal part only. Product assemblies and nonmetal components are explicitly out of scope.

## SMP-012-01 - Adjustable Drip-Line End Clamp

Part name: Adjustable Drip-Line End Clamp - single metal part

Material: 1045 medium-carbon steel, normalized (durable wear surface for workshop loading)

Envelope: `{"axial_bore_diameter_mm": 9, "outer_diameter_mm": 29, "overall_length_mm": 118, "wall_minimum_mm": 10}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Adjustable Drip-Line End Clamp'. The broader use
case is: Field irrigation systems that use flexible polyethylene drip tubing in vegetable beds or
orchards. The chosen deliverable is only the metal body implied by: Cam-lock clamp body with a
curved tube channel, hinge boss, latch hook, and thumb cam surface. All other product elements are
external reference items and must not be modeled. The part must perform this mechanical role:
Pinches and locks the open end of a drip line so the tube can be flushed, resealed, or reopened
without cutting. It is intentionally included in the SubCAD limit corpus because: Requires blended
cylindrical tube seating, asymmetric hinge geometry, latch clearances, cam contact surfaces, and
realistic wall thickness transitions. The part is made from 1045 medium-carbon steel, normalized
using round bar stock. Start from one cut length of round metal bar. Turn the outside, face both
ends, bore the center, then mill secondary flats, slots, and radial holes as needed. No separate
inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 29 mm and length 118 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 9 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 19 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 9 mm wide over 110 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M5 holes through the top flat at X=39 mm and X=78 mm.
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
- Do not broaden the requirement back into the full product idea named 'Adjustable Drip-Line End Clamp'; this requirement is only for its chosen metal part.

---

## SMP-012-02 - Pruning Shear Blade Pivot Carrier

Part name: Pruning Shear Blade Pivot Carrier - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 46, "length_mm": 145, "width_mm": 70}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Pruning Shear Blade Pivot Carrier'. The broader use
case is: Bypass pruning shears used for cutting stems, vines, and small branches. The chosen
deliverable is only the metal body implied by: Forged or machined pivot carrier half with blade
pocket, pivot boss, spring seat, and handle transition. All other product elements are external
reference items and must not be modeled. The part must perform this mechanical role: Holds the pivot
screw, supports the moving blade, and maintains blade alignment under cutting load. It is
intentionally included in the SubCAD limit corpus because: Combines organic ergonomic contours with
precise coaxial pivot features, recessed pockets, tapered ribs, and high-load filleted transitions.
The part is made from low-carbon steel, ASTM A36 or equivalent using rectangular block stock. Start
from one rectangular metal block or plate. Saw oversize, face all datum sides, then machine the
pockets, holes, slots, angled faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 145 mm x 70 mm x 46 mm.
- mounting hole pattern: Drill two through holes diameter 13 mm on the length centerline at X=14 mm and X=131 mm, Y=35 mm.
- functional center feature: Machine a central obround slot 48 mm long x 17 mm wide through the part, centered at X=72 mm, Y=35 mm.
- top relief pocket: Mill a rectangular relief pocket 36 mm x 23 mm x 13 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- machined angled reference face: Machine one top reference face at 12 degrees over the last 29 mm of length.

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
- Do not broaden the requirement back into the full product idea named 'Pruning Shear Blade Pivot Carrier'; this requirement is only for its chosen metal part.

---

## SMP-012-03 - Micro-Sprinkler Stake Head Adapter

Part name: Micro-Sprinkler Stake Head Adapter - single metal part

Material: 1045 medium-carbon steel, normalized (durable wear surface for workshop loading)

Envelope: `{"height_mm": 57, "length_mm": 155, "width_mm": 75}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Micro-Sprinkler Stake Head Adapter'. The broader
use case is: Low-pressure garden and greenhouse irrigation using small sprinkler heads mounted on
stakes. The chosen deliverable is only the metal body implied by: Compact adapter body with barb
inlet, stake socket, nozzle thread, and angled flow passage. All other product elements are external
reference items and must not be modeled. The part must perform this mechanical role: Connects a
vertical support stake, feed tube, and threaded sprinkler nozzle into one adjustable junction. It is
intentionally included in the SubCAD limit corpus because: Tests intersecting internal passages,
hose barb profiles, molded-looking external ribs, threaded cylindrical features, and angled
connector geometry. The part is made from 1045 medium-carbon steel, normalized using rectangular
block stock. Start from one rectangular metal block or plate. Saw oversize, face all datum sides,
then machine the pockets, holes, slots, angled faces, grooves, and edge treatments into that same
solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 155 mm x 75 mm x 57 mm.
- mounting hole pattern: Drill two through holes diameter 10 mm on the length centerline at X=15 mm and X=140 mm, Y=37 mm.
- functional center feature: Machine a central obround slot 51 mm long x 16 mm wide through the part, centered at X=77 mm, Y=37 mm.
- top relief pocket: Mill a rectangular relief pocket 38 mm x 25 mm x 1 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- machined angled reference face: Machine one top reference face at 35 degrees over the last 31 mm of length.
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
- Do not broaden the requirement back into the full product idea named 'Micro-Sprinkler Stake Head Adapter'; this requirement is only for its chosen metal part.

---

## SMP-012-04 - Seed Drill Metering Roller

Part name: Seed Drill Metering Roller - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 23, "outer_diameter_mm": 71, "overall_length_mm": 95, "wall_minimum_mm": 24}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Seed Drill Metering Roller'. The broader use case
is: Small manual or walk-behind seed drills for sowing vegetable seeds in rows. The chosen
deliverable is only the metal body implied by: Cylindrical metering roller with radial seed cells,
shaft bore, indexing groove, and end retention shoulder. All other product elements are external
reference items and must not be modeled. The part must perform this mechanical role: Meters seeds by
carrying them in repeated pockets from a hopper into the drop chute. It is intentionally included in
the SubCAD limit corpus because: Needs repeated patterned cavities on a curved surface, precise
angular spacing, pocket edge radii, shaft alignment, and manufacturable undercut-aware details. The
part is made from low-carbon steel, ASTM A36 or equivalent using round bar stock. Start from one cut
length of round metal bar. Turn the outside, face both ends, bore the center, then mill secondary
flats, slots, and radial holes as needed. No separate inserts or fasteners are part of the
deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 71 mm and length 95 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 23 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 33 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 23 mm wide over 87 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M6 holes through the top flat at X=31 mm and X=63 mm.
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
- Do not broaden the requirement back into the full product idea named 'Seed Drill Metering Roller'; this requirement is only for its chosen metal part.

---

## SMP-012-05 - Garden Hose Quick-Coupler Lock Sleeve

Part name: Garden Hose Quick-Coupler Lock Sleeve - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 20, "outer_diameter_mm": 81, "overall_length_mm": 107, "wall_minimum_mm": 30}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Garden Hose Quick-Coupler Lock Sleeve'. The broader
use case is: Reusable hose fittings for garden irrigation, washdown stations, and small farm water
lines. The chosen deliverable is only the metal body implied by: Cylindrical sliding sleeve with
grip knurling, internal retention groove, chamfered lead-in, and stop shoulder. All other product
elements are external reference items and must not be modeled. The part must perform this mechanical
role: Slides over a coupler body to retain locking balls or latch tabs around a mating plug. It is
intentionally included in the SubCAD limit corpus because: Tests concentric internal and external
features, fine grip texture, hidden groove representation, chamfer consistency, and functional
sliding clearances. The part is made from low-carbon steel, ASTM A36 or equivalent using round bar
stock. Start from one cut length of round metal bar. Turn the outside, face both ends, bore the
center, then mill secondary flats, slots, and radial holes as needed. No separate inserts or
fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 81 mm and length 107 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 20 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 30 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 27 mm wide over 99 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M7 holes through the top flat at X=35 mm and X=71 mm.
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
- Do not broaden the requirement back into the full product idea named 'Garden Hose Quick-Coupler Lock Sleeve'; this requirement is only for its chosen metal part.

---

## SMP-012-06 - Trellis Wire Tensioner Ratchet Wheel

Part name: Trellis Wire Tensioner Ratchet Wheel - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 17, "outer_diameter_mm": 69, "overall_length_mm": 114, "wall_minimum_mm": 26}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Trellis Wire Tensioner Ratchet Wheel'. The broader
use case is: Vineyard, orchard, and garden trellis systems where support wires need periodic
tensioning. The chosen deliverable is only the metal body implied by: Ratchet spool wheel with wire
slot, central square drive, toothed perimeter, and side flanges. All other product elements are
external reference items and must not be modeled. The part must perform this mechanical role: Winds
trellis wire and locks against reverse rotation using a pawl. It is intentionally included in the
SubCAD limit corpus because: Requires accurately repeated ratchet teeth, spool-like geometry, drive
socket detail, wire capture slots, and robust flange-to-hub transitions. The part is made from low-
carbon steel, ASTM A36 or equivalent using round bar stock. Start from one cut length of round metal
bar. Turn the outside, face both ends, bore the center, then mill secondary flats, slots, and radial
holes as needed. No separate inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 69 mm and length 114 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 17 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 27 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 23 mm wide over 106 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M8 holes through the top flat at X=38 mm and X=76 mm.
- split relief slit: Cut one full-length radial slit 4 mm wide from the outside to the axial bore on datum-B side.
- outside edge treatment: Break all outside circular edges with 1.0 mm chamfers and keep internal bore edges visibly chamfered.
- cross relief slot: Machine one transverse slot 6 mm wide across the top flat at X=57 mm, depth 6 mm.

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
- Do not broaden the requirement back into the full product idea named 'Trellis Wire Tensioner Ratchet Wheel'; this requirement is only for its chosen metal part.

---

## SMP-012-07 - Irrigation Filter Bowl Clamp Ring

Part name: Irrigation Filter Bowl Clamp Ring - single metal part

Material: 1045 medium-carbon steel, normalized (durable wear surface for workshop loading)

Envelope: `{"height_mm": 65, "length_mm": 105, "width_mm": 75}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Irrigation Filter Bowl Clamp Ring'. The broader use
case is: Inline mesh filters used before drip irrigation zones to protect emitters from sediment.
The chosen deliverable is only the metal body implied by: Split clamp ring with hinge lug, over-
center latch lug, seal compression face, and ribbed outer grip. All other product elements are
external reference items and must not be modeled. The part must perform this mechanical role:
Compresses and secures a removable filter bowl against the filter head seal. It is intentionally
included in the SubCAD limit corpus because: Tests split circular forms, hinge and latch alignment,
gasket compression surfaces, ribbed grip details, and nontrivial assembly clearance. The part is
made from 1045 medium-carbon steel, normalized using rectangular block stock. Start from one
rectangular metal block or plate. Saw oversize, face all datum sides, then machine the pockets,
holes, slots, angled faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 105 mm x 75 mm x 65 mm.
- mounting hole pattern: Drill two through holes diameter 8 mm on the length centerline at X=15 mm and X=90 mm, Y=37 mm.
- functional center feature: Machine a central obround slot 35 mm long x 18 mm wide through the part, centered at X=52 mm, Y=37 mm.
- top relief pocket: Mill a rectangular relief pocket 26 mm x 25 mm x 21 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Irrigation Filter Bowl Clamp Ring'; this requirement is only for its chosen metal part.

---

## SMP-012-08 - Cultivator Tine Mounting Socket

Part name: Cultivator Tine Mounting Socket - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 14, "outer_diameter_mm": 70, "overall_length_mm": 116, "wall_minimum_mm": 28}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Cultivator Tine Mounting Socket'. The broader use
case is: Small walk-behind cultivators or hand-pushed weeders with replaceable spring tines. The
chosen deliverable is only the metal body implied by: Angled socket block with tapered tine bore,
cross-pin hole, frame mounting bosses, and reinforcing web. All other product elements are external
reference items and must not be modeled. The part must perform this mechanical role: Receives and
locks a curved tine while transferring soil resistance loads into the frame. It is intentionally
included in the SubCAD limit corpus because: Combines angled bores, load-bearing gussets,
intersecting fastener holes, tapered retention geometry, and heavy fillets around stress paths. The
part is made from low-carbon steel, ASTM A36 or equivalent using round bar stock. Start from one cut
length of round metal bar. Turn the outside, face both ends, bore the center, then mill secondary
flats, slots, and radial holes as needed. No separate inserts or fasteners are part of the
deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 70 mm and length 116 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 14 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 24 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 23 mm wide over 108 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M5 holes through the top flat at X=38 mm and X=77 mm.
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
- Do not broaden the requirement back into the full product idea named 'Cultivator Tine Mounting Socket'; this requirement is only for its chosen metal part.

---

## SMP-012-09 - Grafting Knife Folding Lock Bar

Part name: Grafting Knife Folding Lock Bar - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 32, "length_mm": 120, "width_mm": 90}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Grafting Knife Folding Lock Bar'. The broader use
case is: Folding grafting knives used by nursery workers and orchard growers. The chosen deliverable
is only the metal body implied by: Thin spring lock bar with pivot hole, blade tang contact face,
thumb relief, and formed spring profile. All other product elements are external reference items and
must not be modeled. The part must perform this mechanical role: Locks the blade open while allowing
controlled release for folding. It is intentionally included in the SubCAD limit corpus because:
Challenges CAD representation with thin spring geometry, precise contact faces, small relief
cutouts, bend-like profiles, and tolerance-sensitive pivot spacing. The part is made from low-carbon
steel, ASTM A36 or equivalent using rectangular block stock. Start from one rectangular metal block
or plate. Saw oversize, face all datum sides, then machine the pockets, holes, slots, angled faces,
grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 120 mm x 90 mm x 32 mm.
- mounting hole pattern: Drill two through holes diameter 8 mm on the length centerline at X=18 mm and X=102 mm, Y=45 mm.
- functional center feature: Machine a central obround slot 40 mm long x 17 mm wide through the part, centered at X=60 mm, Y=45 mm.
- top relief pocket: Mill a rectangular relief pocket 30 mm x 30 mm x 11 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Grafting Knife Folding Lock Bar'; this requirement is only for its chosen metal part.

---

## SMP-012-10 - Rain Barrel Spigot Bulkhead Nut

Part name: Rain Barrel Spigot Bulkhead Nut - single metal part

Material: 1045 medium-carbon steel, normalized (durable wear surface for workshop loading)

Envelope: `{"height_mm": 57, "length_mm": 205, "width_mm": 60}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Rain Barrel Spigot Bulkhead Nut'. The broader use
case is: Garden rainwater harvesting barrels fitted with low-pressure spigots and hose outlets. The
chosen deliverable is only the metal body implied by: Large internally threaded bulkhead nut with
scalloped grip perimeter, gasket seat, barrel-wall relief face, and lead-in chamfer. All other
product elements are external reference items and must not be modeled. The part must perform this
mechanical role: Clamps a spigot fitting through a curved plastic barrel wall while compressing a
gasket. It is intentionally included in the SubCAD limit corpus because: Tests large thread-like
cylindrical detail, ergonomic scalloped edges, sealing faces, curvature-aware mounting context, and
realistic compression hardware geometry. The part is made from 1045 medium-carbon steel, normalized
using rectangular block stock. Start from one rectangular metal block or plate. Saw oversize, face
all datum sides, then machine the pockets, holes, slots, angled faces, grooves, and edge treatments
into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 205 mm x 60 mm x 57 mm.
- mounting hole pattern: Drill two through holes diameter 12 mm on the length centerline at X=12 mm and X=193 mm, Y=30 mm.
- functional center feature: Machine a central obround slot 68 mm long x 17 mm wide through the part, centered at X=102 mm, Y=30 mm.
- top relief pocket: Mill a rectangular relief pocket 51 mm x 20 mm x 4 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
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
- Do not broaden the requirement back into the full product idea named 'Rain Barrel Spigot Bulkhead Nut'; this requirement is only for its chosen metal part.

---
