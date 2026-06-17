# Agent 030 Single Metal Part Requirements

Domain: home appliance repair hardware, washing-machine/dryer fixtures, refrigerator mechanisms, dishwasher parts, and service alignment tools

Each item below is one metal part only. Product assemblies and nonmetal components are explicitly out of scope.

## SMP-030-01 - Washing Machine Drum Spider Arm Replacement Hub

Part name: Washing Machine Drum Spider Arm Replacement Hub - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 58, "length_mm": 215, "width_mm": 55}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Washing Machine Drum Spider Arm Replacement Hub'.
The broader use case is: Front-load washing machines use a cast metal spider assembly to connect the
drum to the drive shaft and support high-speed spin loads. The chosen deliverable is only the metal
body implied by: Three-arm radial hub with central splined bore, raised bearing land, ribbed arms,
and bolt bosses at each arm end. All other product elements are external reference items and must
not be modeled. The part must perform this mechanical role: Transmit torque from the drive shaft to
the drum while keeping the drum centered under wet laundry imbalance. It is intentionally included
in the SubCAD limit corpus because: Combines radial symmetry, tapered organic arms, filleted ribs,
coaxial bores, bolt patterns, and nonuniform boss geometry in one machined part. The part is made
from low-carbon steel, ASTM A36 or equivalent using rectangular block stock. Start from one
rectangular metal block or plate. Saw oversize, face all datum sides, then machine the pockets,
holes, slots, angled faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 215 mm x 55 mm x 58 mm.
- mounting hole pattern: Drill two through holes diameter 8 mm on the length centerline at X=11 mm and X=204 mm, Y=27 mm.
- functional center feature: Machine a central obround slot 71 mm long x 13 mm wide through the part, centered at X=107 mm, Y=27 mm.
- top relief pocket: Mill a rectangular relief pocket 53 mm x 18 mm x 6 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- machined angled reference face: Machine one top reference face at 24 degrees over the last 43 mm of length.

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
- Do not broaden the requirement back into the full product idea named 'Washing Machine Drum Spider Arm Replacement Hub'; this requirement is only for its chosen metal part.

---

## SMP-030-02 - Dryer Idler Pulley Tension Bracket

Part name: Dryer Idler Pulley Tension Bracket - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"length_mm": 185, "thickness_mm": 6, "width_mm": 105}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Dryer Idler Pulley Tension Bracket'. The broader
use case is: Belt-driven clothes dryers use an idler pulley bracket to maintain belt tension against
the rotating drum. The chosen deliverable is only the metal body implied by: Bent plate-style
bracket with pivot hole, pulley axle boss, spring hook tab, reinforcing flange, and slotted mounting
hole. All other product elements are external reference items and must not be modeled. The part must
perform this mechanical role: Hold a pulley axle at a precise offset while allowing spring-loaded
belt tensioning. It is intentionally included in the SubCAD limit corpus because: Requires flat
plate features, bends or stepped offsets, asymmetric holes, tab details, slots, and load-bearing
bosses with clear mechanical relationships. The part is made from low-carbon steel, ASTM A36 or
equivalent using sheet or plate stock. Start from one flat sheet or plate blank. Cut the outside
profile, machine holes, slots, pockets, lips, and relief features into that same piece. If bends are
called out, they are bends in the same sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 185 mm x 105 mm x 6 mm.
- mounting hole pattern: Drill two through holes diameter 10 mm on the length centerline at X=21 mm and X=164 mm, Y=52 mm.
- functional center feature: Machine a central obround slot 61 mm long x 16 mm wide through the part, centered at X=92 mm, Y=52 mm.
- top relief pocket: Mill a rectangular relief pocket 46 mm x 35 mm x 1 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- serrated contact edge: Cut 9 equal triangular serrations across the rear edge, each 5 mm deep.
- integral hook lip: Leave an integral hook lip on one short end, projecting 10 mm and undercut 4 mm for registration.

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
- The feature named 'integral hook lip' is present with the stated size and position.
- All required chamfers, reliefs, and edge treatments are visible in STEP and STL outputs.
- No extra parts, fasteners, hardware, labels, cosmetic meshes, or nonmetal components are present.
- Flat datums remain planar and usable; pockets or slots do not accidentally break unsupported walls.

Negative requirements:
- Represent exactly one metal part only.
- Do not model screws, nuts, springs, bushings, bearings, rubber pads, plastic covers, electronics, labels, handles, knobs, adhesives, weld beads, or separate inserts.
- Do not convert the part into an assembly or multiple bodies.
- Do not replace through holes, slots, pockets, grooves, flats, tapers, or chamfers with cosmetic markings.
- Do not omit datum-critical features just because they are small.
- Do not broaden the requirement back into the full product idea named 'Dryer Idler Pulley Tension Bracket'; this requirement is only for its chosen metal part.

---

## SMP-030-03 - Refrigerator Door Hinge Cam Lift Block

Part name: Refrigerator Door Hinge Cam Lift Block - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 14, "outer_diameter_mm": 74, "overall_length_mm": 101, "wall_minimum_mm": 30}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Refrigerator Door Hinge Cam Lift Block'. The
broader use case is: Many refrigerator doors use hinge cams to lift and self-close the door during
the final swing angle. The chosen deliverable is only the metal body implied by: Cylindrical hinge
insert with spiral ramp surface, central pivot bore, keyed anti-rotation notch, and wear pads. All
other product elements are external reference items and must not be modeled. The part must perform
this mechanical role: Create a controlled rising cam path that helps the door close and compress the
gasket evenly. It is intentionally included in the SubCAD limit corpus because: Challenges CAD
representation with helical or ramped cam geometry, coaxial features, keyed cutouts, contact
surfaces, and precise angular transitions. The part is made from low-carbon steel, ASTM A36 or
equivalent using round bar stock. Start from one cut length of round metal bar. Turn the outside,
face both ends, bore the center, then mill secondary flats, slots, and radial holes as needed. No
separate inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 74 mm and length 101 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 14 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 24 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 24 mm wide over 93 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M4 holes through the top flat at X=33 mm and X=67 mm.
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
- Do not broaden the requirement back into the full product idea named 'Refrigerator Door Hinge Cam Lift Block'; this requirement is only for its chosen metal part.

---

## SMP-030-04 - Dishwasher Upper Rack Height Adjuster Rail Block

Part name: Dishwasher Upper Rack Height Adjuster Rail Block - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 18, "outer_diameter_mm": 56, "overall_length_mm": 73, "wall_minimum_mm": 19}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Dishwasher Upper Rack Height Adjuster Rail Block'.
The broader use case is: Adjustable dishwasher racks use sliding blocks and detents to raise or
lower the upper rack for tall dishes. The chosen deliverable is only the metal body implied by:
Molded or machined guide block with vertical channel, detent pockets, latch window, roller pin
holes, and rail engagement ribs. All other product elements are external reference items and must
not be modeled. The part must perform this mechanical role: Guide the rack support through multiple
height positions and lock it into stable detent stops. It is intentionally included in the SubCAD
limit corpus because: Includes nested channels, repeated detent forms, thin ribs, through-holes,
rectangular cutouts, and features that must align on multiple faces. The part is made from low-
carbon steel, ASTM A36 or equivalent using round bar stock. Start from one cut length of round metal
bar. Turn the outside, face both ends, bore the center, then mill secondary flats, slots, and radial
holes as needed. No separate inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 56 mm and length 73 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 18 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 28 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 18 mm wide over 65 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M7 holes through the top flat at X=24 mm and X=48 mm.
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
- Do not broaden the requirement back into the full product idea named 'Dishwasher Upper Rack Height Adjuster Rail Block'; this requirement is only for its chosen metal part.

---

## SMP-030-05 - Washing Machine Motor Alignment Shim Gauge

Part name: Washing Machine Motor Alignment Shim Gauge - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"length_mm": 185, "thickness_mm": 9, "width_mm": 140}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Washing Machine Motor Alignment Shim Gauge'. The
broader use case is: Service technicians need alignment tools when replacing belt-drive motors or
adjusting pulley tracking in washers. The chosen deliverable is only the metal body implied by:
Stepped gauge plate with reference ledges, offset measurement fingers, elongated bolt clearance
slots, and engraved depth marks. All other product elements are external reference items and must
not be modeled. The part must perform this mechanical role: Set the motor mounting height and pulley
offset relative to the drum pulley during service. It is intentionally included in the SubCAD limit
corpus because: Tests stepped planar geometry, thin precision fingers, slot placement, measurement
references, chamfers, and dimensional intent across multiple offsets. The part is made from low-
carbon steel, ASTM A36 or equivalent using sheet or plate stock. Start from one flat sheet or plate
blank. Cut the outside profile, machine holes, slots, pockets, lips, and relief features into that
same piece. If bends are called out, they are bends in the same sheet part, not separate welded
pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 185 mm x 140 mm x 9 mm.
- mounting hole pattern: Drill two through holes diameter 7 mm on the length centerline at X=28 mm and X=157 mm, Y=70 mm.
- functional center feature: Machine a central obround slot 61 mm long x 8 mm wide through the part, centered at X=92 mm, Y=70 mm.
- top relief pocket: Mill a rectangular relief pocket 46 mm x 46 mm x 3 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- serrated contact edge: Cut 9 equal triangular serrations across the rear edge, each 2 mm deep.

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
- Do not broaden the requirement back into the full product idea named 'Washing Machine Motor Alignment Shim Gauge'; this requirement is only for its chosen metal part.

---

## SMP-030-06 - Refrigerator Ice Maker Ejector Shaft Coupler

Part name: Refrigerator Ice Maker Ejector Shaft Coupler - single metal part

Material: 4140 alloy steel, prehard (strong cylindrical metal part with threaded and slotted details)

Envelope: `{"axial_bore_diameter_mm": 19, "outer_diameter_mm": 76, "overall_length_mm": 59, "wall_minimum_mm": 28}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Refrigerator Ice Maker Ejector Shaft Coupler'. The
broader use case is: Automatic ice makers use a rotating ejector shaft to push formed cubes from the
tray into the bin. The chosen deliverable is only the metal body implied by: Short cylindrical
coupler with D-bore on one side, cross-slot socket on the other, retaining groove, and flexible
relief cuts. All other product elements are external reference items and must not be modeled. The
part must perform this mechanical role: Couple a small drive motor output to the ejector shaft while
absorbing minor misalignment. It is intentionally included in the SubCAD limit corpus because:
Combines two different internal drive profiles, grooves, relief slots, concentric cylinders, and
small toleranced coupling features. The part is made from 4140 alloy steel, prehard using round bar
stock. Start from one cut length of round metal bar. Turn the outside, face both ends, bore the
center, then mill secondary flats, slots, and radial holes as needed. No separate inserts or
fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 76 mm and length 59 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 19 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 29 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 25 mm wide over 51 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M4 holes through the top flat at X=19 mm and X=39 mm.
- split relief slit: Cut one full-length radial slit 2 mm wide from the outside to the axial bore on datum-B side.
- outside edge treatment: Break all outside circular edges with 1.0 mm chamfers and keep internal bore edges visibly chamfered.
- cross relief slot: Machine one transverse slot 4 mm wide across the top flat at X=29 mm, depth 7 mm.

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
- Do not broaden the requirement back into the full product idea named 'Refrigerator Ice Maker Ejector Shaft Coupler'; this requirement is only for its chosen metal part.

---

## SMP-030-07 - Dishwasher Spray Arm Bearing Turret

Part name: Dishwasher Spray Arm Bearing Turret - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 8, "outer_diameter_mm": 28, "overall_length_mm": 95, "wall_minimum_mm": 10}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Dishwasher Spray Arm Bearing Turret'. The broader
use case is: Rotating dishwasher spray arms ride on a central turret that feeds water while allowing
low-friction rotation. The chosen deliverable is only the metal body implied by: Vertical turret
fitting with stepped cylindrical body, central water bore, radial outlet ports, snap-ring groove,
and flange base. All other product elements are external reference items and must not be modeled.
The part must perform this mechanical role: Support the spray arm, seal the water path, and provide
a bearing surface for smooth rotation. It is intentionally included in the SubCAD limit corpus
because: Requires coaxial stepped solids, internal flow passages, radial holes intersecting a
central bore, retaining grooves, and seal-seat geometry. The part is made from low-carbon steel,
ASTM A36 or equivalent using round bar stock. Start from one cut length of round metal bar. Turn the
outside, face both ends, bore the center, then mill secondary flats, slots, and radial holes as
needed. No separate inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 28 mm and length 95 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 8 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 18 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 9 mm wide over 87 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M6 holes through the top flat at X=31 mm and X=63 mm.
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
- Do not broaden the requirement back into the full product idea named 'Dishwasher Spray Arm Bearing Turret'; this requirement is only for its chosen metal part.

---

## SMP-030-08 - Dryer Drum Roller Axle Support Bracket

Part name: Dryer Drum Roller Axle Support Bracket - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 23, "outer_diameter_mm": 69, "overall_length_mm": 43, "wall_minimum_mm": 23}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Dryer Drum Roller Axle Support Bracket'. The
broader use case is: Clothes dryer drums are supported by rollers mounted to brackets inside the
cabinet. The chosen deliverable is only the metal body implied by: Stamped-style support bracket
with upright axle boss, triangular gussets, base mounting slots, locating tabs, and raised embosses.
All other product elements are external reference items and must not be modeled. The part must
perform this mechanical role: Hold the roller axle square to the drum path while resisting vibration
and thermal cycling. It is intentionally included in the SubCAD limit corpus because: Tests angled
gussets, bosses rising from sheet-like geometry, slots, tabs, emboss-like raised areas, and
relationships between thin and thick features. The part is made from low-carbon steel, ASTM A36 or
equivalent using round bar stock. Start from one cut length of round metal bar. Turn the outside,
face both ends, bore the center, then mill secondary flats, slots, and radial holes as needed. No
separate inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 69 mm and length 43 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 23 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 33 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 23 mm wide over 35 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M7 holes through the top flat at X=14 mm and X=28 mm.
- split relief slit: Cut one full-length radial slit 3 mm wide from the outside to the axial bore on datum-B side.
- outside edge treatment: Break all outside circular edges with 1.0 mm chamfers and keep internal bore edges visibly chamfered.
- cross relief slot: Machine one transverse slot 5 mm wide across the top flat at X=21 mm, depth 6 mm.

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
- Do not broaden the requirement back into the full product idea named 'Dryer Drum Roller Axle Support Bracket'; this requirement is only for its chosen metal part.

---

## SMP-030-09 - Washer Suspension Rod Calibration Clamp

Part name: Washer Suspension Rod Calibration Clamp - single metal part

Material: 1045 medium-carbon steel, normalized (durable wear surface for workshop loading)

Envelope: `{"axial_bore_diameter_mm": 17, "outer_diameter_mm": 87, "overall_length_mm": 84, "wall_minimum_mm": 35}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Washer Suspension Rod Calibration Clamp'. The
broader use case is: Top-load washers use suspension rods and springs that may need service
alignment after tub or rod replacement. The chosen deliverable is only the metal body implied by:
Split collar clamp with semicircular bore, hinge knuckle, screw boss, height reference stop, and
anti-slip inner ridges. All other product elements are external reference items and must not be
modeled. The part must perform this mechanical role: Clamp around a suspension rod to hold a
temporary calibration height while springs are checked or replaced. It is intentionally included in
the SubCAD limit corpus because: Includes split circular geometry, hinge barrels, screw clearance
and threaded boss regions, small internal ridges, and asymmetric clamp details. The part is made
from 1045 medium-carbon steel, normalized using round bar stock. Start from one cut length of round
metal bar. Turn the outside, face both ends, bore the center, then mill secondary flats, slots, and
radial holes as needed. No separate inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 87 mm and length 84 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 17 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 27 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 29 mm wide over 76 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M4 holes through the top flat at X=28 mm and X=56 mm.
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
- Do not broaden the requirement back into the full product idea named 'Washer Suspension Rod Calibration Clamp'; this requirement is only for its chosen metal part.

---

## SMP-030-10 - Refrigerator Compressor Foot Leveling Spacer

Part name: Refrigerator Compressor Foot Leveling Spacer - single metal part

Material: 1045 medium-carbon steel, normalized (durable wear surface for workshop loading)

Envelope: `{"axial_bore_diameter_mm": 12, "outer_diameter_mm": 49, "overall_length_mm": 41, "wall_minimum_mm": 18}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Refrigerator Compressor Foot Leveling Spacer'. The
broader use case is: Replacement refrigerator compressors often need vibration-isolating spacers or
adapters to match cabinet mounting holes. The chosen deliverable is only the metal body implied by:
Low rectangular spacer block with raised circular grommet seat, countersunk mounting hole, offset
locating pin, and underside relief pocket. All other product elements are external reference items
and must not be modeled. The part must perform this mechanical role: Adapt compressor foot geometry
to the cabinet base while maintaining level height and rubber grommet compression. It is
intentionally included in the SubCAD limit corpus because: Tests mixed prismatic and cylindrical
features, countersinks, offset pins, underside pockets, filleted load surfaces, and clear top-bottom
feature orientation. The part is made from 1045 medium-carbon steel, normalized using round bar
stock. Start from one cut length of round metal bar. Turn the outside, face both ends, bore the
center, then mill secondary flats, slots, and radial holes as needed. No separate inserts or
fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 49 mm and length 41 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 12 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 22 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 16 mm wide over 33 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M8 holes through the top flat at X=13 mm and X=27 mm.
- split relief slit: Cut one full-length radial slit 2 mm wide from the outside to the axial bore on datum-B side.
- outside edge treatment: Break all outside circular edges with 1.0 mm chamfers and keep internal bore edges visibly chamfered.
- cross relief slot: Machine one transverse slot 4 mm wide across the top flat at X=20 mm, depth 4 mm.

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
- Do not broaden the requirement back into the full product idea named 'Refrigerator Compressor Foot Leveling Spacer'; this requirement is only for its chosen metal part.

---
