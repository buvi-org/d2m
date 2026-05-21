# TODO

Current baseline:

- Latest pushed viewer commit before the current trust slice: `25de657 Upgrade SubCAD viewer operation review`
- Core local tests expected to remain green:
  - `python test_agentic_translator.py`
  - `python test_sim_bridge.py`
  - `python test_subcad_integration.py`
  - `python test_fixturing_integration.py`
  - `python test_subcad_shopfloor_v1.py`
  - `python test_subcad_phase2_toolpaths.py`
  - `python test_subcad_visualization.py`
  - `python test_subcad_manufacturing_economics.py`

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
  - The compatibility gate now uses a typed pure-operation planner. Current local train/val/test scan finds 100,235 plannable rows out of 100,516.
  - Treat planner coverage as an attempt queue, not success. Each family still needs geometry/toolpath maturation and original-STEP verification before it counts toward 100k.
  - Initial geometry-backed slice is complete for selected-edge chamfers/fillets, lightweight profile pockets/cutouts/contours, and retained profile/cylindrical bosses.
  - Active next slice: Profile Fidelity + Feature-Family Verification v1.
    - Improve rectangle/circle/polygon/slot/arc/spline profile fidelity.
    - Add feature-family benchmark reporting for plannable, attempted, executed, matched, failed, and unsupported rows.
    - Harden translator prompts and repair feedback around pure-operation candidates and original-STEP comparison.
  - Later SubCAD capability maturation targets for 100k: round stock/circle extrusions, shells/thin walls, turning/revolves, sweeps, lofts, and original-STEP verification at scale.
- GNN feature recognition and LLM fine-tuning should wait for execution-scored data.
- RL remains later-stage research after simulator fidelity is validated.
