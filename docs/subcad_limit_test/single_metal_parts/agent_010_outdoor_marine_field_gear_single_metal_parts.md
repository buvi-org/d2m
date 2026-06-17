# Agent 010 Single Metal Part Requirements

Domain: outdoor gear, camping hardware, marine accessories, and rugged field equipment

Each item below is one metal part only. Product assemblies and nonmetal components are explicitly out of scope.

## SMP-010-01 - Cam-Lock Tent Pole Hub

Part name: Cam-Lock Tent Pole Hub - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 20, "outer_diameter_mm": 61, "overall_length_mm": 57, "wall_minimum_mm": 20}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Cam-Lock Tent Pole Hub'. The broader use case is:
Four-season expedition tents using rigid aluminum pole frameworks in high wind. The chosen
deliverable is only the metal body implied by: Machined central hub body with angled cylindrical
sockets, cam bore, detent pockets, and drain channels. All other product elements are external
reference items and must not be modeled. The part must perform this mechanical role: Joins multiple
tent poles at fixed compound angles while a rotating cam locks each pole socket against pullout. It
is intentionally included in the SubCAD limit corpus because: Requires several non-coplanar angled
bores, intersecting socket geometry, rotational cam clearance, asymmetric fillets, and small
retention features. The part is made from low-carbon steel, ASTM A36 or equivalent using round bar
stock. Start from one cut length of round metal bar. Turn the outside, face both ends, bore the
center, then mill secondary flats, slots, and radial holes as needed. No separate inserts or
fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 61 mm and length 57 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 20 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 30 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 20 mm wide over 49 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M4 holes through the top flat at X=19 mm and X=38 mm.
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
- Do not broaden the requirement back into the full product idea named 'Cam-Lock Tent Pole Hub'; this requirement is only for its chosen metal part.

---

## SMP-010-02 - Kayak Deck Gear Track Anchor

Part name: Kayak Deck Gear Track Anchor - single metal part

Material: 4140 alloy steel, prehard (strong cylindrical metal part with threaded and slotted details)

Envelope: `{"axial_bore_diameter_mm": 16, "outer_diameter_mm": 49, "overall_length_mm": 68, "wall_minimum_mm": 16}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Kayak Deck Gear Track Anchor'. The broader use case
is: Sea kayaks and fishing kayaks that mount rod holders, GPS arms, and tie-down accessories on deck
rails. The chosen deliverable is only the metal body implied by: Machined T-slot slider block with
tapered wedge pocket, threaded boss, underside reliefs, and rounded rail-bearing edges. All other
product elements are external reference items and must not be modeled. The part must perform this
mechanical role: Slides into a low-profile deck track and locks accessories in place with a captive
wedge clamp. It is intentionally included in the SubCAD limit corpus because: Combines profile-
driven rail geometry, captured sliding interfaces, tapered internal features, precise edge breaks,
and functional orientation constraints. The part is made from 4140 alloy steel, prehard using round
bar stock. Start from one cut length of round metal bar. Turn the outside, face both ends, bore the
center, then mill secondary flats, slots, and radial holes as needed. No separate inserts or
fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 49 mm and length 68 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 16 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 26 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 16 mm wide over 60 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M7 holes through the top flat at X=22 mm and X=45 mm.
- split relief slit: Cut one full-length radial slit 2 mm wide from the outside to the axial bore on datum-B side.
- outside edge treatment: Break all outside circular edges with 1.0 mm chamfers and keep internal bore edges visibly chamfered.
- cross relief slot: Machine one transverse slot 4 mm wide across the top flat at X=34 mm, depth 4 mm.

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
- Do not broaden the requirement back into the full product idea named 'Kayak Deck Gear Track Anchor'; this requirement is only for its chosen metal part.

---

## SMP-010-03 - Folding Camp Stove Pot Support Arm

Part name: Folding Camp Stove Pot Support Arm - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 55, "length_mm": 140, "width_mm": 75}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Folding Camp Stove Pot Support Arm'. The broader
use case is: Compact backpacking stoves that must support cookware while folding flat for packing.
The chosen deliverable is only the metal body implied by: Machined folding arm with hinge barrel,
stop shoulder, scalloped pot-contact teeth, lightening pockets, and nested folded profile. All other
product elements are external reference items and must not be modeled. The part must perform this
mechanical role: Pivots outward from a burner body and provides a serrated support surface for pots
of varying diameters. It is intentionally included in the SubCAD limit corpus because: Tests hinge-
axis geometry, curved serrations, thin structural ribs, weight-saving cutouts, and interference-
aware folded versus deployed shapes. The part is made from low-carbon steel, ASTM A36 or equivalent
using rectangular block stock. Start from one rectangular metal block or plate. Saw oversize, face
all datum sides, then machine the pockets, holes, slots, angled faces, grooves, and edge treatments
into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 140 mm x 75 mm x 55 mm.
- mounting hole pattern: Drill two through holes diameter 6 mm on the length centerline at X=15 mm and X=125 mm, Y=37 mm.
- functional center feature: Machine a central obround slot 46 mm long x 11 mm wide through the part, centered at X=70 mm, Y=37 mm.
- top relief pocket: Mill a rectangular relief pocket 35 mm x 25 mm x 25 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- serrated contact edge: Cut 5 equal triangular serrations across the rear edge, each 3 mm deep.

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
- Do not broaden the requirement back into the full product idea named 'Folding Camp Stove Pot Support Arm'; this requirement is only for its chosen metal part.

---

## SMP-010-04 - Marine Cleat Quick-Release Fairlead

Part name: Marine Cleat Quick-Release Fairlead - single metal part

Material: AISI 316 stainless steel (corrosion resistance and cleanable metal surfaces)

Envelope: `{"height_mm": 46, "length_mm": 120, "width_mm": 90}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Marine Cleat Quick-Release Fairlead'. The broader
use case is: Small sailboats and tenders needing controlled rope routing near a cleat without
permanent line trapping. The chosen deliverable is only the metal body implied by: Machined fairlead
body with flared rope throat, mounting bosses, swept entry horns, countersunk fastener holes, and
polished bearing radii. All other product elements are external reference items and must not be
modeled. The part must perform this mechanical role: Guides dock line or control line through a
smooth open throat while allowing quick side release under slack. It is intentionally included in
the SubCAD limit corpus because: Requires organic rope-contact surfaces, compound curves,
countersinks, asymmetric open geometry, and high-radius transitions that are hard to express as
simple primitives. The part is made from AISI 316 stainless steel using rectangular block stock.
Start from one rectangular metal block or plate. Saw oversize, face all datum sides, then machine
the pockets, holes, slots, angled faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 120 mm x 90 mm x 46 mm.
- mounting hole pattern: Drill two through holes diameter 13 mm on the length centerline at X=18 mm and X=102 mm, Y=45 mm.
- functional center feature: Machine a central obround slot 40 mm long x 7 mm wide through the part, centered at X=60 mm, Y=45 mm.
- top relief pocket: Mill a rectangular relief pocket 30 mm x 30 mm x 2 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Marine Cleat Quick-Release Fairlead'; this requirement is only for its chosen metal part.

---

## SMP-010-05 - Ice Axe Spike Protector Lock Collar

Part name: Ice Axe Spike Protector Lock Collar - single metal part

Material: 4140 alloy steel, prehard (strong cylindrical metal part with threaded and slotted details)

Envelope: `{"axial_bore_diameter_mm": 11, "outer_diameter_mm": 34, "overall_length_mm": 29, "wall_minimum_mm": 11}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Ice Axe Spike Protector Lock Collar'. The broader
use case is: Mountaineering packs carrying technical ice axes with removable spike covers. The
chosen deliverable is only the metal body implied by: Machined split collar with shaped shaft
channel, bayonet lug slots, pinch screw bridge, and keyed cap-retention ears. All other product
elements are external reference items and must not be modeled. The part must perform this mechanical
role: Clamps around an ice axe shaft and locks a protective spike cap so it cannot fall off during
transport. It is intentionally included in the SubCAD limit corpus because: Tests split-body
geometry, non-round channels, bayonet-slot paths, screw-clearance bridges, and mating-part retention
details. The part is made from 4140 alloy steel, prehard using round bar stock. Start from one cut
length of round metal bar. Turn the outside, face both ends, bore the center, then mill secondary
flats, slots, and radial holes as needed. No separate inserts or fasteners are part of the
deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 34 mm and length 29 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 11 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 21 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 11 mm wide over 21 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M5 holes through the top flat at X=9 mm and X=19 mm.
- split relief slit: Cut one full-length radial slit 3 mm wide from the outside to the axial bore on datum-B side.
- outside edge treatment: Break all outside circular edges with 1.0 mm chamfers and keep internal bore edges visibly chamfered.
- cross relief slot: Machine one transverse slot 5 mm wide across the top flat at X=14 mm, depth 3 mm.

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
- Do not broaden the requirement back into the full product idea named 'Ice Axe Spike Protector Lock Collar'; this requirement is only for its chosen metal part.

---

## SMP-010-06 - Rugged Tripod Ground Spike Foot

Part name: Rugged Tripod Ground Spike Foot - single metal part

Material: 6061-T6 aluminum (low mass with good machinability and stable flat features)

Envelope: `{"axial_bore_diameter_mm": 8, "outer_diameter_mm": 40, "overall_length_mm": 119, "wall_minimum_mm": 16}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Rugged Tripod Ground Spike Foot'. The broader use
case is: Field survey tripods, spotting scopes, and camera supports used on mud, gravel, snow, and
packed soil. The chosen deliverable is only the metal body implied by: Machined foot housing with
conical spike seat, transverse pivot bosses, serrated ground shoulder, drainage slots, and threaded
leg socket. All other product elements are external reference items and must not be modeled. The
part must perform this mechanical role: Replaces a rubber foot with a folding ground spike and broad
shoulder that resists twisting under load. It is intentionally included in the SubCAD limit corpus
because: Includes coaxial threaded features, conical seats, pivot bosses, serrated terrain contact,
and dirt-shedding openings in a compact part. The part is made from 6061-T6 aluminum using round bar
stock. Start from one cut length of round metal bar. Turn the outside, face both ends, bore the
center, then mill secondary flats, slots, and radial holes as needed. No separate inserts or
fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 40 mm and length 119 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 8 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 18 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 13 mm wide over 111 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M7 holes through the top flat at X=39 mm and X=79 mm.
- split relief slit: Cut one full-length radial slit 3 mm wide from the outside to the axial bore on datum-B side.
- outside edge treatment: Break all outside circular edges with 1.0 mm chamfers and keep internal bore edges visibly chamfered.
- cross relief slot: Machine one transverse slot 5 mm wide across the top flat at X=59 mm, depth 4 mm.

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
- Do not broaden the requirement back into the full product idea named 'Rugged Tripod Ground Spike Foot'; this requirement is only for its chosen metal part.

---

## SMP-010-07 - Dive Reel Line Guide Shuttle

Part name: Dive Reel Line Guide Shuttle - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 44, "length_mm": 75, "width_mm": 60}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Dive Reel Line Guide Shuttle'. The broader use case
is: Scuba and cave-diving reels where line must spool evenly without snagging on the frame. The
chosen deliverable is only the metal body implied by: Machined shuttle block with twin guide-rod
bores, radiused line eyelet, anti-rotation flats, and recessed wear insert pocket. All other product
elements are external reference items and must not be modeled. The part must perform this mechanical
role: Guides braided line across the reel width while sliding on parallel rods and maintaining a
rounded low-friction eyelet. It is intentionally included in the SubCAD limit corpus because: Tests
parallel precision bores, smooth internal rope-contact radii, insert recesses, sliding clearances,
and compact symmetry with functional exceptions. The part is made from low-carbon steel, ASTM A36 or
equivalent using rectangular block stock. Start from one rectangular metal block or plate. Saw
oversize, face all datum sides, then machine the pockets, holes, slots, angled faces, grooves, and
edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 75 mm x 60 mm x 44 mm.
- mounting hole pattern: Drill two through holes diameter 9 mm on the length centerline at X=12 mm and X=63 mm, Y=30 mm.
- functional center feature: Machine a central obround slot 30 mm long x 10 mm wide through the part, centered at X=37 mm, Y=30 mm.
- top relief pocket: Mill a rectangular relief pocket 25 mm x 20 mm x 16 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Dive Reel Line Guide Shuttle'; this requirement is only for its chosen metal part.

---

## SMP-010-08 - Backcountry Water Filter Pump Lever

Part name: Backcountry Water Filter Pump Lever - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 12, "outer_diameter_mm": 62, "overall_length_mm": 83, "wall_minimum_mm": 25}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Backcountry Water Filter Pump Lever'. The broader
use case is: Hand-pump water filters used for group camping and remote field expeditions. The chosen
deliverable is only the metal body implied by: Machined lever arm with offset pivot clevis,
ergonomic thumb pad, linkage pin bore, stop tab, and hollowed underside. All other product elements
are external reference items and must not be modeled. The part must perform this mechanical role:
Transfers hand force to a pump piston while folding against the filter body for storage. It is
intentionally included in the SubCAD limit corpus because: Requires offset load paths, clevis
geometry, blended ergonomic surfaces, pin alignment, stop faces, and underside shelling-like relief.
The part is made from low-carbon steel, ASTM A36 or equivalent using round bar stock. Start from one
cut length of round metal bar. Turn the outside, face both ends, bore the center, then mill
secondary flats, slots, and radial holes as needed. No separate inserts or fasteners are part of the
deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 62 mm and length 83 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 12 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 22 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 20 mm wide over 75 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M8 holes through the top flat at X=27 mm and X=55 mm.
- split relief slit: Cut one full-length radial slit 5 mm wide from the outside to the axial bore on datum-B side.
- outside edge treatment: Break all outside circular edges with 1.0 mm chamfers and keep internal bore edges visibly chamfered.
- cross relief slot: Machine one transverse slot 7 mm wide across the top flat at X=41 mm, depth 6 mm.

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
- Do not broaden the requirement back into the full product idea named 'Backcountry Water Filter Pump Lever'; this requirement is only for its chosen metal part.

---

## SMP-010-09 - Boat Hook Telescoping Pole Cam Clamp

Part name: Boat Hook Telescoping Pole Cam Clamp - single metal part

Material: AISI 316 stainless steel (corrosion resistance and cleanable metal surfaces)

Envelope: `{"axial_bore_diameter_mm": 16, "outer_diameter_mm": 49, "overall_length_mm": 30, "wall_minimum_mm": 16}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Boat Hook Telescoping Pole Cam Clamp'. The broader
use case is: Telescoping marine poles used for docking, mooring pickup, and retrieving lines from
the water. The chosen deliverable is only the metal body implied by: Machined clamp collar with
split cylindrical bore, cam-lever lugs, internal compression shoe pocket, hinge pin bosses, and
anti-slip texture grooves. All other product elements are external reference items and must not be
modeled. The part must perform this mechanical role: Locks nested pole sections at adjustable length
using an external cam lever and shaped compression shoe. It is intentionally included in the SubCAD
limit corpus because: Tests split clamp mechanics, cylindrical nesting, lever pivot architecture,
internal pocketing, textured grip features, and clamp-clearance tolerances. The part is made from
AISI 316 stainless steel using round bar stock. Start from one cut length of round metal bar. Turn
the outside, face both ends, bore the center, then mill secondary flats, slots, and radial holes as
needed. No separate inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 49 mm and length 30 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 16 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 26 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 16 mm wide over 22 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M4 holes through the top flat at X=10 mm and X=20 mm.
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
- Do not broaden the requirement back into the full product idea named 'Boat Hook Telescoping Pole Cam Clamp'; this requirement is only for its chosen metal part.

---

## SMP-010-10 - Field Radio Mast Guyline Tensioner

Part name: Field Radio Mast Guyline Tensioner - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"length_mm": 135, "thickness_mm": 8, "width_mm": 90}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Field Radio Mast Guyline Tensioner'. The broader
use case is: Portable communications masts for emergency response, overlanding, and remote survey
teams. The chosen deliverable is only the metal body implied by: Machined tensioner body with angled
rope channels, eccentric locking cam cavity, tie-off eye, ribbed grip flanges, and load-rated anchor
hole. All other product elements are external reference items and must not be modeled. The part must
perform this mechanical role: Adjusts and locks guyline tension while allowing quick release with
gloved hands. It is intentionally included in the SubCAD limit corpus because: Combines rope-path
geometry, eccentric cam clearance, high-load eyelet shapes, grip ribs, and angled through-features
that stress representation of functional mechanical intent. The part is made from low-carbon steel,
ASTM A36 or equivalent using sheet or plate stock. Start from one flat sheet or plate blank. Cut the
outside profile, machine holes, slots, pockets, lips, and relief features into that same piece. If
bends are called out, they are bends in the same sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 135 mm x 90 mm x 8 mm.
- mounting hole pattern: Drill two through holes diameter 7 mm on the length centerline at X=18 mm and X=117 mm, Y=45 mm.
- functional center feature: Machine a central obround slot 45 mm long x 11 mm wide through the part, centered at X=67 mm, Y=45 mm.
- top relief pocket: Mill a rectangular relief pocket 33 mm x 30 mm x 3 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- machined angled reference face: Machine one top reference face at 45 degrees over the last 27 mm of length.

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
- Do not broaden the requirement back into the full product idea named 'Field Radio Mast Guyline Tensioner'; this requirement is only for its chosen metal part.

---
