# STEP-To-SubCAD AI Model Requirements

This note captures the current direction for moving beyond authored SubCAD
programs toward an AI system that can take a STEP file and generate executable
SubCAD.

## Goal

The target is an AI-assisted translation loop:

```text
STEP file + material + quantity + tolerances/PMI when available
-> STEP/B-Rep understanding
-> feature and dimension evidence package
-> AI SubCAD generator
-> SubCAD execution
-> target comparison and manufacturability validation
-> repair loop
-> ranked SubCAD programs with time/cost estimates
```

The output should not be a static process-plan guess. It should be a SubCAD
program that can execute, export a process plan, compare against the original
STEP target, surface validation issues, and estimate engineering time/cost.

## Current Objective And Dataset Gate

The concrete project objective is to train and evaluate a STEP -> pure SubCAD
model/workflow from at least 100,000 original-STEP-verified Zero-to-CAD pairs.
The current local corpus scan has 79,911 plannable rows out of 100,516
Zero-to-CAD rows, but planner coverage is only the attempt queue. Guarded live
pilots currently record 518 unique accepted original-STEP-verified pairs.

A pair is accepted only when:

- The original Zero-to-CAD `model.step` is saved as the immutable target.
- Generated code uses pure SubCAD operations and no hybrid geometry escape
  hatches such as imported opaque B-Rep/mesh reuse, direct CadQuery
  reconstruction, or skipped unsupported features.
- Generated SubCAD executes, exports a generated STEP, and emits the
  process-plan, setup, validation, comparison, economics, and provenance
  artifacts.
- Generated STEP passes original-STEP comparison under the recorded trusted
  match policy and tolerance.
- The manifest records source split/row/UUID, feature families, runner command,
  prompt/model id, comparison method, SubCAD/process-plan schema version, and
  git commit.

## Core Decision

Use STEP/B-Rep derived data as the source of truth. Use vision as supporting
evidence.

Structured geometry should carry exact information:

- Dimensions, positions, radii, depths, volumes, and units.
- Face and edge topology.
- Surface types and adjacency.
- Feature candidates such as holes, pockets, slots, bosses, islands, chamfers,
  fillets, and datum-like faces.
- Tolerances, material, surface finish, and PMI when available from STEP AP242
  or external metadata.

Images and video should help the model and humans understand the part, but
they should not be trusted as the only source of dimensions. Manufacturing
requires exact geometry. A visually plausible 6 mm hole in the wrong location
is still a failed plan.

## Why Vision Is Still Useful

Vision is useful when paired with exact geometry:

- It gives the model a fast global sense of orientation and shape.
- It helps identify top/bottom/side setup intuition.
- It makes missing or surprising features easier to notice during review.
- It helps humans debug why the AI chose a plan.
- It may help the repair loop when feature JSON alone is hard to interpret.

The current recommended evidence format is not "video vs JSON." It is:

```text
JSON for truth.
Images/video for understanding.
SubCAD execution for proof.
Simulation/comparison for trust.
```

## Vision And Dimension Projection

We can create a video from a STEP file and overlay dimensions on the shape.
The important implementation detail is that the dimensions must come from the
STEP/B-Rep extraction, then be projected into the rendered view.

For every rendered view or video frame, save a sidecar manifest:

```json
{
  "frame_id": "top_001",
  "camera": "top",
  "features": [
    {
      "feature_id": "hole_04",
      "type": "hole",
      "screen_bbox": [420, 180, 470, 230],
      "exact_dimensions": {
        "diameter_mm": 6.0,
        "depth_mm": 12.0,
        "center_mm": [20.0, -15.0, 0.0]
      }
    }
  ]
}
```

The overlay should show:

- Overall dimensions.
- Hole diameters, depths, and centers.
- Pocket and slot width, length, depth, and position.
- Feature IDs that match the structured JSON.
- Datum axes and setup-facing hints.
- Hidden or rear-side feature markers when needed.

This lets the AI consume visual context while still having an exact, auditable
mapping back to the STEP-derived geometry.

## Recommended Architecture

Use a staged modular system first. Defer fine-tuning until execution-scored
data exists.

```text
STEP Parser
-> B-Rep / AAG Feature Extractor
-> Evidence Builder
   -> part_understanding.json
   -> features.json
   -> rendered views
   -> optional turntable video
   -> view/frame manifest
-> SubCAD Planning Agent
-> SubCAD Code Generator
-> SubCAD REPL Execution
-> STEP Target Comparison
-> Validation + Economics
-> Repair Agent
```

The AI generator should receive:

- `part_understanding.json`.
- Feature graph JSON.
- Stock, material, setup, machine, and tool inventory context.
- SubCAD API reference.
- Optional rendered images or selected video frames.
- Execution and comparison feedback from earlier attempts.

The AI should return:

- SubCAD Python program.
- Manufacturing assumptions.
- Unresolved ambiguities.
- Required stock and setup intent.
- Selected tool and fixture intent where possible.
- Validation warnings.
- Time/cost estimate once the plan is executable.

## Data Products

For each STEP input, create a durable evidence directory:

```text
sessions/step_evidence/<sample_id>/
  input.step
  part_understanding.json
  features.json
  views/
    top.png
    front.png
    side.png
    iso.png
    manifest.json
  turntable.webm
  generated_subcad.py
  generated_model.step
  process_plan.json
  comparison.json
  validation.json
  economics.json
  manifest.json
```

This gives us both a product artifact and future training/evaluation data.

## Correct Benchmark Flow

There are two different dataset flows, and they must not be confused.

### Translator benchmark flow

This is the immediate proof path for CadQuery/STEP -> SubCAD:

```text
Zero-to-CAD sample
  cadquery_code.py
  ops_trace.json
  original model.step
-> DeepSeek/LLM translator generates SubCAD
-> execute generated SubCAD
-> export generated STEP
-> compare generated STEP against the original Zero-to-CAD model.step
-> save generated SubCAD, comparison metrics, validation, economics, and repair history
```

This is the flow that answers: "Can AI generate SubCAD for an existing CAD
part?" A candidate only counts as successful if it matches the original target
STEP from the source dataset, not a STEP produced from the generated SubCAD.

Implemented runner: `python -m src.data.run_zero_to_cad_translations`.

Useful commands:

```bash
python -m src.data.run_zero_to_cad_translations --scan-compatible --source-dir data/zero_to_cad_100k --split train
python -m src.data.run_zero_to_cad_translations --source-dir data/zero_to_cad_100k --split train --comparison-methods slice --target-successes 100000
```

Current policy:

- The source artifact for every run is the original Zero-to-CAD STEP bytes saved
  as `original_model.step`.
- The translator may converge on volume first, but the batch runner only counts
  a kept sample after original-STEP comparison passes the trusted match policy.
- Rich comparison applies translation-only bounding-box alignment because
  Zero-to-CAD and SubCAD use different local origins for the same physical part.
- For the current 2.5D collection pass, `--comparison-methods slice` is the
  practical trusted mode. The existing vertex-based SDF is useful feedback but
  too noisy on sparse STEP tessellations to be the hard gate.
- The compatibility gate is now a typed pure-operation planner. It maps local
  chamfers/fillets, retained bosses/unions, circle extrusions, shells, revolves,
  sweeps, lofts, cones, spheres, and arbitrary profiles to explicit SubCAD
  operation families instead of skipping them up front.
- Planner compatibility is not success. A sample only becomes a kept pair after
  the generated SubCAD executes and passes original-STEP geometry comparison.

Current scan of `data/zero_to_cad_100k` with the pure planner:

- train: 64,424 plannable rows out of 81,015.
- val: 7,704 plannable rows out of 9,734.
- test: 7,783 plannable rows out of 9,767.
- total: 79,911 plannable rows out of 100,516 local rows.

Guarded live pilots currently record 518 unique accepted original-STEP-verified pairs.
The reduction from earlier planner counts is intentional: closed/inaccessible
shell operations are now rejected as unsupported CNC work instead of counted as
plannable rows.

This means the project moved from "few rows can even be attempted" to "most
rows can be assigned pure operation families." The next proof step is maturing
each operation family's geometry/toolpaths until original-STEP verification
passes at scale.

Geometry-backed pure operation slice:

- Selected-edge chamfer/fillet now route through CadQuery edge selectors.
- Profile pocket/cutout/contour now cut lightweight polygon/circle/rectangle
  profiles in the B-Rep backend.
- Retained-material operations for profile/cylindrical bosses now remove
  surrounding stock around retained islands.
- These are still v1 geometry implementations; original-STEP verification is
  still required before counting translated samples as successful.

Completed implementation slice:

- Improve profile fidelity for rectangle, circle, polygon, slot/obround,
  arc-chain, and spline/polyline approximations.
- Add feature-family benchmark reporting so Zero-to-CAD progress is visible by
  operation family: plannable, attempted, executed, matched, failed, and
  unsupported.
- Harden translator prompts and repair feedback so generated code stays within
  pure SubCAD operations and compares against the original STEP target.

Active next implementation slice:

- Run accepted-index guarded forward scans after the latest verified row and
  classify each blocker before spending larger live batches.
- Promote deterministic builders for families that repeatedly match original
  STEP targets: simple profiles, L-brackets, retained ribs, construction
  patterns, no-op source features, and later thin-wall/turning/surface families.
- Track family metrics for selected, attempted, executed, matched, failed, and
  unsupported rows before scaling any bucket.
- Maintain accepted-index manifests so previously verified rows count toward
  the 100k target without re-running paid/live translator calls.
- Track the corpus-capacity gap explicitly: 79,911 current plannable rows cannot
  yield 100k accepted pairs unless unsupported families mature or more source
  STEP rows are added.
- Release training-ready datasets only as versioned manifests that separate
  accepted original-STEP-verified pairs from failed attempts, manual-review
  rows, and synthetic/self-generated auxiliary pairs.

### Self-generated SubCAD-pair flow

This is only for supervised pretraining and regression data:

```text
generate SubCAD program
-> execute SubCAD
-> export STEP
-> save SubCAD + STEP as a pair
-> verify by re-executing the same SubCAD and comparing to the saved STEP
```

This proves the pair is reproducible and internally consistent. It does not
prove translation quality against Zero-to-CAD or any external STEP file. These
pairs are useful because they provide clean labels, but they are not a live
translator success metric.

Priority order:

1. Run the translator benchmark on real Zero-to-CAD samples.
2. Keep only execution-scored successful translations for evaluation/training.
3. Use self-generated SubCAD pairs as auxiliary supervised data, clearly marked
   as synthetic/self-generated.

## Model Strategy

Start with an agentic multimodal LLM workflow:

1. Build exact STEP/B-Rep evidence.
2. Generate SubCAD from structured evidence, optionally including images.
3. Execute generated SubCAD.
4. Compare the generated geometry to the target STEP.
5. Feed localized geometry, feature, validation, and economics feedback back to
   the model.
6. Keep the best executable candidate.

Only fine-tune after we have many successful, execution-scored examples.
Training on unverified text pairs would create a model that sounds right but
may not produce manufacturable SubCAD.

Training readiness requires a frozen accepted-pair index with original STEP
hashes, generated SubCAD/STEP hashes, comparison policy, prompt/model version,
runner command, SubCAD schema version, and git commit. Failed attempts and
repair traces should remain available for feedback-loop learning, but they are
not part of the primary verified training/evaluation split unless explicitly
labeled as negative or repair data.

## Evaluation

Benchmark three input modes:

1. Structured JSON only.
2. Structured JSON plus still images.
3. Structured JSON plus still images plus video frames.

Measure:

- SubCAD generation success.
- Execution success.
- Target geometry match.
- Missing, extra, shifted, and wrong-size features.
- Validation errors and warnings.
- Number of repair iterations.
- Total time and total cost of the generated plan.
- Whether vision improved or hurt the result.

Keep video in the AI loop only if it measurably improves setup choice,
feature recognition, geometry match, or repair speed.

## Implementation Notes For This Repository

Existing pieces to build on:

- `src/cad_parser/parser.py` already parses STEP geometry features, bounding
  boxes, volume, and closed-shell status.
- `src/cad_parser/renderer.py` already generates standard views and explicitly
  leaves room for dimension annotations.
- `src/simulation/feature_compare.py` already contains feature extraction and
  comparison utilities.
- `src/data/agentic_translator.py` already implements an execution and repair
  loop for CadQuery-to-SubCAD translation.
- SubCAD now provides process plans, validation, visualization, simulation
  handoff, and economics output for generated programs.

The next implementation should add a STEP evidence builder and then adapt the
existing translator loop to consume STEP evidence instead of CadQuery source.

## References

- Autodesk UV-Net shows why B-Rep/topology-native learning is a strong fit for
  CAD geometry: https://www.research.autodesk.com/publications/uv-net-learning-from-boundary-representations/
- NIST describes STEP AP242 as a carrier for model-based engineering data,
  tolerances, and PMI: https://www.nist.gov/publications/portrait-iso-step-tolerancing-standard-enabler-smart-manufacturing-systems
- Recent VLM spatial reasoning benchmarks show that vision models still need
  care around exact spatial reasoning: https://arxiv.org/abs/2503.19707
- CAD-GPT is a useful reference direction for combining CAD construction with
  multimodal spatial reasoning: https://huggingface.co/papers/2412.19663
