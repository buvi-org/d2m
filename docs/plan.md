# d2m — Project Plan

## Current Position

d2m is no longer just the original CAPP roadmap. The repository now contains a substantial subtractive-CAD and simulation prototype, plus an agentic CadQuery -> SubCAD translator. The docs should therefore separate three things:

1. **Implemented and tested** — code that exists and has passing local tests.
2. **Implemented prototype** — code that exists and passes local tests but still needs validation on representative workflows.
3. **Aspirational roadmap** — the original GNN, fine-tuning, UI, and RL plan.

Primary objective as of 2026-05-21: build 100,000 original-STEP-verified
Zero-to-CAD -> pure SubCAD pairs for training/evaluating a STEP-to-SubCAD model.
Rows count only when generated pure SubCAD executes, exports generated STEP and
manufacturing artifacts, and matches the original Zero-to-CAD `model.step`.

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
- Fixture, tool assembly, and multi-setup metadata.
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

Status: complete and passing for the current prototype contract.

The completed Phase 2 contract extends the shop-floor handoff so every Phase 2 operation has authored neutral motion intent that can be previewed, validated, estimated, and passed toward simulation.

The Phase 2 contract includes:

- Non-empty neutral toolpaths for `peck_drill`, `ream`, `bore`, `countersink`, `counterbore`, `thread_mill`, `t_slot`, `dovetail`, `groove`, `surface_3d`, `deburr`, and `spot_face`.
- Process-plan operation records with serialized toolpaths plus summaries that expose move/point count, length, estimated time, and bounds where applicable.
- A preview-only G-code adapter that includes a visible preview warning, units, setup/work offset, tools, operations, feeds/speeds, and neutral motion lines.
- Validation that flags malformed, empty, or unsupported toolpath records before simulation or CAM handoff.
- Cycle-time estimation that prefers authored neutral toolpath length/time over feature-dimension approximations.

Production postprocessing remains deferred. The preview adapter is a review aid only, not a controller-certified NC output.

### Fixture And Tool Inventory v1

Status: complete for the current prototype contract.

SubCAD now treats shop-floor fixtures and tools as structured manufacturing intent instead of arbitrary viewer objects.

The current contract includes:

- Versioned fixture and tool catalog data.
- Fixture semantics for dimensions, clamping zones, clearance zones, setup context, and visualization payloads.
- Selected tool identity and tool assembly metadata, including holder/stickout/flute information where available.
- Backward-compatible operation/process-plan fields for existing tests and downstream callers.
- Browser visualization metadata for fixture bodies, clamp zones, setup context, selected tools, shank/holder geometry, stock states, and operation playback.

This is still not production CAM. The catalogs and viewer provide reviewable intent and validation context; they do not certify that a real machine setup is safe.

### Manufacturing Economics v1

Status: initial implementation slice complete.

SubCAD can now estimate engineering time/cost from process-plan intent without changing the older cutting-time field. The economics layer is a planning and tradeoff aid, not a production quote or ERP integration.

The current contract includes:

- Local machine cost catalog with hourly machine/setup rates, setup minutes, load/unload minutes, and default tool-change seconds.
- Local material cost catalog with density, price/kg, and waste factor.
- Tool catalog/tool spec cost fields for replacement cost, expected life, and optional cost per cutting minute.
- `estimate_cost(...)` for `Stock`, `ProcessPlan`, or process-plan dicts.
- `compare_programs(...)` for fastest, cheapest, weighted-best, and Pareto-optimal program ranking.
- Setup-sheet and visualization metadata for total time, total cost, per-operation cutting/tooling cost, and economics warnings.
- Backward compatibility: `estimated_time_minutes` remains cutting/path time; total time lives in `time_breakdown`.

This should be calibrated against real shop rates and tool life before anyone treats the numbers as commercial quoting inputs.

Current test status:

| Test | Result | Notes |
|------|--------|-------|
| `python test_subcad_integration.py` | PASS, 39/39 | Fluent chain, exports, process-plan JSON, volume monotonicity, immutability, threaded holes, round trip. |
| `python test_fixturing_integration.py` | PASS, 19/19 | Fixture/setup metadata, flip setup, clearance warning path, JSON round trip, error handling. |
| `python test_subcad_shopfloor_v1.py` | PASS | Acceptance coverage for the completed Shop-Floor v1 contract. |
| `python test_subcad_phase2_toolpaths.py` | PASS | Acceptance coverage for completed Phase 2 toolpaths, preview-only G-code, validation, and estimation work. |
| `python test_subcad_visualization.py` | PASS | Visualization package coverage, including current fixture/tool review metadata. |
| `python test_subcad_manufacturing_economics.py` | PASS | Engineering time/cost estimates, tool-change/setup amortization, and program ranking. |

### What SubCAD Can Do Now

SubCAD is now usable as the repository's subtractive machining representation and shop-floor handoff prototype:

- Build CadQuery-backed subtractive programs with the fluent `Stock` API, including core operations, Phase 2 operations, fixtures, setups, work offsets, tools, feeds/speeds, stock, and material metadata.
- Export STEP/STL geometry, `subcad.shop_floor.v1` process-plan JSON, and Markdown/JSON setup sheets for review.
- Preserve neutral toolpaths with summaries for preview, validation, cycle-time estimation, and simulation handoff.
- Render preview-only G-code from neutral motion intent while clearly deferring production controller-specific postprocessing.
- Validate schema and authored toolpath issues before simulation or downstream CAM handoff.
- Export static browser visualization packages for Three.js review of stock, target, toolpaths, selected tools/holders, fixtures, clamp zones, comparison data, and diff markers.
- Estimate engineering total time/cost and compare alternate valid programs by fastest, cheapest, weighted score, and Pareto status.

SubCAD is still a prototype layer. It is best described as a programmable manufacturing-intent, validation, and engineering-estimate layer, not a Fusion/SolidWorks CAM replacement or formal quoting system. It does not yet provide production-certified G-code, industrial CAM strategy coverage, a complete upload-to-plan UI, ERP-backed quoting, or validated simulation/RL outcomes.

### Visualization Direction

Use the browser viewer as the primary visualization surface. Python remains the geometry/simulation source of truth and exports static sessions through `Stock.visualization_package(...)`; `web/visualization.html` loads the package with Three.js.

This gives immediate interactive review without waiting for browser-side simulation:

- Stock and target STL display.
- Neutral toolpath overlay.
- Operation metadata and setup context.
- Selected tool/holder and fixture/clamp-zone review.
- Comparison JSON and overcut/undercut marker display.
- Total time/cost metadata when an economics report is exported.

The longer-term visualization roadmap is pass-level warning/clearance markers, richer per-vertex heatmaps, live WebSocket streaming from Python simulation, then WebGPU material removal once the Python simulator is validated.

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
| `python test_agentic_translator.py` | PASS, 121/121 | Covers non-LLM translator components, corrected Zero-to-CAD runner policy tests, REPL integration, geometry comparison, feedback formatting, and mocked rich-comparison propagation. |

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

## Manufacturing Trust v1

Status: initial implementation slice complete.

This phase moves SubCAD from structured manufacturing intent toward credible engineering validation. Correctness remains more important than adding broad new operation families.

### 1. Inventory-Aware Tool Planning

Goal: choose from available catalog tools instead of inventing ideal cutters.

Current coverage:

- Operation/process-plan records include selected tool id, selected assembly, selection reason, rejected tools, required feature constraints, and warnings/errors when no available tool can satisfy the operation.
- Core operations such as slots, pockets, circular pockets, drilling, facing, contouring, and chamfers use selected tool geometry and safe limits.
- Missing or unsafe tools produce structured validation errors instead of fake-valid toolpaths.

Next hardening:

- Add shop-specific tool preference policy for machine pockets, material/coating, and inventory reservations.
- Bring the same selection metadata depth to more Phase 2 special operations.

### 2. Realistic Pass Planning

Goal: make toolpaths and cycle time reflect actual tool choice.

Current coverage:

- Operations expose roughing, finishing, rest-machining, depth-level, stepover-lane, and per-pass timing metadata.
- Slot and pocket toolpaths visibly change when a selected tool is smaller than the feature.
- Estimated time is derived from generated passes and feed/plunge data.

Next hardening:

- Add more explicit rest-machining records when a second finishing tool is required.
- Validate pass plans against representative shop limits instead of generic safe defaults.

### 3. Fixture, Tool, And Holder Clearance

Goal: detect obvious physical conflicts before simulation or CAM handoff.

Current coverage:

- Sample authored neutral toolpaths against clamp and clearance zones.
- Check cutter, shank, and holder envelopes conservatively.
- Return structured warnings/errors with operation number, tool id, fixture id, zone label, and clearance where available.
- Show warnings in setup sheets and visualization metadata.

Next hardening:

- Extend sampled checks from clamp/clearance zones to simplified fixture-body and stock-envelope collision shapes.
- Add visible marker labels and severity filtering in the viewer.

### 4. Simulation And Comparison Reliability

Goal: harden the now-passing simulation bridge into a useful validation loop.

Current coverage:

- Target-comparison tests cover direct Stock targets plus STEP-path acceptance instead of demo scaled-stock references.
- Prefer explicit neutral toolpaths and selected tool assemblies during simulation, retaining generated simple toolpaths as fallback for legacy dictionaries.
- Add known-good and known-bad cases for pocket depth, overcut slots, wrong drill locations, excessive tool diameter, and clamp/toolpath interference.
- Report final volume, removed volume, overcut/undercut metrics, collision/clearance issues, per-operation timing, and pass/fail status.
- Keep `python test_sim_bridge.py`, `python src\simulation\tri_dexel.py`, and `python -m src.simulation.material_removal` passing.

Next hardening:

- Compare simulated stock against the target, not only final authored geometry.
- Expand benchmark parts from small synthetic examples to real CadQuery/STEP samples.

### 5. Visualization Review Upgrade

Goal: make the browser viewer explain questionable plans, not only draw them.

Current coverage:

- Viewer shows selected tool id, holder id, pass number, operation time, total time, and warnings for the selected operation.
- Toggles cover stock, fixture, clamp zones, toolpath, tool/holder, clearance markers, and comparison diff.
- Visualization packages export pass-plan and clearance-marker data.

## Manufacturing Economics v1

Status: initial implementation slice complete.

Goal: let SubCAD compare valid manufacturing programs by engineering time and cost while preserving the neutral process-plan contract.

Current coverage:

- `src.subcad.economics.estimate_cost(...)` reports cutting time, tool-change time, setup time, load/unload time, total time, material cost, machine cost, setup cost, tooling cost, total cost, warnings, and assumptions.
- `Stock.estimate_cost(...)` and `ProcessPlan.estimate_cost(...)` expose the same estimator through public APIs.
- `src.subcad.economics.compare_programs(...)` ranks candidates by fastest, cheapest, weighted best, and Pareto status.
- Setup sheets and visualization packages carry economics output when requested.
- Browser metadata shows total time, total cost, cost components, machine id, and the engineering-estimate-only status.

Next hardening:

- Calibrate machine/material/tool catalogs from real shop data.
- Add benchmark program pairs that produce the same target with different strategies, then compare quality, time, and cost together.
- Add optional consumables, inspection time, scrap risk, and setup-family reuse.
- Add richer browser comparison views for alternate programs.

## Following Plan After Manufacturing Trust v1

### Validate Mesh and Feature Comparison on Real Samples

Goal: ensure localized comparison feedback is accurate enough to guide the translator.

### Run Live Translation Trials

Goal: measure whether the agentic loop can translate CadQuery samples into equivalent SubCAD programs.

The benchmark target must be the original Zero-to-CAD `model.step` for each
sample. Self-generated SubCAD -> STEP pairs are useful supervised data, but
they are not evidence that the translator can match external CAD.

Current implementation:

- `src.data.run_zero_to_cad_translations` streams local Zero-to-CAD parquet rows,
  writes each original STEP as `original_model.step`, runs the agentic
  translator, exports generated SubCAD/process-plan artifacts, and records
  trusted match policy results.
- `--scan-compatible` now uses the typed pure-operation planner. The local
  train/val/test dataset currently reports 86,923 plannable rows out of
  100,516 rows after rejecting inaccessible closed shells, but this is planner
  coverage rather than verified translation success.
- Original-STEP verification remains the success gate. Each new operation
  family must mature from "planned" to "executes and matches" before it counts
  toward the 100k dataset.
- Guarded live pilots currently record 411 accepted original-STEP-verified pairs across train/val/test splits.
- Use `--comparison-methods slice` for the current 2.5D collection pass; SDF is
  retained as feedback but is too noisy on sparse STEP tessellations to be the
  hard success gate today.
- The typed pure-operation planner and the first geometry-backed pure operation
  slice are complete. Selected-edge chamfers/fillets, lightweight profile
  pockets/cutouts/contours, and retained profile/cylindrical bosses now execute
  through SubCAD geometry rather than being only planned records.

Active next slice:

- Run guarded feature-family batches with explicit attempt, execution, match,
  failure, unsupported, and remaining-to-goal counts.
- Preserve accepted-index manifests so the 411 verified rows count toward future
  runs without re-spending live translator calls.
- Harden retained rib/boss, bottom-face, and side-face setup fidelity while
  keeping side-face additive gussets manual-review/unsupported until oriented
  side-profile machining is implemented.
- Deterministic preflight now accepts layered retained row 31, top-retained
  rib row 34, cylindrical polar-rib row 42, annular-rib row 44, cylindrical
  grid-boss row 45, washer/polar-hole row 46, circular vent plate row 47,
  no-op-aware star/radial-pocket plate row 49, top-chamfer box row 50,
  top-chamfer box row 57, hollow shell-cover row 58, filleted cage row 61,
  split shroud row 62, L-bracket/counterbore row 80, flange/collar row 342, and
  later deterministic profile/chamfer/counterbore rows through train row 80938,
  plus the first split-aware val/test rows, against their original STEP
  targets; the next deterministic target should be chosen from split-aware
  accepted-index guarded scans after the latest verified absolute corpus range.
- Keep accepted programs pure SubCAD: no hybrid/imported opaque geometry, no
  direct CadQuery reconstruction, and no skipped unsupported features.

### Build Dataset From Successful Translations

Goal: create reliable training/evaluation pairs only after execution and comparison are trustworthy.

Dataset policy:

- Primary evaluation pairs come from live translator attempts that execute and
  compare against the original source STEP.
- Self-generated SubCAD pairs are auxiliary pretraining data only and must be
  labeled as synthetic/self-generated.
- Do not report self-generated exact matches as Zero-to-CAD translation success.
- A training-ready release needs a versioned manifest with source split, row
  index, UUID, original STEP hash/path, generated SubCAD and generated STEP
  hash/path, feature-family tags, comparison method/tolerance, validation
  status, economics artifact path, prompt/model id, runner command,
  SubCAD/process-plan schema version, and git commit.
- Failed attempts, manual-review rows, and synthetic/self-generated pairs stay
  in separate manifests from the primary original-STEP-verified split.

### Revisit ML Roadmap

Only after reliable execution/comparison data exists, revisit fine-tuning, GNN feature recognition, and RL.

## Completed Near-Term Slice

### Integrate Phase 2 Toolpaths

Goal: make Phase 2 operations first-class shop-floor intent, not just geometry modifiers.

Acceptance criteria met:

- Every Phase 2 operation emits non-empty neutral toolpath data.
- Process plans preserve Phase 2 toolpaths and expose useful summaries.
- Preview-only G-code export contains warnings and review metadata without claiming production postprocessing.
- Validation catches malformed authored toolpaths.
- Estimated time changes with authored path length and feed rates.
- `python test_subcad_phase2_toolpaths.py` passes.

## Roadmap Status

| Area | Status | Current Decision |
|------|--------|------------------|
| Synthetic data | Complete enough for prototype use | Keep; regenerate only if labels/schema change. |
| SubCAD API | Implemented and passing integration tests | Continue using as canonical subtractive representation. |
| SubCAD Shop-Floor v1 | Complete | Maintain schema, neutral toolpaths, setup sheets, validation, and deferred production G-code contract. |
| Phase 2 toolpaths | Complete | Maintain authored neutral paths, summaries, preview-only G-code adapter, malformed-path validation, and path-based estimates. |
| Fixture/tool inventory v1 | Complete | Maintain structured catalogs, selected tool assemblies, fixture/clamp visualization, and browser review metadata. |
| Manufacturing Economics v1 | Initial slice complete | Maintain engineering estimates, setup/tool-change time, material/machine/setup/tooling cost, and program comparison; calibrate against real shop data next. |
| Agentic translator | Implemented; non-live tests pass | Harden prompts around pure-operation candidates, then run live Zero-to-CAD trials against each original `model.step`. |
| Mesh comparison | Implemented | Verify and tune; no need to reimplement first. |
| Feature comparison | Implemented | Validate on known samples and feed into translator loop. |
| Manufacturing Trust v1 | Initial slice complete | Maintain inventory-aware planning, realistic passes, fixture/tool-holder clearance, simulation comparison reliability, warning-focused visualization, and economics calibration while STEP coverage work continues. |
| Pure STEP-to-SubCAD coverage | Active next priority | Harden retained rib/boss, bottom-face, and side-face setup fidelity; keep feature-family verification reporting; require original-STEP matches before counting dataset pairs. |
| Simulation bridge | Prototype passing tests | Harden as part of Manufacturing Trust v1 against representative target meshes, authored toolpaths, and gouge/deviation cases. |
| STEP-to-SubCAD AI model | Planned | Use STEP/B-Rep feature JSON as source of truth, with rendered views/video as supporting evidence; see `docs/step_to_subcad_ai.md`. |
| GNN feature recognition | Planned | Defer until subtractive workflow proves what features are needed. |
| LLM fine-tuning | Planned | Defer until high-quality execution-scored pairs exist. |
| Product UI | Planned/prototype pieces exist | Defer productization until backend semantics stabilize. |
| RL fine-tuning | Aspirational | Defer until simulator is reliable and externally validated. |

## Original Product Goal

The long-term CAPP goal remains:

> Upload a STEP file -> receive ranked, rule-compliant manufacturing process plans with DFM feedback, cost/time estimates, and explanations.

Current repository reality is narrower:

> Translate/generate subtractive SubCAD programs, execute them, compare the resulting geometry to references, estimate engineering time/cost, and develop a simulation-backed feedback loop.

The recommended plan is to finish the narrower loop first. Once SubCAD execution, comparison, and simulation are reliable, the broader upload-to-plan product roadmap becomes much less speculative.

## Success Criteria

Near-term success:

1. Simulation tests include real target-mesh deviation/gouge cases, not only volume/removal sanity checks.
2. Translator comparison feedback identifies localized geometry errors, not only volume ratio.
3. Live translation trials produce measured success/failure data.
4. Documentation reports measured status, not hoped-for capability.

Roadmap success:

1. End-to-end CAD/metadata input produces a valid process plan.
2. Generated operations execute through SubCAD.
3. Simulation and comparison catch infeasible or geometrically wrong plans.
4. Economics reports allow alternate valid programs to be compared by time, cost, and tradeoff score.
5. UI exposes plans, warnings, geometry feedback, and estimate assumptions clearly.
6. Any ML fine-tuning is evaluated against executable outcomes, not just text similarity.
7. STEP-to-SubCAD generation uses exact STEP/B-Rep evidence as the primary input, with vision/video benchmarked as supporting context rather than treated as geometry truth.
8. The STEP-to-SubCAD training set reaches 100,000 accepted original-STEP-verified Zero-to-CAD pairs, with current progress reported separately from planner coverage: 411 accepted pairs and 86,923 plannable rows out of 100,516 local rows as of 2026-05-21.

## Cost Notes

The previous cost table was tied to the original GNN/fine-tuning-first plan. SubCAD now has an engineering economics estimator for individual manufacturing programs, but project budget planning is still separate. The immediate recommended work is debugging, validation, and calibration, so the near-term project cost is mainly developer time plus any LLM API usage for live translation trials.

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
