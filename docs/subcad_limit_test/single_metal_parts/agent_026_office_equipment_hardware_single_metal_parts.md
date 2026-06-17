# Agent 026 Single Metal Part Requirements

Domain: office equipment, printer/scanner mechanisms, desk hardware, file storage, and workspace adjustment parts

Each item below is one metal part only. Product assemblies and nonmetal components are explicitly out of scope.

## SMP-026-01 - Printer Paper Tray Lift Cam

Part name: Printer Paper Tray Lift Cam - single metal part

Material: 4140 alloy steel, prehard (strong cylindrical metal part with threaded and slotted details)

Envelope: `{"axial_bore_diameter_mm": 12, "outer_diameter_mm": 61, "overall_length_mm": 87, "wall_minimum_mm": 24}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Printer Paper Tray Lift Cam'. The broader use case
is: Laser printer input tray assembly The chosen deliverable is only the metal body implied by:
Eccentric lift cam with keyed shaft bore and follower ramp All other product elements are external
reference items and must not be modeled. The part must perform this mechanical role: Raises the
paper stack incrementally so pickup rollers maintain consistent contact pressure It is intentionally
included in the SubCAD limit corpus because: Requires off-center profiles, curved ramp surfaces,
shaft interfaces, and controlled clearances for moving contact The part is made from 4140 alloy
steel, prehard using round bar stock. Start from one cut length of round metal bar. Turn the
outside, face both ends, bore the center, then mill secondary flats, slots, and radial holes as
needed. No separate inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 61 mm and length 87 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 12 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 22 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 20 mm wide over 79 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M8 holes through the top flat at X=29 mm and X=58 mm.
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
- Do not broaden the requirement back into the full product idea named 'Printer Paper Tray Lift Cam'; this requirement is only for its chosen metal part.

---

## SMP-026-02 - Scanner Lid Counterbalance Hinge Arm

Part name: Scanner Lid Counterbalance Hinge Arm - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 25, "length_mm": 160, "width_mm": 95}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Scanner Lid Counterbalance Hinge Arm'. The broader
use case is: Flatbed scanner or copier lid mechanism The chosen deliverable is only the metal body
implied by: Machined hinge arm with pivot bosses, spring anchor holes, and stop faces All other
product elements are external reference items and must not be modeled. The part must perform this
mechanical role: Supports the scanner lid at multiple opening angles while resisting sudden closure
It is intentionally included in the SubCAD limit corpus because: Combines rotational joints, load-
bearing bosses, angular stops, and asymmetric geometry The part is made from low-carbon steel, ASTM
A36 or equivalent using rectangular block stock. Start from one rectangular metal block or plate.
Saw oversize, face all datum sides, then machine the pockets, holes, slots, angled faces, grooves,
and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 160 mm x 95 mm x 25 mm.
- mounting hole pattern: Drill two through holes diameter 12 mm on the length centerline at X=19 mm and X=141 mm, Y=47 mm.
- functional center feature: Machine a central obround slot 53 mm long x 14 mm wide through the part, centered at X=80 mm, Y=47 mm.
- top relief pocket: Mill a rectangular relief pocket 40 mm x 31 mm x 6 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Scanner Lid Counterbalance Hinge Arm'; this requirement is only for its chosen metal part.

---

## SMP-026-03 - Adjustable Monitor Arm Tilt Knuckle

Part name: Adjustable Monitor Arm Tilt Knuckle - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 35, "length_mm": 145, "width_mm": 115}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Adjustable Monitor Arm Tilt Knuckle'. The broader
use case is: Desk-mounted monitor support arm The chosen deliverable is only the metal body implied
by: Serrated tilt knuckle with central clamp bore and radial teeth All other product elements are
external reference items and must not be modeled. The part must perform this mechanical role: Allows
controlled monitor tilt while locking position under display weight It is intentionally included in
the SubCAD limit corpus because: Tests circular patterns, interlocking teeth, clamp geometry, and
orientation-critical mating surfaces The part is made from low-carbon steel, ASTM A36 or equivalent
using rectangular block stock. Start from one rectangular metal block or plate. Saw oversize, face
all datum sides, then machine the pockets, holes, slots, angled faces, grooves, and edge treatments
into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 145 mm x 115 mm x 35 mm.
- mounting hole pattern: Drill two through holes diameter 8 mm on the length centerline at X=23 mm and X=122 mm, Y=57 mm.
- functional center feature: Machine a central obround slot 48 mm long x 14 mm wide through the part, centered at X=72 mm, Y=57 mm.
- top relief pocket: Mill a rectangular relief pocket 36 mm x 38 mm x 6 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- serrated contact edge: Cut 9 equal triangular serrations across the rear edge, each 4 mm deep.

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
- Do not broaden the requirement back into the full product idea named 'Adjustable Monitor Arm Tilt Knuckle'; this requirement is only for its chosen metal part.

---

## SMP-026-04 - Office Chair Height Lever Bracket

Part name: Office Chair Height Lever Bracket - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"length_mm": 145, "thickness_mm": 4, "width_mm": 125}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Office Chair Height Lever Bracket'. The broader use
case is: Pneumatic office chair adjustment control The chosen deliverable is only the metal body
implied by: Stamped-style machined lever bracket with pivot hole, actuator tab, and cable slot All
other product elements are external reference items and must not be modeled. The part must perform
this mechanical role: Transfers user lever motion to the gas cylinder release button It is
intentionally included in the SubCAD limit corpus because: Requires thin-wall features, offset tabs,
bend-like geometry, pivot alignment, and actuation clearances The part is made from low-carbon
steel, ASTM A36 or equivalent using sheet or plate stock. Start from one flat sheet or plate blank.
Cut the outside profile, machine holes, slots, pockets, lips, and relief features into that same
piece. If bends are called out, they are bends in the same sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 145 mm x 125 mm x 4 mm.
- mounting hole pattern: Drill two through holes diameter 13 mm on the length centerline at X=25 mm and X=120 mm, Y=62 mm.
- functional center feature: Machine a central obround slot 48 mm long x 11 mm wide through the part, centered at X=72 mm, Y=62 mm.
- top relief pocket: Mill a rectangular relief pocket 36 mm x 41 mm x 2 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Office Chair Height Lever Bracket'; this requirement is only for its chosen metal part.

---

## SMP-026-05 - Filing Cabinet Anti-Tip Interlock Slider

Part name: Filing Cabinet Anti-Tip Interlock Slider - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 23, "length_mm": 140, "width_mm": 75}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Filing Cabinet Anti-Tip Interlock Slider'. The
broader use case is: Multi-drawer metal filing cabinet The chosen deliverable is only the metal body
implied by: Vertical interlock slider bar with stepped notches and drawer latch contact faces All
other product elements are external reference items and must not be modeled. The part must perform
this mechanical role: Prevents more than one drawer from opening at the same time It is
intentionally included in the SubCAD limit corpus because: Tests long slender parts, repeated notch
features, precise slot relationships, and functional interference geometry The part is made from
low-carbon steel, ASTM A36 or equivalent using rectangular block stock. Start from one rectangular
metal block or plate. Saw oversize, face all datum sides, then machine the pockets, holes, slots,
angled faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 140 mm x 75 mm x 23 mm.
- mounting hole pattern: Drill two through holes diameter 11 mm on the length centerline at X=15 mm and X=125 mm, Y=37 mm.
- functional center feature: Machine a central obround slot 46 mm long x 18 mm wide through the part, centered at X=70 mm, Y=37 mm.
- top relief pocket: Mill a rectangular relief pocket 35 mm x 25 mm x 3 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- serrated contact edge: Cut 8 equal triangular serrations across the rear edge, each 4 mm deep.

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
- Do not broaden the requirement back into the full product idea named 'Filing Cabinet Anti-Tip Interlock Slider'; this requirement is only for its chosen metal part.

---

## SMP-026-06 - Printer Duplexer Sheet Diverter Gate

Part name: Printer Duplexer Sheet Diverter Gate - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"length_mm": 115, "thickness_mm": 5, "width_mm": 80}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Printer Duplexer Sheet Diverter Gate'. The broader
use case is: Duplex printing path inside an office printer The chosen deliverable is only the metal
body implied by: Pivoting diverter gate with curved guide rib and axle journals All other product
elements are external reference items and must not be modeled. The part must perform this mechanical
role: Redirects paper between the output path and reverse feed path for two-sided printing It is
intentionally included in the SubCAD limit corpus because: Requires thin curved surfaces, rib
geometry, pivot journals, and smooth paper-path transitions The part is made from low-carbon steel,
ASTM A36 or equivalent using sheet or plate stock. Start from one flat sheet or plate blank. Cut the
outside profile, machine holes, slots, pockets, lips, and relief features into that same piece. If
bends are called out, they are bends in the same sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 115 mm x 80 mm x 5 mm.
- mounting hole pattern: Drill two through holes diameter 10 mm on the length centerline at X=16 mm and X=99 mm, Y=40 mm.
- functional center feature: Machine a central obround slot 38 mm long x 17 mm wide through the part, centered at X=57 mm, Y=40 mm.
- top relief pocket: Mill a rectangular relief pocket 28 mm x 26 mm x 1 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Printer Duplexer Sheet Diverter Gate'; this requirement is only for its chosen metal part.

---

## SMP-026-07 - Keyboard Tray Slide Lock Pawl

Part name: Keyboard Tray Slide Lock Pawl - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"length_mm": 210, "thickness_mm": 7, "width_mm": 135}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Keyboard Tray Slide Lock Pawl'. The broader use
case is: Under-desk retractable keyboard tray The chosen deliverable is only the metal body implied
by: Spring-loaded pawl with tooth profile, pivot boss, and release tab All other product elements
are external reference items and must not be modeled. The part must perform this mechanical role:
Locks the tray at selected extension positions and releases with a small handle motion It is
intentionally included in the SubCAD limit corpus because: Tests ratchet teeth, small pivot
features, spring seats, and mechanically meaningful contact angles The part is made from low-carbon
steel, ASTM A36 or equivalent using sheet or plate stock. Start from one flat sheet or plate blank.
Cut the outside profile, machine holes, slots, pockets, lips, and relief features into that same
piece. If bends are called out, they are bends in the same sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 210 mm x 135 mm x 7 mm.
- mounting hole pattern: Drill two through holes diameter 13 mm on the length centerline at X=27 mm and X=183 mm, Y=67 mm.
- functional center feature: Machine a central obround slot 70 mm long x 18 mm wide through the part, centered at X=105 mm, Y=67 mm.
- top relief pocket: Mill a rectangular relief pocket 52 mm x 45 mm x 3 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- serrated contact edge: Cut 7 equal triangular serrations across the rear edge, each 3 mm deep.
- machined angled reference face: Machine one top reference face at 35 degrees over the last 42 mm of length.

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
- Do not broaden the requirement back into the full product idea named 'Keyboard Tray Slide Lock Pawl'; this requirement is only for its chosen metal part.

---

## SMP-026-08 - Document Feeder Separator Roller Hub

Part name: Document Feeder Separator Roller Hub - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 12, "outer_diameter_mm": 61, "overall_length_mm": 89, "wall_minimum_mm": 24}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Document Feeder Separator Roller Hub'. The broader
use case is: Automatic document feeder for scanner or multifunction printer The chosen deliverable
is only the metal body implied by: Roller hub with splined bore, retaining groove, and outer sleeve
shoulder All other product elements are external reference items and must not be modeled. The part
must perform this mechanical role: Mounts a friction roller while coupling it to a drive shaft and
allowing service replacement It is intentionally included in the SubCAD limit corpus because:
Requires concentric cylinders, splines, grooves, shoulders, and tolerance-sensitive rotational
features The part is made from low-carbon steel, ASTM A36 or equivalent using round bar stock. Start
from one cut length of round metal bar. Turn the outside, face both ends, bore the center, then mill
secondary flats, slots, and radial holes as needed. No separate inserts or fasteners are part of the
deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 61 mm and length 89 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 12 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 22 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 20 mm wide over 81 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M7 holes through the top flat at X=29 mm and X=59 mm.
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
- Do not broaden the requirement back into the full product idea named 'Document Feeder Separator Roller Hub'; this requirement is only for its chosen metal part.

---

## SMP-026-09 - Standing Desk Crossbar Clamp Block

Part name: Standing Desk Crossbar Clamp Block - single metal part

Material: 1045 medium-carbon steel, normalized (durable wear surface for workshop loading)

Envelope: `{"height_mm": 23, "length_mm": 220, "width_mm": 50}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Standing Desk Crossbar Clamp Block'. The broader
use case is: Electric height-adjustable desk frame The chosen deliverable is only the metal body
implied by: Clamp block with split bore, bolt bosses, alignment tongue, and relief pockets All other
product elements are external reference items and must not be modeled. The part must perform this
mechanical role: Clamps a telescoping crossbar to the desk leg frame while preserving alignment It
is intentionally included in the SubCAD limit corpus because: Tests split clamp geometry, fastener
features, structural pockets, and assembly-driven constraints The part is made from 1045 medium-
carbon steel, normalized using rectangular block stock. Start from one rectangular metal block or
plate. Saw oversize, face all datum sides, then machine the pockets, holes, slots, angled faces,
grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 220 mm x 50 mm x 23 mm.
- mounting hole pattern: Drill two through holes diameter 9 mm on the length centerline at X=10 mm and X=210 mm, Y=25 mm.
- functional center feature: Machine a central obround slot 73 mm long x 15 mm wide through the part, centered at X=110 mm, Y=25 mm.
- top relief pocket: Mill a rectangular relief pocket 55 mm x 18 mm x 7 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Standing Desk Crossbar Clamp Block'; this requirement is only for its chosen metal part.

---

## SMP-026-10 - Modular Desk Cable Grommet Iris Ring

Part name: Modular Desk Cable Grommet Iris Ring - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 9, "outer_diameter_mm": 45, "overall_length_mm": 59, "wall_minimum_mm": 18}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Modular Desk Cable Grommet Iris Ring'. The broader
use case is: Cable management port in an office desk surface The chosen deliverable is only the
metal body implied by: Rotating iris ring with overlapping blade slots and detent notches All other
product elements are external reference items and must not be modeled. The part must perform this
mechanical role: Adjusts the opening size around routed cables while keeping the desktop pass-
through covered It is intentionally included in the SubCAD limit corpus because: Requires annular
parts, repeating curved slots, detents, overlapping motion paths, and user-adjustable mechanism
geometry The part is made from low-carbon steel, ASTM A36 or equivalent using round bar stock. Start
from one cut length of round metal bar. Turn the outside, face both ends, bore the center, then mill
secondary flats, slots, and radial holes as needed. No separate inserts or fasteners are part of the
deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 45 mm and length 59 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 9 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 19 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 15 mm wide over 51 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M4 holes through the top flat at X=19 mm and X=39 mm.
- split relief slit: Cut one full-length radial slit 6 mm wide from the outside to the axial bore on datum-B side.
- outside edge treatment: Break all outside circular edges with 1.0 mm chamfers and keep internal bore edges visibly chamfered.
- cross relief slot: Machine one transverse slot 8 mm wide across the top flat at X=29 mm, depth 4 mm.

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
- Do not broaden the requirement back into the full product idea named 'Modular Desk Cable Grommet Iris Ring'; this requirement is only for its chosen metal part.

---
