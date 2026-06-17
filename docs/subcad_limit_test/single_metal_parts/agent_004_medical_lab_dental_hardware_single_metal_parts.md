# Agent 004 Single Metal Part Requirements

Domain: medical, lab, and dental non-implant mechanical hardware

Each item below is one metal part only. Product assemblies and nonmetal components are explicitly out of scope.

## SMP-004-01 - Dental Handpiece Sterilization Cassette Hinge Block

Part name: Dental Handpiece Sterilization Cassette Hinge Block - single metal part

Material: AISI 316 stainless steel (corrosion resistance and cleanable metal surfaces)

Envelope: `{"height_mm": 35, "length_mm": 125, "width_mm": 40}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Dental Handpiece Sterilization Cassette Hinge
Block'. The broader use case is: Reusable autoclavable cassette used in dental clinics to organize
high-speed handpieces during cleaning and sterilization. The chosen deliverable is only the metal
body implied by: Machined stainless hinge-and-latch end block with twin hinge barrels, spring slot,
drain reliefs, and keyed lid stops. All other product elements are external reference items and must
not be modeled. The part must perform this mechanical role: Provides a precision pivot and latch
interface for the cassette lid while surviving repeated thermal cycles. It is intentionally included
in the SubCAD limit corpus because: Combines coaxial hinge bores, thin sterilization-drain channels,
asymmetric latch geometry, filleted transitions, and tight positional relationships between
functional features. The part is made from AISI 316 stainless steel using rectangular block stock.
Start from one rectangular metal block or plate. Saw oversize, face all datum sides, then machine
the pockets, holes, slots, angled faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 125 mm x 40 mm x 35 mm.
- mounting hole pattern: Drill two through holes diameter 13 mm on the length centerline at X=10 mm and X=115 mm, Y=20 mm.
- functional center feature: Machine a central obround slot 41 mm long x 12 mm wide through the part, centered at X=62 mm, Y=20 mm.
- top relief pocket: Mill a rectangular relief pocket 31 mm x 18 mm x 3 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Dental Handpiece Sterilization Cassette Hinge Block'; this requirement is only for its chosen metal part.

---

## SMP-004-02 - Benchtop Centrifuge Rotor Adapter

Part name: Benchtop Centrifuge Rotor Adapter - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 17, "outer_diameter_mm": 86, "overall_length_mm": 44, "wall_minimum_mm": 34}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Benchtop Centrifuge Rotor Adapter'. The broader use
case is: Accessory for a small clinical or research centrifuge that lets a fixed-angle rotor accept
a different sample tube size. The chosen deliverable is only the metal body implied by: Machined
aluminum conical tube sleeve with angled bore, stepped tube seat, extraction notch, balance flats,
and bottom relief pocket. All other product elements are external reference items and must not be
modeled. The part must perform this mechanical role: Centers and supports sample tubes at a defined
angle while preserving balance and allowing easy removal. It is intentionally included in the SubCAD
limit corpus because: Requires angled cylindrical cuts through a tapered body, nested coaxial seats,
mass-reduction pockets, orientation-specific notches, and smooth internal radii. The part is made
from low-carbon steel, ASTM A36 or equivalent using round bar stock. Start from one cut length of
round metal bar. Turn the outside, face both ends, bore the center, then mill secondary flats,
slots, and radial holes as needed. No separate inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 86 mm and length 44 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 17 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 27 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 28 mm wide over 36 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M7 holes through the top flat at X=14 mm and X=29 mm.
- split relief slit: Cut one full-length radial slit 5 mm wide from the outside to the axial bore on datum-B side.
- outside edge treatment: Break all outside circular edges with 1.0 mm chamfers and keep internal bore edges visibly chamfered.
- opposed wrench flats: Mill two opposed flats across the outside, leaving 78 mm across flats over the middle third of the length.
- cross relief slot: Machine one transverse slot 7 mm wide across the top flat at X=22 mm, depth 8 mm.

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
- Do not broaden the requirement back into the full product idea named 'Benchtop Centrifuge Rotor Adapter'; this requirement is only for its chosen metal part.

---

## SMP-004-03 - Microscope Slide Warming Stage Clamp

Part name: Microscope Slide Warming Stage Clamp - single metal part

Material: AISI 316 stainless steel (corrosion resistance and cleanable metal surfaces)

Envelope: `{"height_mm": 33, "length_mm": 115, "width_mm": 105}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Microscope Slide Warming Stage Clamp'. The broader
use case is: Clamp component for a heated microscope stage used in pathology or lab sample
preparation. The chosen deliverable is only the metal body implied by: Machined spring clamp arm
with low-profile finger pads, pivot bore, torsion spring pocket, travel stop, and relieved
underside. All other product elements are external reference items and must not be modeled. The part
must perform this mechanical role: Holds glass slides flat against a heated surface without
obscuring the viewing area. It is intentionally included in the SubCAD limit corpus because: Tests
thin compliant arm geometry, ergonomic pad contours, undercuts, pivot alignment, local thickness
changes, and small-radius clearances. The part is made from AISI 316 stainless steel using
rectangular block stock. Start from one rectangular metal block or plate. Saw oversize, face all
datum sides, then machine the pockets, holes, slots, angled faces, grooves, and edge treatments into
that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 115 mm x 105 mm x 33 mm.
- mounting hole pattern: Drill two through holes diameter 9 mm on the length centerline at X=21 mm and X=94 mm, Y=52 mm.
- functional center feature: Machine a central obround slot 38 mm long x 11 mm wide through the part, centered at X=57 mm, Y=52 mm.
- top relief pocket: Mill a rectangular relief pocket 28 mm x 35 mm x 13 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Microscope Slide Warming Stage Clamp'; this requirement is only for its chosen metal part.

---

## SMP-004-04 - Adjustable Dental Impression Tray Handle

Part name: Adjustable Dental Impression Tray Handle - single metal part

Material: AISI 316 stainless steel (corrosion resistance and cleanable metal surfaces)

Envelope: `{"axial_bore_diameter_mm": 23, "outer_diameter_mm": 71, "overall_length_mm": 95, "wall_minimum_mm": 24}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Adjustable Dental Impression Tray Handle'. The
broader use case is: Reusable mechanical handle for dental impression trays that allows controlled
angular positioning before impression material is loaded. The chosen deliverable is only the metal
body implied by: Machined ratcheting handle yoke with curved tooth sector, cross-pin holes, thumb-
release pocket, and tray dovetail receiver. All other product elements are external reference items
and must not be modeled. The part must perform this mechanical role: Locks the tray at selectable
angles for easier placement in different patient mouth geometries. It is intentionally included in
the SubCAD limit corpus because: Includes curved ratchet teeth, mating dovetail geometry, yoke arms
with aligned bores, ergonomic recesses, and load-bearing fillets. The part is made from AISI 316
stainless steel using round bar stock. Start from one cut length of round metal bar. Turn the
outside, face both ends, bore the center, then mill secondary flats, slots, and radial holes as
needed. No separate inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 71 mm and length 95 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 23 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 33 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 23 mm wide over 87 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M7 holes through the top flat at X=31 mm and X=63 mm.
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
- Do not broaden the requirement back into the full product idea named 'Adjustable Dental Impression Tray Handle'; this requirement is only for its chosen metal part.

---

## SMP-004-05 - Lab Pipette Calibration Weight Cradle

Part name: Lab Pipette Calibration Weight Cradle - single metal part

Material: AISI 316 stainless steel (corrosion resistance and cleanable metal surfaces)

Envelope: `{"height_mm": 44, "length_mm": 85, "width_mm": 75}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Lab Pipette Calibration Weight Cradle'. The broader
use case is: Fixture used during pipette calibration to hold small vessels or weighing boats in a
repeatable position on an analytical balance. The chosen deliverable is only the metal body implied
by: Machined stainless weighing cradle with shallow spherical seat, radial drainage grooves, three-
point feet, and tweezer access cutouts. All other product elements are external reference items and
must not be modeled. The part must perform this mechanical role: Positions calibration containers
consistently while minimizing contact area and trapped liquid. It is intentionally included in the
SubCAD limit corpus because: Challenges representation of shallow curved seating surfaces, radial
groove patterns, tiny support feet, symmetric but interrupted geometry, and delicate edge breaks.
The part is made from AISI 316 stainless steel using rectangular block stock. Start from one
rectangular metal block or plate. Saw oversize, face all datum sides, then machine the pockets,
holes, slots, angled faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 85 mm x 75 mm x 44 mm.
- mounting hole pattern: Drill two through holes diameter 6 mm on the length centerline at X=15 mm and X=70 mm, Y=37 mm.
- functional center feature: Machine a central obround slot 30 mm long x 12 mm wide through the part, centered at X=42 mm, Y=37 mm.
- top relief pocket: Mill a rectangular relief pocket 25 mm x 25 mm x 11 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Lab Pipette Calibration Weight Cradle'; this requirement is only for its chosen metal part.

---

## SMP-004-06 - Dental Model Articulator Condyle Guide

Part name: Dental Model Articulator Condyle Guide - single metal part

Material: AISI 316 stainless steel (corrosion resistance and cleanable metal surfaces)

Envelope: `{"height_mm": 33, "length_mm": 190, "width_mm": 80}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Dental Model Articulator Condyle Guide'. The
broader use case is: Component in a dental lab articulator used to simulate jaw movement for crown
and denture work. The chosen deliverable is only the metal body implied by: Machined guide block
with curved slot track, angle scale boss, stop-screw channels, mounting counterbores, and reference
flats. All other product elements are external reference items and must not be modeled. The part
must perform this mechanical role: Guides a condyle pin along a controlled curved path with
adjustable mechanical stops. It is intentionally included in the SubCAD limit corpus because: Tests
swept slot geometry, compound curved paths, screw-adjustment details, engraved or raised indexing
features, and datum-critical mounting surfaces. The part is made from AISI 316 stainless steel using
rectangular block stock. Start from one rectangular metal block or plate. Saw oversize, face all
datum sides, then machine the pockets, holes, slots, angled faces, grooves, and edge treatments into
that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 190 mm x 80 mm x 33 mm.
- mounting hole pattern: Drill two through holes diameter 5 mm on the length centerline at X=16 mm and X=174 mm, Y=40 mm.
- functional center feature: Machine a central obround slot 63 mm long x 15 mm wide through the part, centered at X=95 mm, Y=40 mm.
- top relief pocket: Mill a rectangular relief pocket 47 mm x 26 mm x 8 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- machined angled reference face: Machine one top reference face at 29 degrees over the last 38 mm of length.
- counterbored seat: Add a central counterbore diameter 23 mm x 6 mm deep around the center feature.
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
- The feature named 'machined angled reference face' is present with the stated size and position.
- The feature named 'counterbored seat' is present with the stated size and position.
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
- Do not broaden the requirement back into the full product idea named 'Dental Model Articulator Condyle Guide'; this requirement is only for its chosen metal part.

---

## SMP-004-07 - Microtome Disposable Blade Holder Jaw

Part name: Microtome Disposable Blade Holder Jaw - single metal part

Material: AISI 316 stainless steel (corrosion resistance and cleanable metal surfaces)

Envelope: `{"axial_bore_diameter_mm": 13, "outer_diameter_mm": 40, "overall_length_mm": 48, "wall_minimum_mm": 13}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Microtome Disposable Blade Holder Jaw'. The broader
use case is: Replaceable jaw component for a laboratory microtome used to section paraffin-embedded
tissue samples. The chosen deliverable is only the metal body implied by: Machined hardened steel
clamping jaw with long angled blade shelf, serrated grip ridge, screw bosses, clearance scallops,
and safety chamfers. All other product elements are external reference items and must not be
modeled. The part must perform this mechanical role: Clamps a thin disposable blade at a precise
rake angle while allowing safe blade exchange. It is intentionally included in the SubCAD limit
corpus because: Requires long precision angled planes, very thin ledges, repeated fine ridges, screw
clamping geometry, chamfer hierarchy, and strict parallelism. The part is made from AISI 316
stainless steel using round bar stock. Start from one cut length of round metal bar. Turn the
outside, face both ends, bore the center, then mill secondary flats, slots, and radial holes as
needed. No separate inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 40 mm and length 48 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 13 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 23 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 13 mm wide over 40 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M8 holes through the top flat at X=16 mm and X=32 mm.
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
- Do not broaden the requirement back into the full product idea named 'Microtome Disposable Blade Holder Jaw'; this requirement is only for its chosen metal part.

---

## SMP-004-08 - Orthodontic Wire Bending Turret

Part name: Orthodontic Wire Bending Turret - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 27, "outer_diameter_mm": 82, "overall_length_mm": 78, "wall_minimum_mm": 27}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Orthodontic Wire Bending Turret'. The broader use
case is: Manual bench tool used by orthodontic technicians to form repeatable bends in archwire
outside the patient mouth. The chosen deliverable is only the metal body implied by: Machined
circular turret disk with eccentric forming pins, indexed detent pockets, central bearing bore,
radius grooves, and locking notch. All other product elements are external reference items and must
not be modeled. The part must perform this mechanical role: Provides multiple pin diameters and bend
radii on a compact rotating turret. It is intentionally included in the SubCAD limit corpus because:
Combines circular indexing, repeated off-axis features, mixed pin bosses, shallow forming grooves,
detent geometry, and rotational symmetry broken by locks. The part is made from low-carbon steel,
ASTM A36 or equivalent using round bar stock. Start from one cut length of round metal bar. Turn the
outside, face both ends, bore the center, then mill secondary flats, slots, and radial holes as
needed. No separate inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 82 mm and length 78 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 27 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 37 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 27 mm wide over 70 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M5 holes through the top flat at X=26 mm and X=52 mm.
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
- Do not broaden the requirement back into the full product idea named 'Orthodontic Wire Bending Turret'; this requirement is only for its chosen metal part.

---

## SMP-004-09 - Lab Tube Decapper Cam Plate

Part name: Lab Tube Decapper Cam Plate - single metal part

Material: AISI 316 stainless steel (corrosion resistance and cleanable metal surfaces)

Envelope: `{"axial_bore_diameter_mm": 16, "outer_diameter_mm": 83, "overall_length_mm": 75, "wall_minimum_mm": 33}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Lab Tube Decapper Cam Plate'. The broader use case
is: Mechanism component in a benchtop sample tube decapper for non-automated or semi-automated lab
workflows. The chosen deliverable is only the metal body implied by: Machined cam plate with spiral
cam slot, follower entry ramp, mounting holes, hard stops, and lightening pockets. All other product
elements are external reference items and must not be modeled. The part must perform this mechanical
role: Transforms a handle motion into a controlled lifting and twisting action on screw caps. It is
intentionally included in the SubCAD limit corpus because: Tests noncircular slot paths, ramped cam
surfaces, mechanical stop faces, offset mounting patterns, and pockets that must avoid functional
cam regions. The part is made from AISI 316 stainless steel using round bar stock. Start from one
cut length of round metal bar. Turn the outside, face both ends, bore the center, then mill
secondary flats, slots, and radial holes as needed. No separate inserts or fasteners are part of the
deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 83 mm and length 75 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 16 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 26 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 27 mm wide over 67 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M5 holes through the top flat at X=25 mm and X=50 mm.
- split relief slit: Cut one full-length radial slit 6 mm wide from the outside to the axial bore on datum-B side.
- outside edge treatment: Break all outside circular edges with 1.0 mm chamfers and keep internal bore edges visibly chamfered.
- cross relief slot: Machine one transverse slot 8 mm wide across the top flat at X=37 mm, depth 8 mm.

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
- Do not broaden the requirement back into the full product idea named 'Lab Tube Decapper Cam Plate'; this requirement is only for its chosen metal part.

---

## SMP-004-10 - Dental Vacuum Trap Quick-Release Collar

Part name: Dental Vacuum Trap Quick-Release Collar - single metal part

Material: AISI 316 stainless steel (corrosion resistance and cleanable metal surfaces)

Envelope: `{"axial_bore_diameter_mm": 8, "outer_diameter_mm": 35, "overall_length_mm": 33, "wall_minimum_mm": 13}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Dental Vacuum Trap Quick-Release Collar'. The
broader use case is: Reusable collar for a dental suction line debris trap that lets staff remove a
collection cup for cleaning. The chosen deliverable is only the metal body implied by: Machined
polymer or aluminum bayonet collar with internal interrupted lugs, grip flutes, O-ring groove, stop
tabs, and drain orientation mark. All other product elements are external reference items and must
not be modeled. The part must perform this mechanical role: Locks a transparent trap cup onto the
suction housing with a quarter-turn bayonet action. It is intentionally included in the SubCAD limit
corpus because: Requires internal bayonet features, annular sealing grooves, interrupted rotational
geometry, exterior grip patterning, and precise axial clearances. The part is made from AISI 316
stainless steel using round bar stock. Start from one cut length of round metal bar. Turn the
outside, face both ends, bore the center, then mill secondary flats, slots, and radial holes as
needed. No separate inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 35 mm and length 33 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 8 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 18 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 11 mm wide over 25 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M8 holes through the top flat at X=11 mm and X=22 mm.
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
- Do not broaden the requirement back into the full product idea named 'Dental Vacuum Trap Quick-Release Collar'; this requirement is only for its chosen metal part.

---
