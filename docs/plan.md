# d2m — Project Plan

## Current Position

d2m is no longer just the original CAPP roadmap. The repository now contains a substantial subtractive-CAD and simulation prototype, plus an agentic CadQuery -> SubCAD translator. The docs should therefore separate three things:

1. **Implemented and tested** — code that exists and has passing local tests.
2. **Implemented prototype** — code that exists and passes local tests but still needs validation on representative workflows.
3. **Aspirational roadmap** — the original GNN, fine-tuning, UI, and RL plan.

## Implemented Status

### Synthetic Dataset

- `generate_synthetic_data.py` and `convert_dataset.py` exist.
- `synthetic_10k_samples.7z` contains the generated synthetic dataset.
- Current dataset status: 9,994 labeled synthetic CAD parts with STEP/JSON/renders are available.

### SubCAD Core

SubCAD is implemented as the current machining representation layer:

- Fluent `Stock` API for subtractive operations.
- STEP/STL export.
- Process-plan JSON export and summary.
- Tool/material helpers.
- Fixture and multi-setup metadata.
- Integration bridge toward simulation tools.

### SubCAD Shop-Floor v1

Status: complete for the current prototype contract.

SubCAD process plans now serve as the shop-floor-ready intermediate handoff while keeping controller-specific production G-code out of scope.

The v1 contract includes:

- Schema identifier `subcad.shop_floor.v1`.
- Required plan fields for material, stock dimensions, units, tools, operations, setup/work-offset metadata, validation buckets, estimated time, and tool changes.
- Backward-compatible fields already used by prototype tests: `operation`, `tool_type`, `tool_diameter_mm`, `depth_mm`, `position`, `feeds_speeds`, `total_operations`, and `tools_used`.
- Neutral toolpath data for rapid/feed/plunge/retract/dwell/arc moves with safe Z, feed/spindle/coolant intent, length/time summaries, and JSON round-trip support.
- Setup-sheet export in Markdown and JSON containing stock, material, tools, operations, setups, work offsets, warnings/errors, and a deferred-G-code note.
- Validation buckets that distinguish blocking errors from warnings and notes.

Acceptance coverage is tracked in `test_subcad_shopfloor_v1.py`. It is intentionally focused on the integration contract rather than the internal implementation.

### Phase 2 Toolpaths

Current integration target: extend the completed shop-floor handoff so every Phase 2 operation has authored neutral motion intent that can be previewed, validated, estimated, and passed toward simulation.

The Phase 2 contract should include:

- Non-empty neutral toolpaths for `peck_drill`, `ream`, `bore`, `countersink`, `counterbore`, `thread_mill`, `t_slot`, `dovetail`, `groove`, `surface_3d`, `deburr`, and `spot_face`.
- Process-plan operation records with serialized toolpaths plus summaries that expose move/point count, length, estimated time, and bounds where applicable.
- A preview-only G-code adapter that includes a visible preview warning, units, setup/work offset, tools, operations, feeds/speeds, and neutral motion lines.
- Validation that flags malformed, empty, or unsupported toolpath records before simulation or CAM handoff.
- Cycle-time estimation that prefers authored neutral toolpath length/time over feature-dimension approximations.

Production postprocessing remains deferred. The preview adapter is a review aid only, not a controller-certified NC output.

Current test status:

| Test | Result | Notes |
|------|--------|-------|
| `python test_subcad_integration.py` | PASS, 39/39 | Fluent chain, exports, process-plan JSON, volume monotonicity, immutability, threaded holes, round trip. |
| `python test_fixturing_integration.py` | PASS, 19/19 | Fixture/setup metadata, flip setup, clearance warning path, JSON round trip, error handling. |
| `python test_subcad_shopfloor_v1.py` | PASS target | Acceptance coverage for the completed Shop-Floor v1 contract. |
| `python test_subcad_phase2_toolpaths.py` | New acceptance | Expected to pass after Agents 1-4 integrate Phase 2 toolpath, preview, validation, and estimation work. |

### Agentic Translator

The CadQuery -> SubCAD translator infrastructure exists in `src/data/agentic_translator.py`.

Implemented capabilities:

- Provider abstraction for DeepSeek, Anthropic, and OpenAI.
- Prompt builders for system, initial user prompt, and iteration feedback.
- LLM response code extraction.
- REPL execution through `run_subcad()`.
- Convergence controller that tracks success, improvement, stagnation, divergence, execution failure, and safety cap.
- Geometry comparison through `compare_to_reference()`.
- Optional richer mesh and feature comparison paths are present in the translator code.

Current test status:

| Test | Result | Notes |
|------|--------|-------|
| `python test_agentic_translator.py` | PASS, 55/55 | Covers non-LLM translator components, REPL integration, geometry comparison, feedback formatting, and mocked rich-comparison propagation. |

Important caveat: the passing translator test is not a live LLM success metric. No live DeepSeek/Anthropic/OpenAI translation batch is documented as passing here.

### Mesh / Feature Comparison

The original session note described localized comparison as a recommendation. The repository now contains implementation work:

- `src/simulation/mesh_compare.py` implements per-vertex signed deviation, Z-slice comparison, clustering, and feedback formatting.
- `src/simulation/feature_compare.py` contains feature-aware comparison support.
- `src/data/agentic_translator.py` has hooks for mesh and feature comparison feedback.

Recommended next step is not to build these from scratch; it is to verify them against representative translated samples and tune how their outputs influence translator scoring and iteration prompts.

## Recently Fixed Blocker

### Simulation Core: Zero Tri-Dexel Volume

`python test_sim_bridge.py` previously failed because tri-dexel initialization produced empty columns and `0.0` volume. That root cause has been fixed by adding an `rtree`-free ray/triangle fallback and storing hit distances relative to the grid ray origin.

| Test | Result | Failure |
|------|--------|---------|
| `python test_sim_bridge.py` | PASS, 51/51 | Stock volume, modified columns, and positive material removal are verified. |

Verified follow-up tests:

- `python src\simulation\tri_dexel.py` passes. Box volume error is 0.00%; sphere volume error is 0.14%.
- `python -m src.simulation.material_removal` passes. Initial stock volume is nonzero and all material removal self-tests pass.
- `python test_sim_bridge.py` passes 51/51.

Simulation should now be described as a passing prototype path, not a production validator. The next work is validation quality: real target meshes, richer toolpaths, gouge/deviation accuracy, and representative performance.

## Recommended Plan

### 1. Integrate Phase 2 Toolpaths

Goal: make Phase 2 operations first-class shop-floor intent, not just geometry modifiers.

Acceptance criteria:

- Every Phase 2 operation emits non-empty neutral toolpath data.
- Process plans preserve Phase 2 toolpaths and expose useful summaries.
- Preview-only G-code export contains warnings and review metadata without claiming production postprocessing.
- Validation catches malformed authored toolpaths.
- Estimated time changes with authored path length and feed rates.
- `python test_subcad_phase2_toolpaths.py` passes after implementation lands.

### 2. Harden Simulation Validation

Goal: move beyond “bridge tests pass” toward trustworthy simulation feedback.

Acceptance criteria:

- Use real target meshes instead of demo scaled-stock references for validation endpoints.
- Compare simulated stock against target meshes with mesh/feature feedback.
- Add gouge/deviation assertions to tests.
- Prefer explicit neutral toolpaths from schema v1 when present, with the existing generated simple toolpath path retained as a fallback for older operation dictionaries.
- Keep `python test_sim_bridge.py`, `python src\simulation\tri_dexel.py`, and `python -m src.simulation.material_removal` passing.

### 3. Validate Mesh and Feature Comparison on Real Samples

Goal: ensure localized comparison feedback is accurate enough to guide the translator.

Acceptance criteria:

- Per-vertex/SDF feedback distinguishes overcut vs undercut on known fixtures.
- Z-slice comparison identifies pocket-depth and through-hole mismatches.
- Feature-aware comparison produces actionable feedback for holes, pockets, slots, and chamfers.
- Translator history stores compact comparison output without overwhelming prompts.

### 4. Run Live Translation Trials

Goal: measure whether the agentic loop can translate CadQuery samples into equivalent SubCAD programs.

Acceptance criteria:

- Run live translations on the exploration samples with an API key configured.
- Record success rate, convergence iterations, failure categories, and token/cost profile.
- Save successful CadQuery/SubCAD pairs for later training.
- Do not claim translator success beyond the tested sample set.

### 5. Build Dataset From Successful Translations

Goal: create reliable training/evaluation pairs only after execution and comparison are trustworthy.

Acceptance criteria:

- Batch translation pipeline records source CadQuery, generated SubCAD, execution result, comparison metrics, and feedback.
- Failed translations are retained with reason labels for improvement.
- Dataset split separates training, validation, and hard negative cases.

### 6. Revisit ML Roadmap

Only after reliable execution/comparison data exists:

- Train or fine-tune a code-generation/planning model.
- Evaluate rule compliance and geometry fidelity separately.
- Consider GNN feature recognition if it remains necessary for the product workflow.
- Treat RL as late-stage research after simulation fidelity is validated.

## Roadmap Status

| Area | Status | Current Decision |
|------|--------|------------------|
| Synthetic data | Complete enough for prototype use | Keep; regenerate only if labels/schema change. |
| SubCAD API | Implemented and passing integration tests | Continue using as canonical subtractive representation. |
| SubCAD Shop-Floor v1 | Complete | Maintain schema, neutral toolpaths, setup sheets, validation, and deferred production G-code contract. |
| Phase 2 toolpaths | Current integration | Add authored neutral paths, summaries, preview-only G-code adapter, malformed-path validation, and path-based estimates. |
| Agentic translator | Implemented; non-live tests pass | Run live trials after simulation/comparison validation. |
| Mesh comparison | Implemented | Verify and tune; no need to reimplement first. |
| Feature comparison | Implemented | Validate on known samples and feed into translator loop. |
| Simulation bridge | Prototype passing tests | Harden against representative target meshes, toolpaths, and gouge/deviation cases. |
| GNN feature recognition | Planned | Defer until subtractive workflow proves what features are needed. |
| LLM fine-tuning | Planned | Defer until high-quality execution-scored pairs exist. |
| Product UI | Planned/prototype pieces exist | Defer productization until backend semantics stabilize. |
| RL fine-tuning | Aspirational | Defer until simulator is reliable and externally validated. |

## Original Product Goal

The long-term CAPP goal remains:

> Upload a STEP file -> receive ranked, rule-compliant manufacturing process plans with DFM feedback, cost/time estimates, and explanations.

Current repository reality is narrower:

> Translate/generate subtractive SubCAD programs, execute them, compare the resulting geometry to references, and develop a simulation-backed feedback loop.

The recommended plan is to finish the narrower loop first. Once SubCAD execution, comparison, and simulation are reliable, the broader upload-to-plan product roadmap becomes much less speculative.

## Success Criteria

Near-term success:

1. Translator comparison feedback identifies localized geometry errors, not only volume ratio.
2. Live translation trials produce measured success/failure data.
3. Simulation tests include real target-mesh deviation/gouge cases, not only volume/removal sanity checks.
4. Documentation reports measured status, not hoped-for capability.

Roadmap success:

1. End-to-end CAD/metadata input produces a valid process plan.
2. Generated operations execute through SubCAD.
3. Simulation and comparison catch infeasible or geometrically wrong plans.
4. UI exposes plans, warnings, and geometry feedback clearly.
5. Any ML fine-tuning is evaluated against executable outcomes, not just text similarity.

## Cost Notes

The previous cost table was tied to the original GNN/fine-tuning-first plan. The immediate recommended work is debugging and validation, so the near-term cost is mainly developer time plus any LLM API usage for live translation trials.

GPU/fine-tuning spend should wait until:

- The simulation bridge is validated beyond sanity tests.
- Live translation trials identify the real failure modes.
- There is a clean dataset of execution-scored examples.

## Deferred Aspirational Items

These remain useful future directions but are not implemented product status:

- GNN feature recognition trained on MFCAD/MFCAD++.
- DeepSeek managed fine-tuning for manufacturing planning.
- Full Streamlit/React production UI.
- Neo4j-backed production knowledge graph.
- Injection molding simulation.
- RL fine-tuning from simulator rewards.
- ERP/shop-floor integration.
- Fusion 360/SolidWorks plugin.
- Multi-tenant SaaS quoting product.
