# Agent 038 Single Metal Part Requirements

Domain: dental lab equipment, orthodontic bench fixtures, non-clinical prosthetic fabrication aids, and sterilization tray hardware

Each item below is one metal part only. Product assemblies and nonmetal components are explicitly out of scope.

## SMP-038-01 - Articulator Calibration Stand

Part name: Articulator Calibration Stand - single metal part

Material: AISI 316 stainless steel (corrosion resistance and cleanable metal surfaces)

Envelope: `{"height_mm": 70, "length_mm": 115, "width_mm": 100}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Articulator Calibration Stand'. The broader use
case is: Dental lab bench setup for holding articulator frames during setup and inspection. The
chosen deliverable is only the metal body implied by: Angled support cradle with indexed locating
features All other product elements are external reference items and must not be modeled. The part
must perform this mechanical role: Stabilizes an articulator while allowing repeatable viewing and
adjustment access. It is intentionally included in the SubCAD limit corpus because: Combines sloped
rests, asymmetric stops, shallow pockets, and clearance cutouts that challenge feature hierarchy
without needing exact dimensions. The part is made from AISI 316 stainless steel using rectangular
block stock. Start from one rectangular metal block or plate. Saw oversize, face all datum sides,
then machine the pockets, holes, slots, angled faces, grooves, and edge treatments into that same
solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 115 mm x 100 mm x 70 mm.
- mounting hole pattern: Drill two through holes diameter 8 mm on the length centerline at X=20 mm and X=95 mm, Y=50 mm.
- functional center feature: Machine a central obround slot 38 mm long x 9 mm wide through the part, centered at X=57 mm, Y=50 mm.
- top relief pocket: Mill a rectangular relief pocket 28 mm x 33 mm x 19 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- machined angled reference face: Machine one top reference face at 25 degrees over the last 23 mm of length.

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
- Do not broaden the requirement back into the full product idea named 'Articulator Calibration Stand'; this requirement is only for its chosen metal part.

---

## SMP-038-02 - Wax Rim Forming Block

Part name: Wax Rim Forming Block - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 67, "length_mm": 85, "width_mm": 85}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Wax Rim Forming Block'. The broader use case is:
Non-clinical prosthetic fabrication aid for shaping occlusal wax rims on the bench. The chosen
deliverable is only the metal body implied by: Contoured forming block with channel and overflow lip
All other product elements are external reference items and must not be modeled. The part must
perform this mechanical role: Guides wax into consistent curved profiles while keeping excess
material contained. It is intentionally included in the SubCAD limit corpus because: Tests
representation of smooth troughs, raised lips, tapered entry zones, and transitions between flat
handling areas and organic guide surfaces. The part is made from low-carbon steel, ASTM A36 or
equivalent using rectangular block stock. Start from one rectangular metal block or plate. Saw
oversize, face all datum sides, then machine the pockets, holes, slots, angled faces, grooves, and
edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 85 mm x 85 mm x 67 mm.
- mounting hole pattern: Drill two through holes diameter 9 mm on the length centerline at X=17 mm and X=68 mm, Y=42 mm.
- functional center feature: Machine a central obround slot 30 mm long x 10 mm wide through the part, centered at X=42 mm, Y=42 mm.
- top relief pocket: Mill a rectangular relief pocket 25 mm x 28 mm x 8 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Wax Rim Forming Block'; this requirement is only for its chosen metal part.

---

## SMP-038-03 - Orthodontic Wire Bending Fixture

Part name: Orthodontic Wire Bending Fixture - single metal part

Material: AISI 316 stainless steel (corrosion resistance and cleanable metal surfaces)

Envelope: `{"length_mm": 235, "thickness_mm": 4, "width_mm": 145}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Orthodontic Wire Bending Fixture'. The broader use
case is: Orthodontic lab bench fixture used to organize and guide manual forming of appliance wires.
The chosen deliverable is only the metal body implied by: Curved guide plate with removable peg
locations All other product elements are external reference items and must not be modeled. The part
must perform this mechanical role: Provides repeatable bend reference paths and grip points for wire
shaping. It is intentionally included in the SubCAD limit corpus because: Stresses arrays of small
locating holes, curved guide rails, relief notches, and a surface layout that is functional but not
purely rectangular. The part is made from AISI 316 stainless steel using sheet or plate stock. Start
from one flat sheet or plate blank. Cut the outside profile, machine holes, slots, pockets, lips,
and relief features into that same piece. If bends are called out, they are bends in the same sheet
part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 235 mm x 145 mm x 4 mm.
- mounting hole pattern: Drill two through holes diameter 8 mm on the length centerline at X=29 mm and X=206 mm, Y=72 mm.
- functional center feature: Machine a central obround slot 78 mm long x 9 mm wide through the part, centered at X=117 mm, Y=72 mm.
- top relief pocket: Mill a rectangular relief pocket 58 mm x 48 mm x 2 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Orthodontic Wire Bending Fixture'; this requirement is only for its chosen metal part.

---

## SMP-038-04 - Retainer Acrylic Trim Support

Part name: Retainer Acrylic Trim Support - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 27, "length_mm": 155, "width_mm": 55}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Retainer Acrylic Trim Support'. The broader use
case is: Bench aid for trimming and finishing removable orthodontic retainers away from patient
contact. The chosen deliverable is only the metal body implied by: Soft-contour nest with clamp
bridge All other product elements are external reference items and must not be modeled. The part
must perform this mechanical role: Holds acrylic appliances securely while exposing edge regions for
rotary finishing. It is intentionally included in the SubCAD limit corpus because: Requires nested
cavities, protective rounded contact regions, bridge clearance, and ergonomic access openings around
an irregular workpiece. The part is made from low-carbon steel, ASTM A36 or equivalent using
rectangular block stock. Start from one rectangular metal block or plate. Saw oversize, face all
datum sides, then machine the pockets, holes, slots, angled faces, grooves, and edge treatments into
that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 155 mm x 55 mm x 27 mm.
- mounting hole pattern: Drill two through holes diameter 7 mm on the length centerline at X=11 mm and X=144 mm, Y=27 mm.
- functional center feature: Machine a central obround slot 51 mm long x 18 mm wide through the part, centered at X=77 mm, Y=27 mm.
- top relief pocket: Mill a rectangular relief pocket 38 mm x 18 mm x 6 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Retainer Acrylic Trim Support'; this requirement is only for its chosen metal part.

---

## SMP-038-05 - Denture Tooth Sorting Tray

Part name: Denture Tooth Sorting Tray - single metal part

Material: AISI 316 stainless steel (corrosion resistance and cleanable metal surfaces)

Envelope: `{"length_mm": 155, "thickness_mm": 8, "width_mm": 70}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Denture Tooth Sorting Tray'. The broader use case
is: Dental prosthetic fabrication bench organizer for arranging artificial teeth during setup. The
chosen deliverable is only the metal body implied by: Compartment tray with curved labeled recesses
All other product elements are external reference items and must not be modeled. The part must
perform this mechanical role: Separates tooth components by position while keeping labels and picks
visible. It is intentionally included in the SubCAD limit corpus because: Tests shallow pocket
repetition, nonuniform compartment shapes, label panels, and scoopable edges within one molded tray
concept. The part is made from AISI 316 stainless steel using sheet or plate stock. Start from one
flat sheet or plate blank. Cut the outside profile, machine holes, slots, pockets, lips, and relief
features into that same piece. If bends are called out, they are bends in the same sheet part, not
separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 155 mm x 70 mm x 8 mm.
- mounting hole pattern: Drill two through holes diameter 11 mm on the length centerline at X=14 mm and X=141 mm, Y=35 mm.
- functional center feature: Machine a central obround slot 51 mm long x 15 mm wide through the part, centered at X=77 mm, Y=35 mm.
- top relief pocket: Mill a rectangular relief pocket 38 mm x 23 mm x 1 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Denture Tooth Sorting Tray'; this requirement is only for its chosen metal part.

---

## SMP-038-06 - Ceramic Crown Glaze Rack

Part name: Ceramic Crown Glaze Rack - single metal part

Material: AISI 316 stainless steel (corrosion resistance and cleanable metal surfaces)

Envelope: `{"length_mm": 175, "thickness_mm": 6, "width_mm": 50}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Ceramic Crown Glaze Rack'. The broader use case is:
Dental lab equipment accessory for supporting restorations before furnace handling. The chosen
deliverable is only the metal body implied by: Perforated rack plate with raised support bosses All
other product elements are external reference items and must not be modeled. The part must perform
this mechanical role: Keeps small crown forms elevated and spaced for coating or drying workflows.
It is intentionally included in the SubCAD limit corpus because: Challenges CAD with dense
perforations, low-height standoffs, filleted boss bases, and the need to distinguish structural
plate from delicate supports. The part is made from AISI 316 stainless steel using sheet or plate
stock. Start from one flat sheet or plate blank. Cut the outside profile, machine holes, slots,
pockets, lips, and relief features into that same piece. If bends are called out, they are bends in
the same sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 175 mm x 50 mm x 6 mm.
- mounting hole pattern: Drill two through holes diameter 10 mm on the length centerline at X=10 mm and X=165 mm, Y=25 mm.
- functional center feature: Machine a central obround slot 58 mm long x 10 mm wide through the part, centered at X=87 mm, Y=25 mm.
- top relief pocket: Mill a rectangular relief pocket 43 mm x 18 mm x 3 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Ceramic Crown Glaze Rack'; this requirement is only for its chosen metal part.

---

## SMP-038-07 - Implant Model Analog Organizer

Part name: Implant Model Analog Organizer - single metal part

Material: AISI 316 stainless steel (corrosion resistance and cleanable metal surfaces)

Envelope: `{"height_mm": 40, "length_mm": 120, "width_mm": 95}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Implant Model Analog Organizer'. The broader use
case is: Non-clinical dental model fabrication station for managing model analog components. The
chosen deliverable is only the metal body implied by: Stepped organizer block with varied socket
profiles All other product elements are external reference items and must not be modeled. The part
must perform this mechanical role: Stores small analog parts upright and groups them by case during
bench work. It is intentionally included in the SubCAD limit corpus because: Mixes circular, keyed,
and slotted receptacles on stepped terraces, testing semantic recognition of part-specific sockets.
The part is made from AISI 316 stainless steel using rectangular block stock. Start from one
rectangular metal block or plate. Saw oversize, face all datum sides, then machine the pockets,
holes, slots, angled faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 120 mm x 95 mm x 40 mm.
- mounting hole pattern: Drill two through holes diameter 8 mm on the length centerline at X=19 mm and X=101 mm, Y=47 mm.
- functional center feature: Machine a central obround slot 40 mm long x 16 mm wide through the part, centered at X=60 mm, Y=47 mm.
- top relief pocket: Mill a rectangular relief pocket 30 mm x 31 mm x 2 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Implant Model Analog Organizer'; this requirement is only for its chosen metal part.

---

## SMP-038-08 - Sterilization Cassette Latch Plate

Part name: Sterilization Cassette Latch Plate - single metal part

Material: 6061-T6 aluminum (low mass with good machinability and stable flat features)

Envelope: `{"length_mm": 110, "thickness_mm": 5, "width_mm": 75}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Sterilization Cassette Latch Plate'. The broader
use case is: Sterilization tray hardware for securing instrument cassette lids during handling. The
chosen deliverable is only the metal body implied by: Flat latch plate with hook nose and thumb tab
All other product elements are external reference items and must not be modeled. The part must
perform this mechanical role: Provides a spring-compatible latch surface and visual locked
orientation. It is intentionally included in the SubCAD limit corpus because: Includes thin sheet
geometry, folded-like hooks, embossed direction cues, and contact clearances that are subtle but
functionally important. The part is made from 6061-T6 aluminum using sheet or plate stock. Start
from one flat sheet or plate blank. Cut the outside profile, machine holes, slots, pockets, lips,
and relief features into that same piece. If bends are called out, they are bends in the same sheet
part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 110 mm x 75 mm x 5 mm.
- mounting hole pattern: Drill two through holes diameter 6 mm on the length centerline at X=15 mm and X=95 mm, Y=37 mm.
- functional center feature: Machine a central obround slot 36 mm long x 7 mm wide through the part, centered at X=55 mm, Y=37 mm.
- top relief pocket: Mill a rectangular relief pocket 27 mm x 25 mm x 1 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- integral hook lip: Leave an integral hook lip on one short end, projecting 7 mm and undercut 3 mm for registration.

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
- Do not broaden the requirement back into the full product idea named 'Sterilization Cassette Latch Plate'; this requirement is only for its chosen metal part.

---

## SMP-038-09 - Bur Block Cleaning Insert

Part name: Bur Block Cleaning Insert - single metal part

Material: AISI 316 stainless steel (corrosion resistance and cleanable metal surfaces)

Envelope: `{"height_mm": 35, "length_mm": 120, "width_mm": 110}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Bur Block Cleaning Insert'. The broader use case
is: Dental lab sterilization tray insert for holding rotary burs through cleaning cycles. The chosen
deliverable is only the metal body implied by: Perforated insert block with drainage underside All
other product elements are external reference items and must not be modeled. The part must perform
this mechanical role: Keeps bur shanks separated and accessible while allowing fluid drainage. It is
intentionally included in the SubCAD limit corpus because: Tests repeated small bores, countersunk
approach features, underside channels, and the distinction between storage holes and fluid paths.
The part is made from AISI 316 stainless steel using rectangular block stock. Start from one
rectangular metal block or plate. Saw oversize, face all datum sides, then machine the pockets,
holes, slots, angled faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 120 mm x 110 mm x 35 mm.
- mounting hole pattern: Drill two through holes diameter 5 mm on the length centerline at X=22 mm and X=98 mm, Y=55 mm.
- functional center feature: Machine a central obround slot 40 mm long x 10 mm wide through the part, centered at X=60 mm, Y=55 mm.
- top relief pocket: Mill a rectangular relief pocket 30 mm x 36 mm x 7 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Bur Block Cleaning Insert'; this requirement is only for its chosen metal part.

---

## SMP-038-10 - Orthodontic Bracket Placement Board

Part name: Orthodontic Bracket Placement Board - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"length_mm": 190, "thickness_mm": 12, "width_mm": 135}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Orthodontic Bracket Placement Board'. The broader
use case is: Orthodontic bench fixture for staging bracket sets during appliance preparation. The
chosen deliverable is only the metal body implied by: Low profile board with angled wells and pickup
grooves All other product elements are external reference items and must not be modeled. The part
must perform this mechanical role: Presents bracket groups in a stable layout with pickup access for
tweezers. It is intentionally included in the SubCAD limit corpus because: Requires many tiny tilted
recesses, fine access grooves, side labels, and a board geometry that must remain readable at small
feature scale. The part is made from low-carbon steel, ASTM A36 or equivalent using sheet or plate
stock. Start from one flat sheet or plate blank. Cut the outside profile, machine holes, slots,
pockets, lips, and relief features into that same piece. If bends are called out, they are bends in
the same sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 190 mm x 135 mm x 12 mm.
- mounting hole pattern: Drill two through holes diameter 5 mm on the length centerline at X=27 mm and X=163 mm, Y=67 mm.
- functional center feature: Machine a central obround slot 63 mm long x 11 mm wide through the part, centered at X=95 mm, Y=67 mm.
- top relief pocket: Mill a rectangular relief pocket 47 mm x 45 mm x 1 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- machined angled reference face: Machine one top reference face at 10 degrees over the last 38 mm of length.

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
- Do not broaden the requirement back into the full product idea named 'Orthodontic Bracket Placement Board'; this requirement is only for its chosen metal part.

---

## SMP-038-11 - Model Pin Drilling Guide

Part name: Model Pin Drilling Guide - single metal part

Material: AISI 316 stainless steel (corrosion resistance and cleanable metal surfaces)

Envelope: `{"axial_bore_diameter_mm": 14, "outer_diameter_mm": 58, "overall_length_mm": 97, "wall_minimum_mm": 22}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Model Pin Drilling Guide'. The broader use case is:
Dental model fabrication aid for preparing removable die bases on the lab bench. The chosen
deliverable is only the metal body implied by: Adjustable guide rail with sliding drill bushings All
other product elements are external reference items and must not be modeled. The part must perform
this mechanical role: Aligns drill approach positions relative to a plaster model base. It is
intentionally included in the SubCAD limit corpus because: Combines rail slots, sliding collars,
bushing holes, clamp pads, and positional logic that tests assembly-like interpretation in a single
concept. The part is made from AISI 316 stainless steel using round bar stock. Start from one cut
length of round metal bar. Turn the outside, face both ends, bore the center, then mill secondary
flats, slots, and radial holes as needed. No separate inserts or fasteners are part of the
deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 58 mm and length 97 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 14 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 24 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 19 mm wide over 89 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M4 holes through the top flat at X=32 mm and X=64 mm.
- split relief slit: Cut one full-length radial slit 6 mm wide from the outside to the axial bore on datum-B side.
- outside edge treatment: Break all outside circular edges with 1.0 mm chamfers and keep internal bore edges visibly chamfered.
- cross relief slot: Machine one transverse slot 8 mm wide across the top flat at X=48 mm, depth 5 mm.

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
- Do not broaden the requirement back into the full product idea named 'Model Pin Drilling Guide'; this requirement is only for its chosen metal part.

---

## SMP-038-12 - Vacuum Forming Sheet Clamp Frame

Part name: Vacuum Forming Sheet Clamp Frame - single metal part

Material: AISI 316 stainless steel (corrosion resistance and cleanable metal surfaces)

Envelope: `{"length_mm": 185, "thickness_mm": 12, "width_mm": 140}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Vacuum Forming Sheet Clamp Frame'. The broader use
case is: Orthodontic lab equipment accessory for thermoforming retainer sheets over models. The
chosen deliverable is only the metal body implied by: Open clamp frame with hinged edge bars All
other product elements are external reference items and must not be modeled. The part must perform
this mechanical role: Holds thermoplastic sheet edges evenly before forming. It is intentionally
included in the SubCAD limit corpus because: Tests thin frame loops, hinge knuckles, latch tabs,
compression surfaces, and a large central void that must be preserved. The part is made from AISI
316 stainless steel using sheet or plate stock. Start from one flat sheet or plate blank. Cut the
outside profile, machine holes, slots, pockets, lips, and relief features into that same piece. If
bends are called out, they are bends in the same sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 185 mm x 140 mm x 12 mm.
- mounting hole pattern: Drill two through holes diameter 7 mm on the length centerline at X=28 mm and X=157 mm, Y=70 mm.
- functional center feature: Machine a central obround slot 61 mm long x 12 mm wide through the part, centered at X=92 mm, Y=70 mm.
- top relief pocket: Mill a rectangular relief pocket 46 mm x 46 mm x 2 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Vacuum Forming Sheet Clamp Frame'; this requirement is only for its chosen metal part.

---

## SMP-038-13 - Plaster Model Drying Rack

Part name: Plaster Model Drying Rack - single metal part

Material: AISI 316 stainless steel (corrosion resistance and cleanable metal surfaces)

Envelope: `{"height_mm": 41, "length_mm": 135, "width_mm": 100}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Plaster Model Drying Rack'. The broader use case
is: Dental lab bench storage for air drying cast models after trimming or washing. The chosen
deliverable is only the metal body implied by: Slotted angled shelf with raised stops All other
product elements are external reference items and must not be modeled. The part must perform this
mechanical role: Supports models at a slight incline while allowing airflow and drip clearance. It
is intentionally included in the SubCAD limit corpus because: Involves repeated angled slots,
drainage gaps, raised end stops, and load-bearing ribs that create a layered functional surface. The
part is made from AISI 316 stainless steel using rectangular block stock. Start from one rectangular
metal block or plate. Saw oversize, face all datum sides, then machine the pockets, holes, slots,
angled faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 135 mm x 100 mm x 41 mm.
- mounting hole pattern: Drill two through holes diameter 10 mm on the length centerline at X=20 mm and X=115 mm, Y=50 mm.
- functional center feature: Machine a central obround slot 45 mm long x 12 mm wide through the part, centered at X=67 mm, Y=50 mm.
- top relief pocket: Mill a rectangular relief pocket 33 mm x 33 mm x 18 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- machined angled reference face: Machine one top reference face at 30 degrees over the last 27 mm of length.

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
- Do not broaden the requirement back into the full product idea named 'Plaster Model Drying Rack'; this requirement is only for its chosen metal part.

---

## SMP-038-14 - Denture Flask Spacer Cradle

Part name: Denture Flask Spacer Cradle - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 39, "length_mm": 125, "width_mm": 100}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Denture Flask Spacer Cradle'. The broader use case
is: Prosthetic fabrication aid for positioning denture flasks during packing preparation. The chosen
deliverable is only the metal body implied by: Heavy cradle base with opposing contour blocks All
other product elements are external reference items and must not be modeled. The part must perform
this mechanical role: Keeps flask halves aligned and separated during staging. It is intentionally
included in the SubCAD limit corpus because: Challenges modeling of opposing curved supports, broad
stability feet, relief pockets, and robust contact regions for a heavy lab item. The part is made
from low-carbon steel, ASTM A36 or equivalent using rectangular block stock. Start from one
rectangular metal block or plate. Saw oversize, face all datum sides, then machine the pockets,
holes, slots, angled faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 125 mm x 100 mm x 39 mm.
- mounting hole pattern: Drill two through holes diameter 10 mm on the length centerline at X=20 mm and X=105 mm, Y=50 mm.
- functional center feature: Machine a central obround slot 41 mm long x 16 mm wide through the part, centered at X=62 mm, Y=50 mm.
- top relief pocket: Mill a rectangular relief pocket 31 mm x 33 mm x 14 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Denture Flask Spacer Cradle'; this requirement is only for its chosen metal part.

---

## SMP-038-15 - Inlay Wax Sprue Tree Holder

Part name: Inlay Wax Sprue Tree Holder - single metal part

Material: AISI 316 stainless steel (corrosion resistance and cleanable metal surfaces)

Envelope: `{"height_mm": 55, "length_mm": 75, "width_mm": 55}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Inlay Wax Sprue Tree Holder'. The broader use case
is: Dental lab casting prep accessory used before investment workflows. The chosen deliverable is
only the metal body implied by: Upright post stand with radial clamp arms All other product elements
are external reference items and must not be modeled. The part must perform this mechanical role:
Holds wax sprue assemblies upright without deforming delicate branches. It is intentionally included
in the SubCAD limit corpus because: Tests radial organization, slender supports, gentle clamp jaws,
and clearance envelopes around fragile tree-like workpieces. The part is made from AISI 316
stainless steel using rectangular block stock. Start from one rectangular metal block or plate. Saw
oversize, face all datum sides, then machine the pockets, holes, slots, angled faces, grooves, and
edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 75 mm x 55 mm x 55 mm.
- mounting hole pattern: Drill two through holes diameter 9 mm on the length centerline at X=11 mm and X=64 mm, Y=27 mm.
- functional center feature: Machine a central obround slot 30 mm long x 12 mm wide through the part, centered at X=37 mm, Y=27 mm.
- top relief pocket: Mill a rectangular relief pocket 25 mm x 18 mm x 23 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Inlay Wax Sprue Tree Holder'; this requirement is only for its chosen metal part.

---

## SMP-038-16 - Sterilization Tray Corner Protector

Part name: Sterilization Tray Corner Protector - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"length_mm": 105, "thickness_mm": 10, "width_mm": 100}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Sterilization Tray Corner Protector'. The broader
use case is: Sterilization tray hardware added to reduce denting and improve stacking behavior. The
chosen deliverable is only the metal body implied by: Clip-on corner cap with internal ribs All
other product elements are external reference items and must not be modeled. The part must perform
this mechanical role: Protects tray corners while creating a stable nesting interface. It is
intentionally included in the SubCAD limit corpus because: Requires an L-shaped shell, snap lips,
internal ribbing, rounded outside edges, and subtle undercuts for retention. The part is made from
low-carbon steel, ASTM A36 or equivalent using sheet or plate stock. Start from one flat sheet or
plate blank. Cut the outside profile, machine holes, slots, pockets, lips, and relief features into
that same piece. If bends are called out, they are bends in the same sheet part, not separate welded
pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 105 mm x 100 mm x 10 mm.
- mounting hole pattern: Drill two through holes diameter 7 mm on the length centerline at X=20 mm and X=85 mm, Y=50 mm.
- functional center feature: Machine a central obround slot 35 mm long x 17 mm wide through the part, centered at X=52 mm, Y=50 mm.
- top relief pocket: Mill a rectangular relief pocket 26 mm x 33 mm x 1 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- integral hook lip: Leave an integral hook lip on one short end, projecting 16 mm and undercut 2 mm for registration.

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
- Do not broaden the requirement back into the full product idea named 'Sterilization Tray Corner Protector'; this requirement is only for its chosen metal part.

---

## SMP-038-17 - Lab Handpiece Rest

Part name: Lab Handpiece Rest - single metal part

Material: AISI 316 stainless steel (corrosion resistance and cleanable metal surfaces)

Envelope: `{"height_mm": 43, "length_mm": 145, "width_mm": 110}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Lab Handpiece Rest'. The broader use case is:
Dental lab bench fixture for setting down rotary handpieces during prosthetic finishing. The chosen
deliverable is only the metal body implied by: Saddle rest with raised bit clearance tunnel All
other product elements are external reference items and must not be modeled. The part must perform
this mechanical role: Keeps the handpiece from rolling while protecting the working bit from
contact. It is intentionally included in the SubCAD limit corpus because: Combines cylindrical
cradle surfaces, tunnel-like clearance, anti-roll feet, and a compact ergonomic form with multiple
tangent transitions. The part is made from AISI 316 stainless steel using rectangular block stock.
Start from one rectangular metal block or plate. Saw oversize, face all datum sides, then machine
the pockets, holes, slots, angled faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 145 mm x 110 mm x 43 mm.
- mounting hole pattern: Drill two through holes diameter 9 mm on the length centerline at X=22 mm and X=123 mm, Y=55 mm.
- functional center feature: Machine a central obround slot 48 mm long x 14 mm wide through the part, centered at X=72 mm, Y=55 mm.
- top relief pocket: Mill a rectangular relief pocket 36 mm x 36 mm x 1 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Lab Handpiece Rest'; this requirement is only for its chosen metal part.

---

## SMP-038-18 - Orthodontic Elastic Sorting Carousel

Part name: Orthodontic Elastic Sorting Carousel - single metal part

Material: AISI 316 stainless steel (corrosion resistance and cleanable metal surfaces)

Envelope: `{"length_mm": 135, "thickness_mm": 8, "width_mm": 65}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Orthodontic Elastic Sorting Carousel'. The broader
use case is: Orthodontic lab bench organizer for elastics and small appliance consumables. The
chosen deliverable is only the metal body implied by: Circular tray body with partitioned wells All
other product elements are external reference items and must not be modeled. The part must perform
this mechanical role: Separates small elastics into accessible compartments with a rotating
presentation surface. It is intentionally included in the SubCAD limit corpus because: Tests radial
partitions, shallow scoop wells, central bearing boss, and lid alignment features without relying on
rectangular repetition. The part is made from AISI 316 stainless steel using sheet or plate stock.
Start from one flat sheet or plate blank. Cut the outside profile, machine holes, slots, pockets,
lips, and relief features into that same piece. If bends are called out, they are bends in the same
sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 135 mm x 65 mm x 8 mm.
- mounting hole pattern: Drill two through holes diameter 6 mm on the length centerline at X=13 mm and X=122 mm, Y=32 mm.
- functional center feature: Machine a central obround slot 45 mm long x 17 mm wide through the part, centered at X=67 mm, Y=32 mm.
- top relief pocket: Mill a rectangular relief pocket 33 mm x 21 mm x 3 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Orthodontic Elastic Sorting Carousel'; this requirement is only for its chosen metal part.

---

## SMP-038-19 - Temporary Crown Shell Holder

Part name: Temporary Crown Shell Holder - single metal part

Material: AISI 316 stainless steel (corrosion resistance and cleanable metal surfaces)

Envelope: `{"height_mm": 67, "length_mm": 95, "width_mm": 40}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Temporary Crown Shell Holder'. The broader use case
is: Dental prosthetic bench aid for trimming provisional crown shells outside clinical use. The
chosen deliverable is only the metal body implied by: Expandable mandrel with tapered support petals
All other product elements are external reference items and must not be modeled. The part must
perform this mechanical role: Holds thin shell forms from the inside while leaving margins exposed.
It is intentionally included in the SubCAD limit corpus because: Requires tapered petal geometry,
split expansion gaps, smooth internal support surfaces, and clear distinction between flexible and
rigid-looking features. The part is made from AISI 316 stainless steel using rectangular block
stock. Start from one rectangular metal block or plate. Saw oversize, face all datum sides, then
machine the pockets, holes, slots, angled faces, grooves, and edge treatments into that same solid
piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 95 mm x 40 mm x 67 mm.
- mounting hole pattern: Drill two through holes diameter 9 mm on the length centerline at X=10 mm and X=85 mm, Y=20 mm.
- functional center feature: Machine a central obround slot 31 mm long x 18 mm wide through the part, centered at X=47 mm, Y=20 mm.
- top relief pocket: Mill a rectangular relief pocket 25 mm x 18 mm x 24 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- machined angled reference face: Machine one top reference face at 37 degrees over the last 19 mm of length.

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
- Do not broaden the requirement back into the full product idea named 'Temporary Crown Shell Holder'; this requirement is only for its chosen metal part.

---

## SMP-038-20 - Sintering Bead Containment Dish

Part name: Sintering Bead Containment Dish - single metal part

Material: AISI 316 stainless steel (corrosion resistance and cleanable metal surfaces)

Envelope: `{"height_mm": 21, "length_mm": 200, "width_mm": 70}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Sintering Bead Containment Dish'. The broader use
case is: Dental lab equipment accessory for supporting zirconia parts in a bead medium. The chosen
deliverable is only the metal body implied by: Shallow refractory dish with textured retrieval ramp
All other product elements are external reference items and must not be modeled. The part must
perform this mechanical role: Contains support beads while allowing easy retrieval of small
restorations. It is intentionally included in the SubCAD limit corpus because: Mixes a bowl-like
cavity, low retaining wall, textured ramp, and small pour relief, challenging surface and feature
intent. The part is made from AISI 316 stainless steel using rectangular block stock. Start from one
rectangular metal block or plate. Saw oversize, face all datum sides, then machine the pockets,
holes, slots, angled faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 200 mm x 70 mm x 21 mm.
- mounting hole pattern: Drill two through holes diameter 10 mm on the length centerline at X=14 mm and X=186 mm, Y=35 mm.
- functional center feature: Machine a central obround slot 66 mm long x 10 mm wide through the part, centered at X=100 mm, Y=35 mm.
- top relief pocket: Mill a rectangular relief pocket 50 mm x 23 mm x 3 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Sintering Bead Containment Dish'; this requirement is only for its chosen metal part.

---

## SMP-038-21 - Impression Tray Repair Clamp

Part name: Impression Tray Repair Clamp - single metal part

Material: AISI 316 stainless steel (corrosion resistance and cleanable metal surfaces)

Envelope: `{"length_mm": 250, "thickness_mm": 12, "width_mm": 120}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Impression Tray Repair Clamp'. The broader use case
is: Non-clinical bench fixture for stabilizing impression trays during lab-side repair or
modification. The chosen deliverable is only the metal body implied by: Curved jaw clamp with handle
notch All other product elements are external reference items and must not be modeled. The part must
perform this mechanical role: Holds curved tray handles and rims in a fixed orientation for adhesive
work. It is intentionally included in the SubCAD limit corpus because: Tests opposing concave jaws,
notched handle clearance, screw boss placement, and the need to represent gripping without excessive
detail. The part is made from AISI 316 stainless steel using sheet or plate stock. Start from one
flat sheet or plate blank. Cut the outside profile, machine holes, slots, pockets, lips, and relief
features into that same piece. If bends are called out, they are bends in the same sheet part, not
separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 250 mm x 120 mm x 12 mm.
- mounting hole pattern: Drill two through holes diameter 8 mm on the length centerline at X=24 mm and X=226 mm, Y=60 mm.
- functional center feature: Machine a central obround slot 83 mm long x 9 mm wide through the part, centered at X=125 mm, Y=60 mm.
- top relief pocket: Mill a rectangular relief pocket 62 mm x 40 mm x 1 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Impression Tray Repair Clamp'; this requirement is only for its chosen metal part.

---

## SMP-038-22 - Sterile Pack Divider Rail

Part name: Sterile Pack Divider Rail - single metal part

Material: AISI 316 stainless steel (corrosion resistance and cleanable metal surfaces)

Envelope: `{"height_mm": 20, "length_mm": 150, "width_mm": 90}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Sterile Pack Divider Rail'. The broader use case
is: Sterilization tray hardware for separating wrapped small dental instruments inside a tray. The
chosen deliverable is only the metal body implied by: Snap-in divider rail with sliding partition
tabs All other product elements are external reference items and must not be modeled. The part must
perform this mechanical role: Creates removable partitions that hold packs upright and visible. It
is intentionally included in the SubCAD limit corpus because: Combines long rail channels, clip
feet, adjustable tab geometry, and repeated but repositionable partition features. The part is made
from AISI 316 stainless steel using rectangular block stock. Start from one rectangular metal block
or plate. Saw oversize, face all datum sides, then machine the pockets, holes, slots, angled faces,
grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 150 mm x 90 mm x 20 mm.
- mounting hole pattern: Drill two through holes diameter 8 mm on the length centerline at X=18 mm and X=132 mm, Y=45 mm.
- functional center feature: Machine a central obround slot 50 mm long x 17 mm wide through the part, centered at X=75 mm, Y=45 mm.
- top relief pocket: Mill a rectangular relief pocket 37 mm x 30 mm x 3 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- integral hook lip: Leave an integral hook lip on one short end, projecting 15 mm and undercut 6 mm for registration.

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
- Do not broaden the requirement back into the full product idea named 'Sterile Pack Divider Rail'; this requirement is only for its chosen metal part.

---

## SMP-038-23 - Occlusal Plane Reference Platform

Part name: Occlusal Plane Reference Platform - single metal part

Material: AISI 316 stainless steel (corrosion resistance and cleanable metal surfaces)

Envelope: `{"length_mm": 110, "thickness_mm": 10, "width_mm": 85}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Occlusal Plane Reference Platform'. The broader use
case is: Dental lab setup aid for checking model orientation during prosthetic planning. The chosen
deliverable is only the metal body implied by: Flat reference plate with leveling pads and sight
grooves All other product elements are external reference items and must not be modeled. The part
must perform this mechanical role: Provides a visual reference surface and adjustable model support
points. It is intentionally included in the SubCAD limit corpus because: Tests planar datum
expression, embedded sight grooves, adjustable pad sockets, and the relationship between visual
alignment features and support features. The part is made from AISI 316 stainless steel using sheet
or plate stock. Start from one flat sheet or plate blank. Cut the outside profile, machine holes,
slots, pockets, lips, and relief features into that same piece. If bends are called out, they are
bends in the same sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 110 mm x 85 mm x 10 mm.
- mounting hole pattern: Drill two through holes diameter 13 mm on the length centerline at X=17 mm and X=93 mm, Y=42 mm.
- functional center feature: Machine a central obround slot 36 mm long x 10 mm wide through the part, centered at X=55 mm, Y=42 mm.
- top relief pocket: Mill a rectangular relief pocket 27 mm x 28 mm x 4 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Occlusal Plane Reference Platform'; this requirement is only for its chosen metal part.

---

## SMP-038-24 - Orthodontic Appliance Soldering Jig

Part name: Orthodontic Appliance Soldering Jig - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 17, "outer_diameter_mm": 89, "overall_length_mm": 51, "wall_minimum_mm": 36}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Orthodontic Appliance Soldering Jig'. The broader
use case is: Orthodontic bench fixture for holding appliance wires and bands during solder
preparation. The chosen deliverable is only the metal body implied by: Heat-resistant jig block with
pin slots and clamp fingers All other product elements are external reference items and must not be
modeled. The part must perform this mechanical role: Locks small parts in a repeatable relationship
while keeping joint areas exposed. It is intentionally included in the SubCAD limit corpus because:
Requires mixed straight and curved slots, finger clamps, heat relief areas, and open access around
intersecting wire paths. The part is made from low-carbon steel, ASTM A36 or equivalent using round
bar stock. Start from one cut length of round metal bar. Turn the outside, face both ends, bore the
center, then mill secondary flats, slots, and radial holes as needed. No separate inserts or
fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 89 mm and length 51 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 17 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 27 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 29 mm wide over 43 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M8 holes through the top flat at X=17 mm and X=34 mm.
- split relief slit: Cut one full-length radial slit 3 mm wide from the outside to the axial bore on datum-B side.
- outside edge treatment: Break all outside circular edges with 1.0 mm chamfers and keep internal bore edges visibly chamfered.
- cross relief slot: Machine one transverse slot 5 mm wide across the top flat at X=25 mm, depth 8 mm.

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
- Do not broaden the requirement back into the full product idea named 'Orthodontic Appliance Soldering Jig'; this requirement is only for its chosen metal part.

---

## SMP-038-25 - Denture Base Polishing Support

Part name: Denture Base Polishing Support - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 27, "length_mm": 140, "width_mm": 90}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Denture Base Polishing Support'. The broader use
case is: Prosthetic fabrication bench aid for supporting denture bases during finishing. The chosen
deliverable is only the metal body implied by: Padded cradle form with rocking lock foot All other
product elements are external reference items and must not be modeled. The part must perform this
mechanical role: Cradles a denture base while exposing outer surfaces for polishing access. It is
intentionally included in the SubCAD limit corpus because: Challenges CAD with broad organic support
contours, replaceable pad regions, underside stabilizer features, and asymmetric access cutaways.
The part is made from low-carbon steel, ASTM A36 or equivalent using rectangular block stock. Start
from one rectangular metal block or plate. Saw oversize, face all datum sides, then machine the
pockets, holes, slots, angled faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 140 mm x 90 mm x 27 mm.
- mounting hole pattern: Drill two through holes diameter 11 mm on the length centerline at X=18 mm and X=122 mm, Y=45 mm.
- functional center feature: Machine a central obround slot 46 mm long x 15 mm wide through the part, centered at X=70 mm, Y=45 mm.
- top relief pocket: Mill a rectangular relief pocket 35 mm x 30 mm x 8 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Denture Base Polishing Support'; this requirement is only for its chosen metal part.

---

## SMP-038-26 - Autoclave Tray Handle Adapter

Part name: Autoclave Tray Handle Adapter - single metal part

Material: 1045 medium-carbon steel, normalized (durable wear surface for workshop loading)

Envelope: `{"axial_bore_diameter_mm": 8, "outer_diameter_mm": 30, "overall_length_mm": 56, "wall_minimum_mm": 11}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Autoclave Tray Handle Adapter'. The broader use
case is: Sterilization tray hardware for improving grip on hot or gloved tray handling. The chosen
deliverable is only the metal body implied by: Clip-on handle sleeve with insulated grip ribs All
other product elements are external reference items and must not be modeled. The part must perform
this mechanical role: Adds a removable grip interface to a metal tray rim. It is intentionally
included in the SubCAD limit corpus because: Tests thin rim capture geometry, ribbed grip texture,
snap retention lips, and a part that must read as both sleeve and handle. The part is made from 1045
medium-carbon steel, normalized using round bar stock. Start from one cut length of round metal bar.
Turn the outside, face both ends, bore the center, then mill secondary flats, slots, and radial
holes as needed. No separate inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 30 mm and length 56 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 8 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 18 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 10 mm wide over 48 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M4 holes through the top flat at X=18 mm and X=37 mm.
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
- Do not broaden the requirement back into the full product idea named 'Autoclave Tray Handle Adapter'; this requirement is only for its chosen metal part.

---

## SMP-038-27 - Crown Margin Inspection Turntable

Part name: Crown Margin Inspection Turntable - single metal part

Material: AISI 316 stainless steel (corrosion resistance and cleanable metal surfaces)

Envelope: `{"height_mm": 48, "length_mm": 150, "width_mm": 75}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Crown Margin Inspection Turntable'. The broader use
case is: Dental lab bench fixture for rotating small restorations during visual inspection. The
chosen deliverable is only the metal body implied by: Low rotary puck with interchangeable crown
nest All other product elements are external reference items and must not be modeled. The part must
perform this mechanical role: Lets a technician turn a crown shell smoothly while keeping it
centered. It is intentionally included in the SubCAD limit corpus because: Combines circular
bearing-like layers, shallow interchangeable inserts, centering cones, and finger scallops in a
compact assembly. The part is made from AISI 316 stainless steel using rectangular block stock.
Start from one rectangular metal block or plate. Saw oversize, face all datum sides, then machine
the pockets, holes, slots, angled faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 150 mm x 75 mm x 48 mm.
- mounting hole pattern: Drill two through holes diameter 10 mm on the length centerline at X=15 mm and X=135 mm, Y=37 mm.
- functional center feature: Machine a central obround slot 50 mm long x 12 mm wide through the part, centered at X=75 mm, Y=37 mm.
- top relief pocket: Mill a rectangular relief pocket 37 mm x 25 mm x 7 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Crown Margin Inspection Turntable'; this requirement is only for its chosen metal part.

---

## SMP-038-28 - Alginate Mixing Bowl Stabilizer

Part name: Alginate Mixing Bowl Stabilizer - single metal part

Material: AISI 316 stainless steel (corrosion resistance and cleanable metal surfaces)

Envelope: `{"height_mm": 50, "length_mm": 155, "width_mm": 55}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Alginate Mixing Bowl Stabilizer'. The broader use
case is: Dental lab bench accessory for stabilizing mixing bowls during material preparation outside
the operatory. The chosen deliverable is only the metal body implied by: Weighted ring base with
flexible grip pads All other product elements are external reference items and must not be modeled.
The part must perform this mechanical role: Prevents bowl slip while leaving the rim accessible for
spatula movement. It is intentionally included in the SubCAD limit corpus because: Requires annular
geometry, segmented pads, raised anti-slip texture, and open access around a nested bowl without
modeling the bowl itself. The part is made from AISI 316 stainless steel using rectangular block
stock. Start from one rectangular metal block or plate. Saw oversize, face all datum sides, then
machine the pockets, holes, slots, angled faces, grooves, and edge treatments into that same solid
piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 155 mm x 55 mm x 50 mm.
- mounting hole pattern: Drill two through holes diameter 13 mm on the length centerline at X=11 mm and X=144 mm, Y=27 mm.
- functional center feature: Machine a central obround slot 51 mm long x 16 mm wide through the part, centered at X=77 mm, Y=27 mm.
- top relief pocket: Mill a rectangular relief pocket 38 mm x 18 mm x 7 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Alginate Mixing Bowl Stabilizer'; this requirement is only for its chosen metal part.

---

## SMP-038-29 - Sterilization Mesh Lid Retainer

Part name: Sterilization Mesh Lid Retainer - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"length_mm": 255, "thickness_mm": 3, "width_mm": 90}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Sterilization Mesh Lid Retainer'. The broader use
case is: Sterilization tray hardware for holding a mesh lid down during washing and transfer. The
chosen deliverable is only the metal body implied by: Edge retainer clip with dual spring tabs All
other product elements are external reference items and must not be modeled. The part must perform
this mechanical role: Secures a removable perforated lid with accessible release tabs. It is
intentionally included in the SubCAD limit corpus because: Tests thin clip geometry, spring-tab
relief gaps, hook engagement surfaces, and repeated perforation-clearance features near the tray
edge. The part is made from low-carbon steel, ASTM A36 or equivalent using sheet or plate stock.
Start from one flat sheet or plate blank. Cut the outside profile, machine holes, slots, pockets,
lips, and relief features into that same piece. If bends are called out, they are bends in the same
sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 255 mm x 90 mm x 3 mm.
- mounting hole pattern: Drill two through holes diameter 6 mm on the length centerline at X=18 mm and X=237 mm, Y=45 mm.
- functional center feature: Machine a central obround slot 85 mm long x 14 mm wide through the part, centered at X=127 mm, Y=45 mm.
- top relief pocket: Mill a rectangular relief pocket 63 mm x 30 mm x 2 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- integral hook lip: Leave an integral hook lip on one short end, projecting 18 mm and undercut 5 mm for registration.

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
- Do not broaden the requirement back into the full product idea named 'Sterilization Mesh Lid Retainer'; this requirement is only for its chosen metal part.

---

## SMP-038-30 - Orthodontic Expansion Screw Assembly Block

Part name: Orthodontic Expansion Screw Assembly Block - single metal part

Material: AISI 316 stainless steel (corrosion resistance and cleanable metal surfaces)

Envelope: `{"height_mm": 65, "length_mm": 110, "width_mm": 85}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Orthodontic Expansion Screw Assembly Block'. The
broader use case is: Orthodontic lab bench aid for arranging expansion screw components before
embedding in appliances. The chosen deliverable is only the metal body implied by: Alignment block
with keyed central pocket and arm grooves All other product elements are external reference items
and must not be modeled. The part must perform this mechanical role: Holds small screw bodies and
arms in the desired orientation during setup. It is intentionally included in the SubCAD limit
corpus because: Combines keyed recesses, narrow grooves, orientation arrows, and clampable side
reliefs that test fine mechanical feature intent. The part is made from AISI 316 stainless steel
using rectangular block stock. Start from one rectangular metal block or plate. Saw oversize, face
all datum sides, then machine the pockets, holes, slots, angled faces, grooves, and edge treatments
into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 110 mm x 85 mm x 65 mm.
- mounting hole pattern: Drill two through holes diameter 13 mm on the length centerline at X=17 mm and X=93 mm, Y=42 mm.
- functional center feature: Machine a central obround slot 36 mm long x 15 mm wide through the part, centered at X=55 mm, Y=42 mm.
- top relief pocket: Mill a rectangular relief pocket 27 mm x 28 mm x 19 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Orthodontic Expansion Screw Assembly Block'; this requirement is only for its chosen metal part.

---
