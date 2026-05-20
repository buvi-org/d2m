# TODO

Current baseline:

- Latest pushed commit previously noted: `aa9910c Fix simulation bridge and wire rich translator feedback`
- Core local tests expected to remain green:
  - `python test_agentic_translator.py`
  - `python test_sim_bridge.py`
  - `python test_subcad_integration.py`
  - `python test_fixturing_integration.py`

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

Status: complete and passing for the current prototype contract. Keep the acceptance test green while Simulation Reliability becomes the active next priority.

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
- Continue running the existing SubCAD, fixturing, translator, and simulation bridge tests as regression coverage.

## Active Next Priority: Simulation Reliability

Goal: move the now-passing simulation bridge from sanity coverage toward trustworthy prototype validation.

1. Validate against representative target meshes.
   - Use real target meshes instead of demo scaled-stock references for validation endpoints.
   - Compare simulated stock against target meshes with mesh/feature feedback.

2. Exercise authored neutral toolpaths.
   - Prefer explicit schema v1/Phase 2 neutral toolpaths when present.
   - Retain generated simple toolpaths as a fallback for older operation dictionaries.

3. Add reliability assertions.
   - Add gouge/deviation checks for known machining cases.
   - Keep volume/material-removal coverage green while expanding accuracy checks.

4. Track representative performance.
   - Measure runtime and stability on practical stock sizes and toolpath lengths.
   - Avoid claiming production simulation validity until these cases are documented.

## What SubCAD Can Do Now

- Build subtractive machining programs with the fluent `Stock` API, including core and Phase 2 operations.
- Represent fixtures, setups, work offsets, stock/material metadata, tools, feeds/speeds, and process-plan summaries.
- Export STEP/STL geometry, `subcad.shop_floor.v1` process-plan JSON, and Markdown/JSON setup sheets.
- Serialize neutral toolpaths for preview, validation, estimation, and simulation handoff.
- Render preview-only G-code with explicit non-production warnings.
- Validate malformed/empty authored toolpaths and estimate cycle time from authored path length/feed data where available.

Still deferred: controller-certified production G-code, production UI, live translator success claims, and validated simulation/RL workflows.

## Deferred Roadmap

- Live translator trials remain next after simulation reliability improves.
- GNN feature recognition and LLM fine-tuning should wait for execution-scored data.
- RL remains later-stage research after simulator fidelity is validated.
