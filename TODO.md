# TODO

Current baseline:

- Latest pushed commit previously noted: `aa9910c Fix simulation bridge and wire rich translator feedback`
- Core local tests expected to remain green:
  - `python test_agentic_translator.py`
  - `python test_sim_bridge.py`
  - `python test_subcad_integration.py`
  - `python test_fixturing_integration.py`

## SubCAD Shop-Floor v1

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

## Integration Checks

- Add and run `python test_subcad_shopfloor_v1.py` once Agents 1-4 finish their integration work.
- The test covers schema v1 required/backward fields, non-empty neutral toolpaths, setup-sheet content, fluent Phase 2 API, validation warnings/errors, and simulation bridge toolpath fallback/preference.
- Continue running the existing SubCAD, fixturing, translator, and simulation bridge tests as regression coverage.

## Deferred Roadmap

- Live translator trials remain next after shop-floor v1 stabilizes.
- GNN feature recognition and LLM fine-tuning should wait for execution-scored data.
- RL remains later-stage research after simulator fidelity is validated.
