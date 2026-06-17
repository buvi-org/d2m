# Agent 015 Single Metal Part Requirements

Domain: textile, sewing, leatherworking, embroidery, and craft-machine hardware

Each item below is one metal part only. Product assemblies and nonmetal components are explicitly out of scope.

## SMP-015-01 - Walking-Foot Sewing Machine Feed Dog

Part name: Walking-Foot Sewing Machine Feed Dog - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 70, "length_mm": 200, "width_mm": 70}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Walking-Foot Sewing Machine Feed Dog'. The broader
use case is: Industrial sewing machine for thick canvas, denim, and layered upholstery fabric The
chosen deliverable is only the metal body implied by: Serrated feed dog block with staggered tooth
rows, mounting slots, and needle clearance channel All other product elements are external reference
items and must not be modeled. The part must perform this mechanical role: Grip and advance fabric
layers in sync with the presser foot without slippage It is intentionally included in the SubCAD
limit corpus because: Requires repeated fine teeth on an irregular top surface, precise slot
placement, asymmetric clearances, and functional contact geometry The part is made from low-carbon
steel, ASTM A36 or equivalent using rectangular block stock. Start from one rectangular metal block
or plate. Saw oversize, face all datum sides, then machine the pockets, holes, slots, angled faces,
grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 200 mm x 70 mm x 70 mm.
- mounting hole pattern: Drill two through holes diameter 11 mm on the length centerline at X=14 mm and X=186 mm, Y=35 mm.
- functional center feature: Machine a central obround slot 66 mm long x 17 mm wide through the part, centered at X=100 mm, Y=35 mm.
- top relief pocket: Mill a rectangular relief pocket 50 mm x 23 mm x 15 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- serrated contact edge: Cut 7 equal triangular serrations across the rear edge, each 4 mm deep.

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
- Do not broaden the requirement back into the full product idea named 'Walking-Foot Sewing Machine Feed Dog'; this requirement is only for its chosen metal part.

---

## SMP-015-02 - Leather Strap Edge Beveler Guide Shoe

Part name: Leather Strap Edge Beveler Guide Shoe - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"length_mm": 245, "thickness_mm": 6, "width_mm": 55}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Leather Strap Edge Beveler Guide Shoe'. The broader
use case is: Bench-mounted leatherworking edge beveling tool for belts, straps, and harness
components The chosen deliverable is only the metal body implied by: Contoured guide shoe with
V-groove, blade window, radiused entry lip, and clamp screw bosses All other product elements are
external reference items and must not be modeled. The part must perform this mechanical role: Hold a
leather strap at a consistent offset and angle while guiding it past a cutting blade It is
intentionally included in the SubCAD limit corpus because: Combines angled grooves, flowing guide
surfaces, sharp blade clearances, small bosses, and ergonomic contact transitions The part is made
from low-carbon steel, ASTM A36 or equivalent using sheet or plate stock. Start from one flat sheet
or plate blank. Cut the outside profile, machine holes, slots, pockets, lips, and relief features
into that same piece. If bends are called out, they are bends in the same sheet part, not separate
welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 245 mm x 55 mm x 6 mm.
- mounting hole pattern: Drill two through holes diameter 11 mm on the length centerline at X=11 mm and X=234 mm, Y=27 mm.
- functional center feature: Machine a central obround slot 81 mm long x 10 mm wide through the part, centered at X=122 mm, Y=27 mm.
- top relief pocket: Mill a rectangular relief pocket 61 mm x 18 mm x 3 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- centered V-groove: Cut a 90 degree V-groove along the full X length on the top face, groove mouth 27 mm wide and depth 3 mm.
- machined angled reference face: Machine one top reference face at 36 degrees over the last 49 mm of length.
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
- The feature named 'centered V-groove' is present with the stated size and position.
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
- Do not broaden the requirement back into the full product idea named 'Leather Strap Edge Beveler Guide Shoe'; this requirement is only for its chosen metal part.

---

## SMP-015-03 - Embroidery Hoop Quick-Lock Cam Clamp

Part name: Embroidery Hoop Quick-Lock Cam Clamp - single metal part

Material: 1045 medium-carbon steel, normalized (durable wear surface for workshop loading)

Envelope: `{"height_mm": 19, "length_mm": 180, "width_mm": 85}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Embroidery Hoop Quick-Lock Cam Clamp'. The broader
use case is: Commercial embroidery machine hooping fixture for fast fabric tensioning The chosen
deliverable is only the metal body implied by: Eccentric cam lever with curved bearing face, hinge
bore, detent notch, and finger tab All other product elements are external reference items and must
not be modeled. The part must perform this mechanical role: Lock the outer hoop against the inner
hoop with repeatable fabric tension using a rotating cam It is intentionally included in the SubCAD
limit corpus because: Tests eccentric profiles, smooth cam contact surfaces, detents, hinge
alignment, and nonuniform lever geometry The part is made from 1045 medium-carbon steel, normalized
using rectangular block stock. Start from one rectangular metal block or plate. Saw oversize, face
all datum sides, then machine the pockets, holes, slots, angled faces, grooves, and edge treatments
into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 180 mm x 85 mm x 19 mm.
- mounting hole pattern: Drill two through holes diameter 7 mm on the length centerline at X=17 mm and X=163 mm, Y=42 mm.
- functional center feature: Machine a central obround slot 60 mm long x 14 mm wide through the part, centered at X=90 mm, Y=42 mm.
- top relief pocket: Mill a rectangular relief pocket 45 mm x 28 mm x 2 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Embroidery Hoop Quick-Lock Cam Clamp'; this requirement is only for its chosen metal part.

---

## SMP-015-04 - Rotary Cutter Blade Depth Collar

Part name: Rotary Cutter Blade Depth Collar - single metal part

Material: 4140 alloy steel, prehard (strong cylindrical metal part with threaded and slotted details)

Envelope: `{"axial_bore_diameter_mm": 9, "outer_diameter_mm": 38, "overall_length_mm": 113, "wall_minimum_mm": 14}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Rotary Cutter Blade Depth Collar'. The broader use
case is: Craft cutting tool used for quilting fabric, felt, and pattern paper The chosen deliverable
is only the metal body implied by: Threaded depth-control collar with scalloped grip rim, blade
guard flange, and index marks All other product elements are external reference items and must not
be modeled. The part must perform this mechanical role: Limit exposed blade depth while allowing
fine adjustment for material thickness It is intentionally included in the SubCAD limit corpus
because: Requires circular threading context, knurled or scalloped perimeter detail, thin guard
features, and rotational adjustment semantics The part is made from 4140 alloy steel, prehard using
round bar stock. Start from one cut length of round metal bar. Turn the outside, face both ends,
bore the center, then mill secondary flats, slots, and radial holes as needed. No separate inserts
or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 38 mm and length 113 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 9 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 19 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 12 mm wide over 105 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M6 holes through the top flat at X=37 mm and X=75 mm.
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
- Do not broaden the requirement back into the full product idea named 'Rotary Cutter Blade Depth Collar'; this requirement is only for its chosen metal part.

---

## SMP-015-05 - Serger Looper Carrier Arm

Part name: Serger Looper Carrier Arm - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 40, "length_mm": 195, "width_mm": 75}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Serger Looper Carrier Arm'. The broader use case
is: Overlock sewing machine mechanism for forming interlocked edge stitches The chosen deliverable
is only the metal body implied by: Offset looper carrier arm with split clamp bore, tapered neck,
timing slot, and replaceable looper mount All other product elements are external reference items
and must not be modeled. The part must perform this mechanical role: Carry the looper tip through a
timed arc around the needle path It is intentionally included in the SubCAD limit corpus because:
Challenges CAD with compound offsets, thin curved arms, split clamping geometry, slot-and-bore
relationships, and collision-critical clearances The part is made from low-carbon steel, ASTM A36 or
equivalent using rectangular block stock. Start from one rectangular metal block or plate. Saw
oversize, face all datum sides, then machine the pockets, holes, slots, angled faces, grooves, and
edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 195 mm x 75 mm x 40 mm.
- mounting hole pattern: Drill two through holes diameter 13 mm on the length centerline at X=15 mm and X=180 mm, Y=37 mm.
- functional center feature: Machine a central obround slot 65 mm long x 11 mm wide through the part, centered at X=97 mm, Y=37 mm.
- top relief pocket: Mill a rectangular relief pocket 48 mm x 25 mm x 7 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- machined angled reference face: Machine one top reference face at 19 degrees over the last 39 mm of length.

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
- Do not broaden the requirement back into the full product idea named 'Serger Looper Carrier Arm'; this requirement is only for its chosen metal part.

---

## SMP-015-06 - Weaving Loom Shuttle Race Insert

Part name: Weaving Loom Shuttle Race Insert - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 33, "length_mm": 205, "width_mm": 35}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Weaving Loom Shuttle Race Insert'. The broader use
case is: Small handloom or sample loom that throws a shuttle across warp threads The chosen
deliverable is only the metal body implied by: Curved shuttle race insert with concave running
channel, countersunk mounts, and raised end stops All other product elements are external reference
items and must not be modeled. The part must perform this mechanical role: Provide a low-friction
track that keeps the shuttle aligned during travel It is intentionally included in the SubCAD limit
corpus because: Tests long shallow curves, concave tracks, end-stop transitions, countersinks, and
parts whose function depends on continuous surface shape The part is made from low-carbon steel,
ASTM A36 or equivalent using rectangular block stock. Start from one rectangular metal block or
plate. Saw oversize, face all datum sides, then machine the pockets, holes, slots, angled faces,
grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 205 mm x 35 mm x 33 mm.
- mounting hole pattern: Drill two through holes diameter 8 mm on the length centerline at X=10 mm and X=195 mm, Y=17 mm.
- functional center feature: Machine a central obround slot 68 mm long x 9 mm wide through the part, centered at X=102 mm, Y=17 mm.
- top relief pocket: Mill a rectangular relief pocket 51 mm x 18 mm x 1 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Weaving Loom Shuttle Race Insert'; this requirement is only for its chosen metal part.

---

## SMP-015-07 - Buttonhole Attachment Template Cam

Part name: Buttonhole Attachment Template Cam - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"length_mm": 90, "thickness_mm": 8, "width_mm": 45}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Buttonhole Attachment Template Cam'. The broader
use case is: Mechanical buttonhole attachment for domestic sewing machines The chosen deliverable is
only the metal body implied by: Profile cam disk with asymmetric lobed groove, central drive bore,
timing notch, and retaining groove All other product elements are external reference items and must
not be modeled. The part must perform this mechanical role: Drive needle swing and fabric movement
pattern to form a consistent buttonhole shape It is intentionally included in the SubCAD limit
corpus because: Requires representing noncircular cam paths, internal grooves, rotational
registration, and shape-driven motion intent The part is made from low-carbon steel, ASTM A36 or
equivalent using sheet or plate stock. Start from one flat sheet or plate blank. Cut the outside
profile, machine holes, slots, pockets, lips, and relief features into that same piece. If bends are
called out, they are bends in the same sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 90 mm x 45 mm x 8 mm.
- mounting hole pattern: Drill two through holes diameter 8 mm on the length centerline at X=10 mm and X=80 mm, Y=22 mm.
- functional center feature: Machine a central obround slot 30 mm long x 18 mm wide through the part, centered at X=45 mm, Y=22 mm.
- top relief pocket: Mill a rectangular relief pocket 25 mm x 18 mm x 1 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Buttonhole Attachment Template Cam'; this requirement is only for its chosen metal part.

---

## SMP-015-08 - Leather Skiving Machine Presser Foot

Part name: Leather Skiving Machine Presser Foot - single metal part

Material: 1045 medium-carbon steel, normalized (durable wear surface for workshop loading)

Envelope: `{"height_mm": 69, "length_mm": 170, "width_mm": 95}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Leather Skiving Machine Presser Foot'. The broader
use case is: Leather skiving machine used to thin edges before folding or stitching The chosen
deliverable is only the metal body implied by: Narrow presser foot with curved sole, blade relief
crescent, height-adjustment boss, and side guide face All other product elements are external
reference items and must not be modeled. The part must perform this mechanical role: Press leather
against the feed roller and blade while controlling skive width It is intentionally included in the
SubCAD limit corpus because: Combines thin functional lips, curved pressure surfaces, tight blade
relief geometry, and small adjustment interfaces The part is made from 1045 medium-carbon steel,
normalized using rectangular block stock. Start from one rectangular metal block or plate. Saw
oversize, face all datum sides, then machine the pockets, holes, slots, angled faces, grooves, and
edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 170 mm x 95 mm x 69 mm.
- mounting hole pattern: Drill two through holes diameter 11 mm on the length centerline at X=19 mm and X=151 mm, Y=47 mm.
- functional center feature: Machine a central obround slot 56 mm long x 8 mm wide through the part, centered at X=85 mm, Y=47 mm.
- top relief pocket: Mill a rectangular relief pocket 42 mm x 31 mm x 31 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Leather Skiving Machine Presser Foot'; this requirement is only for its chosen metal part.

---

## SMP-015-09 - Embroidery Thread Tension Disc Hub

Part name: Embroidery Thread Tension Disc Hub - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 23, "length_mm": 185, "width_mm": 40}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Embroidery Thread Tension Disc Hub'. The broader
use case is: Multi-needle embroidery machine upper thread tension assembly The chosen deliverable is
only the metal body implied by: Stepped hub with spring seat, thread guide notch, retaining groove,
and anti-rotation flat All other product elements are external reference items and must not be
modeled. The part must perform this mechanical role: Center and preload paired tension discs while
routing thread through a controlled path It is intentionally included in the SubCAD limit corpus
because: Tests concentric stepped geometry, small thread-path features, spring seating surfaces,
grooves, flats, and assembly-oriented constraints The part is made from low-carbon steel, ASTM A36
or equivalent using rectangular block stock. Start from one rectangular metal block or plate. Saw
oversize, face all datum sides, then machine the pockets, holes, slots, angled faces, grooves, and
edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 185 mm x 40 mm x 23 mm.
- mounting hole pattern: Drill two through holes diameter 7 mm on the length centerline at X=10 mm and X=175 mm, Y=20 mm.
- functional center feature: Machine a central obround slot 61 mm long x 15 mm wide through the part, centered at X=92 mm, Y=20 mm.
- top relief pocket: Mill a rectangular relief pocket 46 mm x 18 mm x 11 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- serrated contact edge: Cut 5 equal triangular serrations across the rear edge, each 5 mm deep.
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
- Do not broaden the requirement back into the full product idea named 'Embroidery Thread Tension Disc Hub'; this requirement is only for its chosen metal part.

---

## SMP-015-10 - Bias Tape Maker Folding Funnel

Part name: Bias Tape Maker Folding Funnel - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 40, "length_mm": 145, "width_mm": 65}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Bias Tape Maker Folding Funnel'. The broader use
case is: Sewing and quilting attachment that folds fabric strips before stitching The chosen
deliverable is only the metal body implied by: Formed folding funnel body with tapered inlet, curled
side channels, exit throat, and mounting tab All other product elements are external reference items
and must not be modeled. The part must perform this mechanical role: Guide flat fabric tape into
symmetrical folded edges at a fixed finished width It is intentionally included in the SubCAD limit
corpus because: Stresses CAD representation with sheet-like curved guide surfaces, tapered
transitions, mirrored but nontrivial channels, and thin-wall manufacturing intent The part is made
from low-carbon steel, ASTM A36 or equivalent using rectangular block stock. Start from one
rectangular metal block or plate. Saw oversize, face all datum sides, then machine the pockets,
holes, slots, angled faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 145 mm x 65 mm x 40 mm.
- mounting hole pattern: Drill two through holes diameter 10 mm on the length centerline at X=13 mm and X=132 mm, Y=32 mm.
- functional center feature: Machine a central obround slot 48 mm long x 8 mm wide through the part, centered at X=72 mm, Y=32 mm.
- top relief pocket: Mill a rectangular relief pocket 36 mm x 21 mm x 20 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- machined angled reference face: Machine one top reference face at 20 degrees over the last 29 mm of length.

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
- Do not broaden the requirement back into the full product idea named 'Bias Tape Maker Folding Funnel'; this requirement is only for its chosen metal part.

---
