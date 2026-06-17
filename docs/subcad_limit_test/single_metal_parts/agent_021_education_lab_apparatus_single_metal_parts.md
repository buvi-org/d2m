# Agent 021 Single Metal Part Requirements

Domain: education lab apparatus, physics demos, STEM kits, classroom mechanisms, and training fixtures

Each item below is one metal part only. Product assemblies and nonmetal components are explicitly out of scope.

## SMP-021-01 - Adjustable Inclined Plane Hinge Block

Part name: Adjustable Inclined Plane Hinge Block - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"length_mm": 165, "thickness_mm": 9, "width_mm": 100}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Adjustable Inclined Plane Hinge Block'. The broader
use case is: Classroom mechanics apparatus for demonstrating friction, acceleration, and component
resolution on slopes. The chosen deliverable is only the metal body implied by: Machined hinge-and-
indexing side bracket with angle detents and a pivot bore. All other product elements are external
reference items and must not be modeled. The part must perform this mechanical role: Allows a ramp
to pivot and lock at repeatable angles for physics experiments. It is intentionally included in the
SubCAD limit corpus because: Requires representing coaxial hinge geometry, radial detent patterns,
angular references, clearance slots, and structurally meaningful mounting features. The part is made
from low-carbon steel, ASTM A36 or equivalent using sheet or plate stock. Start from one flat sheet
or plate blank. Cut the outside profile, machine holes, slots, pockets, lips, and relief features
into that same piece. If bends are called out, they are bends in the same sheet part, not separate
welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 165 mm x 100 mm x 9 mm.
- mounting hole pattern: Drill two through holes diameter 6 mm on the length centerline at X=20 mm and X=145 mm, Y=50 mm.
- functional center feature: Machine a central obround slot 55 mm long x 15 mm wide through the part, centered at X=82 mm, Y=50 mm.
- top relief pocket: Mill a rectangular relief pocket 41 mm x 33 mm x 2 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- machined angled reference face: Machine one top reference face at 15 degrees over the last 33 mm of length.

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
- Do not broaden the requirement back into the full product idea named 'Adjustable Inclined Plane Hinge Block'; this requirement is only for its chosen metal part.

---

## SMP-021-02 - Projectile Launcher Elevation Quadrant

Part name: Projectile Launcher Elevation Quadrant - single metal part

Material: AISI 316 stainless steel (corrosion resistance and cleanable metal surfaces)

Envelope: `{"length_mm": 190, "thickness_mm": 9, "width_mm": 70}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Projectile Launcher Elevation Quadrant'. The
broader use case is: Physics lab projectile-motion demonstrator used to set launch angle and compare
measured range against theory. The chosen deliverable is only the metal body implied by: Curved
quadrant plate with pivot hole, degree scale region, arced locking slot, and mounting bosses. All
other product elements are external reference items and must not be modeled. The part must perform
this mechanical role: Provides precise elevation adjustment and locking for a spring or pneumatic
projectile launcher. It is intentionally included in the SubCAD limit corpus because: Tests curved
profiles, concentric arcs, angular slots, hole patterns on radial layouts, and mixed cosmetic versus
functional surfaces. The part is made from AISI 316 stainless steel using sheet or plate stock.
Start from one flat sheet or plate blank. Cut the outside profile, machine holes, slots, pockets,
lips, and relief features into that same piece. If bends are called out, they are bends in the same
sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 190 mm x 70 mm x 9 mm.
- mounting hole pattern: Drill two through holes diameter 9 mm on the length centerline at X=14 mm and X=176 mm, Y=35 mm.
- functional center feature: Machine a central obround slot 63 mm long x 13 mm wide through the part, centered at X=95 mm, Y=35 mm.
- top relief pocket: Mill a rectangular relief pocket 47 mm x 23 mm x 2 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Projectile Launcher Elevation Quadrant'; this requirement is only for its chosen metal part.

---

## SMP-021-03 - Optical Bench Lens Carrier

Part name: Optical Bench Lens Carrier - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 19, "length_mm": 185, "width_mm": 90}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Optical Bench Lens Carrier'. The broader use case
is: STEM optics kit for teaching focal length, image formation, and ray diagrams. The chosen
deliverable is only the metal body implied by: Machined sliding carriage with rail groove, vertical
post socket, clamp screw bore, and lens-retainer frame. All other product elements are external
reference items and must not be modeled. The part must perform this mechanical role: Holds a lens
upright while sliding along a rail and allowing height adjustment. It is intentionally included in
the SubCAD limit corpus because: Combines precision rail-fit features, vertical datum relationships,
circular optical openings, thin retaining lips, and screw-access clearances. The part is made from
low-carbon steel, ASTM A36 or equivalent using rectangular block stock. Start from one rectangular
metal block or plate. Saw oversize, face all datum sides, then machine the pockets, holes, slots,
angled faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 185 mm x 90 mm x 19 mm.
- mounting hole pattern: Drill two through holes diameter 5 mm on the length centerline at X=18 mm and X=167 mm, Y=45 mm.
- functional center feature: Machine a central obround slot 61 mm long x 17 mm wide through the part, centered at X=92 mm, Y=45 mm.
- top relief pocket: Mill a rectangular relief pocket 46 mm x 30 mm x 1 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Optical Bench Lens Carrier'; this requirement is only for its chosen metal part.

---

## SMP-021-04 - Pendulum Length Adjustment Clamp

Part name: Pendulum Length Adjustment Clamp - single metal part

Material: 1045 medium-carbon steel, normalized (durable wear surface for workshop loading)

Envelope: `{"axial_bore_diameter_mm": 21, "outer_diameter_mm": 63, "overall_length_mm": 24, "wall_minimum_mm": 21}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Pendulum Length Adjustment Clamp'. The broader use
case is: Classroom pendulum apparatus for studying period, amplitude, and gravitational
acceleration. The chosen deliverable is only the metal body implied by: Compact clamp block with
pivot eye, split clamping channel, scale pointer boss, and fastener holes. All other product
elements are external reference items and must not be modeled. The part must perform this mechanical
role: Locks a pendulum string or rod at a selectable length without disturbing the pivot alignment.
It is intentionally included in the SubCAD limit corpus because: Tests small mechanical clearances,
split-body geometry, aligned holes, nested channels, and datum-sensitive features. The part is made
from 1045 medium-carbon steel, normalized using round bar stock. Start from one cut length of round
metal bar. Turn the outside, face both ends, bore the center, then mill secondary flats, slots, and
radial holes as needed. No separate inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 63 mm and length 24 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 21 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 31 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 21 mm wide over 16 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M6 holes through the top flat at X=8 mm and X=16 mm.
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
- Do not broaden the requirement back into the full product idea named 'Pendulum Length Adjustment Clamp'; this requirement is only for its chosen metal part.

---

## SMP-021-05 - Force Table Pulley Mount

Part name: Force Table Pulley Mount - single metal part

Material: AISI 316 stainless steel (corrosion resistance and cleanable metal surfaces)

Envelope: `{"axial_bore_diameter_mm": 15, "outer_diameter_mm": 75, "overall_length_mm": 59, "wall_minimum_mm": 30}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Force Table Pulley Mount'. The broader use case is:
Vector addition and equilibrium lab apparatus used with hanging masses and strings. The chosen
deliverable is only the metal body implied by: Edge-clamping pulley bracket with curved table
contact face, pulley axle boss, and thumb-screw clamp feature. All other product elements are
external reference items and must not be modeled. The part must perform this mechanical role:
Positions a pulley around the edge of a circular force table at selectable angular locations. It is
intentionally included in the SubCAD limit corpus because: Requires curved mating surfaces, offset
axle geometry, clamp mechanics, load-bearing bosses, and asymmetric bracket shapes. The part is made
from AISI 316 stainless steel using round bar stock. Start from one cut length of round metal bar.
Turn the outside, face both ends, bore the center, then mill secondary flats, slots, and radial
holes as needed. No separate inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 75 mm and length 59 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 15 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 25 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 25 mm wide over 51 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M7 holes through the top flat at X=19 mm and X=39 mm.
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
- Do not broaden the requirement back into the full product idea named 'Force Table Pulley Mount'; this requirement is only for its chosen metal part.

---

## SMP-021-06 - Training Gear Pair Alignment Fixture

Part name: Training Gear Pair Alignment Fixture - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"length_mm": 145, "thickness_mm": 6, "width_mm": 130}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Training Gear Pair Alignment Fixture'. The broader
use case is: Mechanical STEM kit for demonstrating gear ratio, backlash, and center-distance
effects. The chosen deliverable is only the metal body implied by: Slotted base plate with parallel
adjustment tracks, bearing pockets, reference marks, and mounting holes. All other product elements
are external reference items and must not be modeled. The part must perform this mechanical role:
Holds two interchangeable gears at controlled center distances for classroom demonstrations. It is
intentionally included in the SubCAD limit corpus because: Tests repeated slots, bearing seats,
center-distance constraints, symmetrical layouts, and features that imply assembly motion. The part
is made from low-carbon steel, ASTM A36 or equivalent using sheet or plate stock. Start from one
flat sheet or plate blank. Cut the outside profile, machine holes, slots, pockets, lips, and relief
features into that same piece. If bends are called out, they are bends in the same sheet part, not
separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 145 mm x 130 mm x 6 mm.
- mounting hole pattern: Drill two through holes diameter 11 mm on the length centerline at X=26 mm and X=119 mm, Y=65 mm.
- functional center feature: Machine a central obround slot 48 mm long x 7 mm wide through the part, centered at X=72 mm, Y=65 mm.
- top relief pocket: Mill a rectangular relief pocket 36 mm x 43 mm x 1 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Training Gear Pair Alignment Fixture'; this requirement is only for its chosen metal part.

---

## SMP-021-07 - Cam Profile Demonstration Follower Guide

Part name: Cam Profile Demonstration Follower Guide - single metal part

Material: 4140 alloy steel, prehard (strong cylindrical metal part with threaded and slotted details)

Envelope: `{"axial_bore_diameter_mm": 15, "outer_diameter_mm": 77, "overall_length_mm": 44, "wall_minimum_mm": 31}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Cam Profile Demonstration Follower Guide'. The
broader use case is: Mechanisms teaching fixture for showing how cam shapes convert rotation into
reciprocating motion. The chosen deliverable is only the metal body implied by: Machined follower
guide block with vertical slide channel, cam clearance window, roller axle bore, and mounting
flange. All other product elements are external reference items and must not be modeled. The part
must perform this mechanical role: Constrains a follower so students can observe displacement
generated by different cam profiles. It is intentionally included in the SubCAD limit corpus
because: Combines enclosed channels, open windows, bearing bores, sliding clearances, and
mechanically meaningful internal cutouts. The part is made from 4140 alloy steel, prehard using
round bar stock. Start from one cut length of round metal bar. Turn the outside, face both ends,
bore the center, then mill secondary flats, slots, and radial holes as needed. No separate inserts
or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 77 mm and length 44 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 15 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 25 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 25 mm wide over 36 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M4 holes through the top flat at X=14 mm and X=29 mm.
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
- Do not broaden the requirement back into the full product idea named 'Cam Profile Demonstration Follower Guide'; this requirement is only for its chosen metal part.

---

## SMP-021-08 - Resonance Beam Clamp Support

Part name: Resonance Beam Clamp Support - single metal part

Material: 1045 medium-carbon steel, normalized (durable wear surface for workshop loading)

Envelope: `{"height_mm": 58, "length_mm": 115, "width_mm": 95}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Resonance Beam Clamp Support'. The broader use case
is: Physics demonstration kit for vibration, resonance, and cantilever beam experiments. The chosen
deliverable is only the metal body implied by: Heavy clamp support block with stepped beam pocket,
pressure-pad recess, clamp screw holes, and bench-mounting slots. All other product elements are
external reference items and must not be modeled. The part must perform this mechanical role:
Rigidly clamps a beam specimen while allowing repeatable overhang length adjustment. It is
intentionally included in the SubCAD limit corpus because: Tests stepped pockets, clamping geometry,
load-path-aware massing, long slots, and relationships between flat reference surfaces. The part is
made from 1045 medium-carbon steel, normalized using rectangular block stock. Start from one
rectangular metal block or plate. Saw oversize, face all datum sides, then machine the pockets,
holes, slots, angled faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 115 mm x 95 mm x 58 mm.
- mounting hole pattern: Drill two through holes diameter 10 mm on the length centerline at X=19 mm and X=96 mm, Y=47 mm.
- functional center feature: Machine a central obround slot 38 mm long x 8 mm wide through the part, centered at X=57 mm, Y=47 mm.
- top relief pocket: Mill a rectangular relief pocket 28 mm x 31 mm x 8 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- serrated contact edge: Cut 10 equal triangular serrations across the rear edge, each 5 mm deep.
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
- Do not broaden the requirement back into the full product idea named 'Resonance Beam Clamp Support'; this requirement is only for its chosen metal part.

---

## SMP-021-09 - Magnetic Field Coil Stand Bracket

Part name: Magnetic Field Coil Stand Bracket - single metal part

Material: AISI 316 stainless steel (corrosion resistance and cleanable metal surfaces)

Envelope: `{"length_mm": 245, "thickness_mm": 8, "width_mm": 115}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Magnetic Field Coil Stand Bracket'. The broader use
case is: Electromagnetism lab apparatus for positioning coils, Hall probes, or compass cards. The
chosen deliverable is only the metal body implied by: U-shaped coil support bracket with circular
cradle, cable relief channel, base mounting holes, and vertical gussets. All other product elements
are external reference items and must not be modeled. The part must perform this mechanical role:
Supports a circular coil at a defined height and orientation while leaving the field region
accessible. It is intentionally included in the SubCAD limit corpus because: Requires partial
circular supports, open-frame geometry, cable-management features, gussets, and orientation-critical
mounting planes. The part is made from AISI 316 stainless steel using sheet or plate stock. Start
from one flat sheet or plate blank. Cut the outside profile, machine holes, slots, pockets, lips,
and relief features into that same piece. If bends are called out, they are bends in the same sheet
part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 245 mm x 115 mm x 8 mm.
- mounting hole pattern: Drill two through holes diameter 12 mm on the length centerline at X=23 mm and X=222 mm, Y=57 mm.
- functional center feature: Machine a central obround slot 81 mm long x 12 mm wide through the part, centered at X=122 mm, Y=57 mm.
- top relief pocket: Mill a rectangular relief pocket 61 mm x 38 mm x 4 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Magnetic Field Coil Stand Bracket'; this requirement is only for its chosen metal part.

---

## SMP-021-10 - Hydraulic Pascal Press Demonstrator Frame

Part name: Hydraulic Pascal Press Demonstrator Frame - single metal part

Material: 1045 medium-carbon steel, normalized (durable wear surface for workshop loading)

Envelope: `{"axial_bore_diameter_mm": 14, "outer_diameter_mm": 57, "overall_length_mm": 119, "wall_minimum_mm": 21}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Hydraulic Pascal Press Demonstrator Frame'. The
broader use case is: Classroom fluid mechanics fixture for demonstrating pressure multiplication and
force transmission. The chosen deliverable is only the metal body implied by: Machined frame side
plate with dual cylinder saddles, linkage pivot holes, spacer bosses, and base slots. All other
product elements are external reference items and must not be modeled. The part must perform this
mechanical role: Holds two syringe or piston cylinders in aligned positions while supporting a small
load platform. It is intentionally included in the SubCAD limit corpus because: Tests multi-axis
alignment, repeated but differently sized circular seats, structural side-plate profiling, pivot
relationships, and assembly-driven clearances. The part is made from 1045 medium-carbon steel,
normalized using round bar stock. Start from one cut length of round metal bar. Turn the outside,
face both ends, bore the center, then mill secondary flats, slots, and radial holes as needed. No
separate inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 57 mm and length 119 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 14 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 24 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 19 mm wide over 111 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M7 holes through the top flat at X=39 mm and X=79 mm.
- split relief slit: Cut one full-length radial slit 5 mm wide from the outside to the axial bore on datum-B side.
- outside edge treatment: Break all outside circular edges with 1.0 mm chamfers and keep internal bore edges visibly chamfered.
- cross relief slot: Machine one transverse slot 7 mm wide across the top flat at X=59 mm, depth 5 mm.

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
- Do not broaden the requirement back into the full product idea named 'Hydraulic Pascal Press Demonstrator Frame'; this requirement is only for its chosen metal part.

---
