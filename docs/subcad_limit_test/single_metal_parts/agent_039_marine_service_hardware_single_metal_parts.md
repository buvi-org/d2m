# Agent 039 Single Metal Part Requirements

Domain: marine engine service, boat deck hardware, rigging tools, bilge systems, and dock equipment

Each item below is one metal part only. Product assemblies and nonmetal components are explicitly out of scope.

## SMP-039-01 - Outboard Lower Unit Service Cradle

Part name: Outboard Lower Unit Service Cradle - single metal part

Material: AISI 316 stainless steel (corrosion resistance and cleanable metal surfaces)

Envelope: `{"height_mm": 61, "length_mm": 90, "width_mm": 75}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Outboard Lower Unit Service Cradle'. The broader
use case is: Marine mechanics need a stable bench fixture for handling removed outboard lower units
during inspection, draining, seal work, and reassembly. The chosen deliverable is only the metal
body implied by: Contoured cradle frame with adjustable padded supports and clampable mounting base.
All other product elements are external reference items and must not be modeled. The part must
perform this mechanical role: Support an irregular engine gearcase in several service orientations
while keeping drain points, skeg, prop shaft area, and fastener zones accessible. It is
intentionally included in the SubCAD limit corpus because: Requires representing asymmetric organic
support contact, tilted service positions, clearance windows, and fixture adjustability without
relying on simple block-like geometry. The part is made from AISI 316 stainless steel using
rectangular block stock. Start from one rectangular metal block or plate. Saw oversize, face all
datum sides, then machine the pockets, holes, slots, angled faces, grooves, and edge treatments into
that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 90 mm x 75 mm x 61 mm.
- mounting hole pattern: Drill two through holes diameter 11 mm on the length centerline at X=15 mm and X=75 mm, Y=37 mm.
- functional center feature: Machine a central obround slot 30 mm long x 18 mm wide through the part, centered at X=45 mm, Y=37 mm.
- top relief pocket: Mill a rectangular relief pocket 25 mm x 25 mm x 29 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Outboard Lower Unit Service Cradle'; this requirement is only for its chosen metal part.

---

## SMP-039-02 - Portable Propeller Puller With Hub Guard

Part name: Portable Propeller Puller With Hub Guard - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"length_mm": 205, "thickness_mm": 9, "width_mm": 55}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Portable Propeller Puller With Hub Guard'. The
broader use case is: Boat yards often remove stubborn propellers from shafts while trying to avoid
damage to blades, hubs, threads, and nearby running gear. The chosen deliverable is only the metal
body implied by: Yoke-style puller body with protective hub cup and sliding reaction arms. All other
product elements are external reference items and must not be modeled. The part must perform this
mechanical role: Apply controlled pulling force around a propeller hub while shielding vulnerable
surfaces and keeping the tool centered on the shaft. It is intentionally included in the SubCAD
limit corpus because: Challenges CAD with radial symmetry, curved blade clearance, movable arms,
nested protective surfaces, and force-path readability. The part is made from low-carbon steel, ASTM
A36 or equivalent using sheet or plate stock. Start from one flat sheet or plate blank. Cut the
outside profile, machine holes, slots, pockets, lips, and relief features into that same piece. If
bends are called out, they are bends in the same sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 205 mm x 55 mm x 9 mm.
- mounting hole pattern: Drill two through holes diameter 7 mm on the length centerline at X=11 mm and X=194 mm, Y=27 mm.
- functional center feature: Machine a central obround slot 68 mm long x 9 mm wide through the part, centered at X=102 mm, Y=27 mm.
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
- Do not broaden the requirement back into the full product idea named 'Portable Propeller Puller With Hub Guard'; this requirement is only for its chosen metal part.

---

## SMP-039-03 - Deck Cleat Load Spreader Backing Plate

Part name: Deck Cleat Load Spreader Backing Plate - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"length_mm": 145, "thickness_mm": 8, "width_mm": 105}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Deck Cleat Load Spreader Backing Plate'. The
broader use case is: Boat owners retrofit or service deck cleats where underside access is awkward
and the deck laminate needs broader load distribution. The chosen deliverable is only the metal body
implied by: Curved backing plate with captive fastener features and edge relief cutouts. All other
product elements are external reference items and must not be modeled. The part must perform this
mechanical role: Spread cleat fastener loads below a deck while adapting to underside curvature and
allowing tool access around nearby obstructions. It is intentionally included in the SubCAD limit
corpus because: Tests curved thin-plate forms, underside installation constraints, countersunk or
captive hardware features, and non-rectangular relief geometry. The part is made from low-carbon
steel, ASTM A36 or equivalent using sheet or plate stock. Start from one flat sheet or plate blank.
Cut the outside profile, machine holes, slots, pockets, lips, and relief features into that same
piece. If bends are called out, they are bends in the same sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 145 mm x 105 mm x 8 mm.
- mounting hole pattern: Drill two through holes diameter 7 mm on the length centerline at X=21 mm and X=124 mm, Y=52 mm.
- functional center feature: Machine a central obround slot 48 mm long x 16 mm wide through the part, centered at X=72 mm, Y=52 mm.
- top relief pocket: Mill a rectangular relief pocket 36 mm x 35 mm x 2 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Deck Cleat Load Spreader Backing Plate'; this requirement is only for its chosen metal part.

---

## SMP-039-04 - Flush Hatch Latch Service Jig

Part name: Flush Hatch Latch Service Jig - single metal part

Material: AISI 316 stainless steel (corrosion resistance and cleanable metal surfaces)

Envelope: `{"height_mm": 57, "length_mm": 120, "width_mm": 105}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Flush Hatch Latch Service Jig'. The broader use
case is: Marine technicians replace flush deck hatch latches where alignment between the latch
barrel, gasket compression, and strike plate is difficult to judge. The chosen deliverable is only
the metal body implied by: Flat alignment jig with recessed latch pocket, strike reference face, and
gasket clearance gauge surfaces. All other product elements are external reference items and must
not be modeled. The part must perform this mechanical role: Hold hatch latch components in the
correct relationship while marking, drilling, or checking gasket compression. It is intentionally
included in the SubCAD limit corpus because: Combines shallow recesses, planar datum references,
gasket offset logic, and temporary installation geometry in a compact tool. The part is made from
AISI 316 stainless steel using rectangular block stock. Start from one rectangular metal block or
plate. Saw oversize, face all datum sides, then machine the pockets, holes, slots, angled faces,
grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 120 mm x 105 mm x 57 mm.
- mounting hole pattern: Drill two through holes diameter 8 mm on the length centerline at X=21 mm and X=99 mm, Y=52 mm.
- functional center feature: Machine a central obround slot 40 mm long x 9 mm wide through the part, centered at X=60 mm, Y=52 mm.
- top relief pocket: Mill a rectangular relief pocket 30 mm x 35 mm x 1 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Flush Hatch Latch Service Jig'; this requirement is only for its chosen metal part.

---

## SMP-039-05 - Rigging Turnbuckle Safety Clip Installer

Part name: Rigging Turnbuckle Safety Clip Installer - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"length_mm": 90, "thickness_mm": 6, "width_mm": 75}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Rigging Turnbuckle Safety Clip Installer'. The
broader use case is: Sailboat rigging service involves installing and removing small safety clips on
turnbuckles in tight deck or mast-base locations. The chosen deliverable is only the metal body
implied by: Slim forked hand tool with clip-retaining groove and angled handle. All other product
elements are external reference items and must not be modeled. The part must perform this mechanical
role: Guide a safety clip into a turnbuckle body while keeping fingers clear of sharp wire ends and
confined fittings. It is intentionally included in the SubCAD limit corpus because: Tests small
retained-part geometry, narrow slots, angled access, ergonomic surfaces, and interaction with
existing rigging hardware. The part is made from low-carbon steel, ASTM A36 or equivalent using
sheet or plate stock. Start from one flat sheet or plate blank. Cut the outside profile, machine
holes, slots, pockets, lips, and relief features into that same piece. If bends are called out, they
are bends in the same sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 90 mm x 75 mm x 6 mm.
- mounting hole pattern: Drill two through holes diameter 13 mm on the length centerline at X=15 mm and X=75 mm, Y=37 mm.
- functional center feature: Machine a central obround slot 30 mm long x 15 mm wide through the part, centered at X=45 mm, Y=37 mm.
- top relief pocket: Mill a rectangular relief pocket 25 mm x 25 mm x 2 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- machined angled reference face: Machine one top reference face at 11 degrees over the last 18 mm of length.
- integral hook lip: Leave an integral hook lip on one short end, projecting 6 mm and undercut 6 mm for registration.

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
- Do not broaden the requirement back into the full product idea named 'Rigging Turnbuckle Safety Clip Installer'; this requirement is only for its chosen metal part.

---

## SMP-039-06 - Standing Rigging Tension Reference Gauge

Part name: Standing Rigging Tension Reference Gauge - single metal part

Material: 6061-T6 aluminum (low mass with good machinability and stable flat features)

Envelope: `{"height_mm": 24, "length_mm": 110, "width_mm": 40}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Standing Rigging Tension Reference Gauge'. The
broader use case is: Boat service crews need a quick physical reference for checking repeatable
rigging tension without full electronic instrumentation. The chosen deliverable is only the metal
body implied by: Clamp-on gauge frame with wire saddles, spring-loaded deflection shoe, and pointer
scale body. All other product elements are external reference items and must not be modeled. The
part must perform this mechanical role: Deflect a wire rope in a controlled way and show a
mechanical indication related to tension. It is intentionally included in the SubCAD limit corpus
because: Involves open-frame structure, cable contact saddles, moving indicator linkage, spring
travel volume, and readable mechanical reference surfaces. The part is made from 6061-T6 aluminum
using rectangular block stock. Start from one rectangular metal block or plate. Saw oversize, face
all datum sides, then machine the pockets, holes, slots, angled faces, grooves, and edge treatments
into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 110 mm x 40 mm x 24 mm.
- mounting hole pattern: Drill two through holes diameter 8 mm on the length centerline at X=10 mm and X=100 mm, Y=20 mm.
- functional center feature: Machine a central obround slot 36 mm long x 12 mm wide through the part, centered at X=55 mm, Y=20 mm.
- top relief pocket: Mill a rectangular relief pocket 27 mm x 18 mm x 3 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Standing Rigging Tension Reference Gauge'; this requirement is only for its chosen metal part.

---

## SMP-039-07 - Bilge Pump Float Switch Debris Shield

Part name: Bilge Pump Float Switch Debris Shield - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"length_mm": 185, "thickness_mm": 10, "width_mm": 100}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Bilge Pump Float Switch Debris Shield'. The broader
use case is: Bilge compartments collect leaves, hair, wire ties, and service debris that can jam
float switches and cause unreliable pump behavior. The chosen deliverable is only the metal body
implied by: Perforated cage cover with snap-on base and hinged inspection flap. All other product
elements are external reference items and must not be modeled. The part must perform this mechanical
role: Protect a float switch from debris while allowing free water flow and manual testing access.
It is intentionally included in the SubCAD limit corpus because: Tests perforated protective
geometry, hinge details, snap features, wet-environment access, and internal clearance for a moving
float. The part is made from low-carbon steel, ASTM A36 or equivalent using sheet or plate stock.
Start from one flat sheet or plate blank. Cut the outside profile, machine holes, slots, pockets,
lips, and relief features into that same piece. If bends are called out, they are bends in the same
sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 185 mm x 100 mm x 10 mm.
- mounting hole pattern: Drill two through holes diameter 7 mm on the length centerline at X=20 mm and X=165 mm, Y=50 mm.
- functional center feature: Machine a central obround slot 61 mm long x 17 mm wide through the part, centered at X=92 mm, Y=50 mm.
- top relief pocket: Mill a rectangular relief pocket 46 mm x 33 mm x 3 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Bilge Pump Float Switch Debris Shield'; this requirement is only for its chosen metal part.

---

## SMP-039-08 - Bilge Hose Anti-Kink Bulkhead Guide

Part name: Bilge Hose Anti-Kink Bulkhead Guide - single metal part

Material: AISI 316 stainless steel (corrosion resistance and cleanable metal surfaces)

Envelope: `{"length_mm": 130, "thickness_mm": 10, "width_mm": 95}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Bilge Hose Anti-Kink Bulkhead Guide'. The broader
use case is: Marine installers route bilge discharge hose through cramped compartments where bends
near bulkheads can restrict flow. The chosen deliverable is only the metal body implied by: Curved
saddle bracket with hose-retaining straps and bulkhead mounting flange. All other product elements
are external reference items and must not be modeled. The part must perform this mechanical role:
Guide a flexible hose through a smooth bend and secure it to a bulkhead without crushing or kinking.
It is intentionally included in the SubCAD limit corpus because: Requires curved path geometry,
strap interfaces, flexible-hose clearance, flange orientation, and compact mounting features. The
part is made from AISI 316 stainless steel using sheet or plate stock. Start from one flat sheet or
plate blank. Cut the outside profile, machine holes, slots, pockets, lips, and relief features into
that same piece. If bends are called out, they are bends in the same sheet part, not separate welded
pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 130 mm x 95 mm x 10 mm.
- mounting hole pattern: Drill two through holes diameter 8 mm on the length centerline at X=19 mm and X=111 mm, Y=47 mm.
- functional center feature: Machine a central obround slot 43 mm long x 17 mm wide through the part, centered at X=65 mm, Y=47 mm.
- top relief pocket: Mill a rectangular relief pocket 32 mm x 31 mm x 2 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Bilge Hose Anti-Kink Bulkhead Guide'; this requirement is only for its chosen metal part.

---

## SMP-039-09 - Dock Line Chafe Guard With Quick Wrap

Part name: Dock Line Chafe Guard With Quick Wrap - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 9, "outer_diameter_mm": 29, "overall_length_mm": 84, "wall_minimum_mm": 10}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Dock Line Chafe Guard With Quick Wrap'. The broader
use case is: Dock lines rub against cleats, chocks, pilings, and rub rails, especially during
changing tide or wake conditions. The chosen deliverable is only the metal body implied by: Flexible
sleeve body with interlocking edge profile and textured outer wear surface. All other product
elements are external reference items and must not be modeled. The part must perform this mechanical
role: Wrap around a dock line and provide a replaceable wear surface that stays positioned at the
contact area. It is intentionally included in the SubCAD limit corpus because: Tests flexible sleeve
representation, partial cylindrical wrapping, interlocking edges, textured wear zones, and rope-
contact behavior. The part is made from low-carbon steel, ASTM A36 or equivalent using round bar
stock. Start from one cut length of round metal bar. Turn the outside, face both ends, bore the
center, then mill secondary flats, slots, and radial holes as needed. No separate inserts or
fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 29 mm and length 84 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 9 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 19 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 9 mm wide over 76 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M5 holes through the top flat at X=28 mm and X=56 mm.
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
- Do not broaden the requirement back into the full product idea named 'Dock Line Chafe Guard With Quick Wrap'; this requirement is only for its chosen metal part.

---

## SMP-039-10 - Folding Dock Step With Wet-Grip Tread

Part name: Folding Dock Step With Wet-Grip Tread - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"length_mm": 225, "thickness_mm": 6, "width_mm": 130}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Folding Dock Step With Wet-Grip Tread'. The broader
use case is: Marinas and private docks often need a compact step that can fold away from walk paths
while remaining usable with wet footwear. The chosen deliverable is only the metal body implied by:
Hinged tread platform with side brackets, latch detail, and molded grip pattern. All other product
elements are external reference items and must not be modeled. The part must perform this mechanical
role: Provide a fold-down stepping surface with secure traction and a lockable stowed position. It
is intentionally included in the SubCAD limit corpus because: Challenges CAD with moving hinge
states, tread texture, lock geometry, load path through brackets, and stowed versus deployed
envelopes. The part is made from low-carbon steel, ASTM A36 or equivalent using sheet or plate
stock. Start from one flat sheet or plate blank. Cut the outside profile, machine holes, slots,
pockets, lips, and relief features into that same piece. If bends are called out, they are bends in
the same sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 225 mm x 130 mm x 6 mm.
- mounting hole pattern: Drill two through holes diameter 8 mm on the length centerline at X=26 mm and X=199 mm, Y=65 mm.
- functional center feature: Machine a central obround slot 75 mm long x 14 mm wide through the part, centered at X=112 mm, Y=65 mm.
- top relief pocket: Mill a rectangular relief pocket 56 mm x 43 mm x 2 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Folding Dock Step With Wet-Grip Tread'; this requirement is only for its chosen metal part.

---

## SMP-039-11 - Fuel Water Separator Bowl Wrench

Part name: Fuel Water Separator Bowl Wrench - single metal part

Material: AISI 316 stainless steel (corrosion resistance and cleanable metal surfaces)

Envelope: `{"height_mm": 59, "length_mm": 170, "width_mm": 100}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Fuel Water Separator Bowl Wrench'. The broader use
case is: Marine engine service includes removing clear separator bowls that can be slippery,
fragile, and hard to access below filters. The chosen deliverable is only the metal body implied by:
Cup-style wrench with scalloped inner grip ribs and offset handle socket. All other product elements
are external reference items and must not be modeled. The part must perform this mechanical role:
Grip a filter bowl evenly for removal without point loading the transparent housing. It is
intentionally included in the SubCAD limit corpus because: Tests thin cup geometry, internal rib
patterns, fragile-part contact control, offset tool clearance, and service orientation. The part is
made from AISI 316 stainless steel using rectangular block stock. Start from one rectangular metal
block or plate. Saw oversize, face all datum sides, then machine the pockets, holes, slots, angled
faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 170 mm x 100 mm x 59 mm.
- mounting hole pattern: Drill two through holes diameter 7 mm on the length centerline at X=20 mm and X=150 mm, Y=50 mm.
- functional center feature: Machine a central obround slot 56 mm long x 17 mm wide through the part, centered at X=85 mm, Y=50 mm.
- top relief pocket: Mill a rectangular relief pocket 42 mm x 33 mm x 6 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Fuel Water Separator Bowl Wrench'; this requirement is only for its chosen metal part.

---

## SMP-039-12 - Stern Drive Bellows Clamp Positioning Tool

Part name: Stern Drive Bellows Clamp Positioning Tool - single metal part

Material: 1045 medium-carbon steel, normalized (durable wear surface for workshop loading)

Envelope: `{"height_mm": 68, "length_mm": 135, "width_mm": 115}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Stern Drive Bellows Clamp Positioning Tool'. The
broader use case is: Stern drive bellows replacement requires placing clamps around flexible boots
in crowded transom assemblies. The chosen deliverable is only the metal body implied by: Curved
clamp guide with hooked end, handle, and visual seating reference. All other product elements are
external reference items and must not be modeled. The part must perform this mechanical role: Hold
and guide a clamp band into the proper seating area around a flexible bellows lip. It is
intentionally included in the SubCAD limit corpus because: Includes curved approach geometry,
interaction with flexible bellows, hidden seating references, and narrow access around adjacent
hardware. The part is made from 1045 medium-carbon steel, normalized using rectangular block stock.
Start from one rectangular metal block or plate. Saw oversize, face all datum sides, then machine
the pockets, holes, slots, angled faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 135 mm x 115 mm x 68 mm.
- mounting hole pattern: Drill two through holes diameter 6 mm on the length centerline at X=23 mm and X=112 mm, Y=57 mm.
- functional center feature: Machine a central obround slot 45 mm long x 11 mm wide through the part, centered at X=67 mm, Y=57 mm.
- top relief pocket: Mill a rectangular relief pocket 33 mm x 38 mm x 33 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- integral hook lip: Leave an integral hook lip on one short end, projecting 14 mm and undercut 3 mm for registration.

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
- Do not broaden the requirement back into the full product idea named 'Stern Drive Bellows Clamp Positioning Tool'; this requirement is only for its chosen metal part.

---

## SMP-039-13 - Mast Base Wiring Drip Loop Organizer

Part name: Mast Base Wiring Drip Loop Organizer - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"length_mm": 255, "thickness_mm": 5, "width_mm": 65}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Mast Base Wiring Drip Loop Organizer'. The broader
use case is: Sailboat mast wiring often enters through deck glands where wires need strain relief
and drip-loop organization to reduce leaks. The chosen deliverable is only the metal body implied
by: Low-profile cable guide plate with staggered saddles and drainage channels. All other product
elements are external reference items and must not be modeled. The part must perform this mechanical
role: Organize cable loops and guide water away from entry glands while keeping service access
clear. It is intentionally included in the SubCAD limit corpus because: Tests routed cable
management, drainage geometry, low-profile deck fit, multiple passage paths, and serviceable clamp
features. The part is made from low-carbon steel, ASTM A36 or equivalent using sheet or plate stock.
Start from one flat sheet or plate blank. Cut the outside profile, machine holes, slots, pockets,
lips, and relief features into that same piece. If bends are called out, they are bends in the same
sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 255 mm x 65 mm x 5 mm.
- mounting hole pattern: Drill two through holes diameter 11 mm on the length centerline at X=13 mm and X=242 mm, Y=32 mm.
- functional center feature: Machine a central obround slot 85 mm long x 7 mm wide through the part, centered at X=127 mm, Y=32 mm.
- top relief pocket: Mill a rectangular relief pocket 63 mm x 21 mm x 2 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Mast Base Wiring Drip Loop Organizer'; this requirement is only for its chosen metal part.

---

## SMP-039-14 - Marine Battery Box Tie-Down Rail

Part name: Marine Battery Box Tie-Down Rail - single metal part

Material: AISI 316 stainless steel (corrosion resistance and cleanable metal surfaces)

Envelope: `{"length_mm": 230, "thickness_mm": 6, "width_mm": 115}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Marine Battery Box Tie-Down Rail'. The broader use
case is: Boat batteries need secure retention while allowing inspection, ventilation, and quick
strap replacement in cramped lockers. The chosen deliverable is only the metal body implied by: Base
rail with strap slots, raised standoffs, and corner guards. All other product elements are external
reference items and must not be modeled. The part must perform this mechanical role: Provide a
corrosion-resistant rail system for routing retention straps around a battery box without blocking
lid access. It is intentionally included in the SubCAD limit corpus because: Combines strap path
modeling, raised supports, edge protection, access clearance, and load-bearing rail features. The
part is made from AISI 316 stainless steel using sheet or plate stock. Start from one flat sheet or
plate blank. Cut the outside profile, machine holes, slots, pockets, lips, and relief features into
that same piece. If bends are called out, they are bends in the same sheet part, not separate welded
pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 230 mm x 115 mm x 6 mm.
- mounting hole pattern: Drill two through holes diameter 10 mm on the length centerline at X=23 mm and X=207 mm, Y=57 mm.
- functional center feature: Machine a central obround slot 76 mm long x 14 mm wide through the part, centered at X=115 mm, Y=57 mm.
- top relief pocket: Mill a rectangular relief pocket 57 mm x 38 mm x 3 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Marine Battery Box Tie-Down Rail'; this requirement is only for its chosen metal part.

---

## SMP-039-15 - Dock Pedestal Cable Hanger

Part name: Dock Pedestal Cable Hanger - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 54, "length_mm": 120, "width_mm": 100}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Dock Pedestal Cable Hanger'. The broader use case
is: Marina shore-power cables often hang from dock pedestals and need organized storage that avoids
sharp bends and water pooling. The chosen deliverable is only the metal body implied by: Wall-
mounted curved hanger with drip grooves and locking retaining lip. All other product elements are
external reference items and must not be modeled. The part must perform this mechanical role: Hold
coiled shore-power cable off the deck with a smooth support surface and drainage-friendly shape. It
is intentionally included in the SubCAD limit corpus because: Requires large-radius support forms,
retaining lips, drainage grooves, mounting bosses, and weight-bearing wall interface. The part is
made from low-carbon steel, ASTM A36 or equivalent using rectangular block stock. Start from one
rectangular metal block or plate. Saw oversize, face all datum sides, then machine the pockets,
holes, slots, angled faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 120 mm x 100 mm x 54 mm.
- mounting hole pattern: Drill two through holes diameter 5 mm on the length centerline at X=20 mm and X=100 mm, Y=50 mm.
- functional center feature: Machine a central obround slot 40 mm long x 16 mm wide through the part, centered at X=60 mm, Y=50 mm.
- top relief pocket: Mill a rectangular relief pocket 30 mm x 33 mm x 23 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Dock Pedestal Cable Hanger'; this requirement is only for its chosen metal part.

---

## SMP-039-16 - Through-Hull Fitting Bedding Scraper

Part name: Through-Hull Fitting Bedding Scraper - single metal part

Material: AISI 316 stainless steel (corrosion resistance and cleanable metal surfaces)

Envelope: `{"height_mm": 37, "length_mm": 120, "width_mm": 60}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Through-Hull Fitting Bedding Scraper'. The broader
use case is: Marine refit work includes removing old sealant around through-hull fittings without
gouging hull laminate or metal flanges. The chosen deliverable is only the metal body implied by:
Curved scraper head with replaceable blade pocket and depth-limiting shoe. All other product
elements are external reference items and must not be modeled. The part must perform this mechanical
role: Scrape cured bedding compound around circular fittings while following flange curvature and
controlling blade depth. It is intentionally included in the SubCAD limit corpus because: Tests
circular-contact tooling, controlled blade projection, replaceable inserts, ergonomic handle angle,
and surface-following geometry. The part is made from AISI 316 stainless steel using rectangular
block stock. Start from one rectangular metal block or plate. Saw oversize, face all datum sides,
then machine the pockets, holes, slots, angled faces, grooves, and edge treatments into that same
solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 120 mm x 60 mm x 37 mm.
- mounting hole pattern: Drill two through holes diameter 12 mm on the length centerline at X=12 mm and X=108 mm, Y=30 mm.
- functional center feature: Machine a central obround slot 40 mm long x 11 mm wide through the part, centered at X=60 mm, Y=30 mm.
- top relief pocket: Mill a rectangular relief pocket 30 mm x 20 mm x 15 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- machined angled reference face: Machine one top reference face at 44 degrees over the last 24 mm of length.

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
- Do not broaden the requirement back into the full product idea named 'Through-Hull Fitting Bedding Scraper'; this requirement is only for its chosen metal part.

---

## SMP-039-17 - Anchor Roller Service Alignment Block

Part name: Anchor Roller Service Alignment Block - single metal part

Material: 4140 alloy steel, prehard (strong cylindrical metal part with threaded and slotted details)

Envelope: `{"axial_bore_diameter_mm": 17, "outer_diameter_mm": 86, "overall_length_mm": 117, "wall_minimum_mm": 34}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Anchor Roller Service Alignment Block'. The broader
use case is: Bow anchor rollers wear, bend, or misalign, making it difficult to center the roller,
pin, and chain path during replacement. The chosen deliverable is only the metal body implied by:
Removable alignment block with chain-groove reference and side cheek spacers. All other product
elements are external reference items and must not be modeled. The part must perform this mechanical
role: Temporarily align roller cheeks and chain path while a roller or pin is fitted. It is
intentionally included in the SubCAD limit corpus because: Combines channel geometry, removable
fixture logic, nested clearances between side plates, and alignment references for rotating parts.
The part is made from 4140 alloy steel, prehard using round bar stock. Start from one cut length of
round metal bar. Turn the outside, face both ends, bore the center, then mill secondary flats,
slots, and radial holes as needed. No separate inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 86 mm and length 117 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 17 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 27 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 28 mm wide over 109 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M8 holes through the top flat at X=39 mm and X=78 mm.
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
- Do not broaden the requirement back into the full product idea named 'Anchor Roller Service Alignment Block'; this requirement is only for its chosen metal part.

---

## SMP-039-18 - Scupper Flap Replacement Fixture

Part name: Scupper Flap Replacement Fixture - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 49, "length_mm": 95, "width_mm": 55}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Scupper Flap Replacement Fixture'. The broader use
case is: Deck scupper flaps degrade and are often serviced near curved transoms or cockpit drains
where alignment affects sealing. The chosen deliverable is only the metal body implied by: Curved
face fixture with flap pocket, hinge guide, and temporary clamp pads. All other product elements are
external reference items and must not be modeled. The part must perform this mechanical role: Hold a
replacement flap and hinge strip in position while fasteners are started and sealant is applied. It
is intentionally included in the SubCAD limit corpus because: Tests curved sealing faces, flexible
flap accommodation, hinge alignment, clamp pad placement, and wet-side drainage clearance. The part
is made from low-carbon steel, ASTM A36 or equivalent using rectangular block stock. Start from one
rectangular metal block or plate. Saw oversize, face all datum sides, then machine the pockets,
holes, slots, angled faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 95 mm x 55 mm x 49 mm.
- mounting hole pattern: Drill two through holes diameter 7 mm on the length centerline at X=11 mm and X=84 mm, Y=27 mm.
- functional center feature: Machine a central obround slot 31 mm long x 15 mm wide through the part, centered at X=47 mm, Y=27 mm.
- top relief pocket: Mill a rectangular relief pocket 25 mm x 18 mm x 10 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Scupper Flap Replacement Fixture'; this requirement is only for its chosen metal part.

---

## SMP-039-19 - Marine Hose Clamp Torque Access Driver

Part name: Marine Hose Clamp Torque Access Driver - single metal part

Material: AISI 316 stainless steel (corrosion resistance and cleanable metal surfaces)

Envelope: `{"axial_bore_diameter_mm": 15, "outer_diameter_mm": 47, "overall_length_mm": 95, "wall_minimum_mm": 16}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Marine Hose Clamp Torque Access Driver'. The
broader use case is: Engine rooms contain hose clamps on coolant, fuel, and exhaust hoses that are
hard to tighten consistently from awkward angles. The chosen deliverable is only the metal body
implied by: Offset driver head with guide sleeve, torque indicator body, and low-clearance handle.
All other product elements are external reference items and must not be modeled. The part must
perform this mechanical role: Reach clamp screws around hoses and fittings while keeping the driver
aligned and limiting over-tightening. It is intentionally included in the SubCAD limit corpus
because: Involves offset rotational axes, limited access envelopes, moving torque indicator
features, and hose-adjacent clearance geometry. The part is made from AISI 316 stainless steel using
round bar stock. Start from one cut length of round metal bar. Turn the outside, face both ends,
bore the center, then mill secondary flats, slots, and radial holes as needed. No separate inserts
or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 47 mm and length 95 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 15 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 25 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 15 mm wide over 87 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M5 holes through the top flat at X=31 mm and X=63 mm.
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
- Do not broaden the requirement back into the full product idea named 'Marine Hose Clamp Torque Access Driver'; this requirement is only for its chosen metal part.

---

## SMP-039-20 - Removable Swim Platform Cleat Adapter

Part name: Removable Swim Platform Cleat Adapter - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 29, "length_mm": 90, "width_mm": 70}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Removable Swim Platform Cleat Adapter'. The broader
use case is: Small boats sometimes need temporary tie-off points on swim platforms without permanent
hardware changes. The chosen deliverable is only the metal body implied by: Clamp-on cleat body with
padded jaws and integrated horn shape. All other product elements are external reference items and
must not be modeled. The part must perform this mechanical role: Clamp to a platform edge and
provide a temporary cleat surface with protective pads and anti-rotation features. It is
intentionally included in the SubCAD limit corpus because: Tests clamp jaw motion, soft pad
interfaces, cleat horn geometry, anti-rotation surfaces, and removable load path representation. The
part is made from low-carbon steel, ASTM A36 or equivalent using rectangular block stock. Start from
one rectangular metal block or plate. Saw oversize, face all datum sides, then machine the pockets,
holes, slots, angled faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 90 mm x 70 mm x 29 mm.
- mounting hole pattern: Drill two through holes diameter 7 mm on the length centerline at X=14 mm and X=76 mm, Y=35 mm.
- functional center feature: Machine a central obround slot 30 mm long x 7 mm wide through the part, centered at X=45 mm, Y=35 mm.
- top relief pocket: Mill a rectangular relief pocket 25 mm x 23 mm x 8 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Removable Swim Platform Cleat Adapter'; this requirement is only for its chosen metal part.

---

## SMP-039-21 - Bilge Pump Cartridge Twist Tool

Part name: Bilge Pump Cartridge Twist Tool - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 33, "length_mm": 115, "width_mm": 85}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Bilge Pump Cartridge Twist Tool'. The broader use
case is: Many bilge pumps use removable cartridges that can stick from grime, mineral deposits, or
poor hand access. The chosen deliverable is only the metal body implied by: Ring-shaped twist tool
with internal drive lugs and raised grip wings. All other product elements are external reference
items and must not be modeled. The part must perform this mechanical role: Engage the pump cartridge
tabs and apply twist leverage without breaking plastic pump features. It is intentionally included
in the SubCAD limit corpus because: Challenges CAD with internal lug geometry, bayonet engagement
logic, hand-grip forms, and clearance around pump housings. The part is made from low-carbon steel,
ASTM A36 or equivalent using rectangular block stock. Start from one rectangular metal block or
plate. Saw oversize, face all datum sides, then machine the pockets, holes, slots, angled faces,
grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 115 mm x 85 mm x 33 mm.
- mounting hole pattern: Drill two through holes diameter 5 mm on the length centerline at X=17 mm and X=98 mm, Y=42 mm.
- functional center feature: Machine a central obround slot 38 mm long x 18 mm wide through the part, centered at X=57 mm, Y=42 mm.
- top relief pocket: Mill a rectangular relief pocket 28 mm x 28 mm x 1 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Bilge Pump Cartridge Twist Tool'; this requirement is only for its chosen metal part.

---

## SMP-039-22 - Lifeline Gate Latch Alignment Spacer

Part name: Lifeline Gate Latch Alignment Spacer - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"length_mm": 155, "thickness_mm": 8, "width_mm": 110}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Lifeline Gate Latch Alignment Spacer'. The broader
use case is: Sailboat lifeline gates need repeatable latch alignment after stanchion service, cable
replacement, or gate hardware changes. The chosen deliverable is only the metal body implied by:
Clip-on spacer body with latch-reference pockets and cable clearance slots. All other product
elements are external reference items and must not be modeled. The part must perform this mechanical
role: Temporarily space and align gate latch parts while cable tension and terminal positions are
adjusted. It is intentionally included in the SubCAD limit corpus because: Tests slender clip
features, cable pass-throughs, latch pocket geometry, temporary assembly references, and small
hardware interaction. The part is made from low-carbon steel, ASTM A36 or equivalent using sheet or
plate stock. Start from one flat sheet or plate blank. Cut the outside profile, machine holes,
slots, pockets, lips, and relief features into that same piece. If bends are called out, they are
bends in the same sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 155 mm x 110 mm x 8 mm.
- mounting hole pattern: Drill two through holes diameter 13 mm on the length centerline at X=22 mm and X=133 mm, Y=55 mm.
- functional center feature: Machine a central obround slot 51 mm long x 12 mm wide through the part, centered at X=77 mm, Y=55 mm.
- top relief pocket: Mill a rectangular relief pocket 38 mm x 36 mm x 1 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- integral hook lip: Leave an integral hook lip on one short end, projecting 14 mm and undercut 3 mm for registration.

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
- Do not broaden the requirement back into the full product idea named 'Lifeline Gate Latch Alignment Spacer'; this requirement is only for its chosen metal part.

---

## SMP-039-23 - Dock Fender Rail Quick Clamp

Part name: Dock Fender Rail Quick Clamp - single metal part

Material: 1045 medium-carbon steel, normalized (durable wear surface for workshop loading)

Envelope: `{"axial_bore_diameter_mm": 14, "outer_diameter_mm": 72, "overall_length_mm": 101, "wall_minimum_mm": 29}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Dock Fender Rail Quick Clamp'. The broader use case
is: Dock fenders are frequently repositioned for different hull shapes and mooring conditions
without permanent dock modifications. The chosen deliverable is only the metal body implied by: Cam
clamp bracket with rounded rail saddle and line-retaining cleat. All other product elements are
external reference items and must not be modeled. The part must perform this mechanical role: Clamp
a fender line or fender body to a dock rail with quick repositioning and anti-slip grip. It is
intentionally included in the SubCAD limit corpus because: Involves cam action, rounded rail
contact, rope retention, textured grip pads, and variable dock rail profiles. The part is made from
1045 medium-carbon steel, normalized using round bar stock. Start from one cut length of round metal
bar. Turn the outside, face both ends, bore the center, then mill secondary flats, slots, and radial
holes as needed. No separate inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 72 mm and length 101 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 14 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 24 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 24 mm wide over 93 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M8 holes through the top flat at X=33 mm and X=67 mm.
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
- Do not broaden the requirement back into the full product idea named 'Dock Fender Rail Quick Clamp'; this requirement is only for its chosen metal part.

---

## SMP-039-24 - Impeller Vane Preload Sleeve

Part name: Impeller Vane Preload Sleeve - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 8, "outer_diameter_mm": 30, "overall_length_mm": 74, "wall_minimum_mm": 11}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Impeller Vane Preload Sleeve'. The broader use case
is: Raw-water pump impellers can be difficult to install because the flexible vanes must be folded
into the pump cavity direction. The chosen deliverable is only the metal body implied by: Split
tapered sleeve with internal vane guides and release tabs. All other product elements are external
reference items and must not be modeled. The part must perform this mechanical role: Compress and
orient impeller vanes before insertion into a pump housing. It is intentionally included in the
SubCAD limit corpus because: Requires representing flexible vane interaction, tapered internal
surfaces, split tool behavior, and directional guide features. The part is made from low-carbon
steel, ASTM A36 or equivalent using round bar stock. Start from one cut length of round metal bar.
Turn the outside, face both ends, bore the center, then mill secondary flats, slots, and radial
holes as needed. No separate inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 30 mm and length 74 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 8 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 18 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 10 mm wide over 66 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M8 holes through the top flat at X=24 mm and X=49 mm.
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
- Do not broaden the requirement back into the full product idea named 'Impeller Vane Preload Sleeve'; this requirement is only for its chosen metal part.

---

## SMP-039-25 - Cockpit Drain Strainer Lift Tool

Part name: Cockpit Drain Strainer Lift Tool - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 33, "length_mm": 150, "width_mm": 110}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Cockpit Drain Strainer Lift Tool'. The broader use
case is: Deck and cockpit drain strainers become stuck from sealant, corrosion, or debris and are
often too flush to grip by hand. The chosen deliverable is only the metal body implied by: Low-
profile pronged key with protective underside pad and cross handle. All other product elements are
external reference items and must not be modeled. The part must perform this mechanical role: Engage
strainer slots and lift or rotate the insert without damaging surrounding gelcoat. It is
intentionally included in the SubCAD limit corpus because: Tests prong-slot engagement, shallow
clearance, protective pad surfaces, rotational hand tool geometry, and delicate deck contact. The
part is made from low-carbon steel, ASTM A36 or equivalent using rectangular block stock. Start from
one rectangular metal block or plate. Saw oversize, face all datum sides, then machine the pockets,
holes, slots, angled faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 150 mm x 110 mm x 33 mm.
- mounting hole pattern: Drill two through holes diameter 11 mm on the length centerline at X=22 mm and X=128 mm, Y=55 mm.
- functional center feature: Machine a central obround slot 50 mm long x 17 mm wide through the part, centered at X=75 mm, Y=55 mm.
- top relief pocket: Mill a rectangular relief pocket 37 mm x 36 mm x 1 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Cockpit Drain Strainer Lift Tool'; this requirement is only for its chosen metal part.

---

## SMP-039-26 - Boat Cover Snap Stud Locator

Part name: Boat Cover Snap Stud Locator - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"length_mm": 100, "thickness_mm": 11, "width_mm": 45}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Boat Cover Snap Stud Locator'. The broader use case
is: Canvas shops and owners install snap fasteners on uneven deck edges and need consistent
placement relative to existing fabric snaps. The chosen deliverable is only the metal body implied
by: Adjustable locator strip with snap-receiving sockets and deck marking tips. All other product
elements are external reference items and must not be modeled. The part must perform this mechanical
role: Transfer snap positions from cover fabric to deck hardware locations while accounting for edge
curvature. It is intentionally included in the SubCAD limit corpus because: Combines adjustable
indexing, small socket features, fabric-to-deck transfer geometry, and curved edge reference
handling. The part is made from low-carbon steel, ASTM A36 or equivalent using sheet or plate stock.
Start from one flat sheet or plate blank. Cut the outside profile, machine holes, slots, pockets,
lips, and relief features into that same piece. If bends are called out, they are bends in the same
sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 100 mm x 45 mm x 11 mm.
- mounting hole pattern: Drill two through holes diameter 12 mm on the length centerline at X=10 mm and X=90 mm, Y=22 mm.
- functional center feature: Machine a central obround slot 33 mm long x 16 mm wide through the part, centered at X=50 mm, Y=22 mm.
- top relief pocket: Mill a rectangular relief pocket 25 mm x 18 mm x 3 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Boat Cover Snap Stud Locator'; this requirement is only for its chosen metal part.

---

## SMP-039-27 - Dock Ladder Standoff Foot

Part name: Dock Ladder Standoff Foot - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"length_mm": 215, "thickness_mm": 6, "width_mm": 150}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Dock Ladder Standoff Foot'. The broader use case
is: Dock ladders need replaceable feet that protect hulls, reduce dock wear, and adapt to uneven
mounting surfaces. The chosen deliverable is only the metal body implied by: Molded foot pad with
socket cup, ribbed contact face, and retention strap groove. All other product elements are external
reference items and must not be modeled. The part must perform this mechanical role: Provide a
cushioned standoff between a ladder leg and dock or hull-facing surface while resisting rotation. It
is intentionally included in the SubCAD limit corpus because: Tests soft pad geometry, socketed
tubular interfaces, ribbed contact surfaces, strap grooves, and non-slip orientation features. The
part is made from low-carbon steel, ASTM A36 or equivalent using sheet or plate stock. Start from
one flat sheet or plate blank. Cut the outside profile, machine holes, slots, pockets, lips, and
relief features into that same piece. If bends are called out, they are bends in the same sheet
part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 215 mm x 150 mm x 6 mm.
- mounting hole pattern: Drill two through holes diameter 10 mm on the length centerline at X=30 mm and X=185 mm, Y=75 mm.
- functional center feature: Machine a central obround slot 71 mm long x 18 mm wide through the part, centered at X=107 mm, Y=75 mm.
- top relief pocket: Mill a rectangular relief pocket 53 mm x 50 mm x 2 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Dock Ladder Standoff Foot'; this requirement is only for its chosen metal part.

---

## SMP-039-28 - Outboard Cowling Latch Inspection Prop

Part name: Outboard Cowling Latch Inspection Prop - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 29, "length_mm": 175, "width_mm": 60}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Outboard Cowling Latch Inspection Prop'. The
broader use case is: Service technicians inspect outboard engines with cowlings partially open,
where latches and seals can be awkward to hold clear. The chosen deliverable is only the metal body
implied by: Articulating prop arm with soft end pads and quick-lock hinge. All other product
elements are external reference items and must not be modeled. The part must perform this mechanical
role: Prop and stabilize an engine cowling during latch, gasket, and wiring inspection. It is
intentionally included in the SubCAD limit corpus because: Involves articulated states, soft contact
pads, hinge locking detail, irregular cowling contact, and service clearance representation. The
part is made from low-carbon steel, ASTM A36 or equivalent using rectangular block stock. Start from
one rectangular metal block or plate. Saw oversize, face all datum sides, then machine the pockets,
holes, slots, angled faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 175 mm x 60 mm x 29 mm.
- mounting hole pattern: Drill two through holes diameter 11 mm on the length centerline at X=12 mm and X=163 mm, Y=30 mm.
- functional center feature: Machine a central obround slot 58 mm long x 9 mm wide through the part, centered at X=87 mm, Y=30 mm.
- top relief pocket: Mill a rectangular relief pocket 43 mm x 20 mm x 2 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Outboard Cowling Latch Inspection Prop'; this requirement is only for its chosen metal part.

---

## SMP-039-29 - Deck Fill Cap Grip Adapter

Part name: Deck Fill Cap Grip Adapter - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 14, "outer_diameter_mm": 56, "overall_length_mm": 60, "wall_minimum_mm": 21}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Deck Fill Cap Grip Adapter'. The broader use case
is: Fuel, water, and waste deck fill caps can seize or become difficult to open without scratching
polished deck hardware. The chosen deliverable is only the metal body implied by: Round cap adapter
with keyed underside, protective skirt, and folding leverage handle. All other product elements are
external reference items and must not be modeled. The part must perform this mechanical role: Grip a
deck fill cap key pattern and provide leverage while protecting the surrounding deck ring. It is
intentionally included in the SubCAD limit corpus because: Tests keyed underside geometry,
protective skirt clearance, folding handle states, rotational tool contact, and polished-surface
protection. The part is made from low-carbon steel, ASTM A36 or equivalent using round bar stock.
Start from one cut length of round metal bar. Turn the outside, face both ends, bore the center,
then mill secondary flats, slots, and radial holes as needed. No separate inserts or fasteners are
part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 56 mm and length 60 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 14 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 24 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 18 mm wide over 52 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M4 holes through the top flat at X=20 mm and X=40 mm.
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
- Do not broaden the requirement back into the full product idea named 'Deck Fill Cap Grip Adapter'; this requirement is only for its chosen metal part.

---

## SMP-039-30 - Marina Hose Bib Anti-Drip Holster

Part name: Marina Hose Bib Anti-Drip Holster - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"length_mm": 130, "thickness_mm": 4, "width_mm": 110}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Marina Hose Bib Anti-Drip Holster'. The broader use
case is: Dockside washdown hoses and bibs often drip onto walkways or hang loosely from pedestals
after use. The chosen deliverable is only the metal body implied by: Pedestal-mounted holster cup
with angled rest, drain channel, and hose clip. All other product elements are external reference
items and must not be modeled. The part must perform this mechanical role: Hold a hose nozzle or bib
tail upward and route residual water into a small drain path. It is intentionally included in the
SubCAD limit corpus because: Combines angled support, water drainage, cylindrical hose capture, wall
mounting, and open cup geometry in a dock environment. The part is made from low-carbon steel, ASTM
A36 or equivalent using sheet or plate stock. Start from one flat sheet or plate blank. Cut the
outside profile, machine holes, slots, pockets, lips, and relief features into that same piece. If
bends are called out, they are bends in the same sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 130 mm x 110 mm x 4 mm.
- mounting hole pattern: Drill two through holes diameter 7 mm on the length centerline at X=22 mm and X=108 mm, Y=55 mm.
- functional center feature: Machine a central obround slot 43 mm long x 11 mm wide through the part, centered at X=65 mm, Y=55 mm.
- top relief pocket: Mill a rectangular relief pocket 32 mm x 36 mm x 2 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- machined angled reference face: Machine one top reference face at 27 degrees over the last 26 mm of length.
- integral hook lip: Leave an integral hook lip on one short end, projecting 9 mm and undercut 3 mm for registration.

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
- Do not broaden the requirement back into the full product idea named 'Marina Hose Bib Anti-Drip Holster'; this requirement is only for its chosen metal part.

---
