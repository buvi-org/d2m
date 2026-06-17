# Single Metal Part Requirements

This folder contains Stage 2 review candidates generated from the raw SubCAD
limit-test ideas.

Current frozen input size: 540 raw ideas from 42 agent files.

Boundary rule:

- Each requirement describes exactly one metal part.
- The allowed starting forms are sheet, rod, plate, or block.
- Larger products, assemblies, electronics, plastic, rubber, bearings, bushings,
  springs, bought-out fasteners, labels, and coatings are outside the modeled
  scope.
- If the raw idea was a multi-part product, the Stage 2 requirement selects one
  metal part from that product and describes only that part.
- These are English review candidates. After review, accepted entries become
  immutable product truth for SubCAD program generation.

Files:

- `agent_###_*.json`: machine-readable Stage 2 requirements for one source agent.
- `agent_###_*.md`: human-readable review copy for the same requirements.
- `all_single_metal_parts.jsonl`: one JSON object per requirement.
- `manifest.json`: file counts, part counts, and generation rule summary.
