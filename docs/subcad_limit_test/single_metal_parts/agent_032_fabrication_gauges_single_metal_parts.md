# Agent 032 Single Metal Part Requirements

Domain: metalworking inspection gauges, welding fixtures, fabrication layout tools, and deburring shop aids

Each item below is one metal part only. Product assemblies and nonmetal components are explicitly out of scope.

## SMP-032-01 - Adjustable Fillet Weld Profile Comparator

Part name: Adjustable Fillet Weld Profile Comparator - single metal part

Material: 1045 medium-carbon steel, normalized (durable wear surface for workshop loading)

Envelope: `{"height_mm": 68, "length_mm": 90, "width_mm": 65}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Adjustable Fillet Weld Profile Comparator'. The
broader use case is: A handheld inspection gauge used by welders and quality technicians to compare
fillet weld shape, throat feel, toe blend, and convexity across varied joint styles without needing
a dedicated gauge for each weld family. The chosen deliverable is only the metal body implied by: A
flat gauge body with pivoting profile leaves, sliding reference noses, and finger grip cutouts. All
other product elements are external reference items and must not be modeled. The part must perform
this mechanical role: Presents multiple sliding and pivoting reference faces that can be brought
against a weld bead to visually and tactilely compare profile regularity. It is intentionally
included in the SubCAD limit corpus because: Requires representing nested moving gauge leaves,
curved comparison edges, thin reference surfaces, and readable shop-floor affordances without
relying on exact numeric sizing. The part is made from 1045 medium-carbon steel, normalized using
rectangular block stock. Start from one rectangular metal block or plate. Saw oversize, face all
datum sides, then machine the pockets, holes, slots, angled faces, grooves, and edge treatments into
that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 90 mm x 65 mm x 68 mm.
- mounting hole pattern: Drill two through holes diameter 11 mm on the length centerline at X=13 mm and X=77 mm, Y=32 mm.
- functional center feature: Machine a central obround slot 30 mm long x 18 mm wide through the part, centered at X=45 mm, Y=32 mm.
- top relief pocket: Mill a rectangular relief pocket 25 mm x 21 mm x 12 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Adjustable Fillet Weld Profile Comparator'; this requirement is only for its chosen metal part.

---

## SMP-032-02 - Magnetic Tack Weld Corner Holding Fixture

Part name: Magnetic Tack Weld Corner Holding Fixture - single metal part

Material: 1045 medium-carbon steel, normalized (durable wear surface for workshop loading)

Envelope: `{"height_mm": 33, "length_mm": 165, "width_mm": 120}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Magnetic Tack Weld Corner Holding Fixture'. The
broader use case is: A compact fabrication bench fixture for holding two metal workpieces in a
repeatable corner relationship while tack welds are placed before final welding. The chosen
deliverable is only the metal body implied by: A triangular fixture frame with embedded magnet
pockets, heat relief slots, and open torch access cutouts. All other product elements are external
reference items and must not be modeled. The part must perform this mechanical role: Uses magnetic
contact pads and relieved welding access windows to hold parts while leaving torch clearance around
the corner. It is intentionally included in the SubCAD limit corpus because: Challenges CAD
generation with mixed solid and void regions, magnet insert recesses, weld-access geometry, and
functional symmetry that must be visually legible. The part is made from 1045 medium-carbon steel,
normalized using rectangular block stock. Start from one rectangular metal block or plate. Saw
oversize, face all datum sides, then machine the pockets, holes, slots, angled faces, grooves, and
edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 165 mm x 120 mm x 33 mm.
- mounting hole pattern: Drill two through holes diameter 8 mm on the length centerline at X=24 mm and X=141 mm, Y=60 mm.
- functional center feature: Machine a central obround slot 55 mm long x 16 mm wide through the part, centered at X=82 mm, Y=60 mm.
- top relief pocket: Mill a rectangular relief pocket 41 mm x 40 mm x 5 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Magnetic Tack Weld Corner Holding Fixture'; this requirement is only for its chosen metal part.

---

## SMP-032-03 - Sheet Metal Edge Burr Detection Comb

Part name: Sheet Metal Edge Burr Detection Comb - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"length_mm": 205, "thickness_mm": 10, "width_mm": 120}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Sheet Metal Edge Burr Detection Comb'. The broader
use case is: A deburring station aid used after shearing, punching, or laser cutting to quickly
detect sharp raised burrs along sheet edges before parts move downstream. The chosen deliverable is
only the metal body implied by: A handle-backed comb with graduated flexible tines, a protective
nose, and replaceable wear strip features. All other product elements are external reference items
and must not be modeled. The part must perform this mechanical role: Draws a row of flexible feeler
teeth along an edge so snagging or deflection reveals burr presence and direction. It is
intentionally included in the SubCAD limit corpus because: Tests the ability to model many thin
repeated compliant features, a comfortable handle, protective guards, and a serviceable insert
concept. The part is made from low-carbon steel, ASTM A36 or equivalent using sheet or plate stock.
Start from one flat sheet or plate blank. Cut the outside profile, machine holes, slots, pockets,
lips, and relief features into that same piece. If bends are called out, they are bends in the same
sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 205 mm x 120 mm x 10 mm.
- mounting hole pattern: Drill two through holes diameter 5 mm on the length centerline at X=24 mm and X=181 mm, Y=60 mm.
- functional center feature: Machine a central obround slot 68 mm long x 9 mm wide through the part, centered at X=102 mm, Y=60 mm.
- top relief pocket: Mill a rectangular relief pocket 51 mm x 40 mm x 5 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Sheet Metal Edge Burr Detection Comb'; this requirement is only for its chosen metal part.

---

## SMP-032-04 - Pipe Saddle Layout Wrap Gauge

Part name: Pipe Saddle Layout Wrap Gauge - single metal part

Material: 1045 medium-carbon steel, normalized (durable wear surface for workshop loading)

Envelope: `{"height_mm": 49, "length_mm": 160, "width_mm": 85}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Pipe Saddle Layout Wrap Gauge'. The broader use
case is: A fabrication layout tool for marking saddle cuts and intersection curves on pipe before
cutting or fit-up in welded pipe assemblies. The chosen deliverable is only the metal body implied
by: A flexible wrap band with curved stencil slots, alignment tabs, indexing marks, and locking
overlap features. All other product elements are external reference items and must not be modeled.
The part must perform this mechanical role: Wraps around round stock and exposes traceable curve
slots for common branch intersection layouts while maintaining alignment around the circumference.
It is intentionally included in the SubCAD limit corpus because: Requires capturing a flexible band
concept, curved layout apertures, repeatable registration features, and a part whose function
depends on wrapping around cylindrical work. The part is made from 1045 medium-carbon steel,
normalized using rectangular block stock. Start from one rectangular metal block or plate. Saw
oversize, face all datum sides, then machine the pockets, holes, slots, angled faces, grooves, and
edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 160 mm x 85 mm x 49 mm.
- mounting hole pattern: Drill two through holes diameter 13 mm on the length centerline at X=17 mm and X=143 mm, Y=42 mm.
- functional center feature: Machine a central obround slot 53 mm long x 8 mm wide through the part, centered at X=80 mm, Y=42 mm.
- top relief pocket: Mill a rectangular relief pocket 40 mm x 28 mm x 14 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- centered V-groove: Cut a 90 degree V-groove along the full X length on the top face, groove mouth 42 mm wide and depth 16 mm.

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
- All required chamfers, reliefs, and edge treatments are visible in STEP and STL outputs.
- No extra parts, fasteners, hardware, labels, cosmetic meshes, or nonmetal components are present.
- Flat datums remain planar and usable; pockets or slots do not accidentally break unsupported walls.

Negative requirements:
- Represent exactly one metal part only.
- Do not model screws, nuts, springs, bushings, bearings, rubber pads, plastic covers, electronics, labels, handles, knobs, adhesives, weld beads, or separate inserts.
- Do not convert the part into an assembly or multiple bodies.
- Do not replace through holes, slots, pockets, grooves, flats, tapers, or chamfers with cosmetic markings.
- Do not omit datum-critical features just because they are small.
- Do not broaden the requirement back into the full product idea named 'Pipe Saddle Layout Wrap Gauge'; this requirement is only for its chosen metal part.

---

## SMP-032-05 - Tabbed Plate Fit-Up Gap Gauge

Part name: Tabbed Plate Fit-Up Gap Gauge - single metal part

Material: 1045 medium-carbon steel, normalized (durable wear surface for workshop loading)

Envelope: `{"length_mm": 180, "thickness_mm": 4, "width_mm": 110}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Tabbed Plate Fit-Up Gap Gauge'. The broader use
case is: A simple inspection and setup tool used during welded plate assembly to check whether root
openings, lap gaps, or spacer clearances are consistent before tacking. The chosen deliverable is
only the metal body implied by: A pivoted stack of flat gauge tabs mounted to a thumb plate with a
stop arc and retaining fastener boss. All other product elements are external reference items and
must not be modeled. The part must perform this mechanical role: Offers a fan of stepped tabs that
can be inserted between plates to compare gap ranges and highlight uneven fit-up. It is
intentionally included in the SubCAD limit corpus because: Exercises representation of stacked thin
components, stepped feeler geometry, pivot hardware, stop limits, and inspection-oriented human
interaction. The part is made from 1045 medium-carbon steel, normalized using sheet or plate stock.
Start from one flat sheet or plate blank. Cut the outside profile, machine holes, slots, pockets,
lips, and relief features into that same piece. If bends are called out, they are bends in the same
sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 180 mm x 110 mm x 4 mm.
- mounting hole pattern: Drill two through holes diameter 12 mm on the length centerline at X=22 mm and X=158 mm, Y=55 mm.
- functional center feature: Machine a central obround slot 60 mm long x 7 mm wide through the part, centered at X=90 mm, Y=55 mm.
- top relief pocket: Mill a rectangular relief pocket 45 mm x 36 mm x 1 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- serrated contact edge: Cut 9 equal triangular serrations across the rear edge, each 5 mm deep.

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
- Do not broaden the requirement back into the full product idea named 'Tabbed Plate Fit-Up Gap Gauge'; this requirement is only for its chosen metal part.

---

## SMP-032-06 - Deburring Wheel Angle Rest

Part name: Deburring Wheel Angle Rest - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 17, "outer_diameter_mm": 51, "overall_length_mm": 64, "wall_minimum_mm": 17}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Deburring Wheel Angle Rest'. The broader use case
is: A bench-mounted shop aid that helps operators hold small parts at consistent presentation angles
against a deburring wheel or abrasive belt. The chosen deliverable is only the metal body implied
by: A slotted base with tilting rest plate, replaceable edge rails, clamp knobs, and chip clearance
pockets. All other product elements are external reference items and must not be modeled. The part
must perform this mechanical role: Provides adjustable angled support faces and sacrificial edge
rails that guide parts while keeping hands away from the abrasive contact zone. It is intentionally
included in the SubCAD limit corpus because: Tests assemblies with adjustable planes, slotted
travel, replaceable wear elements, guarded operator zones, and debris-management cutouts. The part
is made from low-carbon steel, ASTM A36 or equivalent using round bar stock. Start from one cut
length of round metal bar. Turn the outside, face both ends, bore the center, then mill secondary
flats, slots, and radial holes as needed. No separate inserts or fasteners are part of the
deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 51 mm and length 64 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 17 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 27 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 17 mm wide over 56 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M6 holes through the top flat at X=21 mm and X=42 mm.
- split relief slit: Cut one full-length radial slit 6 mm wide from the outside to the axial bore on datum-B side.
- outside edge treatment: Break all outside circular edges with 1.0 mm chamfers and keep internal bore edges visibly chamfered.
- cross relief slot: Machine one transverse slot 8 mm wide across the top flat at X=32 mm, depth 5 mm.

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
- Do not broaden the requirement back into the full product idea named 'Deburring Wheel Angle Rest'; this requirement is only for its chosen metal part.

---

## SMP-032-07 - Weld Coupon Bend Fixture Locator

Part name: Weld Coupon Bend Fixture Locator - single metal part

Material: 1045 medium-carbon steel, normalized (durable wear surface for workshop loading)

Envelope: `{"height_mm": 39, "length_mm": 125, "width_mm": 100}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Weld Coupon Bend Fixture Locator'. The broader use
case is: A quality-control fixture used to position small welded test coupons consistently before
bending, marking, or visual inspection. The chosen deliverable is only the metal body implied by: A
compact locator block with coupon channels, raised centering ribs, open inspection window, and stop
shoulders. All other product elements are external reference items and must not be modeled. The part
must perform this mechanical role: Cradles coupons against stops and centering ribs so the weld zone
aligns to a reference window or press contact region. It is intentionally included in the SubCAD
limit corpus because: Requires clear depiction of datum surfaces, channels, visual inspection
access, raised ribs, and asymmetrical features tied to workpiece orientation. The part is made from
1045 medium-carbon steel, normalized using rectangular block stock. Start from one rectangular metal
block or plate. Saw oversize, face all datum sides, then machine the pockets, holes, slots, angled
faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 125 mm x 100 mm x 39 mm.
- mounting hole pattern: Drill two through holes diameter 9 mm on the length centerline at X=20 mm and X=105 mm, Y=50 mm.
- functional center feature: Machine a central obround slot 41 mm long x 17 mm wide through the part, centered at X=62 mm, Y=50 mm.
- top relief pocket: Mill a rectangular relief pocket 31 mm x 33 mm x 10 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Weld Coupon Bend Fixture Locator'; this requirement is only for its chosen metal part.

---

## SMP-032-08 - Scribe Line Offset Bridge

Part name: Scribe Line Offset Bridge - single metal part

Material: 1045 medium-carbon steel, normalized (durable wear surface for workshop loading)

Envelope: `{"height_mm": 52, "length_mm": 140, "width_mm": 55}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Scribe Line Offset Bridge'. The broader use case
is: A fabrication layout hand tool for marking parallel offset lines along plate edges, flanges, or
cut profiles when preparing weld seams and bend lines. The chosen deliverable is only the metal body
implied by: A U-shaped sliding bridge with edge follower feet, locking offset carriage, and
protected scribe holder. All other product elements are external reference items and must not be
modeled. The part must perform this mechanical role: Bridges over an edge while guiding a scribe
point at a selectable offset from the workpiece boundary. It is intentionally included in the SubCAD
limit corpus because: Challenges CAD with bridging geometry, sliding offset mechanisms, small tool-
holding details, and surfaces that reference an external workpiece edge. The part is made from 1045
medium-carbon steel, normalized using rectangular block stock. Start from one rectangular metal
block or plate. Saw oversize, face all datum sides, then machine the pockets, holes, slots, angled
faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 140 mm x 55 mm x 52 mm.
- mounting hole pattern: Drill two through holes diameter 6 mm on the length centerline at X=11 mm and X=129 mm, Y=27 mm.
- functional center feature: Machine a central obround slot 46 mm long x 10 mm wide through the part, centered at X=70 mm, Y=27 mm.
- top relief pocket: Mill a rectangular relief pocket 35 mm x 18 mm x 2 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Scribe Line Offset Bridge'; this requirement is only for its chosen metal part.

---

## SMP-032-09 - Torch Nozzle Standoff Gauge Ring

Part name: Torch Nozzle Standoff Gauge Ring - single metal part

Material: 1045 medium-carbon steel, normalized (durable wear surface for workshop loading)

Envelope: `{"height_mm": 48, "length_mm": 125, "width_mm": 45}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Torch Nozzle Standoff Gauge Ring'. The broader use
case is: A welding and cutting setup aid used to verify consistent torch nozzle standoff from a work
surface before starting a pass or cut. The chosen deliverable is only the metal body implied by: A
split ring body with spring latch detail, radial reference fingers, and heat-relief openings. All
other product elements are external reference items and must not be modeled. The part must perform
this mechanical role: Clips around a nozzle or rests against it and presents reference fingers that
indicate whether the torch is held at the intended clearance and angle. It is intentionally included
in the SubCAD limit corpus because: Tests circular clamp forms, split-body retention, radial
protrusions, heat-aware voids, and functional interaction with a cylindrical tool. The part is made
from 1045 medium-carbon steel, normalized using rectangular block stock. Start from one rectangular
metal block or plate. Saw oversize, face all datum sides, then machine the pockets, holes, slots,
angled faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 125 mm x 45 mm x 48 mm.
- mounting hole pattern: Drill two through holes diameter 7 mm on the length centerline at X=10 mm and X=115 mm, Y=22 mm.
- functional center feature: Machine a central obround slot 41 mm long x 11 mm wide through the part, centered at X=62 mm, Y=22 mm.
- top relief pocket: Mill a rectangular relief pocket 31 mm x 18 mm x 2 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Torch Nozzle Standoff Gauge Ring'; this requirement is only for its chosen metal part.

---

## SMP-032-10 - Flange Squareness Shadow Gauge

Part name: Flange Squareness Shadow Gauge - single metal part

Material: 1045 medium-carbon steel, normalized (durable wear surface for workshop loading)

Envelope: `{"length_mm": 145, "thickness_mm": 4, "width_mm": 130}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Flange Squareness Shadow Gauge'. The broader use
case is: An inspection gauge for checking whether welded tabs, small flanges, or brackets stand
square to a base plate during fabrication. The chosen deliverable is only the metal body implied by:
An L-shaped gauge frame with relieved inside corner, sight windows, reference rails, and knurled
grip pads. All other product elements are external reference items and must not be modeled. The part
must perform this mechanical role: Seats on the base plate and frames the upright part with
contrasting side references so light gaps reveal angular error. It is intentionally included in the
SubCAD limit corpus because: Requires modeling precision reference faces, relief clearances, viewing
apertures, grip texture cues, and inspection logic based on light-gap visibility. The part is made
from 1045 medium-carbon steel, normalized using sheet or plate stock. Start from one flat sheet or
plate blank. Cut the outside profile, machine holes, slots, pockets, lips, and relief features into
that same piece. If bends are called out, they are bends in the same sheet part, not separate welded
pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 145 mm x 130 mm x 4 mm.
- mounting hole pattern: Drill two through holes diameter 11 mm on the length centerline at X=26 mm and X=119 mm, Y=65 mm.
- functional center feature: Machine a central obround slot 48 mm long x 10 mm wide through the part, centered at X=72 mm, Y=65 mm.
- top relief pocket: Mill a rectangular relief pocket 36 mm x 43 mm x 2 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Flange Squareness Shadow Gauge'; this requirement is only for its chosen metal part.

---
