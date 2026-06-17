# Agent 040 Single Metal Part Requirements

Domain: vending machines, kiosks, ticketing machines, coin/bill handling, and public-payment service hardware

Each item below is one metal part only. Product assemblies and nonmetal components are explicitly out of scope.

## SMP-040-01 - Modular vending machine product spiral tray

Part name: Modular vending machine product spiral tray - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"length_mm": 105, "thickness_mm": 9, "width_mm": 90}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Modular vending machine product spiral tray'. The
broader use case is: A snack vending machine uses removable trays that guide packaged products
toward a dispensing bay while allowing quick restocking. The chosen deliverable is only the metal
body implied by: A molded tray insert with repeated channel dividers, retention lips, and mounting
features. All other product elements are external reference items and must not be modeled. The part
must perform this mechanical role: Hold products in separate lanes and advance them toward the
customer pickup area. It is intentionally included in the SubCAD limit corpus because: The part
combines repeated cavities, thin walls, rounded product guides, and alignment details that challenge
patterning and feature hierarchy. The part is made from low-carbon steel, ASTM A36 or equivalent
using sheet or plate stock. Start from one flat sheet or plate blank. Cut the outside profile,
machine holes, slots, pockets, lips, and relief features into that same piece. If bends are called
out, they are bends in the same sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 105 mm x 90 mm x 9 mm.
- mounting hole pattern: Drill two through holes diameter 6 mm on the length centerline at X=18 mm and X=87 mm, Y=45 mm.
- functional center feature: Machine a central obround slot 35 mm long x 10 mm wide through the part, centered at X=52 mm, Y=45 mm.
- top relief pocket: Mill a rectangular relief pocket 26 mm x 30 mm x 2 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Modular vending machine product spiral tray'; this requirement is only for its chosen metal part.

---

## SMP-040-02 - Outdoor kiosk weather hood

Part name: Outdoor kiosk weather hood - single metal part

Material: 6061-T6 aluminum (low mass with good machinability and stable flat features)

Envelope: `{"height_mm": 28, "length_mm": 165, "width_mm": 35}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Outdoor kiosk weather hood'. The broader use case
is: A public payment kiosk needs a protective hood around its screen and card reader for exposure to
rain and glare. The chosen deliverable is only the metal body implied by: A formed front canopy with
side cheeks, drip edges, and integrated fastener bosses. All other product elements are external
reference items and must not be modeled. The part must perform this mechanical role: Shield user-
facing controls while preserving access, visibility, and drainage. It is intentionally included in
the SubCAD limit corpus because: The geometry requires angled surfaces, overhangs, recessed service
zones, and subtle edge treatments in one coherent shell. The part is made from 6061-T6 aluminum
using rectangular block stock. Start from one rectangular metal block or plate. Saw oversize, face
all datum sides, then machine the pockets, holes, slots, angled faces, grooves, and edge treatments
into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 165 mm x 35 mm x 28 mm.
- mounting hole pattern: Drill two through holes diameter 6 mm on the length centerline at X=10 mm and X=155 mm, Y=17 mm.
- functional center feature: Machine a central obround slot 55 mm long x 16 mm wide through the part, centered at X=82 mm, Y=17 mm.
- top relief pocket: Mill a rectangular relief pocket 41 mm x 18 mm x 3 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- machined angled reference face: Machine one top reference face at 14 degrees over the last 33 mm of length.

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
- Do not broaden the requirement back into the full product idea named 'Outdoor kiosk weather hood'; this requirement is only for its chosen metal part.

---

## SMP-040-03 - Ticket machine printer paper guide

Part name: Ticket machine printer paper guide - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 35, "length_mm": 120, "width_mm": 80}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Ticket machine printer paper guide'. The broader
use case is: A transit ticketing machine routes printed tickets from an internal printer to a
customer-accessible slot. The chosen deliverable is only the metal body implied by: A curved chute
with anti-snag ribs, access cutouts, and latch tabs. All other product elements are external
reference items and must not be modeled. The part must perform this mechanical role: Guide flexible
paper through a smooth path without jams or snag points. It is intentionally included in the SubCAD
limit corpus because: The design tests curved internal passages, smooth transitions, thin rib
networks, and serviceable enclosure features. The part is made from low-carbon steel, ASTM A36 or
equivalent using rectangular block stock. Start from one rectangular metal block or plate. Saw
oversize, face all datum sides, then machine the pockets, holes, slots, angled faces, grooves, and
edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 120 mm x 80 mm x 35 mm.
- mounting hole pattern: Drill two through holes diameter 10 mm on the length centerline at X=16 mm and X=104 mm, Y=40 mm.
- functional center feature: Machine a central obround slot 40 mm long x 14 mm wide through the part, centered at X=60 mm, Y=40 mm.
- top relief pocket: Mill a rectangular relief pocket 30 mm x 26 mm x 14 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Ticket machine printer paper guide'; this requirement is only for its chosen metal part.

---

## SMP-040-04 - Coin validator removable funnel

Part name: Coin validator removable funnel - single metal part

Material: 6061-T6 aluminum (low mass with good machinability and stable flat features)

Envelope: `{"height_mm": 50, "length_mm": 125, "width_mm": 115}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Coin validator removable funnel'. The broader use
case is: A coin-operated kiosk directs inserted coins from the entry bezel into a validation module.
The chosen deliverable is only the metal body implied by: A tapered funnel with mounting ears, anti-
bounce surfaces, and a narrow exit throat. All other product elements are external reference items
and must not be modeled. The part must perform this mechanical role: Collect coins from a broad
entry zone and deliver them consistently to the validator throat. It is intentionally included in
the SubCAD limit corpus because: The part mixes freeform tapering, gravity-fed flow surfaces,
mounting geometry, and clearance-sensitive exit features. The part is made from 6061-T6 aluminum
using rectangular block stock. Start from one rectangular metal block or plate. Saw oversize, face
all datum sides, then machine the pockets, holes, slots, angled faces, grooves, and edge treatments
into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 125 mm x 115 mm x 50 mm.
- mounting hole pattern: Drill two through holes diameter 6 mm on the length centerline at X=23 mm and X=102 mm, Y=57 mm.
- functional center feature: Machine a central obround slot 41 mm long x 18 mm wide through the part, centered at X=62 mm, Y=57 mm.
- top relief pocket: Mill a rectangular relief pocket 31 mm x 38 mm x 12 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- machined angled reference face: Machine one top reference face at 10 degrees over the last 25 mm of length.

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
- Do not broaden the requirement back into the full product idea named 'Coin validator removable funnel'; this requirement is only for its chosen metal part.

---

## SMP-040-05 - Bill acceptor service cassette handle

Part name: Bill acceptor service cassette handle - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 64, "length_mm": 80, "width_mm": 35}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Bill acceptor service cassette handle'. The broader
use case is: A bill-handling cabinet includes a removable cash cassette for secure collection and
maintenance. The chosen deliverable is only the metal body implied by: A reinforced pull handle with
recessed grip geometry, latch clearance, and security indexing. All other product elements are
external reference items and must not be modeled. The part must perform this mechanical role:
Provide a durable grip and keyed interface for removing a cash cassette from the machine. It is
intentionally included in the SubCAD limit corpus because: The handle needs ergonomic contours,
internal reinforcement, asymmetric latch reliefs, and manufacturable transitions. The part is made
from low-carbon steel, ASTM A36 or equivalent using rectangular block stock. Start from one
rectangular metal block or plate. Saw oversize, face all datum sides, then machine the pockets,
holes, slots, angled faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 80 mm x 35 mm x 64 mm.
- mounting hole pattern: Drill two through holes diameter 13 mm on the length centerline at X=10 mm and X=70 mm, Y=17 mm.
- functional center feature: Machine a central obround slot 30 mm long x 13 mm wide through the part, centered at X=40 mm, Y=17 mm.
- top relief pocket: Mill a rectangular relief pocket 25 mm x 18 mm x 4 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Bill acceptor service cassette handle'; this requirement is only for its chosen metal part.

---

## SMP-040-06 - Parking pay station coin return cup

Part name: Parking pay station coin return cup - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 37, "length_mm": 145, "width_mm": 55}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Parking pay station coin return cup'. The broader
use case is: A parking pay station returns rejected coins or change to a shallow customer retrieval
area. The chosen deliverable is only the metal body implied by: A recessed cup insert with scooped
floor, raised front lip, and drain features. All other product elements are external reference items
and must not be modeled. The part must perform this mechanical role: Receive falling coins and make
them easy to remove while preventing spill-out. It is intentionally included in the SubCAD limit
corpus because: The object tests concave surfaces, user-access ergonomics, lip profiles, and small
functional openings. The part is made from low-carbon steel, ASTM A36 or equivalent using
rectangular block stock. Start from one rectangular metal block or plate. Saw oversize, face all
datum sides, then machine the pockets, holes, slots, angled faces, grooves, and edge treatments into
that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 145 mm x 55 mm x 37 mm.
- mounting hole pattern: Drill two through holes diameter 7 mm on the length centerline at X=11 mm and X=134 mm, Y=27 mm.
- functional center feature: Machine a central obround slot 48 mm long x 8 mm wide through the part, centered at X=72 mm, Y=27 mm.
- top relief pocket: Mill a rectangular relief pocket 36 mm x 18 mm x 18 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Parking pay station coin return cup'; this requirement is only for its chosen metal part.

---

## SMP-040-07 - Self-service kiosk card reader bezel

Part name: Self-service kiosk card reader bezel - single metal part

Material: 6061-T6 aluminum (low mass with good machinability and stable flat features)

Envelope: `{"length_mm": 135, "thickness_mm": 8, "width_mm": 70}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Self-service kiosk card reader bezel'. The broader
use case is: A payment kiosk presents a card reader module through a vandal-resistant front panel.
The chosen deliverable is only the metal body implied by: A contoured bezel with chamfered lead-in,
screw covers, and anti-pry flanges. All other product elements are external reference items and must
not be modeled. The part must perform this mechanical role: Frame the payment reader, guide card
insertion, and protect surrounding enclosure edges. It is intentionally included in the SubCAD limit
corpus because: The part requires nested openings, precise front-facing contours, hidden attachment
details, and durable edge geometry. The part is made from 6061-T6 aluminum using sheet or plate
stock. Start from one flat sheet or plate blank. Cut the outside profile, machine holes, slots,
pockets, lips, and relief features into that same piece. If bends are called out, they are bends in
the same sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 135 mm x 70 mm x 8 mm.
- mounting hole pattern: Drill two through holes diameter 13 mm on the length centerline at X=14 mm and X=121 mm, Y=35 mm.
- functional center feature: Machine a central obround slot 45 mm long x 9 mm wide through the part, centered at X=67 mm, Y=35 mm.
- top relief pocket: Mill a rectangular relief pocket 33 mm x 23 mm x 3 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Self-service kiosk card reader bezel'; this requirement is only for its chosen metal part.

---

## SMP-040-08 - Transit gate token escrow door

Part name: Transit gate token escrow door - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"length_mm": 180, "thickness_mm": 9, "width_mm": 55}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Transit gate token escrow door'. The broader use
case is: A fare machine temporarily holds a token before routing it to acceptance or return paths.
The chosen deliverable is only the metal body implied by: A pivoting gate plate with axle bosses,
stop tabs, and contoured token contact faces. All other product elements are external reference
items and must not be modeled. The part must perform this mechanical role: Block or release a small
payment token while aligning it with downstream tracks. It is intentionally included in the SubCAD
limit corpus because: The mechanism tests rotational features, contact surfaces, thin plate
strength, and precise stop geometry. The part is made from low-carbon steel, ASTM A36 or equivalent
using sheet or plate stock. Start from one flat sheet or plate blank. Cut the outside profile,
machine holes, slots, pockets, lips, and relief features into that same piece. If bends are called
out, they are bends in the same sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 180 mm x 55 mm x 9 mm.
- mounting hole pattern: Drill two through holes diameter 5 mm on the length centerline at X=11 mm and X=169 mm, Y=27 mm.
- functional center feature: Machine a central obround slot 60 mm long x 11 mm wide through the part, centered at X=90 mm, Y=27 mm.
- top relief pocket: Mill a rectangular relief pocket 45 mm x 18 mm x 1 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Transit gate token escrow door'; this requirement is only for its chosen metal part.

---

## SMP-040-09 - Vending pickup bay anti-theft flap

Part name: Vending pickup bay anti-theft flap - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"length_mm": 235, "thickness_mm": 7, "width_mm": 75}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Vending pickup bay anti-theft flap'. The broader
use case is: A vending machine pickup bay needs a barrier that allows product retrieval but
discourages reach-in theft. The chosen deliverable is only the metal body implied by: A hinged flap
with curved shield face, side pivots, and weighted return detail. All other product elements are
external reference items and must not be modeled. The part must perform this mechanical role: Swing
open for customer access while blocking direct access to the storage area. It is intentionally
included in the SubCAD limit corpus because: The design includes a moving panel, curved blocking
surfaces, hinge geometry, and clearance-aware side features. The part is made from low-carbon steel,
ASTM A36 or equivalent using sheet or plate stock. Start from one flat sheet or plate blank. Cut the
outside profile, machine holes, slots, pockets, lips, and relief features into that same piece. If
bends are called out, they are bends in the same sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 235 mm x 75 mm x 7 mm.
- mounting hole pattern: Drill two through holes diameter 5 mm on the length centerline at X=15 mm and X=220 mm, Y=37 mm.
- functional center feature: Machine a central obround slot 78 mm long x 17 mm wide through the part, centered at X=117 mm, Y=37 mm.
- top relief pocket: Mill a rectangular relief pocket 58 mm x 25 mm x 2 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Vending pickup bay anti-theft flap'; this requirement is only for its chosen metal part.

---

## SMP-040-10 - Kiosk receipt bin overflow guard

Part name: Kiosk receipt bin overflow guard - single metal part

Material: 6061-T6 aluminum (low mass with good machinability and stable flat features)

Envelope: `{"length_mm": 250, "thickness_mm": 10, "width_mm": 65}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Kiosk receipt bin overflow guard'. The broader use
case is: A public kiosk with a receipt printer needs a front insert that prevents loose paper from
clogging the exit area. The chosen deliverable is only the metal body implied by: A sloped paper
guard with raised side rails, tear-edge clearance, and snap mounts. All other product elements are
external reference items and must not be modeled. The part must perform this mechanical role: Guide
receipts outward and keep abandoned paper away from the printer mouth. It is intentionally included
in the SubCAD limit corpus because: The part tests shallow angled planes, thin guide rails, snap-fit
details, and printer-adjacent clearances. The part is made from 6061-T6 aluminum using sheet or
plate stock. Start from one flat sheet or plate blank. Cut the outside profile, machine holes,
slots, pockets, lips, and relief features into that same piece. If bends are called out, they are
bends in the same sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 250 mm x 65 mm x 10 mm.
- mounting hole pattern: Drill two through holes diameter 12 mm on the length centerline at X=13 mm and X=237 mm, Y=32 mm.
- functional center feature: Machine a central obround slot 83 mm long x 13 mm wide through the part, centered at X=125 mm, Y=32 mm.
- top relief pocket: Mill a rectangular relief pocket 62 mm x 21 mm x 5 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- machined angled reference face: Machine one top reference face at 32 degrees over the last 50 mm of length.

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
- Do not broaden the requirement back into the full product idea named 'Kiosk receipt bin overflow guard'; this requirement is only for its chosen metal part.

---

## SMP-040-11 - Bill stacker compression paddle

Part name: Bill stacker compression paddle - single metal part

Material: 1045 medium-carbon steel, normalized (durable wear surface for workshop loading)

Envelope: `{"height_mm": 64, "length_mm": 205, "width_mm": 70}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Bill stacker compression paddle'. The broader use
case is: A bill acceptor stacks inserted banknotes into a secure cassette after validation. The
chosen deliverable is only the metal body implied by: A flat paddle with compliant ribs, guide
slots, and reinforced actuator connection. All other product elements are external reference items
and must not be modeled. The part must perform this mechanical role: Push flexible bills into a
compact stack while avoiding wrinkling or misalignment. It is intentionally included in the SubCAD
limit corpus because: It challenges representation of thin broad surfaces, structural ribbing,
sliding interfaces, and soft-contact geometry. The part is made from 1045 medium-carbon steel,
normalized using rectangular block stock. Start from one rectangular metal block or plate. Saw
oversize, face all datum sides, then machine the pockets, holes, slots, angled faces, grooves, and
edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 205 mm x 70 mm x 64 mm.
- mounting hole pattern: Drill two through holes diameter 6 mm on the length centerline at X=14 mm and X=191 mm, Y=35 mm.
- functional center feature: Machine a central obround slot 68 mm long x 18 mm wide through the part, centered at X=102 mm, Y=35 mm.
- top relief pocket: Mill a rectangular relief pocket 51 mm x 23 mm x 25 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Bill stacker compression paddle'; this requirement is only for its chosen metal part.

---

## SMP-040-12 - Kiosk speaker grille insert

Part name: Kiosk speaker grille insert - single metal part

Material: 6061-T6 aluminum (low mass with good machinability and stable flat features)

Envelope: `{"height_mm": 30, "length_mm": 205, "width_mm": 110}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Kiosk speaker grille insert'. The broader use case
is: An information kiosk provides audio prompts through a protected front-panel speaker area. The
chosen deliverable is only the metal body implied by: A perforated grille insert with rear
standoffs, outer frame, and drainage channels. All other product elements are external reference
items and must not be modeled. The part must perform this mechanical role: Allow sound transmission
while protecting the speaker from tampering and debris. It is intentionally included in the SubCAD
limit corpus because: The part uses repeated openings, thin webs, enclosure mating features, and
small environmental details. The part is made from 6061-T6 aluminum using rectangular block stock.
Start from one rectangular metal block or plate. Saw oversize, face all datum sides, then machine
the pockets, holes, slots, angled faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 205 mm x 110 mm x 30 mm.
- mounting hole pattern: Drill two through holes diameter 10 mm on the length centerline at X=22 mm and X=183 mm, Y=55 mm.
- functional center feature: Machine a central obround slot 68 mm long x 9 mm wide through the part, centered at X=102 mm, Y=55 mm.
- top relief pocket: Mill a rectangular relief pocket 51 mm x 36 mm x 1 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Kiosk speaker grille insert'; this requirement is only for its chosen metal part.

---

## SMP-040-13 - Ticket dispenser tear bar carrier

Part name: Ticket dispenser tear bar carrier - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 57, "length_mm": 110, "width_mm": 75}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Ticket dispenser tear bar carrier'. The broader use
case is: A ticket vending unit lets users tear printed passes cleanly at the exit slot. The chosen
deliverable is only the metal body implied by: A carrier rail with serration support, paper
clearance slot, and fastening lands. All other product elements are external reference items and
must not be modeled. The part must perform this mechanical role: Support a serrated tear edge and
align paper as it exits the printer path. It is intentionally included in the SubCAD limit corpus
because: The representation must capture sharp functional edges, long narrow features, slot
geometry, and mounting pads. The part is made from low-carbon steel, ASTM A36 or equivalent using
rectangular block stock. Start from one rectangular metal block or plate. Saw oversize, face all
datum sides, then machine the pockets, holes, slots, angled faces, grooves, and edge treatments into
that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 110 mm x 75 mm x 57 mm.
- mounting hole pattern: Drill two through holes diameter 10 mm on the length centerline at X=15 mm and X=95 mm, Y=37 mm.
- functional center feature: Machine a central obround slot 36 mm long x 17 mm wide through the part, centered at X=55 mm, Y=37 mm.
- top relief pocket: Mill a rectangular relief pocket 27 mm x 25 mm x 15 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- serrated contact edge: Cut 5 equal triangular serrations across the rear edge, each 4 mm deep.

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
- Do not broaden the requirement back into the full product idea named 'Ticket dispenser tear bar carrier'; this requirement is only for its chosen metal part.

---

## SMP-040-14 - Coin hopper outlet gate

Part name: Coin hopper outlet gate - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 24, "length_mm": 185, "width_mm": 95}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Coin hopper outlet gate'. The broader use case is:
A change-making machine meters coins from a hopper into a payout chute. The chosen deliverable is
only the metal body implied by: A sliding gate with shaped coin pocket, guide ribs, and actuator
tab. All other product elements are external reference items and must not be modeled. The part must
perform this mechanical role: Control coin release from the hopper while resisting jams and wear. It
is intentionally included in the SubCAD limit corpus because: The part combines sliding constraints,
shallow pockets, ribbed guidance, and wear-sensitive contact edges. The part is made from low-carbon
steel, ASTM A36 or equivalent using rectangular block stock. Start from one rectangular metal block
or plate. Saw oversize, face all datum sides, then machine the pockets, holes, slots, angled faces,
grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 185 mm x 95 mm x 24 mm.
- mounting hole pattern: Drill two through holes diameter 12 mm on the length centerline at X=19 mm and X=166 mm, Y=47 mm.
- functional center feature: Machine a central obround slot 61 mm long x 11 mm wide through the part, centered at X=92 mm, Y=47 mm.
- top relief pocket: Mill a rectangular relief pocket 46 mm x 31 mm x 3 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Coin hopper outlet gate'; this requirement is only for its chosen metal part.

---

## SMP-040-15 - Public kiosk maintenance latch cover

Part name: Public kiosk maintenance latch cover - single metal part

Material: 6061-T6 aluminum (low mass with good machinability and stable flat features)

Envelope: `{"length_mm": 135, "thickness_mm": 9, "width_mm": 50}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Public kiosk maintenance latch cover'. The broader
use case is: A streetside service kiosk hides its maintenance latch behind a small tamper-resistant
cover. The chosen deliverable is only the metal body implied by: A flush cover plate with recessed
key access, hinge knuckles, and pry-resistant perimeter. All other product elements are external
reference items and must not be modeled. The part must perform this mechanical role: Protect a
service latch from casual access while allowing authorized opening. It is intentionally included in
the SubCAD limit corpus because: It tests flush surface alignment, small hinge details, recessed
access geometry, and security-driven edge profiles. The part is made from 6061-T6 aluminum using
sheet or plate stock. Start from one flat sheet or plate blank. Cut the outside profile, machine
holes, slots, pockets, lips, and relief features into that same piece. If bends are called out, they
are bends in the same sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 135 mm x 50 mm x 9 mm.
- mounting hole pattern: Drill two through holes diameter 8 mm on the length centerline at X=10 mm and X=125 mm, Y=25 mm.
- functional center feature: Machine a central obround slot 45 mm long x 17 mm wide through the part, centered at X=67 mm, Y=25 mm.
- top relief pocket: Mill a rectangular relief pocket 33 mm x 18 mm x 4 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Public kiosk maintenance latch cover'; this requirement is only for its chosen metal part.

---

## SMP-040-16 - Reverse vending bottle entry throat

Part name: Reverse vending bottle entry throat - single metal part

Material: 4140 alloy steel, prehard (strong cylindrical metal part with threaded and slotted details)

Envelope: `{"axial_bore_diameter_mm": 14, "outer_diameter_mm": 72, "overall_length_mm": 80, "wall_minimum_mm": 29}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Reverse vending bottle entry throat'. The broader
use case is: A recycling machine accepts containers through a guided entry before scanning and
sorting. The chosen deliverable is only the metal body implied by: A rounded entry throat with
funnel ribs, shield baffles, and sensor windows. All other product elements are external reference
items and must not be modeled. The part must perform this mechanical role: Center an inserted
container and discourage users from reaching into the machine. It is intentionally included in the
SubCAD limit corpus because: The shape requires blended openings, internal baffles, repeated guide
ribs, and transparent sensor clearance zones. The part is made from 4140 alloy steel, prehard using
round bar stock. Start from one cut length of round metal bar. Turn the outside, face both ends,
bore the center, then mill secondary flats, slots, and radial holes as needed. No separate inserts
or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 72 mm and length 80 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 14 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 24 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 24 mm wide over 72 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M8 holes through the top flat at X=26 mm and X=53 mm.
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
- Do not broaden the requirement back into the full product idea named 'Reverse vending bottle entry throat'; this requirement is only for its chosen metal part.

---

## SMP-040-17 - Kiosk barcode scanner shroud

Part name: Kiosk barcode scanner shroud - single metal part

Material: 6061-T6 aluminum (low mass with good machinability and stable flat features)

Envelope: `{"height_mm": 65, "length_mm": 90, "width_mm": 75}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Kiosk barcode scanner shroud'. The broader use case
is: A ticketing kiosk includes a scanner window for reading mobile tickets and printed codes. The
chosen deliverable is only the metal body implied by: A recessed shroud with angled walls, window
frame, and anti-glare hood. All other product elements are external reference items and must not be
modeled. The part must perform this mechanical role: Shade the scanner, guide user placement, and
protect the scan window. It is intentionally included in the SubCAD limit corpus because: The design
challenges angled recesses, frame geometry, line-of-sight constraints, and user-facing surface
transitions. The part is made from 6061-T6 aluminum using rectangular block stock. Start from one
rectangular metal block or plate. Saw oversize, face all datum sides, then machine the pockets,
holes, slots, angled faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 90 mm x 75 mm x 65 mm.
- mounting hole pattern: Drill two through holes diameter 10 mm on the length centerline at X=15 mm and X=75 mm, Y=37 mm.
- functional center feature: Machine a central obround slot 30 mm long x 13 mm wide through the part, centered at X=45 mm, Y=37 mm.
- top relief pocket: Mill a rectangular relief pocket 25 mm x 25 mm x 17 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- machined angled reference face: Machine one top reference face at 29 degrees over the last 18 mm of length.

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
- Do not broaden the requirement back into the full product idea named 'Kiosk barcode scanner shroud'; this requirement is only for its chosen metal part.

---

## SMP-040-18 - Coin sorting rail segment

Part name: Coin sorting rail segment - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 69, "length_mm": 175, "width_mm": 60}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Coin sorting rail segment'. The broader use case
is: A coin handling module routes coins by size and path after initial validation. The chosen
deliverable is only the metal body implied by: A rail segment with curved track bed, retaining wall,
and adjustable stop interface. All other product elements are external reference items and must not
be modeled. The part must perform this mechanical role: Guide rolling coins along a controlled track
toward sorting features. It is intentionally included in the SubCAD limit corpus because: The part
tests narrow curved channels, rolling contact surfaces, retention geometry, and modular alignment
features. The part is made from low-carbon steel, ASTM A36 or equivalent using rectangular block
stock. Start from one rectangular metal block or plate. Saw oversize, face all datum sides, then
machine the pockets, holes, slots, angled faces, grooves, and edge treatments into that same solid
piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 175 mm x 60 mm x 69 mm.
- mounting hole pattern: Drill two through holes diameter 13 mm on the length centerline at X=12 mm and X=163 mm, Y=30 mm.
- functional center feature: Machine a central obround slot 58 mm long x 16 mm wide through the part, centered at X=87 mm, Y=30 mm.
- top relief pocket: Mill a rectangular relief pocket 43 mm x 20 mm x 12 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Coin sorting rail segment'; this requirement is only for its chosen metal part.

---

## SMP-040-19 - Bill acceptor entry mouth

Part name: Bill acceptor entry mouth - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 8, "outer_diameter_mm": 29, "overall_length_mm": 24, "wall_minimum_mm": 10}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Bill acceptor entry mouth'. The broader use case
is: A payment terminal guides banknotes from the exterior bezel into internal feed rollers. The
chosen deliverable is only the metal body implied by: A tapered entry mouth with rounded lips,
central guide ribs, and sensor clearance. All other product elements are external reference items
and must not be modeled. The part must perform this mechanical role: Lead bills into the transport
path while rejecting folded corners and misfeeds. It is intentionally included in the SubCAD limit
corpus because: It needs smooth funnel geometry, thin alignment ribs, integrated openings, and
careful front-to-back transitions. The part is made from low-carbon steel, ASTM A36 or equivalent
using round bar stock. Start from one cut length of round metal bar. Turn the outside, face both
ends, bore the center, then mill secondary flats, slots, and radial holes as needed. No separate
inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 29 mm and length 24 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 8 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 18 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 9 mm wide over 16 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M6 holes through the top flat at X=8 mm and X=16 mm.
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
- Do not broaden the requirement back into the full product idea named 'Bill acceptor entry mouth'; this requirement is only for its chosen metal part.

---

## SMP-040-20 - Laundry payment kiosk coin vault liner

Part name: Laundry payment kiosk coin vault liner - single metal part

Material: 6061-T6 aluminum (low mass with good machinability and stable flat features)

Envelope: `{"height_mm": 20, "length_mm": 75, "width_mm": 50}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Laundry payment kiosk coin vault liner'. The
broader use case is: A shared laundry payment station stores collected coins in a removable secure
vault. The chosen deliverable is only the metal body implied by: A drop-in liner with sloped floor,
impact ribs, and keyed locating tabs. All other product elements are external reference items and
must not be modeled. The part must perform this mechanical role: Protect the vault interior from
abrasion and guide coins away from the access door. It is intentionally included in the SubCAD limit
corpus because: The model combines sloping internal planes, abrasion ribs, keyed placement features,
and enclosure-fit tolerances. The part is made from 6061-T6 aluminum using rectangular block stock.
Start from one rectangular metal block or plate. Saw oversize, face all datum sides, then machine
the pockets, holes, slots, angled faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 75 mm x 50 mm x 20 mm.
- mounting hole pattern: Drill two through holes diameter 10 mm on the length centerline at X=10 mm and X=65 mm, Y=25 mm.
- functional center feature: Machine a central obround slot 30 mm long x 18 mm wide through the part, centered at X=37 mm, Y=25 mm.
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
- Do not broaden the requirement back into the full product idea named 'Laundry payment kiosk coin vault liner'; this requirement is only for its chosen metal part.

---

## SMP-040-21 - Vending machine cup drop carousel plate

Part name: Vending machine cup drop carousel plate - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"length_mm": 100, "thickness_mm": 7, "width_mm": 85}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Vending machine cup drop carousel plate'. The
broader use case is: A beverage vending machine separates stacked cups before drink dispensing. The
chosen deliverable is only the metal body implied by: A rotating plate with scalloped pockets,
center hub, and retaining edge details. All other product elements are external reference items and
must not be modeled. The part must perform this mechanical role: Index cup stacks and release a
single cup into the filling area. It is intentionally included in the SubCAD limit corpus because:
The part challenges radial repetition, curved pocket cutouts, hub geometry, and moving-system
clearances. The part is made from low-carbon steel, ASTM A36 or equivalent using sheet or plate
stock. Start from one flat sheet or plate blank. Cut the outside profile, machine holes, slots,
pockets, lips, and relief features into that same piece. If bends are called out, they are bends in
the same sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 100 mm x 85 mm x 7 mm.
- mounting hole pattern: Drill two through holes diameter 12 mm on the length centerline at X=17 mm and X=83 mm, Y=42 mm.
- functional center feature: Machine a central obround slot 33 mm long x 11 mm wide through the part, centered at X=50 mm, Y=42 mm.
- top relief pocket: Mill a rectangular relief pocket 25 mm x 28 mm x 2 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Vending machine cup drop carousel plate'; this requirement is only for its chosen metal part.

---

## SMP-040-22 - Kiosk cash drawer guide rail

Part name: Kiosk cash drawer guide rail - single metal part

Material: 6061-T6 aluminum (low mass with good machinability and stable flat features)

Envelope: `{"height_mm": 53, "length_mm": 180, "width_mm": 65}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Kiosk cash drawer guide rail'. The broader use case
is: A service technician slides a cash drawer out of a payment kiosk during collection. The chosen
deliverable is only the metal body implied by: A structural rail with stop features, screw bosses,
and captured sliding surfaces. All other product elements are external reference items and must not
be modeled. The part must perform this mechanical role: Support guided drawer motion while resisting
twist and unauthorized removal. It is intentionally included in the SubCAD limit corpus because: The
object tests long structural geometry, repeated mounting features, stop details, and sliding
interface representation. The part is made from 6061-T6 aluminum using rectangular block stock.
Start from one rectangular metal block or plate. Saw oversize, face all datum sides, then machine
the pockets, holes, slots, angled faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 180 mm x 65 mm x 53 mm.
- mounting hole pattern: Drill two through holes diameter 10 mm on the length centerline at X=13 mm and X=167 mm, Y=32 mm.
- functional center feature: Machine a central obround slot 60 mm long x 8 mm wide through the part, centered at X=90 mm, Y=32 mm.
- top relief pocket: Mill a rectangular relief pocket 45 mm x 21 mm x 12 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Kiosk cash drawer guide rail'; this requirement is only for its chosen metal part.

---

## SMP-040-23 - Ticket machine illuminated button collar

Part name: Ticket machine illuminated button collar - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 9, "outer_diameter_mm": 49, "overall_length_mm": 117, "wall_minimum_mm": 20}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Ticket machine illuminated button collar'. The
broader use case is: A public ticket machine uses illuminated push buttons for fare selection or
confirmation. The chosen deliverable is only the metal body implied by: A translucent collar with
stepped flange, light-channel geometry, and sealing lip. All other product elements are external
reference items and must not be modeled. The part must perform this mechanical role: Frame a button,
carry light around its edge, and seal the panel opening. It is intentionally included in the SubCAD
limit corpus because: The part tests concentric profiles, material-specific light paths, sealing
details, and small front-panel features. The part is made from low-carbon steel, ASTM A36 or
equivalent using round bar stock. Start from one cut length of round metal bar. Turn the outside,
face both ends, bore the center, then mill secondary flats, slots, and radial holes as needed. No
separate inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 49 mm and length 117 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 9 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 19 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 16 mm wide over 109 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M4 holes through the top flat at X=39 mm and X=78 mm.
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
- Do not broaden the requirement back into the full product idea named 'Ticket machine illuminated button collar'; this requirement is only for its chosen metal part.

---

## SMP-040-24 - Payment kiosk privacy side wing

Part name: Payment kiosk privacy side wing - single metal part

Material: 6061-T6 aluminum (low mass with good machinability and stable flat features)

Envelope: `{"length_mm": 100, "thickness_mm": 10, "width_mm": 90}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Payment kiosk privacy side wing'. The broader use
case is: A card payment kiosk reduces shoulder-surfing around PIN entry and screen prompts. The
chosen deliverable is only the metal body implied by: A side wing panel with curved leading edge,
mounting flange, and stiffening ribs. All other product elements are external reference items and
must not be modeled. The part must perform this mechanical role: Block side views of sensitive input
areas without interfering with user access. It is intentionally included in the SubCAD limit corpus
because: The shape combines thin protective panels, curved ergonomic edges, bracket-like mounting,
and ribbed reinforcement. The part is made from 6061-T6 aluminum using sheet or plate stock. Start
from one flat sheet or plate blank. Cut the outside profile, machine holes, slots, pockets, lips,
and relief features into that same piece. If bends are called out, they are bends in the same sheet
part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 100 mm x 90 mm x 10 mm.
- mounting hole pattern: Drill two through holes diameter 8 mm on the length centerline at X=18 mm and X=82 mm, Y=45 mm.
- functional center feature: Machine a central obround slot 33 mm long x 18 mm wide through the part, centered at X=50 mm, Y=45 mm.
- top relief pocket: Mill a rectangular relief pocket 25 mm x 30 mm x 1 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Payment kiosk privacy side wing'; this requirement is only for its chosen metal part.

---

## SMP-040-25 - Coin return acoustic dampener insert

Part name: Coin return acoustic dampener insert - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 48, "length_mm": 100, "width_mm": 65}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Coin return acoustic dampener insert'. The broader
use case is: A coin-operated public machine reduces noise when returned coins drop into a metal cup.
The chosen deliverable is only the metal body implied by: A removable soft insert with textured
floor, perimeter lip, and drain reliefs. All other product elements are external reference items and
must not be modeled. The part must perform this mechanical role: Absorb coin impact and keep
returned coins visible and retrievable. It is intentionally included in the SubCAD limit corpus
because: The part tests flexible-material cues, shallow texture, nested fit geometry, and functional
surface relief. The part is made from low-carbon steel, ASTM A36 or equivalent using rectangular
block stock. Start from one rectangular metal block or plate. Saw oversize, face all datum sides,
then machine the pockets, holes, slots, angled faces, grooves, and edge treatments into that same
solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 100 mm x 65 mm x 48 mm.
- mounting hole pattern: Drill two through holes diameter 7 mm on the length centerline at X=13 mm and X=87 mm, Y=32 mm.
- functional center feature: Machine a central obround slot 33 mm long x 12 mm wide through the part, centered at X=50 mm, Y=32 mm.
- top relief pocket: Mill a rectangular relief pocket 25 mm x 21 mm x 3 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Coin return acoustic dampener insert'; this requirement is only for its chosen metal part.

---

## SMP-040-26 - Self-checkout kiosk bag hook bracket

Part name: Self-checkout kiosk bag hook bracket - single metal part

Material: 6061-T6 aluminum (low mass with good machinability and stable flat features)

Envelope: `{"axial_bore_diameter_mm": 8, "outer_diameter_mm": 39, "overall_length_mm": 42, "wall_minimum_mm": 15}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Self-checkout kiosk bag hook bracket'. The broader
use case is: A small public payment kiosk provides a bag hook near the payment area for customer
convenience. The chosen deliverable is only the metal body implied by: A hooked bracket with
thickened root, concealed fastener pocket, and rounded nose. All other product elements are external
reference items and must not be modeled. The part must perform this mechanical role: Hold a hanging
load while staying compact and vandal resistant. It is intentionally included in the SubCAD limit
corpus because: The geometry asks for load-bearing curvature, hidden fastening, variable thickness,
and smooth public-touch surfaces. The part is made from 6061-T6 aluminum using round bar stock.
Start from one cut length of round metal bar. Turn the outside, face both ends, bore the center,
then mill secondary flats, slots, and radial holes as needed. No separate inserts or fasteners are
part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 39 mm and length 42 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 8 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 18 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 13 mm wide over 34 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M6 holes through the top flat at X=14 mm and X=28 mm.
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
- Do not broaden the requirement back into the full product idea named 'Self-checkout kiosk bag hook bracket'; this requirement is only for its chosen metal part.

---

## SMP-040-27 - Parking meter solar panel frame

Part name: Parking meter solar panel frame - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"length_mm": 150, "thickness_mm": 3, "width_mm": 140}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Parking meter solar panel frame'. The broader use
case is: A standalone parking payment meter uses a small solar panel on its upper housing. The
chosen deliverable is only the metal body implied by: An angled frame with gasket channel, corner
bosses, and cable pass-through. All other product elements are external reference items and must not
be modeled. The part must perform this mechanical role: Hold the panel at a protected angle while
sealing it into the meter enclosure. It is intentionally included in the SubCAD limit corpus
because: The part blends inclined frame geometry, seal grooves, wiring openings, and enclosure
attachment features. The part is made from low-carbon steel, ASTM A36 or equivalent using sheet or
plate stock. Start from one flat sheet or plate blank. Cut the outside profile, machine holes,
slots, pockets, lips, and relief features into that same piece. If bends are called out, they are
bends in the same sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 150 mm x 140 mm x 3 mm.
- mounting hole pattern: Drill two through holes diameter 11 mm on the length centerline at X=28 mm and X=122 mm, Y=70 mm.
- functional center feature: Machine a central obround slot 50 mm long x 8 mm wide through the part, centered at X=75 mm, Y=70 mm.
- top relief pocket: Mill a rectangular relief pocket 37 mm x 46 mm x 1 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- machined angled reference face: Machine one top reference face at 35 degrees over the last 30 mm of length.

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
- Do not broaden the requirement back into the full product idea named 'Parking meter solar panel frame'; this requirement is only for its chosen metal part.

---

## SMP-040-28 - Transit card reload kiosk tap pad

Part name: Transit card reload kiosk tap pad - single metal part

Material: 6061-T6 aluminum (low mass with good machinability and stable flat features)

Envelope: `{"length_mm": 130, "thickness_mm": 8, "width_mm": 115}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Transit card reload kiosk tap pad'. The broader use
case is: A fare reload kiosk gives users a marked contactless area for tapping stored-value cards.
The chosen deliverable is only the metal body implied by: A shallow pad insert with raised alignment
border, icon recess, and rear mounting clips. All other product elements are external reference
items and must not be modeled. The part must perform this mechanical role: Create a durable target
surface over the contactless reader while guiding card placement. It is intentionally included in
the SubCAD limit corpus because: The design tests low-relief surface features, tactile borders,
clipped mounting, and visual-symbol accommodation without code. The part is made from 6061-T6
aluminum using sheet or plate stock. Start from one flat sheet or plate blank. Cut the outside
profile, machine holes, slots, pockets, lips, and relief features into that same piece. If bends are
called out, they are bends in the same sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 130 mm x 115 mm x 8 mm.
- mounting hole pattern: Drill two through holes diameter 11 mm on the length centerline at X=23 mm and X=107 mm, Y=57 mm.
- functional center feature: Machine a central obround slot 43 mm long x 14 mm wide through the part, centered at X=65 mm, Y=57 mm.
- top relief pocket: Mill a rectangular relief pocket 32 mm x 38 mm x 3 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- integral hook lip: Leave an integral hook lip on one short end, projecting 18 mm and undercut 6 mm for registration.

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
- Do not broaden the requirement back into the full product idea named 'Transit card reload kiosk tap pad'; this requirement is only for its chosen metal part.

---

## SMP-040-29 - Bill recycler diverter flap

Part name: Bill recycler diverter flap - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 70, "length_mm": 110, "width_mm": 70}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Bill recycler diverter flap'. The broader use case
is: A cash-handling service terminal routes accepted bills either to storage or to a recycle
cassette. The chosen deliverable is only the metal body implied by: A thin diverter flap with curved
leading edge, pivot bosses, and actuator lug. All other product elements are external reference
items and must not be modeled. The part must perform this mechanical role: Redirect bills between
transport paths with minimal friction and clear actuation. It is intentionally included in the
SubCAD limit corpus because: The mechanism stresses thin moving surfaces, tangent flow paths, pivot
features, and asymmetric actuator geometry. The part is made from low-carbon steel, ASTM A36 or
equivalent using rectangular block stock. Start from one rectangular metal block or plate. Saw
oversize, face all datum sides, then machine the pockets, holes, slots, angled faces, grooves, and
edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 110 mm x 70 mm x 70 mm.
- mounting hole pattern: Drill two through holes diameter 12 mm on the length centerline at X=14 mm and X=96 mm, Y=35 mm.
- functional center feature: Machine a central obround slot 36 mm long x 13 mm wide through the part, centered at X=55 mm, Y=35 mm.
- top relief pocket: Mill a rectangular relief pocket 27 mm x 23 mm x 34 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Bill recycler diverter flap'; this requirement is only for its chosen metal part.

---

## SMP-040-30 - Vending machine service door hinge reinforcement

Part name: Vending machine service door hinge reinforcement - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"length_mm": 210, "thickness_mm": 6, "width_mm": 115}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Vending machine service door hinge reinforcement'.
The broader use case is: A large vending enclosure needs reinforced internal hinge support for
repeated maintenance access. The chosen deliverable is only the metal body implied by: A
reinforcement plate with hinge boss pads, formed ribs, and cable relief notches. All other product
elements are external reference items and must not be modeled. The part must perform this mechanical
role: Distribute hinge loads across the cabinet door while preserving internal clearance. It is
intentionally included in the SubCAD limit corpus because: The part combines flat structural stock,
raised pads, formed stiffeners, and irregular clearance cutouts. The part is made from low-carbon
steel, ASTM A36 or equivalent using sheet or plate stock. Start from one flat sheet or plate blank.
Cut the outside profile, machine holes, slots, pockets, lips, and relief features into that same
piece. If bends are called out, they are bends in the same sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 210 mm x 115 mm x 6 mm.
- mounting hole pattern: Drill two through holes diameter 13 mm on the length centerline at X=23 mm and X=187 mm, Y=57 mm.
- functional center feature: Machine a central obround slot 70 mm long x 8 mm wide through the part, centered at X=105 mm, Y=57 mm.
- top relief pocket: Mill a rectangular relief pocket 52 mm x 38 mm x 1 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Vending machine service door hinge reinforcement'; this requirement is only for its chosen metal part.

---
