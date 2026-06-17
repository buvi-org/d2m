# Agent 017 Single Metal Part Requirements

Domain: HVAC, plumbing, pump fittings, valve accessories, and building-service mechanical hardware

Each item below is one metal part only. Product assemblies and nonmetal components are explicitly out of scope.

## SMP-017-01 - Flanged Pump Suction Diffuser Body

Part name: Flanged Pump Suction Diffuser Body - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"length_mm": 100, "thickness_mm": 4, "width_mm": 60}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Flanged Pump Suction Diffuser Body'. The broader
use case is: Inline centrifugal pump installations in HVAC chilled-water or condenser-water loops.
The chosen deliverable is only the metal body implied by: Cast or machined diffuser housing with
offset inlet, flanged outlet, internal strainer seat, drain boss, and removable access cover
interface. All other product elements are external reference items and must not be modeled. The part
must perform this mechanical role: Straightens inlet flow, captures debris, and provides a compact
transition between piping and pump suction flange. It is intentionally included in the SubCAD limit
corpus because: Combines non-coaxial pipe transitions, flange bolt patterns, internal seating
geometry, angled flow passages, bosses, and service-cover features in one part. The part is made
from low-carbon steel, ASTM A36 or equivalent using sheet or plate stock. Start from one flat sheet
or plate blank. Cut the outside profile, machine holes, slots, pockets, lips, and relief features
into that same piece. If bends are called out, they are bends in the same sheet part, not separate
welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 100 mm x 60 mm x 4 mm.
- mounting hole pattern: Drill two through holes diameter 6 mm on the length centerline at X=12 mm and X=88 mm, Y=30 mm.
- functional center feature: Machine a central obround slot 33 mm long x 17 mm wide through the part, centered at X=50 mm, Y=30 mm.
- top relief pocket: Mill a rectangular relief pocket 25 mm x 20 mm x 1 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- machined angled reference face: Machine one top reference face at 27 degrees over the last 20 mm of length.

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
- Do not broaden the requirement back into the full product idea named 'Flanged Pump Suction Diffuser Body'; this requirement is only for its chosen metal part.

---

## SMP-017-02 - Grooved Pipe Butterfly Valve Gearbox Mount Yoke

Part name: Grooved Pipe Butterfly Valve Gearbox Mount Yoke - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 39, "length_mm": 215, "width_mm": 60}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Grooved Pipe Butterfly Valve Gearbox Mount Yoke'.
The broader use case is: Valve accessory used on grooved-end butterfly valves in building-service
water systems. The chosen deliverable is only the metal body implied by: Machined bridge yoke with
stem bore, actuator bolt pattern, curved saddle underside, anti-rotation lugs, and clearance
pockets. All other product elements are external reference items and must not be modeled. The part
must perform this mechanical role: Supports and aligns a manual gearbox or actuator above the valve
stem while transferring torque into the valve shaft. It is intentionally included in the SubCAD
limit corpus because: Requires accurate coaxial shaft features, mixed circular and rectangular
mounting patterns, curved mating surfaces, pockets, and orientation-critical lugs. The part is made
from low-carbon steel, ASTM A36 or equivalent using rectangular block stock. Start from one
rectangular metal block or plate. Saw oversize, face all datum sides, then machine the pockets,
holes, slots, angled faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 215 mm x 60 mm x 39 mm.
- mounting hole pattern: Drill two through holes diameter 8 mm on the length centerline at X=12 mm and X=203 mm, Y=30 mm.
- functional center feature: Machine a central obround slot 71 mm long x 15 mm wide through the part, centered at X=107 mm, Y=30 mm.
- top relief pocket: Mill a rectangular relief pocket 53 mm x 20 mm x 2 mm deep on the top face, centered between the mounting holes.
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
- Do not broaden the requirement back into the full product idea named 'Grooved Pipe Butterfly Valve Gearbox Mount Yoke'; this requirement is only for its chosen metal part.

---

## SMP-017-03 - Condensate Trap Cleanout Union Body

Part name: Condensate Trap Cleanout Union Body - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"axial_bore_diameter_mm": 23, "outer_diameter_mm": 94, "overall_length_mm": 65, "wall_minimum_mm": 35}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Condensate Trap Cleanout Union Body'. The broader
use case is: HVAC air-handler condensate drain piping where traps require maintenance access. The
chosen deliverable is only the metal body implied by: Machined U-trap body with threaded pipe ends,
raised cleanout boss, plug seat, internal curved passage, and wrench flats. All other product
elements are external reference items and must not be modeled. The part must perform this mechanical
role: Forms a water-seal trap section with a removable cleanout connection for clearing sludge or
biological buildup. It is intentionally included in the SubCAD limit corpus because: Tests swept
internal fluid paths, threaded cylindrical interfaces, offset service bosses, sealing shoulders, and
flats on otherwise rounded plumbing geometry. The part is made from low-carbon steel, ASTM A36 or
equivalent using round bar stock. Start from one cut length of round metal bar. Turn the outside,
face both ends, bore the center, then mill secondary flats, slots, and radial holes as needed. No
separate inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 94 mm and length 65 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 23 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 33 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 31 mm wide over 57 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M6 holes through the top flat at X=21 mm and X=43 mm.
- split relief slit: Cut one full-length radial slit 2 mm wide from the outside to the axial bore on datum-B side.
- outside edge treatment: Break all outside circular edges with 1.0 mm chamfers and keep internal bore edges visibly chamfered.
- opposed wrench flats: Mill two opposed flats across the outside, leaving 86 mm across flats over the middle third of the length.

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
- All required chamfers, reliefs, and edge treatments are visible in STEP and STL outputs.
- No extra parts, fasteners, hardware, labels, cosmetic meshes, or nonmetal components are present.
- Round features are coaxial unless the requirement explicitly says they are radial or offset.

Negative requirements:
- Represent exactly one metal part only.
- Do not model screws, nuts, springs, bushings, bearings, rubber pads, plastic covers, electronics, labels, handles, knobs, adhesives, weld beads, or separate inserts.
- Do not convert the part into an assembly or multiple bodies.
- Do not replace through holes, slots, pockets, grooves, flats, tapers, or chamfers with cosmetic markings.
- Do not omit datum-critical features just because they are small.
- Do not broaden the requirement back into the full product idea named 'Condensate Trap Cleanout Union Body'; this requirement is only for its chosen metal part.

---

## SMP-017-04 - Balancing Valve Memory Stop Collar

Part name: Balancing Valve Memory Stop Collar - single metal part

Material: 4140 alloy steel, prehard (strong cylindrical metal part with threaded and slotted details)

Envelope: `{"axial_bore_diameter_mm": 10, "outer_diameter_mm": 32, "overall_length_mm": 73, "wall_minimum_mm": 11}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Balancing Valve Memory Stop Collar'. The broader
use case is: Hydronic balancing valves used to set and preserve flow positions in HVAC distribution
branches. The chosen deliverable is only the metal body implied by: Split collar with indexed arc
scale, clamp screw ears, stem bore, stop tab, and small detent pockets. All other product elements
are external reference items and must not be modeled. The part must perform this mechanical role:
Locks a valve handwheel or stem at a calibrated preset position after commissioning. It is
intentionally included in the SubCAD limit corpus because: Includes split-ring geometry, fine
angular indexing, asymmetric clamp ears, small repeated detents, and functional interference-control
features. The part is made from 4140 alloy steel, prehard using round bar stock. Start from one cut
length of round metal bar. Turn the outside, face both ends, bore the center, then mill secondary
flats, slots, and radial holes as needed. No separate inserts or fasteners are part of the
deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 32 mm and length 73 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 10 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 20 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 10 mm wide over 65 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M8 holes through the top flat at X=24 mm and X=48 mm.
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
- Do not broaden the requirement back into the full product idea named 'Balancing Valve Memory Stop Collar'; this requirement is only for its chosen metal part.

---

## SMP-017-05 - Pump Seal Flush Port Manifold Block

Part name: Pump Seal Flush Port Manifold Block - single metal part

Material: 4140 alloy steel, prehard (strong cylindrical metal part with threaded and slotted details)

Envelope: `{"axial_bore_diameter_mm": 8, "outer_diameter_mm": 33, "overall_length_mm": 69, "wall_minimum_mm": 12}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Pump Seal Flush Port Manifold Block'. The broader
use case is: Auxiliary fitting for mechanical seal cooling or flushing on HVAC and plumbing booster
pumps. The chosen deliverable is only the metal body implied by: Compact machined manifold block
with intersecting drilled passages, threaded ports on multiple faces, mounting holes, and plug
bosses. All other product elements are external reference items and must not be modeled. The part
must perform this mechanical role: Routes a controlled flush line between pump casing, seal chamber,
drain, and instrumentation ports. It is intentionally included in the SubCAD limit corpus because:
Challenges CAD representation with hidden intersecting bores, multi-face port orientation, sealing
spotfaces, plugs, and precise passage relationships. The part is made from 4140 alloy steel, prehard
using round bar stock. Start from one cut length of round metal bar. Turn the outside, face both
ends, bore the center, then mill secondary flats, slots, and radial holes as needed. No separate
inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 33 mm and length 69 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 8 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 18 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 11 mm wide over 61 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M6 holes through the top flat at X=23 mm and X=46 mm.
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
- Do not broaden the requirement back into the full product idea named 'Pump Seal Flush Port Manifold Block'; this requirement is only for its chosen metal part.

---

## SMP-017-06 - Duct-Mounted Static Pressure Probe Compression Fitting

Part name: Duct-Mounted Static Pressure Probe Compression Fitting - single metal part

Material: 1045 medium-carbon steel, normalized (durable wear surface for workshop loading)

Envelope: `{"length_mm": 220, "thickness_mm": 3, "width_mm": 90}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Duct-Mounted Static Pressure Probe Compression
Fitting'. The broader use case is: HVAC duct pressure sensing for VAV systems and air-handling unit
controls. The chosen deliverable is only the metal body implied by: Machined compression fitting
body with duct-side flange, tapered ferrule seat, probe bore, locking nut thread, and gasket groove.
All other product elements are external reference items and must not be modeled. The part must
perform this mechanical role: Holds and seals a small pressure probe tube through sheet-metal duct
wall while allowing depth adjustment. It is intentionally included in the SubCAD limit corpus
because: Mixes thin-wall mounting flange geometry, concentric sealing cones, external threads, small
through-bores, and gasket retention details. The part is made from 1045 medium-carbon steel,
normalized using sheet or plate stock. Start from one flat sheet or plate blank. Cut the outside
profile, machine holes, slots, pockets, lips, and relief features into that same piece. If bends are
called out, they are bends in the same sheet part, not separate welded pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 220 mm x 90 mm x 3 mm.
- mounting hole pattern: Drill two through holes diameter 13 mm on the length centerline at X=18 mm and X=202 mm, Y=45 mm.
- functional center feature: Machine a central obround slot 73 mm long x 16 mm wide through the part, centered at X=110 mm, Y=45 mm.
- top relief pocket: Mill a rectangular relief pocket 55 mm x 30 mm x 2 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- machined angled reference face: Machine one top reference face at 34 degrees over the last 44 mm of length.
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
- Do not broaden the requirement back into the full product idea named 'Duct-Mounted Static Pressure Probe Compression Fitting'; this requirement is only for its chosen metal part.

---

## SMP-017-07 - Strainer Blowdown Valve Adapter Elbow

Part name: Strainer Blowdown Valve Adapter Elbow - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 23, "length_mm": 105, "width_mm": 40}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Strainer Blowdown Valve Adapter Elbow'. The broader
use case is: Y-strainers and basket strainers in pump rooms requiring piped blowdown connections.
The chosen deliverable is only the metal body implied by: Machined 45-degree elbow adapter with male
inlet thread, female outlet thread, hex wrench section, drain passage, and sealing shoulder. All
other product elements are external reference items and must not be modeled. The part must perform
this mechanical role: Adapts a strainer drain port to an angled valve outlet while maintaining
wrench access and clearance from the strainer body. It is intentionally included in the SubCAD limit
corpus because: Tests angled cylindrical passages, compound threaded ends, hex-to-round transitions,
sealing faces, and realistic service-clearance geometry. The part is made from low-carbon steel,
ASTM A36 or equivalent using rectangular block stock. Start from one rectangular metal block or
plate. Saw oversize, face all datum sides, then machine the pockets, holes, slots, angled faces,
grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 105 mm x 40 mm x 23 mm.
- mounting hole pattern: Drill two through holes diameter 10 mm on the length centerline at X=10 mm and X=95 mm, Y=20 mm.
- functional center feature: Machine a central obround slot 35 mm long x 17 mm wide through the part, centered at X=52 mm, Y=20 mm.
- top relief pocket: Mill a rectangular relief pocket 26 mm x 18 mm x 4 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
- machined angled reference face: Machine one top reference face at 45 degrees over the last 21 mm of length.
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
- Do not broaden the requirement back into the full product idea named 'Strainer Blowdown Valve Adapter Elbow'; this requirement is only for its chosen metal part.

---

## SMP-017-08 - Pressure Reducing Valve Pilot Tubing Bracket

Part name: Pressure Reducing Valve Pilot Tubing Bracket - single metal part

Material: 1045 medium-carbon steel, normalized (durable wear surface for workshop loading)

Envelope: `{"axial_bore_diameter_mm": 11, "outer_diameter_mm": 59, "overall_length_mm": 24, "wall_minimum_mm": 24}`

Datum orientation: Use the cylinder axis as X. The left faced end is datum A at X=0. The radial direction through the largest flat or slot is datum B. Positive Z points upward from the part centerline when the main flat faces up.

Full description:

Make the single metal part for the product idea 'Pressure Reducing Valve Pilot Tubing Bracket'. The
broader use case is: Valve accessory for pilot-operated pressure reducing valves in domestic water
booster systems. The chosen deliverable is only the metal body implied by: Formed or machined
standoff bracket with valve-body saddle, tube clamp channels, slotted mounting holes, and raised
protective ribs. All other product elements are external reference items and must not be modeled.
The part must perform this mechanical role: Positions and protects small pilot tubing and fittings
around the main valve body. It is intentionally included in the SubCAD limit corpus because:
Represents a context-specific bracket with curved saddle fit, narrow tube-retention features, slots,
ribs, and installation-driven asymmetry. The part is made from 1045 medium-carbon steel, normalized
using round bar stock. Start from one cut length of round metal bar. Turn the outside, face both
ends, bore the center, then mill secondary flats, slots, and radial holes as needed. No separate
inserts or fasteners are part of the deliverable.

Functional features:
- single cylindrical body: Turn one coaxial cylinder to OD 59 mm and length 24 mm from solid round bar.
- axial through bore: Machine a centered through bore diameter 11 mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.
- end counterbores: Add shallow concentric counterbores on both ends, diameter 21 mm x 3 mm deep.
- milled reference flat: Mill one longitudinal flat 19 mm wide over 16 mm of length, centered on the top side.
- radial clamp holes: Add two radial tapped M5 holes through the top flat at X=8 mm and X=16 mm.
- split relief slit: Cut one full-length radial slit 5 mm wide from the outside to the axial bore on datum-B side.
- outside edge treatment: Break all outside circular edges with 1.0 mm chamfers and keep internal bore edges visibly chamfered.
- cross relief slot: Machine one transverse slot 7 mm wide across the top flat at X=12 mm, depth 5 mm.

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
- Do not broaden the requirement back into the full product idea named 'Pressure Reducing Valve Pilot Tubing Bracket'; this requirement is only for its chosen metal part.

---

## SMP-017-09 - Grooved Coupling Sprinkler Drain Test Port Insert

Part name: Grooved Coupling Sprinkler Drain Test Port Insert - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"height_mm": 43, "length_mm": 160, "width_mm": 85}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Grooved Coupling Sprinkler Drain Test Port Insert'.
The broader use case is: Building-service fire protection or plumbing test assemblies using grooved
mechanical couplings. The chosen deliverable is only the metal body implied by: Curved coupling
insert segment with pipe-radius underside, grooved-joint sealing land, threaded radial port, and
anti-slip shoulders. All other product elements are external reference items and must not be
modeled. The part must perform this mechanical role: Adds a small drain or test-gauge connection at
a grooved pipe joint without adding a full tee fitting. It is intentionally included in the SubCAD
limit corpus because: Requires partial cylindrical shell geometry, radial boss placement, groove-
compatible sealing surfaces, and small threaded penetrations through curved walls. The part is made
from low-carbon steel, ASTM A36 or equivalent using rectangular block stock. Start from one
rectangular metal block or plate. Saw oversize, face all datum sides, then machine the pockets,
holes, slots, angled faces, grooves, and edge treatments into that same solid piece.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 160 mm x 85 mm x 43 mm.
- mounting hole pattern: Drill two through holes diameter 9 mm on the length centerline at X=17 mm and X=143 mm, Y=42 mm.
- functional center feature: Machine a central obround slot 53 mm long x 13 mm wide through the part, centered at X=80 mm, Y=42 mm.
- top relief pocket: Mill a rectangular relief pocket 40 mm x 28 mm x 8 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
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
- Do not broaden the requirement back into the full product idea named 'Grooved Coupling Sprinkler Drain Test Port Insert'; this requirement is only for its chosen metal part.

---

## SMP-017-10 - Air Separator Vent Float Chamber Cap

Part name: Air Separator Vent Float Chamber Cap - single metal part

Material: low-carbon steel, ASTM A36 or equivalent (general-purpose single-piece metal stock)

Envelope: `{"length_mm": 90, "thickness_mm": 7, "width_mm": 90}`

Datum orientation: Use the finished bottom face as datum A. Use the long left edge as datum B and the near short edge as datum C. The origin is the lower-left-near corner of the finished rectangular envelope; X follows length, Y follows width, and Z is upward.

Full description:

Make the single metal part for the product idea 'Air Separator Vent Float Chamber Cap'. The broader
use case is: Hydronic air separators in HVAC mechanical rooms with automatic air vent assemblies.
The chosen deliverable is only the metal body implied by: Machined domed cap with large sealing
flange, central vent boss, internal float clearance cavity, small outlet thread, and wrench flats.
All other product elements are external reference items and must not be modeled. The part must
perform this mechanical role: Closes the float chamber, supports the vent mechanism, and provides
threaded service and outlet connections. It is intentionally included in the SubCAD limit corpus
because: Combines external dome contours, internal cavity constraints, sealing flanges, concentric
and eccentric bosses, threads, flats, and serviceable assembly interfaces. The part is made from
low-carbon steel, ASTM A36 or equivalent using sheet or plate stock. Start from one flat sheet or
plate blank. Cut the outside profile, machine holes, slots, pockets, lips, and relief features into
that same piece. If bends are called out, they are bends in the same sheet part, not separate welded
pieces.

Functional features:
- single rectangular metal body: Machine one body with finished envelope 90 mm x 90 mm x 7 mm.
- mounting hole pattern: Drill two through holes diameter 8 mm on the length centerline at X=18 mm and X=72 mm, Y=45 mm.
- functional center feature: Machine a central obround slot 30 mm long x 13 mm wide through the part, centered at X=45 mm, Y=45 mm.
- top relief pocket: Mill a rectangular relief pocket 25 mm x 30 mm x 3 mm deep on the top face, centered between the mounting holes.
- edge chamfers: Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.
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
- Do not broaden the requirement back into the full product idea named 'Air Separator Vent Float Chamber Cap'; this requirement is only for its chosen metal part.

---
