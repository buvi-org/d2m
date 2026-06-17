# Agent 020 Single Metal Part Requirements

Domain: rugged field cases, emergency-response equipment, non-weapon protective/service hardware, and rescue-tool accessories

Each item below is one metal part only. Product assemblies and nonmetal components are explicitly out of scope.

## SMP-020-01 - Rugged Waterproof Drone Battery Transit Case

Part name: Rugged Waterproof Drone Battery Transit Case - single metal part

Material: 6061-T6 aluminum (low mass with good machinability and stable flat features)

Envelope: `{"length_mm": 175, "thickness_mm": 7, "width_mm": 110}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Rugged Waterproof Drone Battery Transit Case'. The
broader use case is: Field teams transporting spare UAV batteries for search mapping, inspection, or
disaster assessment. The chosen deliverable is only the metal body implied by: Machined internal
battery tray with isolated pockets, drain channels, and lid-compression bosses. All other product
elements are external reference items and must not be modeled. The part must perform this mechanical
role: Protects multiple battery packs from impact, water ingress, and accidental terminal contact
during transport. It is intentionally included in the SubCAD limit corpus because: Requires repeated
pocket geometry, clearance spacing, rounded protective ribs, gasket compression features, and
asymmetric terminal-protection details. The part is made from 6061-T6 aluminum using sheet or plate
stock. Start from one flat sheet or plate blank. Cut the outside profile, machine holes, slots,
pockets, lips, and relief features into that same piece. If bends are called out, they are bends in
the same sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 175 mm x 110 mm x 7 mm.
- mounting hole pattern: Drill two through holes diameter 7 mm on the length centerline at X=22 mm and X=153 mm, Y=55 mm.
- functional center feature: Machine a central obround slot 58 mm long x 11 mm wide through the part, centered at X=87 mm, Y=55 mm.
- top relief pocket: Mill a rectangular relief pocket 43 mm x 36 mm x 3 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Rugged Waterproof Drone Battery Transit Case'; this requirement is only for its chosen metal part.

---

## SMP-020-02 - Ambulance Rail-Mount Oxygen Regulator Guard

Part name: Ambulance Rail-Mount Oxygen Regulator Guard - single metal part

Material: AISI 316 stainless steel (corrosion resistance and cleanable metal surfaces)

Envelope: `{"length_mm": 250, "thickness_mm": 6, "width_mm": 75}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Ambulance Rail-Mount Oxygen Regulator Guard'. The
broader use case is: Emergency medical vehicles where exposed oxygen regulators need protection from
bumps and equipment collisions. The chosen deliverable is only the metal body implied by: Machined
protective cage bracket with rail clamp interface, window cutouts, and hose pass-throughs. All other
product elements are external reference items and must not be modeled. The part must perform this
mechanical role: Shields a regulator while allowing gauge visibility, hose routing, and quick access
for adjustment. It is intentionally included in the SubCAD limit corpus because: Combines clamp
geometry, protective openings, standoff ribs, rounded edges, and constrained access zones around a
delicate device. The part is made from AISI 316 stainless steel using sheet or plate stock. Start
from one flat sheet or plate blank. Cut the outside profile, machine holes, slots, pockets, lips,
and relief features into that same piece. If bends are called out, they are bends in the same sheet
part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 250 mm x 75 mm x 6 mm.
- mounting hole pattern: Drill two through holes diameter 13 mm on the length centerline at X=15 mm and X=235 mm, Y=37 mm.
- functional center feature: Machine a central obround slot 83 mm long x 13 mm wide through the part, centered at X=125 mm, Y=37 mm.
- top relief pocket: Mill a rectangular relief pocket 62 mm x 25 mm x 1 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Ambulance Rail-Mount Oxygen Regulator Guard'; this requirement is only for its chosen metal part.

---

## SMP-020-03 - Flood-Rescue Throw Bag Belt Dock

Part name: Flood-Rescue Throw Bag Belt Dock - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 24, "length_mm": 150, "width_mm": 85}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Flood-Rescue Throw Bag Belt Dock'. The broader use
case is: Swift-water rescue personnel carrying throw bags on modular belts or buoyancy vests. The
chosen deliverable is only the metal body implied by: Machined quick-release belt dock with curved
cradle, latch pocket, and drainage slots. All other product elements are external reference items
and must not be modeled. The part must perform this mechanical role: Holds a rescue rope throw bag
securely while allowing one-handed release under wet conditions. It is intentionally included in the
SubCAD limit corpus because: Tests curved retention surfaces, ergonomic release geometry, slot
arrays, water-drain features, and attachment interfaces. The part is made from low-carbon steel,
ASTM A36 or equivalent using rectangular block stock. Start from one rectangular metal block or
plate. Saw oversize, face all datum sides, then machine the pockets, holes, slots, angled faces,
grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 150 mm x 85 mm x 24 mm.
- mounting hole pattern: Drill two through holes diameter 11 mm on the length centerline at X=17 mm and X=133 mm, Y=42 mm.
- functional center feature: Machine a central obround slot 50 mm long x 17 mm wide through the part, centered at X=75 mm, Y=42 mm.
- top relief pocket: Mill a rectangular relief pocket 37 mm x 28 mm x 1 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Flood-Rescue Throw Bag Belt Dock'; this requirement is only for its chosen metal part.

---

## SMP-020-04 - Field Radio Shock-Isolation Corner Frame

Part name: Field Radio Shock-Isolation Corner Frame - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 26, "length_mm": 200, "width_mm": 95}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Field Radio Shock-Isolation Corner Frame'. The
broader use case is: Disaster-response crews carrying portable radios in rough terrain or temporary
command posts. The chosen deliverable is only the metal body implied by: Machined corner-frame shell
with elastomer insert pockets, exposed control windows, and lanyard anchors. All other product
elements are external reference items and must not be modeled. The part must perform this mechanical
role: Protects a handheld or compact base radio from drops while keeping controls and ports
accessible. It is intentionally included in the SubCAD limit corpus because: Requires offset frames,
corner bosses, recessed insert cavities, port cutouts, and nonuniform protective wall thickness. The
part is made from low-carbon steel, ASTM A36 or equivalent using rectangular block stock. Start from
one rectangular metal block or plate. Saw oversize, face all datum sides, then machine the pockets,
holes, slots, angled faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 200 mm x 95 mm x 26 mm.
- mounting hole pattern: Drill two through holes diameter 13 mm on the length centerline at X=19 mm and X=181 mm, Y=47 mm.
- functional center feature: Machine a central obround slot 66 mm long x 16 mm wide through the part, centered at X=100 mm, Y=47 mm.
- top relief pocket: Mill a rectangular relief pocket 50 mm x 31 mm x 7 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Field Radio Shock-Isolation Corner Frame'; this requirement is only for its chosen metal part.

---

## SMP-020-05 - Collapsible Stretcher Hinge Reinforcement Block

Part name: Collapsible Stretcher Hinge Reinforcement Block - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 13, "outer_diameter_mm": 67, "overall_length_mm": 119, "wall_minimum_mm": 27}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Collapsible Stretcher Hinge Reinforcement Block'.
The broader use case is: Rescue stretchers used in field extraction, industrial sites, and emergency
shelters. The chosen deliverable is only the metal body implied by: Machined hinge block with dual
pivot bores, lock-pin channel, stop faces, and weight-reduction pockets. All other product elements
are external reference items and must not be modeled. The part must perform this mechanical role:
Reinforces a folding stretcher hinge while preserving lock alignment and smooth deployment. It is
intentionally included in the SubCAD limit corpus because: Tests coaxial holes, load-bearing bosses,
mechanical stops, pocketing, and tight alignment constraints. The part is made from low-carbon
steel, ASTM A36 or equivalent using round bar stock. Start from one cut length of round metal bar.
Turn the outside, face both ends, bore the center, then mill secondary flats, slots, and radial
holes as needed. No separate inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 67 mm and length 119 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 13 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 23 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 22 mm wide over 111 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M6 holes through the top flat at X=39 mm and X=79 mm.
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
- Do not broaden the requirement back into the full product idea named 'Collapsible Stretcher Hinge Reinforcement Block'; this requirement is only for its chosen metal part.

---

## SMP-020-06 - Portable Decontamination Shower Hose Manifold Bracket

Part name: Portable Decontamination Shower Hose Manifold Bracket - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"length_mm": 170, "thickness_mm": 6, "width_mm": 80}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Portable Decontamination Shower Hose Manifold
Bracket'. The broader use case is: Emergency hazmat or disaster sites using temporary
decontamination shower systems. The chosen deliverable is only the metal body implied by: Machined
manifold support plate with angled hose ports, valve guards, mounting tabs, and labeling recesses.
All other product elements are external reference items and must not be modeled. The part must
perform this mechanical role: Organizes and supports multiple hose connections while keeping valves
protected and readable. It is intentionally included in the SubCAD limit corpus because: Includes
angled cylindrical features, repeated port spacing, protective raised ribs, shallow engraving zones,
and mount-hole patterns. The part is made from low-carbon steel, ASTM A36 or equivalent using sheet
or plate stock. Start from one flat sheet or plate blank. Cut the outside profile, machine holes,
slots, pockets, lips, and relief features into that same piece. If bends are called out, they are
bends in the same sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 170 mm x 80 mm x 6 mm.
- mounting hole pattern: Drill two through holes diameter 6 mm on the length centerline at X=16 mm and X=154 mm, Y=40 mm.
- functional center feature: Machine a central obround slot 56 mm long x 15 mm wide through the part, centered at X=85 mm, Y=40 mm.
- top relief pocket: Mill a rectangular relief pocket 42 mm x 26 mm x 3 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- machined angled reference face: Machine one top reference face at 39 degrees over the last 34 mm of length.

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
- Do not broaden the requirement back into the full product idea named 'Portable Decontamination Shower Hose Manifold Bracket'; this requirement is only for its chosen metal part.

---

## SMP-020-07 - Hard Case Insert for Thermal Imaging Camera Kit

Part name: Hard Case Insert for Thermal Imaging Camera Kit - single metal part

Material: 6061-T6 aluminum (low mass with good machinability and stable flat features)

Envelope: `{"height_mm": 25, "length_mm": 150, "width_mm": 100}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Hard Case Insert for Thermal Imaging Camera Kit'.
The broader use case is: Fire, rescue, and inspection teams storing a thermal camera, spare battery,
charger, and cable set. The chosen deliverable is only the metal body implied by: Machined or milled
foam-compatible insert master with camera-shaped cavity, accessory wells, and finger-lift reliefs.
All other product elements are external reference items and must not be modeled. The part must
perform this mechanical role: Keeps sensitive imaging equipment organized and protected inside a
rugged field case. It is intentionally included in the SubCAD limit corpus because: Tests nested
organic-adjacent cavities, varied-depth pockets, filleted finger cutouts, labeling pads, and case-
alignment features. The part is made from 6061-T6 aluminum using rectangular block stock. Start from
one rectangular metal block or plate. Saw oversize, face all datum sides, then machine the pockets,
holes, slots, angled faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 150 mm x 100 mm x 25 mm.
- mounting hole pattern: Drill two through holes diameter 6 mm on the length centerline at X=20 mm and X=130 mm, Y=50 mm.
- functional center feature: Machine a central obround slot 50 mm long x 10 mm wide through the part, centered at X=75 mm, Y=50 mm.
- top relief pocket: Mill a rectangular relief pocket 37 mm x 33 mm x 6 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Hard Case Insert for Thermal Imaging Camera Kit'; this requirement is only for its chosen metal part.

---

## SMP-020-08 - Rescue Saw Blade Transport Shield

Part name: Rescue Saw Blade Transport Shield - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"length_mm": 135, "thickness_mm": 12, "width_mm": 135}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Rescue Saw Blade Transport Shield'. The broader use
case is: Emergency crews transporting powered rescue saws separately from consumable abrasive or
carbide blades. The chosen deliverable is only the metal body implied by: Machined circular blade
guard plate with central hub lock, radial ribs, and indexed blade-size stops. All other product
elements are external reference items and must not be modeled. The part must perform this mechanical
role: Protects circular blades from edge damage and protects users from accidental contact during
storage. It is intentionally included in the SubCAD limit corpus because: Requires concentric
circular geometry, radial reinforcement, hub-lock details, stepped diameter references, and edge-
clearance channels. The part is made from low-carbon steel, ASTM A36 or equivalent using sheet or
plate stock. Start from one flat sheet or plate blank. Cut the outside profile, machine holes,
slots, pockets, lips, and relief features into that same piece. If bends are called out, they are
bends in the same sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 135 mm x 135 mm x 12 mm.
- mounting hole pattern: Drill two through holes diameter 13 mm on the length centerline at X=27 mm and X=108 mm, Y=67 mm.
- functional center feature: Machine a central obround slot 45 mm long x 18 mm wide through the part, centered at X=67 mm, Y=67 mm.
- top relief pocket: Mill a rectangular relief pocket 33 mm x 45 mm x 4 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- serrated contact edge: Cut 10 equal triangular serrations across the rear edge, each 4 mm deep.

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
- Do not broaden the requirement back into the full product idea named 'Rescue Saw Blade Transport Shield'; this requirement is only for its chosen metal part.

---

## SMP-020-09 - Temporary Command Post Cable Crossover Protector

Part name: Temporary Command Post Cable Crossover Protector - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 22, "length_mm": 90, "width_mm": 55}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Temporary Command Post Cable Crossover Protector'.
The broader use case is: Emergency operations centers with power, radio, and network cables crossing
walkways. The chosen deliverable is only the metal body implied by: Machined modular cable-channel
segment with interlocking ends, ribbed ramp surfaces, and underside grip pockets. All other product
elements are external reference items and must not be modeled. The part must perform this mechanical
role: Protects cables from foot traffic and reduces trip hazards in temporary field setups. It is
intentionally included in the SubCAD limit corpus because: Tests long channel profiles, interlocking
male-female geometry, patterned traction ribs, underside cavities, and modular repeatability. The
part is made from low-carbon steel, ASTM A36 or equivalent using rectangular block stock. Start from
one rectangular metal block or plate. Saw oversize, face all datum sides, then machine the pockets,
holes, slots, angled faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 90 mm x 55 mm x 22 mm.
- mounting hole pattern: Drill two through holes diameter 5 mm on the length centerline at X=11 mm and X=79 mm, Y=27 mm.
- functional center feature: Machine a central obround slot 30 mm long x 17 mm wide through the part, centered at X=45 mm, Y=27 mm.
- top relief pocket: Mill a rectangular relief pocket 25 mm x 18 mm x 2 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Temporary Command Post Cable Crossover Protector'; this requirement is only for its chosen metal part.

---

## SMP-020-10 - Search-and-Rescue Headlamp Helmet Adapter

Part name: Search-and-Rescue Headlamp Helmet Adapter - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"length_mm": 160, "thickness_mm": 3, "width_mm": 80}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Search-and-Rescue Headlamp Helmet Adapter'. The
broader use case is: Rescue workers mounting high-output headlamps to helmets without permanent
modification. The chosen deliverable is only the metal body implied by: Machined adapter bracket
with slotted adjustment arc, helmet-clip hooks, lamp pivot boss, and cable-retention groove. All
other product elements are external reference items and must not be modeled. The part must perform
this mechanical role: Provides a secure adjustable interface between helmet accessory slots and a
lamp body. It is intentionally included in the SubCAD limit corpus because: Combines hook geometry,
pivot bosses, curved slots, thin retention features, and compact ergonomic clearances. The part is
made from low-carbon steel, ASTM A36 or equivalent using sheet or plate stock. Start from one flat
sheet or plate blank. Cut the outside profile, machine holes, slots, pockets, lips, and relief
features into that same piece. If bends are called out, they are bends in the same sheet part, not
separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 160 mm x 80 mm x 3 mm.
- mounting hole pattern: Drill two through holes diameter 12 mm on the length centerline at X=16 mm and X=144 mm, Y=40 mm.
- functional center feature: Machine a central obround slot 53 mm long x 17 mm wide through the part, centered at X=80 mm, Y=40 mm.
- top relief pocket: Mill a rectangular relief pocket 40 mm x 26 mm x 1 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- integral hook lip: Leave an integral hook lip on one short end, projecting 7 mm and undercut 2 mm for registration.

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
- Do not broaden the requirement back into the full product idea named 'Search-and-Rescue Headlamp Helmet Adapter'; this requirement is only for its chosen metal part.

---
