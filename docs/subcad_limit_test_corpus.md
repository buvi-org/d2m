# SubCAD Limit-Test Corpus

This corpus is intended to test whether SubCAD can represent real mechanical
product intent without weakening the requirement to match current SubCAD
capabilities.

## Non-Negotiable Rule

The first English requirement for a part is the source of truth. After a part
description is frozen, later stages must not dilute, simplify, reinterpret, or
change it to accommodate shortcomings in SubCAD, generation agents, exporters,
viewers, or comparison tooling.

If SubCAD cannot represent a frozen requirement, the result is a SubCAD gap.
The requirement stays intact.

## Corpus Stages

### Stage 1: Raw Product Ideas

Create raw product ideas before any concrete part requirements are written.

The original target was 1000 ideas. On 2026-06-16 the working Stage 1 corpus
was frozen at 540 ideas by user decision because that was enough coverage to
begin part expansion.

- Use independent agent assignments.
- Initial batches used 10 ideas per agent.
- The last active generation batch size was 30 different product ideas per
  agent so the corpus could cover more ground faster.
- Future corpus expansion may continue in 30-idea batches, but the current
  frozen Stage 1 set is 540 ideas.
- Count progress by completed agent outputs, not by edited or curated ideas.
- Every idea must include:
  - `idea_title`
  - `product_context`
  - `core_function`
  - `likely_main_part`
  - `why_it_tests_cad_representation`
- Raw ideas are not yet concrete part specifications.
- Raw ideas must preserve the agent/domain provenance.
- Do not write SubCAD code in this stage.
- Do not filter ideas by current SubCAD capability.
- Do not begin Stage 2 until the current Stage 1 idea set is frozen.

### Stage 2: Concrete Mechanical Part Requirements

Expand each raw product idea into one concrete mechanical part.

The Stage 2 scope is deliberately narrower than the full product idea:

- Each requirement must describe exactly one metal part.
- The part must be made from sheet, rod, plate, or block stock.
- If the raw idea describes a multi-part product, choose one metal part from
  that product and specify only that part.
- Do not include assemblies, fasteners, bearings, springs, bushings, rubber,
  plastic, electronics, labels, adhesives, coatings as geometry, or bought-out
  items.

Each expanded part must include:

- Material and manufacturing context.
- Overall envelope and stock assumptions.
- Complete dimensions in millimeters.
- Datum orientation and coordinate convention.
- All functional features with positions, sizes, depths, radii, chamfers, and
  clearances.
- Required holes, bores, pockets, slots, grooves, ribs, pads, profiles, threads,
  tapers, angled faces, repeating patterns, and surface details.
- Tolerances where they matter.
- Explicit acceptance checklist.
- Explicit negative requirements: things the generated part must not contain,
  omit, approximate away, or move.

The expanded English text becomes immutable once reviewed.

### Stage 3: SubCAD Program Generation

Agents generate SubCAD code from the frozen English part requirement.

- The frozen English requirement is the only product truth.
- Agents may inspect SubCAD API documentation.
- Agents must not alter the requirement.
- Agents must not replace a hard feature with an easier one.
- Agents must not use imported opaque geometry as a shortcut.

### Stage 4: Execution And Manual Review

For each SubCAD program:

- Execute the program.
- Export STEP and STL.
- Generate high-resolution turntable review media.
- Review the result manually against the original frozen English requirement.
- Record pass/fail per acceptance checklist item.
- Record SubCAD language gaps separately from agent mistakes.

## Result Categories

- `pass`: The generated part matches the frozen requirement.
- `agent_error`: SubCAD could likely represent the requirement, but the generated
  program is wrong.
- `subcad_gap`: The requirement is clear, but SubCAD cannot express it correctly.
- `export_or_geometry_bug`: The SubCAD program expresses the intent, but STEP,
  STL, mesh, or visualization output is wrong.
- `review_blocked`: Manual review cannot decide with current artifacts.
