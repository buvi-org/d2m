# TODO

## Project Hierarchy Toward A STEP-To-SubCAD Model

Ultimate goal:

Train and evaluate an AI model/workflow that can take a STEP file and produce
an executable pure SubCAD program. The generated program must reproduce the
original geometry, express manufacturable intent, validate shop-floor
plausibility, and provide time/cost estimates.

The hierarchy is:

1. Model objective.
   - Input: STEP geometry, material, quantity, tolerance/PMI when available,
     and optional rendered visual evidence.
   - Output: pure SubCAD Python program plus process plan, setup sheet,
     validation, simulation/comparison report, visualization package, and
     economics.
   - Proof: execute SubCAD, export generated STEP, compare against the original
     STEP target, and reject failures.

2. Required training/evaluation dataset.
   - Build at least 100,000 original-STEP-verified pairs.
   - Each pair must contain the original STEP, generated pure SubCAD, generated
     STEP, comparison metrics, feature-family tags, validation, process plan,
     setup/economics artifacts, and provenance metadata.
   - A pair counts only when generated SubCAD executes and generated STEP
     matches the original Zero-to-CAD STEP under the trusted comparison policy.

3. Dataset generation pipeline.
   - Parse Zero-to-CAD row: CadQuery source, ops trace, UUID, split, and
     original STEP bytes.
   - Build pure SubCAD feature plan.
   - Generate SubCAD with the translator/model.
   - Execute generated SubCAD.
   - Export generated STEP and manufacturing artifacts.
   - Compare generated STEP to original STEP.
   - Repair with bounded retries.
   - Save accepted and failed attempts with full manifests.

4. Coverage work required before scaling to 100k.
   - Mature operation families until they execute and match: profile, edge
     treatment, retained material, holes, patterns, axisymmetric/turning,
     thin-wall/shell, surface/sweep/loft, and wire/profile cutting.
   - Measure each family separately using feature-family benchmark summaries.
   - Scale live translation only for families with acceptable pass rates.

5. Model training readiness.
   - Keep accepted original-STEP-verified pairs separate from synthetic
     self-generated pairs.
   - Use accepted pairs for evaluation and supervised training/fine-tuning.
   - Use failed attempts and repair traces for feedback-loop training and
     prompt/model improvement.
   - Do not train on unverified SubCAD that merely looks plausible.

6. Future model options.
   - Start with the existing agentic LLM translator loop.
   - Add STEP/B-Rep evidence JSON and optional projected visual frames.
   - Fine-tune only after enough verified pairs exist.
   - From-scratch or self-play training remains research-grade and depends on a
     reliable simulator/comparison environment plus far more compute/data than
     the current RTX 4090 path can provide alone.

Current baseline:

- Latest pushed implementation commit for the coverage/live-pilot slice:
  `6f644a2 Expose face selectors for coverage ops`
- Core local tests expected to remain green:
  - `python test_agentic_translator.py`
  - `python test_sim_bridge.py`
  - `python test_subcad_integration.py`
  - `python test_fixturing_integration.py`
  - `python test_subcad_shopfloor_v1.py`
  - `python test_subcad_phase2_toolpaths.py`
  - `python test_subcad_visualization.py`
  - `python test_subcad_manufacturing_economics.py`

## Workstream A: 100k Original-STEP-Verified Pure SubCAD Dataset

Status: active program goal. The TODO was missing this as a single end-to-end
acceptance plan, so this section is the project truth for "all 100k SubCAD
programs and STEP pairs."

Latest measured dry scan:

- Command: `python -m src.data.run_zero_to_cad_feature_benchmarks --split all --no-summary-file`
- Date: 2026-05-21
- Rows scanned: 100,516.
- Plannable by pure-operation planner: 86,923.
- Unsupported by current planner: 13,593.
- Matched original-STEP-verified pairs: 8 recorded by guarded live pilots:
  - `hole_pilot_006`, train global index 1, UUID
    `420cc2e2-e6c4-23e5-092a-6980c7853952`.
  - `hole_batch_002_filtered`, train global index 8, UUID
    `c691d510-62b1-786d-6815-d0bbe5ece63c`.
  - `hole_batch_003_edge_retry`, train global index 14, UUID
    `715a4e72-092b-d79a-277e-42ff521cef71`.
  - `hole_batch_004_forward_filtered`, train global index 17, UUID
    `648b1adc-9964-9e71-82a5-7a4ceeaf0db9`.
  - `hole_batch_004_forward_filtered`, train global index 18, UUID
    `9771f32b-c614-f1ed-9533-5ff2617f3471`.
  - `hole_batch_007_forward_filtered`, train global index 25, UUID
    `ca8ac443-0284-9d83-4ef9-db3c9b930a47`.
  - `hole_row29_retry_taper_prompt2`, train global index 29, UUID
    `e7b057a8-03c2-5b83-99b5-2cce0bb055c5`.
  - `hole_row23_retry_strict_noop_evidence`, train global index 23, UUID
    `8562152c-3c84-b0c7-e887-1975fe1a0c4e`.
- Note: closed/inaccessible `shell(...)` parts are now rejected as
  `unsupported_unmachinable` instead of being counted as plannable CNC work.
- Note: the first accepted live pair required fixing retained rectangular
  islands/ribs, profile-pocket islands, CadQuery `rect(x, y)` to SubCAD
  `length=X`/`width=Y`, and all-edge chamfer scope.
- Family membership counts overlap because one part can require multiple operation families:
  - edge_treatment: 64,721
  - hole: 61,216
  - retained_material: 46,416
  - cut: 43,039
  - profile: 40,537
  - primitive: 32,796
  - pattern: 20,436
  - boss: 18,803
  - axisymmetric: 12,290
  - surface: 6,690
  - thin_wall: 3,004

Definition of done:

- At least 100,000 accepted pairs exist across the local Zero-to-CAD train/val/test corpus.
- Every accepted pair contains the original source STEP, generated pure SubCAD program, generated STEP, process plan, setup sheet, validation, comparison metrics, simulation metadata when available, economics output, feature-family tags, source row identity, and git/model/prompt version metadata.
- The generated SubCAD executes without hybrid/imported opaque geometry.
- The generated STEP matches the original source STEP under the configured benchmark tolerance, default `0.10 mm` unless a run explicitly records a different tolerance.
- Accepted pairs are counted only after original-STEP comparison passes the trusted match policy.
- Self-generated SubCAD -> STEP pairs are allowed only as auxiliary synthetic/pretraining data and never count as Zero-to-CAD translation success.

Acceptance gates for each kept pair:

1. Source integrity.
   - Save the original Zero-to-CAD `model.step` as the immutable comparison target.
   - Save CadQuery source, ops trace, split, parquet row, global index, and UUID.

2. Pure SubCAD generation.
   - Generated code must use SubCAD operations only.
   - Reject `hybrid_feature`, `import_step`, direct CadQuery reconstruction, opaque B-Rep/mesh reuse, or skipped unsupported features.
   - Store the pure planner candidates and the final operation families used.

3. Execution and manufacturing package.
   - Execute generated SubCAD.
   - Export generated STEP/STL where available.
   - Export `subcad.shop_floor.v1` process plan, validation report, setup sheet, selected tools/fixtures, toolpaths, timing, and economics.

4. Geometry verification.
   - Compare generated STEP against the original source STEP.
   - Record volume, bounding-box, slice/mesh/feature comparison metrics, pass/fail status, tolerance, alignment policy, and localized deviation feedback.
   - Treat comparison failure as failed data, not a partially accepted pair.
   - Current trusted-match gate for guarded pilots requires volume match plus
     rich comparison pass when requested; slice/mesh pilots use minimum score
     95.0 at the recorded tolerance, with volume-only success explicitly
     rejected.

5. Dataset quality control.
   - Write one manifest record per attempt with status: `planned`, `attempted`, `executed`, `matched`, `failed`, `unsupported`, or `manual_review`.
   - Track feature-family pass rates, common repair causes, average iterations, cost/time estimates, and validator warnings.
   - Keep train/val/test split identity intact.
   - Validator errors should reject a kept training pair unless the manifest
     explicitly labels the row as geometry-only research data.

Sub-workstreams required to reach 100k:

1. Feature-family measurement.
   - Use `python -m src.data.run_zero_to_cad_feature_benchmarks --split all` for aggregate planner scans.
   - Use family filters to choose controlled live batches, for example `--family profile --family edge_treatment`.
   - Report plannable, selected, attempted, executed, matched, failed, unsupported, and remaining-to-goal counts.

2. Translator execution loop.
   - Connect the feature-family benchmark runner to the live translator/original-STEP comparison executor.
   - Add retry budgets, stop conditions, and per-family batch limits so AI requests are not wasted.
   - Save repair history and prompt/model metadata for every attempt.

3. Operation-family maturation.
   - Profile family: richer slot/obround, arc-chain, spline/polyline, island, and contour fidelity.
   - Edge treatment family: selected-edge chamfers/fillets with local selectors and tolerance checks.
   - Retained material family: bosses, pads, ribs, raised cylinders, and machining-around islands.
   - Axisymmetric family: round stock, turning, cones/frustums, rings, sleeves, shafts, grooves, and revolved profiles.
   - Thin-wall family: shells, hollow bores, tubes, open cavities, accessibility checks, and wall-thickness validation.
   - Surface family: domes, sweeps, lofts, splines, freeform tolerance machining, and 4/5-axis intent.
   - Pattern family: rectangular/polar/mirror extraction and repeated operation emission.

4. Comparison reliability.
   - Validate the trusted comparison policy with known good/bad STEP examples per family.
   - Improve localized feature feedback before scaling expensive live attempts.
   - Keep volume-only success from being counted as trusted success.

5. Collection orchestration.
   - Run small per-family pilot batches first.
   - Scale only families that achieve acceptable match rates; initial promotion
     target is at least 70% trusted-match rate over a 25-attempt guarded pilot,
     with stop/escalation when three consecutive failures share the same
     missing operation class.
   - Pause or downrank families that repeatedly fail for the same missing capability.
   - Periodically regenerate aggregate summaries and update this TODO with measured counts.

Immediate next implementation targets:

- Done: extend the feature-family benchmark runner with all-split scans, family filters, selected/filtered counts, and aggregate summaries.
- Done: connect the benchmark runner to the existing live translator executor in a guarded mode with explicit `--execute --executor translator`.
- Done: add dataset attempt manifest JSONL utilities and optional benchmark-runner manifest output.
- Done: add Markdown reporting for feature-family benchmark summaries.
- Done: add live pilot stop guardrails for max attempts, max failures, consecutive failures, target matches, and minimum match-rate checks.
- Done: run the first guarded live original-STEP verification pilot for the
  hole/retained-material family; first accepted pair is recorded in
  `runs/zero_to_cad_live_pilots/hole_pilot_006`.
- Done: add manifest-backed accepted-row skipping so future benchmark runs can
  count already verified pairs toward the target without re-spending translator
  calls.
- Done: add feature-family exclusion filters so guarded live batches can avoid
  known high-risk families such as axisymmetric/revolve until their geometry is
  implemented.
- Done: run a filtered hole-family live batch excluding axisymmetric/surface/
  thin-wall rows; accepted row 8 and identified selector/edge-treatment B-Rep
  robustness as the next blocker.
- Done: harden directional edge-chamfer selectors and make edge chamfer degrade
  safely when OpenCascade cannot build the requested chamfer.
- Done: rerun the edge-treatment retry batch; accepted row 14 and isolated row
  13 as a retained-material placement/union geometry gap rather than an edge
  treatment crash.
- Done: add retained-material placement support (`cx`, `cy`, explicit
  stock_envelope) and translator prompt rules for construction-only internal
  unions.
- Done: prevent outside-stock retained islands from cutting away the whole
  stock, and reinforce literal CadQuery `translate((x, y, z))` coordinate use
  in the translator prompt.
- Next: scale the hole/profile/retained-material/axisymmetric pilot from 8
  accepted pairs to a small guarded batch of 10-25 accepted/attempted rows,
  preserving strict stop conditions.
- Next: retry row 13 and the next filtered hole-family rows; if row 13 still
  fails, classify the remaining issue as union/construction-feature detection
  rather than API placement.
- Blocked row: train global index 13 still fails after placement/fallback
  fixes; it is now executable but diverges geometrically, so pause retries until
  feature evidence can distinguish construction-only internal unions from real
  retained material.
- Done: run the next filtered hole-family batch; accepted rows 17 and 18, and
  isolated row 15 as another retained/side-feature geometry blocker.
- Blocked rows: train global indexes 20 and 21 failed in the next filtered
  batch; pause retries until patterned retained ribs and gear/tooth-like
  retained/cut features are planned more explicitly.
- Blocked row: train global index 23 failed because generated code used a bare
  undefined measure variable instead of `m.<name>`; this is a translator prompt
  or static preflight repair issue, not a missing SubCAD operation.
- Done: strengthen translator prompt tests and instructions against bare
  copied measure variables such as `flange_thickness`.
- Blocked row: train global index 23 now executes after the measure prompt fix
  but still diverges geometrically; pause retries until hex/profile feature
  evidence and prompt examples improve.
- Done: run the next filtered batch; accepted row 25.
- Blocked rows: train global index 26 volume-matches but fails trusted geometry,
  and index 28 still hits empty-selection failures after retained/boss planning.
- Done: add translator prompt coverage for `Stock.cylindrical(...)` so round
  stock/circle-extrusion rows are not forced into rectangular stock.
- Done: preserve the best executable translator attempt when a later repair
  attempt fails execution, so useful geometry/comparison results are not lost.
- Done: add geometry-backed tapered-cylinder/frustum support through
  `turn_profile`, classify CadQuery tapered circle extrudes as axisymmetric
  turn-profile work, and tighten the translator prompt so `taper=-angle`
  expands the top diameter instead of shrinking it.
- Done: accept train global index 29 via `hole_row29_retry_taper_prompt2`
  with trusted slice score 100.0.
- Done: split `profile_cutout` from `profile_pocket` geometry semantics:
  through cutouts now retain the requested profile outline and leave a usable
  top face for later pockets/drills.
- Done: add regular polygon profile dict support and clarify that CadQuery
  `.polygon(n, diameter)` maps to SubCAD `circumdiameter=diameter`.
- Blocked row: train global index 28 no longer fails from an empty top face or
  fallback 10x10 profile. It now fails because bottom-side boss/rib retained
  material is not sequenced/accessed correctly; next fix should add explicit
  bottom setup / face-selector handling for retained boss and rib operations.
- Done: add `circumdiameter` profile support so CadQuery `.polygon(n, value)`
  can be translated without confusing its diameter argument with a radius.
- Done: add CadQuery variable-volume evidence to translator prompts so no-op
  source variables/chains can be omitted instead of forced into SubCAD.
- Done: accept train global index 23 via
  `hole_row23_retry_strict_noop_evidence` with trusted slice score 99.4.
- Done: expose `face_selector` through fluent pocket, circular pocket, drill,
  selected retained-material operations, and related coverage ops; update the
  translator prompt to preserve CadQuery workplane face selectors such as
  `<Z` instead of silently converting underside operations to top-side work.
- Next: include the row 23 and row 29 accepted manifests in future
  accepted-index guarded runs, then continue forward to rows after 29 and the
  row 28/30/34/42 retained rib/boss and side-face gusset blockers.

## SubCAD Shop-Floor v1

Status: complete for the current prototype contract. Keep the acceptance test green while the next slice lands.

Goal: make SubCAD output a shop-floor-ready intermediate package without claiming controller-ready CAM. The v1 handoff is a neutral, validated, JSON-serializable process plan plus setup-sheet exports for machinist review.

1. Lock schema v1.
   - Use `subcad.shop_floor.v1` as the schema identifier.
   - Require material, stock dimensions, tools, operations, units, setup/work-offset metadata where applicable, validation buckets, and estimated time/tool changes.
   - Preserve backward-compatible fields such as `operation`, `tool_type`, `tool_diameter_mm`, `depth_mm`, `position`, `feeds_speeds`, `total_operations`, and `tools_used`.

2. Emit neutral toolpaths.
   - Represent motion as controller-neutral moves such as rapid, feed, plunge, retract, dwell, and arc.
   - Include safe Z, feeds/speeds, coolant/spindle intent, length/time summaries, and JSON round-trip support.
   - Keep this layer post-processor agnostic; do not emit production G-code in v1.

3. Export setup sheets.
   - Provide Markdown and JSON exports suitable for review on the shop floor.
   - Include stock, material, tools, operations, setups/work offsets, warnings/errors, and deferred G-code notes.
   - Make warnings visible rather than burying them in operation metadata.

4. Validate key manufacturing issues.
   - Catch missing or invalid required schema fields.
   - Catch bad operation ordering, taps without drilled holes, invalid/empty toolpaths, impossible tool reach, fixture/clamp interference, and missing setup data for multi-setup plans.
   - Return structured validation buckets: `errors`, `warnings`, and `notes`.

5. Bridge simulation to toolpaths.
   - Prefer explicit neutral toolpaths when present.
   - Fall back to generated simple toolpaths for legacy operation dictionaries.
   - Keep `test_sim_bridge.py` passing while adding shop-floor coverage.

6. Defer G-code.
   - Treat controller-specific G-code as a later post-processing layer.
   - Do not mix machine dialects into schema v1.
   - Document exported setup sheets as review artifacts, not proof of machine-safe NC output.

## Phase 2 Toolpaths

Status: complete and passing for the current prototype contract. Keep the acceptance test green while Manufacturing Trust v1 hardening continues.

1. Emit neutral toolpaths for every Phase 2 operation.
   - `peck_drill`, `ream`, `bore`, `countersink`, `counterbore`, `thread_mill`, `t_slot`, `dovetail`, `groove`, `surface_3d`, `deburr`, and `spot_face` must all serialize non-empty motion intent.
   - Include safe Z, move types, feeds/speeds, length/time summaries, and JSON round-trip support.

2. Preserve Phase 2 summaries in process plans.
   - Each Phase 2 operation record should include a `toolpath_summary`.
   - Summaries should be useful for review: move/point count, length, estimated time, and bounds when the path provides positions.

3. Add a preview-only G-code adapter.
   - Include a visible preview/non-production warning.
   - Include units, setup/work offset, tools, operations, feeds/speeds, and neutral motion lines.
   - Keep production postprocessing deferred.

4. Improve validation and estimation.
   - Flag malformed, empty, or unsupported authored toolpaths.
   - Estimate time from authored toolpath length/feed when available instead of falling back to feature approximations.

## Integration Checks

- Keep running `python test_subcad_shopfloor_v1.py` for the completed Shop-Floor v1 contract.
- Keep running `python test_subcad_phase2_toolpaths.py` for the completed Phase 2 toolpath contract.
- The Phase 2 test passes and covers non-empty neutral toolpaths, process-plan summaries, preview-only G-code metadata, malformed-toolpath validation, and authored-path time estimation.
- Keep running `python test_subcad_visualization.py` for browser package coverage, including tool/holder and fixture/clamp-zone review metadata.
- Keep running `python test_subcad_manufacturing_economics.py` for time/cost estimate and program-comparison coverage.
- Continue running the existing SubCAD, fixturing, translator, and simulation bridge tests as regression coverage.

## Fixture And Tool Inventory v1

Status: complete for the current prototype contract. Keep the visualization and process-plan tests green while Manufacturing Trust v1 hardening continues.

Goal: make fixtures and tools first-class shop-floor intent without claiming production CAM readiness.

1. Maintain structured catalogs.
   - Use versioned catalog data for fixture and tool definitions.
   - Preserve fixture/tool semantics such as dimensions, clamp zones, clearance zones, selected catalog id, tool assembly, holder, stickout, flute length, and availability metadata.
   - Keep catalog JSON as the source of truth for v1; CadQuery/STEP/STL/GLB assets remain optional geometry hooks.

2. Preserve selected tool and fixture context.
   - Process plans should keep selected tool id, tool assembly, fixture id, setup/work-offset metadata, and backward-compatible flat tool fields.
   - Setup sheets should expose selected tool/fixture information clearly enough for review.

3. Visualize shop-floor context.
   - Browser packages should include fixture bodies, clamp zones, setup context, selected tool/holder metadata, toolpaths, stock states, and operation playback data.
   - Visualization remains an engineering review aid, not proof of machine safety.

## Manufacturing Trust v1

Status: initial implementation slice complete. Keep the new manufacturing trust tests green while broadening coverage.

Goal: move SubCAD from structured manufacturing intent toward credible engineering validation. The immediate focus is inventory-aware tool planning, realistic pass plans, fixture/tool-holder clearance, and simulation/comparison reliability.

1. Plan from available tools.
   - Initial selector exists and chooses available catalog tools instead of inventing ideal diameters.
   - Operation/process-plan records now preserve selected tool id, selected assembly, selection reason, rejected tools, and warnings/errors.
   - Missing or unsafe tools are surfaced as structured validation issues.
   - Next: broaden policy controls for preferred machine pockets, tool material/coating, and shop-specific inventory constraints.

2. Generate realistic pass plans.
   - Core operations now use actual selected tool geometry and safe limits for stepover/stepdown where authored paths exist.
   - Pass-plan metadata now exposes roughing/finishing/rest flags, depth levels, stepover lanes, total passes, and per-pass timing.
   - Cycle time is recalculated from generated paths.
   - Next: make Phase 2 special tools as inventory-aware as the core operations.

3. Check fixture, cutter, shank, and holder clearance.
   - Authored neutral toolpaths are sampled against clamp and clearance zones.
   - Cutter, shank, and holder envelope checks return structured warnings/errors with operation number, tool id, fixture id, zone label, component, point, and clearance where available.
   - Setup sheets and visualization exports carry warning/marker metadata.
   - Next: extend from semantic zones to simplified fixture-body and stock-envelope collision checks.

4. Harden simulation and comparison.
   - Simulation result now includes status and per-operation timing metadata while continuing to prefer authored neutral toolpaths.
   - Benchmark tests cover known-good and known-bad target comparison cases: overcut, undercut, shifted features, wrong drill locations, and clamp/toolpath interference.
   - Next: validate against larger real CAD/STEP examples and compare simulated stock, not only final authored geometry.

5. Upgrade browser review.
   - Viewer now shows selected tool id, holder id, pass number, operation time, total time, and warnings for the selected operation.
   - Toggles cover stock, fixture, clamp zones, toolpath, tool/holder, clearance markers, and comparison diff.
   - Next: add richer marker labels and comparison heatmap rendering.

## Visualization

Status: browser visualization now supports the current review workflow for stock, target, toolpaths, operation playback, selected tools/holders, fixtures, clamp zones, and engineering economics metadata.

1. Export visualization packages from SubCAD.
   - Use `Stock.visualization_package("web/sessions/latest", target=...)`.
   - Package includes `scene.json`, stock/state meshes, `toolpath.json`, selected tool/holder metadata, fixture/clamp-zone metadata, and optional target/comparison/diff assets.

2. Review in the browser.
   - Serve `web/` and open `visualization.html?session=sessions/latest/scene.json`.
   - Inspect stock mesh, transparent target overlay, neutral toolpaths, operation timeline/playback, selected tool/holder, fixture body, clamp zones, comparison markers, total time, and total cost when economics is exported.

3. Next visualization improvements.
   - Add pass-level details, warning/clearance markers, and clearer selected-operation timing.
   - Add richer per-vertex heatmap rendering in Three.js once comparison reliability improves.
   - Add live WebSocket streaming after Python simulation reliability is stronger.
   - Keep WebGPU material removal as a later acceleration path.

## Manufacturing Economics v1

Status: initial implementation slice complete. Keep the economics acceptance test green while calibrating rates and expanding comparison examples.

Goal: estimate engineering time/cost from the same neutral manufacturing intent so two valid programs can be compared by speed, cost, or a tradeoff score. This is not a formal shop quote or ERP integration.

1. Maintain local costing catalogs.
   - Machine rates live in `src/subcad/catalogs/machines.json`.
   - Material prices/density/waste factors live in `src/subcad/catalogs/materials_cost.json`.
   - Tool wear cost fields live in `src/subcad/catalogs/tools.json` and `ToolSpec`.
   - Next: calibrate rates, tool life, and waste factors against real shop data.

2. Preserve old cycle-time behavior.
   - `estimated_time_minutes` remains cutting/path time for backward compatibility.
   - `estimate_cost(...)` adds total time fields for tool changes, setup, load/unload, and batch amortization.
   - Next: add optional machine-specific rapid/tool-change policies instead of one generic default.

3. Estimate cost.
   - Material cost uses stock volume, density, price/kg, and waste factor.
   - Machine/setup cost uses local machine hourly rates.
   - Tooling cost uses selected tool id, cutting minutes, and tool life/replacement cost.
   - Missing prices warn instead of crashing.
   - Next: account for consumables, inspection time, scrap risk, and setup family reuse.

4. Compare alternate programs.
   - `compare_programs(...)` reports fastest, cheapest, weighted-best, and Pareto-optimal candidates.
   - Invalid plans or failed target comparisons are marked instead of ranked as valid.
   - Next: create benchmark pairs that make the same part with different tools/strategies and compare measured simulated quality, time, and cost together.

5. Surface economics in reports.
   - Setup sheets include machine time, tool-change time, setup time, total time, material/machine/setup/tooling cost, total cost, and a non-quote note.
   - Visualization packages and the browser metadata panel include economics when supplied.
   - Next: add per-pass cost labels and summary comparison views in the browser.

## What SubCAD Can Do Now

- Build subtractive machining programs with the fluent `Stock` API, including core and Phase 2 operations.
- Represent fixtures, setups, work offsets, stock/material metadata, selected tools, tool assemblies, feeds/speeds, and process-plan summaries.
- Export STEP/STL geometry, `subcad.shop_floor.v1` process-plan JSON, and Markdown/JSON setup sheets.
- Serialize neutral toolpaths for preview, validation, estimation, and simulation handoff.
- Render preview-only G-code with explicit non-production warnings.
- Review fixture bodies, clamp zones, selected tools/holders, operation playback, and stock states in the browser viewer.
- Validate malformed/empty authored toolpaths and estimate cycle time from authored path length/feed data where available.
- Estimate engineering total time and cost, including tool changes, setup/load-unload time, machine cost, material cost, and tooling cost.
- Compare candidate programs by fastest, cheapest, weighted tradeoff, and Pareto status.

Still deferred: controller-certified production G-code, formal quoting/ERP integration, production UI, live translator success claims, and validated simulation/RL workflows.

## Deferred Roadmap

- STEP-to-SubCAD AI model planning is documented in `docs/step_to_subcad_ai.md`.
  - Build a STEP evidence package first: exact B-Rep/feature JSON, rendered views, optional turntable video, and a frame manifest mapping projected labels back to exact dimensions.
  - Treat images/video as supporting evidence, not the source of dimensions.
  - Benchmark JSON-only, JSON plus still images, and JSON plus still images/video before committing to multimodal input as a default.
- Live translator trials are the next proof step.
  - Use each Zero-to-CAD sample's original `model.step` as the target.
  - Generate SubCAD with the agentic translator, execute it, and compare the generated STEP against the original target STEP.
  - Save generated SubCAD, comparison metrics, validation, economics, and repair history.
  - Do not count self-generated SubCAD -> STEP pairs as translator success; they are auxiliary supervised/pretraining data only.
  - Use `python -m src.data.run_zero_to_cad_translations` for the corrected flow.
  - The compatibility gate now uses a typed pure-operation planner. Current local train/val/test scan finds 86,923 plannable rows out of 100,516 after rejecting inaccessible closed shells.
  - Treat planner coverage as an attempt queue, not success. Each family still needs geometry/toolpath maturation and original-STEP verification before it counts toward 100k.
  - Initial geometry-backed slice is complete for selected-edge chamfers/fillets, lightweight profile pockets/cutouts/contours, and retained profile/cylindrical bosses.
  - Active next slice: Retained Feature And Face-Setup Fidelity v1.
    - Make top/bottom retained ribs, bosses, pads, and cylinders preserve the intended island volume instead of erasing surrounding upper features.
    - Preserve CadQuery workplane face selectors in generated SubCAD operations and process plans.
    - Gate side-face additive gussets as manual-review/unsupported until oriented side-profile machining is implemented.
    - Continue feature-family benchmark reporting for plannable, attempted, executed, matched, failed, and unsupported rows.
  - Later SubCAD capability maturation targets for 100k: side-face/oriented profile machining, robust retained multi-island planning, shells/thin walls, turning/revolves, sweeps, lofts, and original-STEP verification at scale.
- GNN feature recognition and LLM fine-tuning should wait for execution-scored data.
- RL remains later-stage research after simulator fidelity is validated.
