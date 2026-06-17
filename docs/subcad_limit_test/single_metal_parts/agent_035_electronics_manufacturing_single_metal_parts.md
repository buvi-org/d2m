# Agent 035 Single Metal Part Requirements

Domain: semiconductor, PCB assembly, electronics manufacturing fixtures, test sockets, and ESD-safe handling hardware

Each item below is one metal part only. Product assemblies and nonmetal components are explicitly out of scope.

## SMP-035-01 - ESD-Safe Wafer Cassette Transfer Cradle

Part name: ESD-Safe Wafer Cassette Transfer Cradle - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 47, "length_mm": 135, "width_mm": 85}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'ESD-Safe Wafer Cassette Transfer Cradle'. The
broader use case is: Used at a semiconductor process bench to move wafer cassettes between tools
while minimizing static buildup and handling mistakes. The chosen deliverable is only the metal body
implied by: Molded dissipative polymer cradle with integrated guide rails and contact pads. All
other product elements are external reference items and must not be modeled. The part must perform
this mechanical role: Supports a cassette in a controlled orientation with grippable side shields,
locating stops, and a grounded contact path. It is intentionally included in the SubCAD limit corpus
because: Combines nested open volumes, asymmetric hand clearances, thin protective walls, and
repeated rail-like features that must be represented without relying on simple box primitives. The
part is made from low-carbon steel, ASTM A36 or equivalent using rectangular block stock. Start from
one rectangular metal block or plate. Saw oversize, face all datum sides, then machine the pockets,
holes, slots, angled faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 135 mm x 85 mm x 47 mm.
- mounting hole pattern: Drill two through holes diameter 5 mm on the length centerline at X=17 mm and X=118 mm, Y=42 mm.
- functional center feature: Machine a central obround slot 45 mm long x 12 mm wide through the part, centered at X=67 mm, Y=42 mm.
- top relief pocket: Mill a rectangular relief pocket 33 mm x 28 mm x 12 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'ESD-Safe Wafer Cassette Transfer Cradle'; this requirement is only for its chosen metal part.

---

## SMP-035-02 - Fine-Pitch QFN Manual Test Socket Clamp

Part name: Fine-Pitch QFN Manual Test Socket Clamp - single metal part

Material: 6061-T6 aluminum (low mass with good machinability and stable flat features)

Envelope: `{"axial_bore_diameter_mm": 31, "outer_diameter_mm": 94, "overall_length_mm": 96, "wall_minimum_mm": 31}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Fine-Pitch QFN Manual Test Socket Clamp'. The
broader use case is: Used by electronics test technicians to validate small leadless IC packages
during board bring-up or incoming inspection. The chosen deliverable is only the metal body implied
by: Machined socket body with hinged clamping lid and precision package pocket. All other product
elements are external reference items and must not be modeled. The part must perform this mechanical
role: Holds a QFN package against spring probes with a hinged pressure lid, alignment nest, and
latch that preserves repeatable contact force. It is intentionally included in the SubCAD limit
corpus because: Requires expressing a shallow package nest, hinge geometry, latch undercuts, probe-
field clearance, and contact-pressure surfaces in one compact object. The part is made from 6061-T6
aluminum using round bar stock. Start from one cut length of round metal bar. Turn the outside, face
both ends, bore the center, then mill secondary flats, slots, and radial holes as needed. No
separate inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 94 mm and length 96 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 31 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 41 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 31 mm wide over 88 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M8 holes through the top flat at X=32 mm and X=64 mm.
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
- Do not broaden the requirement back into the full product idea named 'Fine-Pitch QFN Manual Test Socket Clamp'; this requirement is only for its chosen metal part.

---

## SMP-035-03 - PCB Edge-Connector Burn-In Fixture

Part name: PCB Edge-Connector Burn-In Fixture - single metal part

Material: 6061-T6 aluminum (low mass with good machinability and stable flat features)

Envelope: `{"height_mm": 60, "length_mm": 175, "width_mm": 65}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'PCB Edge-Connector Burn-In Fixture'. The broader
use case is: Used in electronics manufacturing to cycle assembled boards through temperature and
power-on burn-in before final shipment. The chosen deliverable is only the metal body implied by:
Rigid fixture frame with card guides, connector support shelf, and locking cam features. All other
product elements are external reference items and must not be modeled. The part must perform this
mechanical role: Guides a PCB into a connector plane, locks the board edge, and exposes airflow
around heat-generating components. It is intentionally included in the SubCAD limit corpus because:
Tests long parallel guide geometry, open-frame construction, cam-lock clearances, airflow cutouts,
and board-retention features without concrete board dimensions. The part is made from 6061-T6
aluminum using rectangular block stock. Start from one rectangular metal block or plate. Saw
oversize, face all datum sides, then machine the pockets, holes, slots, angled faces, grooves, and
edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 175 mm x 65 mm x 60 mm.
- mounting hole pattern: Drill two through holes diameter 6 mm on the length centerline at X=13 mm and X=162 mm, Y=32 mm.
- functional center feature: Machine a central obround slot 58 mm long x 12 mm wide through the part, centered at X=87 mm, Y=32 mm.
- top relief pocket: Mill a rectangular relief pocket 43 mm x 21 mm x 2 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'PCB Edge-Connector Burn-In Fixture'; this requirement is only for its chosen metal part.

---

## SMP-035-04 - Pogo-Pin Programming Fixture for Panelized PCBs

Part name: Pogo-Pin Programming Fixture for Panelized PCBs - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 8, "outer_diameter_mm": 31, "overall_length_mm": 29, "wall_minimum_mm": 11}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Pogo-Pin Programming Fixture for Panelized PCBs'.
The broader use case is: Used on an assembly line to flash firmware into multiple boards before
depanelization. The chosen deliverable is only the metal body implied by: Two-level test fixture
plate with alignment pins, relief pockets, and hinged compression bridge. All other product elements
are external reference items and must not be modeled. The part must perform this mechanical role:
Aligns a panel to a pin bed and applies even top pressure while leaving visual access to status LEDs
and fiducials. It is intentionally included in the SubCAD limit corpus because: Challenges
representation of arrays, layered plates, registration features, spring-contact keepouts, and hinged
pressure structures. The part is made from low-carbon steel, ASTM A36 or equivalent using round bar
stock. Start from one cut length of round metal bar. Turn the outside, face both ends, bore the
center, then mill secondary flats, slots, and radial holes as needed. No separate inserts or
fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 31 mm and length 29 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 8 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 18 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 10 mm wide over 21 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M5 holes through the top flat at X=9 mm and X=19 mm.
- split relief slit: Cut one full-length radial slit 2 mm wide from the outside to the axial bore on datum-B side.
- outside edge treatment: Break all outside circular edges with 1.0 mm chamfers and keep internal bore edges visibly chamfered.
- cross relief slot: Machine one transverse slot 4 mm wide across the top flat at X=14 mm, depth 3 mm.

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
- Do not broaden the requirement back into the full product idea named 'Pogo-Pin Programming Fixture for Panelized PCBs'; this requirement is only for its chosen metal part.

---

## SMP-035-05 - ESD-Safe Component Reel Inspection Stand

Part name: ESD-Safe Component Reel Inspection Stand - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 24, "length_mm": 160, "width_mm": 70}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'ESD-Safe Component Reel Inspection Stand'. The
broader use case is: Used at SMT receiving inspection to check tape-and-reel components without
placing reels flat on a work surface. The chosen deliverable is only the metal body implied by:
Adjustable reel support stand with side disks, axle cradle, and tape guide channel. All other
product elements are external reference items and must not be modeled. The part must perform this
mechanical role: Holds a component reel upright, controls tape feed direction, and provides a
dissipative path to the bench mat. It is intentionally included in the SubCAD limit corpus because:
Includes rotational support geometry, sliding adjustment features, thin guide channels, and mixed
cylindrical and planar structures. The part is made from low-carbon steel, ASTM A36 or equivalent
using rectangular block stock. Start from one rectangular metal block or plate. Saw oversize, face
all datum sides, then machine the pockets, holes, slots, angled faces, grooves, and edge treatments
into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 160 mm x 70 mm x 24 mm.
- mounting hole pattern: Drill two through holes diameter 9 mm on the length centerline at X=14 mm and X=146 mm, Y=35 mm.
- functional center feature: Machine a central obround slot 53 mm long x 7 mm wide through the part, centered at X=80 mm, Y=35 mm.
- top relief pocket: Mill a rectangular relief pocket 40 mm x 23 mm x 8 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'ESD-Safe Component Reel Inspection Stand'; this requirement is only for its chosen metal part.

---

## SMP-035-06 - BGA Rework Stencil Alignment Frame

Part name: BGA Rework Stencil Alignment Frame - single metal part

Material: 6061-T6 aluminum (low mass with good machinability and stable flat features)

Envelope: `{"height_mm": 43, "length_mm": 145, "width_mm": 65}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'BGA Rework Stencil Alignment Frame'. The broader
use case is: Used during electronics repair or prototype rework to align a solder paste stencil over
a BGA footprint. The chosen deliverable is only the metal body implied by: Low-profile alignment
frame with corner clamps, fiducial viewing windows, and stencil retention lips. All other product
elements are external reference items and must not be modeled. The part must perform this mechanical
role: Centers a stencil relative to board fiducials and constrains it flat while keeping the rework
area accessible. It is intentionally included in the SubCAD limit corpus because: Tests thin frame
modeling, transparent access openings, clamp clearances, edge lips, and precision alignment
relationships. The part is made from 6061-T6 aluminum using rectangular block stock. Start from one
rectangular metal block or plate. Saw oversize, face all datum sides, then machine the pockets,
holes, slots, angled faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 145 mm x 65 mm x 43 mm.
- mounting hole pattern: Drill two through holes diameter 13 mm on the length centerline at X=13 mm and X=132 mm, Y=32 mm.
- functional center feature: Machine a central obround slot 48 mm long x 13 mm wide through the part, centered at X=72 mm, Y=32 mm.
- top relief pocket: Mill a rectangular relief pocket 36 mm x 21 mm x 5 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'BGA Rework Stencil Alignment Frame'; this requirement is only for its chosen metal part.

---

## SMP-035-07 - Tray-to-Socket IC Pick Placement Nest

Part name: Tray-to-Socket IC Pick Placement Nest - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"length_mm": 135, "thickness_mm": 5, "width_mm": 120}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Tray-to-Socket IC Pick Placement Nest'. The broader
use case is: Used beside automated or semi-automated test equipment to transfer fragile ICs from
JEDEC trays into sockets. The chosen deliverable is only the metal body implied by: Precision
package nest insert with chamfered pocket, datum stops, and vacuum-tool clearance. All other product
elements are external reference items and must not be modeled. The part must perform this mechanical
role: Presents a single package in a repeatable orientation with bevelled lead-in surfaces and anti-
rotation constraints. It is intentionally included in the SubCAD limit corpus because: Forces
careful description of chamfers, shallow pockets, orientation keys, tool access reliefs, and very
small contact-sensitive support surfaces. The part is made from low-carbon steel, ASTM A36 or
equivalent using sheet or plate stock. Start from one flat sheet or plate blank. Cut the outside
profile, machine holes, slots, pockets, lips, and relief features into that same piece. If bends are
called out, they are bends in the same sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 135 mm x 120 mm x 5 mm.
- mounting hole pattern: Drill two through holes diameter 13 mm on the length centerline at X=24 mm and X=111 mm, Y=60 mm.
- functional center feature: Machine a central obround slot 45 mm long x 12 mm wide through the part, centered at X=67 mm, Y=60 mm.
- top relief pocket: Mill a rectangular relief pocket 33 mm x 40 mm x 1 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Tray-to-Socket IC Pick Placement Nest'; this requirement is only for its chosen metal part.

---

## SMP-035-08 - Conformal Coating Masking Fixture for Connectors

Part name: Conformal Coating Masking Fixture for Connectors - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 26, "length_mm": 220, "width_mm": 65}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Conformal Coating Masking Fixture for Connectors'.
The broader use case is: Used during PCB conformal coating to protect connectors, switches, and test
pads from overspray. The chosen deliverable is only the metal body implied by: Reusable masking
frame with compliant cap islands and alignment bosses. All other product elements are external
reference items and must not be modeled. The part must perform this mechanical role: Covers selected
board features with removable caps while locating from board edges and existing mounting holes. It
is intentionally included in the SubCAD limit corpus because: Combines distributed protective
islands, bridge arms, flexible-looking caps, board-location bosses, and intentionally open areas for
coating exposure. The part is made from low-carbon steel, ASTM A36 or equivalent using rectangular
block stock. Start from one rectangular metal block or plate. Saw oversize, face all datum sides,
then machine the pockets, holes, slots, angled faces, grooves, and edge treatments into that same
solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 220 mm x 65 mm x 26 mm.
- mounting hole pattern: Drill two through holes diameter 13 mm on the length centerline at X=13 mm and X=207 mm, Y=32 mm.
- functional center feature: Machine a central obround slot 73 mm long x 11 mm wide through the part, centered at X=110 mm, Y=32 mm.
- top relief pocket: Mill a rectangular relief pocket 55 mm x 21 mm x 8 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Conformal Coating Masking Fixture for Connectors'; this requirement is only for its chosen metal part.

---

## SMP-035-09 - ESD-Safe SMT Nozzle Change Organizer

Part name: ESD-Safe SMT Nozzle Change Organizer - single metal part

Material: 4140 alloy steel, prehard (strong cylindrical metal part with threaded and slotted details)

Envelope: `{"axial_bore_diameter_mm": 8, "outer_diameter_mm": 30, "overall_length_mm": 37, "wall_minimum_mm": 11}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'ESD-Safe SMT Nozzle Change Organizer'. The broader
use case is: Used at a pick-and-place machine to store and identify small vacuum nozzles during
feeder setup changes. The chosen deliverable is only the metal body implied by: Dissipative
organizer block with stepped pockets, label lands, and grounding strip channel. All other product
elements are external reference items and must not be modeled. The part must perform this mechanical
role: Keeps nozzles separated, upright, and grounded while allowing quick visual identification and
finger access. It is intentionally included in the SubCAD limit corpus because: Tests dense repeated
pocket features, stepped bores, ergonomic finger scoops, label surfaces, and a contrasting
conductive path. The part is made from 4140 alloy steel, prehard using round bar stock. Start from
one cut length of round metal bar. Turn the outside, face both ends, bore the center, then mill
secondary flats, slots, and radial holes as needed. No separate inserts or fasteners are part of the
deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 30 mm and length 37 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 8 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 18 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 10 mm wide over 29 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M5 holes through the top flat at X=12 mm and X=24 mm.
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
- Do not broaden the requirement back into the full product idea named 'ESD-Safe SMT Nozzle Change Organizer'; this requirement is only for its chosen metal part.

---

## SMP-035-10 - Thermal Interface Pad Placement Jig

Part name: Thermal Interface Pad Placement Jig - single metal part

Material: 6061-T6 aluminum (low mass with good machinability and stable flat features)

Envelope: `{"length_mm": 195, "thickness_mm": 9, "width_mm": 45}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Thermal Interface Pad Placement Jig'. The broader
use case is: Used in electronics assembly to place soft thermal pads onto processors, power modules,
or heat-spreader locations consistently. The chosen deliverable is only the metal body implied by:
Flat placement template with soft-pad window, anti-stick bevels, and detachable alignment ears. All
other product elements are external reference items and must not be modeled. The part must perform
this mechanical role: Indexes to a board or module and guides a pad into position without
stretching, contaminating, or misaligning it. It is intentionally included in the SubCAD limit
corpus because: Requires representing thin sheet geometry, large cutouts, removable alignment
features, bevelled release edges, and delicate handling clearances. The part is made from 6061-T6
aluminum using sheet or plate stock. Start from one flat sheet or plate blank. Cut the outside
profile, machine holes, slots, pockets, lips, and relief features into that same piece. If bends are
called out, they are bends in the same sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 195 mm x 45 mm x 9 mm.
- mounting hole pattern: Drill two through holes diameter 9 mm on the length centerline at X=10 mm and X=185 mm, Y=22 mm.
- functional center feature: Machine a central obround slot 65 mm long x 18 mm wide through the part, centered at X=97 mm, Y=22 mm.
- top relief pocket: Mill a rectangular relief pocket 48 mm x 18 mm x 2 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Thermal Interface Pad Placement Jig'; this requirement is only for its chosen metal part.

---
