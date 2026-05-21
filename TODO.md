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

5. Run orchestration and acceptance gates.
   - Run small guarded batches by feature family before broad corpus sweeps.
   - Stop or downrank a family when repeated failures share the same missing
     operation class.
   - Count progress by `selected`, `attempted`, `executed`, `matched`,
     `failed`, `unsupported`, and `remaining_to_goal`.
   - Promote a run only when original-STEP verification, process-plan
     validation, and provenance/version metadata are present.

6. Model training readiness.
   - Keep accepted original-STEP-verified pairs separate from synthetic
     self-generated pairs.
   - Use accepted pairs for evaluation and supervised training/fine-tuning.
   - Use failed attempts and repair traces for feedback-loop training and
     prompt/model improvement.
   - Do not train on unverified SubCAD that merely looks plausible.
   - Version every accepted row by source dataset identity, SubCAD API/schema
     version, comparison policy, prompt/model id, runner command, and git
     commit so later training sets can be reproduced or invalidated.

7. Future model options.
   - Start with the existing agentic LLM translator loop.
   - Add STEP/B-Rep evidence JSON and optional projected visual frames.
   - Fine-tune only after enough verified pairs exist.
   - From-scratch or self-play training remains research-grade and depends on a
     reliable simulator/comparison environment plus far more compute/data than
     the current RTX 4090 path can provide alone.

Current next actions:

- Run the next accepted-index guarded forward scan from the latest accepted row
  and record selected, attempted, executed, matched, failed, unsupported, and
  remaining-to-goal counts.
- Classify the next deterministic blocker before spending larger live batches.
- Maintain an accepted-manifest summary as the source of truth for row counts,
  latest accepted rows, comparison policy, and rejected/manual-review counts;
  propagate that summary to README and docs after each accepted slice.
- Start a separate STEP-only evidence-builder workstream so the eventual model
  can consume STEP/B-Rep evidence directly instead of depending on CadQuery
  source text.
- Close the corpus-capacity gap: 86,923 plannable local rows cannot yield
  100,000 verified pairs alone, so unsupported families must become plannable
  or additional original-STEP source rows must be added.

Current baseline:

- Latest pushed coverage status commit:
  `e05dbf6 Record deterministic profile rows 1278 1293 1458`
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
- Matched original-STEP-verified pairs: 233 recorded by guarded live pilots.
  - Accepted train global indexes:
    `1, 8, 14, 17, 18, 23, 25, 29, 31, 34, 42, 44, 45, 46, 47, 49, 50, 57, 58, 61, 62, 80, 83, 87, 88, 90, 107, 111, 115, 118, 132, 238, 342, 381, 415, 438, 503, 697, 698, 702, 870, 1126, 1170, 1173, 1278, 1293, 1458, 1479, 1536, 1595, 1647, 1823, 1906, 2162, 2209, 2257, 2288, 2450, 2896, 3047, 3175, 3231, 3414, 3487, 3777, 3787, 3966, 4065, 4081, 4227, 4559, 4562, 4811, 5248, 5435, 5442, 5606, 5713, 5983, 6026, 6034, 6207, 6326, 6458, 6477, 6481, 6510, 6623, 7391, 7409, 7434, 7479, 7685, 8273, 9733, 9749, 9752, 9786, 9787, 9794, 9795, 9802, 9803, 9807, 9814, 9856, 9870, 9930, 9980, 10672, 10814, 11218, 11960, 11990, 12098, 12736, 13428, 13541, 13744, 14131, 14381, 14664, 14959, 14960, 14963, 15058, 15062, 15554, 16239, 16491, 16557, 16589, 16624, 16813, 16824, 17567, 17758, 17804, 17826, 18325, 19094, 19463, 20659, 20787, 20817, 21106, 22599, 22770, 22871, 23979, 24356, 24534, 25542, 25668, 26802, 26825, 27306, 28928, 30665, 31041, 31061, 31070, 31196, 31657, 31733, 31759, 31811, 31815, 32032, 32253, 32399, 32464, 32470, 32506, 32721, 32722, 32996, 33124, 33145, 33184, 33200, 33248, 33483, 33543, 33674, 33714, 33920, 33954, 34103, 34111, 34331, 34340, 34345, 34578, 34965, 35018, 35194, 35324, 35344, 35412, 35436, 35699, 36808, 36832, 36982, 36997, 37220, 37328, 38113, 38327, 38336, 38350, 38376, 39195, 39774, 40051, 40203, 40270, 40904, 41047, 41294, 41678, 41918, 42036, 42245, 42272, 42334, 42770, 42988, 43017, 43583, 43639, 44440`.
  - Latest accepted rows include train global indexes 342, 1536, 1595, 1647,
    1823, 1906, 2162, 2209, 2257, 2288, 2450, 3047, 3175, 3231, 3487,
    3777, 4081, 4227, 5606, 1479, 2896, 3414, 3787, 3966, 4065,
    4559, 4562, 4811, 5248, 5435, 5442, 5713, 5983, 6026, 6034,
    6207, 6326, 6458, 6477, 6481, 6510, 6623, 7391, 7409, 7434,
    7479, 7685, 8273, 9733, 9749, 9752, 9786, 9787, 9794, 9795,
    9802, 9803, 9807, 9814, 9856, 9870, 9930, 9980, 10672, 10814,
    11218, 11960,
    12736, 13744, 14131, 14381, 14664, 14959, 15058, 15062, 15554, 16239, 16491,
    16557, 16589, 16624, 16813, 16824, 17567, 17758, 17804, 17826,
    18325, 19094, 19463, 20659, 21106, 22599, 22770, 22871, 23979,
    24356, 24534, 25542, 25668, 26825, 28928, 30665, 31041, 31061,
    31070, 31196, 31657, 31733, 31759, 31811, 31815, 32032, 32253,
    32399, 32464, 32470, 32506, 32721, 32722, 32996, 33124, 33145, 33184,
    33248, 33483, 33543, 33674, 33714, 33920, 33954, 34103, 34111,
    34331, 34340, 34345, 34578, 34965, 35018, 35194, 35324, 35344,
    35412, 35436, 35699, 36808, 36832, 36982, 36997, 37220, 37328,
    38113, 38327, 38336, 38350, 38376, 39195, 39774, 40051, 40203,
    40270, 40904, 41047, 41294, 41678, 41918, 42036, 42245, 42272,
    42334, 42770, 42988, 43017, 43583, 43639, and 44440,
    manifests `runs/zero_to_cad_live_pilots/deterministic_flange_collar_row342_probe/attempts.jsonl`,
    `runs/zero_to_cad_live_pilots/deterministic_row1536_probe/attempts.jsonl`,
    `runs/zero_to_cad_live_pilots/deterministic_profile_row1595_probe/attempts.jsonl`,
    `runs/zero_to_cad_live_pilots/deterministic_profile_row1647_probe/attempts.jsonl`,
    `runs/zero_to_cad_live_pilots/deterministic_profile_row1823_probe/attempts.jsonl`,
    `runs/zero_to_cad_live_pilots/deterministic_profile_row1906_probe/attempts.jsonl`,
    `runs/zero_to_cad_live_pilots/deterministic_box_counterbore_row2162_probe/attempts.jsonl`,
    `runs/zero_to_cad_live_pilots/deterministic_box_hole_row2209_probe/attempts.jsonl`,
    `runs/zero_to_cad_live_pilots/deterministic_profile_row2257_probe/attempts.jsonl`,
    `runs/zero_to_cad_live_pilots/deterministic_box_row2288_probe/attempts.jsonl`,
    `runs/zero_to_cad_live_pilots/deterministic_arc_profile_row2450_probe/attempts.jsonl`,
    `runs/zero_to_cad_live_pilots/deterministic_box_hole_row3047_probe/attempts.jsonl`,
    `runs/zero_to_cad_live_pilots/deterministic_box_chamfer_row3175_probe/attempts.jsonl`,
    `runs/zero_to_cad_live_pilots/deterministic_box_chamfer_row3231_probe/attempts.jsonl`,
    `runs/zero_to_cad_live_pilots/deterministic_arc_profile_row3487_probe/attempts.jsonl`,
    `runs/zero_to_cad_live_pilots/deterministic_box_hole_row3777_probe/attempts.jsonl`,
    `runs/zero_to_cad_live_pilots/deterministic_box_hole_row4081_probe/attempts.jsonl`,
    `runs/zero_to_cad_live_pilots/deterministic_box_chamfer_row4227_probe/attempts.jsonl`,
    `runs/zero_to_cad_live_pilots/deterministic_box_chamfer_row5606_probe/attempts.jsonl`,
    `runs/zero_to_cad_live_pilots/deterministic_rect_plate_row1479_probe/attempts.jsonl`,
    `runs/zero_to_cad_live_pilots/deterministic_profile_row2896_probe/attempts.jsonl`,
    `runs/zero_to_cad_live_pilots/deterministic_profile_row3414_probe/attempts.jsonl`,
    `runs/zero_to_cad_live_pilots/deterministic_profile_row3787_probe/attempts.jsonl`,
    `runs/zero_to_cad_live_pilots/deterministic_profile_row3966_probe/attempts.jsonl`,
    `runs/zero_to_cad_live_pilots/deterministic_profile_row4065_probe/attempts.jsonl`,
    `runs/zero_to_cad_live_pilots/deterministic_profile_row4559_probe/attempts.jsonl`,
    `runs/zero_to_cad_live_pilots/deterministic_profile_row4562_probe/attempts.jsonl`,
    `runs/zero_to_cad_live_pilots/deterministic_profile_row4811_probe/attempts.jsonl`,
    `runs/zero_to_cad_live_pilots/deterministic_profile_row5248_probe/attempts.jsonl`,
    `runs/zero_to_cad_live_pilots/deterministic_profile_row5435_probe/attempts.jsonl`,
    `runs/zero_to_cad_live_pilots/deterministic_profile_row5442_probe/attempts.jsonl`,
    `runs/zero_to_cad_live_pilots/deterministic_profile_row5713_probe/attempts.jsonl`,
    `runs/zero_to_cad_live_pilots/deterministic_profile_row5983_probe/attempts.jsonl`,
    and per-row guarded manifests for rows 6026, 6034, 6207, 6326, 6458,
    6477, 6481, 6510, 6623, 7391, 7409, 7434, 7479, 7685, 8273, 9733,
    9749, 9752, 9786, 9787, 9794, 9795, 9802, 9803, 9807, 9814,
    9856, 9870, 9930, 9980, 10672, 10814, 11218, 11960, 12736,
    13744, 14131, 14381,
    14664, 14959, 15554, 16239, 16491, 16557, 16589, 16624, 16813,
    16824, 17567, 17758, 17804, 17826, 18325, 19094, 19463, 20659,
    21106, 22599, 22770, 22871, 23979, 24356, 24534, 25542, 25668,
    26825, 28928, 30665, 31041, 31061, and per-row guarded manifests
    for rows 33248, 33483, 33543, 33674, 33714, 33920, 33954, 34103,
    34111, 34331, 34340, 34345, 34578, 34965, 35018, 35194, 35324,
    35344, 35412, 35436, 35699, 36808, 36832, 36982, 36997, 37220,
    37328, 38113, 38327, 38336, 38350, 38376, 39195, 39774, 40051,
    40203, 40270, 40904, 41047, 41294, 41678, 41918, 42036, 42245,
    42272, 42334, 42770, 42988, 43017, 43583, 43639, and 44440.
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

6. Training readiness and versioning.
   - Write immutable accepted-pair indexes that include source split, row index,
     UUID, original STEP hash/path, generated SubCAD hash/path, generated STEP
     hash/path, prompt/model id, runner command, comparison method/tolerance,
     SubCAD/process-plan schema version, and git commit.
   - Freeze dataset releases as versioned manifests, for example
     `zero_to_cad_subcad_verified_vYYYYMMDD.jsonl`, and never mix failed,
     manual-review, or synthetic/self-generated rows into the primary verified
     training/evaluation split.
   - Record rejected attempts separately for repair-loop analysis and negative
     examples; do not silently overwrite them with later successes.

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
   - Use accepted-index guarded runs so already verified rows count toward the
     target without re-spending live translator calls.

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
- Next: continue accepted-index guarded forward scans from the 233 accepted
  pairs, preserving strict stop conditions and fixing deterministic blockers
  before spending larger live batches.
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
- Superseded blocker: train global index 23 failed because generated code used a bare
  undefined measure variable instead of `m.<name>`; this is a translator prompt
  or static preflight repair issue, not a missing SubCAD operation.
- Done: strengthen translator prompt tests and instructions against bare
  copied measure variables such as `flange_thickness`.
- Superseded blocker: train global index 23 now executes after the measure prompt fix
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
- Done: include all currently accepted train global indexes through row 9752
  in future
  accepted-index guarded runs.
- Done: add Z-band retained-material support and planner evidence for retained
  rib/boss loops and polar arrays.
- Done: accept train global index 31 via deterministic layered retained
  SubCAD preflight with original-STEP trusted slice score 97.6.
- Done: accept train global index 34 via deterministic top-retained rib
  SubCAD preflight with original-STEP trusted slice score 98.1.
- Done: accept train global index 42 via deterministic cylindrical polar-rib
  SubCAD preflight with original-STEP trusted slice score 95.8.
- Done: add z-band `circular_pocket(..., base_height=...)` support and accept
  train global index 44 via deterministic annular-rib SubCAD preflight with
  original-STEP trusted slice score 100.0.
- Done: accept train global index 45 via deterministic cylindrical grid-boss
  SubCAD preflight with original-STEP trusted slice score 97.5.
- Done: accept train global index 46 via deterministic cylindrical washer /
  polar-hole SubCAD preflight with original-STEP trusted slice score 98.3.
- Done: accept train global index 47 via deterministic circular vent plate
  SubCAD preflight with original-STEP trusted mesh score 100.0.
- Done: add no-op cut-body detection for non-intersecting external CadQuery
  cut variables, add internal-through `profile_pocket(..., through=True)`, and
  accept train global index 49 via deterministic star/radial-pocket plate
  SubCAD preflight with original-STEP trusted mesh score 100.0.
- Done: add deterministic `box(...).faces(">Z").edges().chamfer(...)` support
  and accept train global index 50 with original-STEP trusted mesh score 100.0.
- Done: accept train global index 57 with the deterministic box/chamfer builder
  and original-STEP trusted mesh score 100.0.
- Done: add deterministic hollow shell-cover support that omits non-intersecting
  internal source cuts and accept train global index 58 with original-STEP
  trusted mesh score 100.0.
- Done: add circular-pocket island support, preserve outer-fillet-before-bore
  ordering for cylindrical cages, omit absorbed rib unions, and accept train
  global index 61 with original-STEP trusted mesh score 100.0.
- Done: add deterministic split-shroud support and accept train global index 62
  with original-STEP trusted mesh score 100.0.
- Done: add deterministic Measures/class L-bracket support and accept train
  global index 80 with original-STEP trusted mesh score 100.0.
- Done: fix CadQuery-centered `rarray` evidence for the related L-bracket
  variant, omit absorbed/no-op rib unions, and accept train global index 83
  with original-STEP trusted mesh score 100.0.
- Done: accept train global index 107 with the existing deterministic
  box/chamfer builder and original-STEP trusted mesh score 100.0.
- Done: add deterministic simple profile-extrusion support for CadQuery
  `polyline` and `moveTo`/`lineTo` chains, including implicit-origin
  `lineTo`, and accept train global indexes 111 and 118 with original-STEP
  trusted mesh score 100.0.
- Done: add deterministic L-bracket variants for z-band top ribs, tapered
  L-profiles with no-op cut/hole filtering, and translated box-union L brackets
  with construction-vertex holes; accept train global indexes 87, 88, and 90
  with original-STEP trusted mesh score 100.0.
- Done: add deterministic two-box union profile support and accept train
  global index 115 with original-STEP trusted mesh score 100.0.
- Done: add deterministic z-band base-plus-extension support and accept train
  global index 132 with original-STEP trusted mesh score 100.0.
- Done: accept train global index 238 with the existing deterministic
  profile-extrusion builder and original-STEP trusted mesh score 100.0.
- Done: accept train global indexes 381, 415, and 438 with existing
  deterministic profile/box builders and original-STEP trusted mesh score 100.0.
- Done: accept train global indexes 503, 697, 698, and 702 with existing
  deterministic box/washer/polar-rib builders and original-STEP trusted mesh
  score 100.0.
- Done: accept train global indexes 870, 1126, 1170, and 1173 with existing
  deterministic profile builders and original-STEP trusted mesh score 100.0.
- Blocked row: train global index 1166 has a side ribbed flange and counterbore
  holes; the simple box/chamfer recognizer is now guarded against `cboreHole`,
  `pushPoints`, `polyline`, and extra `extrude` chains.
- Done: add a deterministic cylindrical flange/collar builder for filtered
  hole grids, and accept train global index 342 via
  `deterministic_flange_collar_row342_probe`.
- Done: add variable point-list profile parsing and a simple box center-hole
  deterministic builder; accept train global indexes 1595, 1647, 2209, and
  2257 via guarded original-STEP probes.
- Done: add a simple box counterbore deterministic builder and accept train
  global index 2162 via `deterministic_box_counterbore_row2162_probe`.
- Done: add sampled `threePointArc` support for deterministic profile
  extraction and accept train global index 2450 via
  `deterministic_arc_profile_row2450_probe`.
- Done: accept train global indexes 3047 and 3231 with existing box-hole and
  box-chamfer deterministic builders.
- Done: accept train global indexes 3175 and 3487 with existing box-chamfer and
  sampled arc-profile deterministic builders.
- Done: accept train global indexes 3777, 4081, 4227, and 5606 with existing
  box-hole and box-chamfer deterministic builders.
- Done: add a deterministic raised rectangular plate builder that omits row
  1479's no-op positive `cutBlind` pockets, and accept train global index 1479
  via `deterministic_rect_plate_row1479_probe`.
- Done: accept train global indexes 2896, 3414, 3787, and 3966 with existing
  deterministic profile builders.
- Done: accept train global indexes 4065, 4559, 4562, 4811, 5248, 5435,
  5442, 5713, and 5983 with existing deterministic profile builders.
- Done: accept train global indexes 6026, 6034, 6207, 6326, 6458, 6477,
  6481, 6510, 6623, 7391, 7409, 7434, 7479, 7685, 8273, 9733, 9749,
  and 9752 with existing deterministic profile, chamfer, retained, and
  counterbore builders.
- Done: accept train global indexes 9786, 9794, 9795, and 9802 with existing
  deterministic profile builders.
- Done: accept train global indexes 9807, 9856, 9980, and 10672 with existing
  deterministic profile, chamfer, and counterbore builders.
- Done: accept train global indexes 9870, 9930, 10814, 11218, and 11960
  with existing deterministic profile, drill/counterbore, and chamfer builders.
- Done: accept train global indexes 12736, 13744, 14131, 14381, 14664, and
  14959 with existing deterministic drill and chamfer builders.
- Done: accept train global indexes 15554, 16239, 16557, 16813, 16824,
  17567, 17804, 17826, and 18325 with existing deterministic chamfer and drill
  builders.
- Done: accept train global indexes 16491, 16589, 16624, 17758, 19094, 20659,
  21106, 22770, and 23979 with existing deterministic drill, chamfer, and
  pattern/primitive builders.
- Done: accept train global indexes 19463, 22599, 24356, 24534, 25542, and
  26825 with existing deterministic drill, counterbore, and chamfer builders.
- Done: accept train global indexes 22871, 25668, 28928, 30665, 31041, and
  31061 with existing deterministic drill, counterbore, and chamfer builders.
- Done: add mirrored half-profile support to the deterministic profile builder;
  accept previously blocked train global indexes 9787, 9803, and 9814 with
  original-STEP verification.
- Done: accept train global indexes 11990, 12098, 13428, 13541, 20787, and
  20817 with existing deterministic profile builders after mirrored-profile
  support landed.
- Done: accept train global indexes 14960, 14963, 26802, and 27306 with
  deterministic profile builders.
- Done: add safe loop/append point-list evaluation to the deterministic profile
  builder; accept train global indexes 15058 and 15062 with original-STEP
  verification.
- Done: add deterministic box plus top-rect cutBlind handling with
  SimpleNamespace/Measures numeric resolution; accept train global index 31070
  after preserving the CadQuery positive-cutBlind no-op behavior.
- Done: accept train global indexes 31657, 31733, 31759, 31811, 31815,
  32032, and 32253 with existing deterministic chamfer, counterbore, and
  profile builders.
- Done: accept train global indexes 32721, 32722, 32996, 33124, 33145,
  33184, and 33200 with existing deterministic profile, chamfer, fillet, and
  profile/counterbore builders.
- Done: accept train global indexes 31196, 32399, 32464, and 32506 with
  existing deterministic profile/chamfer/fillet builders.
- Done: add side-face counterbore emission for deterministic profile extrudes
  and expose `face_selector` on fluent `Stock.counterbore`; accept train global
  index 32470 with original-STEP verification.
- Done: accept train global indexes 33248, 33483, 33543, 33674, 33714,
  33920, 33954, 34103, 34111, 34331, 34340, and 34345 with existing
  deterministic profile, chamfer, fillet, and drill builders.
- Done: accept train global indexes 34578, 34965, 35018, 35194, 35324,
  35344, 35412, 35436, 35699, 36808, 36832, 36982, 36997, 37220,
  37328, 38113, 38327, 38336, 38350, and 38376 with existing deterministic
  profile, chamfer, drill, and counterbore builders.
- Done: accept train global indexes 39195, 39774, 40051, 40203, 40270,
  40904, 41047, 41294, 41678, 41918, 42036, 42245, 42272, 42334,
  42770, 42988, 43017, 43583, 43639, and 44440 with existing deterministic
  profile, chamfer, drill, and counterbore builders.
- Blocked row: train global index 34201 is plannable as a rectangular
  counterbore, but deterministic comparison rejects the volume ratio; treat it
  as a counterbore depth/through-cut fidelity blocker before spending more live
  calls on similar rows.
- Blocked rows: train global indexes 6471 and 9028 are plannable and
  executable, but strict original-STEP comparison rejects them; treat 6471 as
  a patterned retained/profile mismatch and 9028 as a scoped side-face chamfer
  mismatch before spending more live calls on similar rows.
- Superseded blockers: train global indexes 9787 and 9803 now pass after
  mirrored half-profile deterministic support.
- Blocked row: train global index 10427 is plannable but rejected by strict
  original-STEP comparison; treat it as a blind-hole depth/location mismatch.
- Superseded blocker: train global index 9814 now passes after mirrored
  half-profile deterministic support.
- Blocked row: train global index 11871 is plannable but rejected by strict
  original-STEP comparison; inspect counterbore diameter/depth semantics before
  retrying similar minimal counterbore rows.
- Next: run the next accepted-index guarded forward scan and fix the next
  deterministic feature-family blocker before spending larger live batches.

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
  - Active next slice: Forward Scan And Bucketization v1.
    - Run accepted-index guarded scans from the latest verified row.
    - Fix the next deterministic blocker only after it is classified.
    - Maintain per-family match metrics before scaling any live batch.
    - Track the corpus-capacity gap: 86,923 currently plannable rows cannot produce 100k accepted pairs unless unsupported families mature or more source STEP rows are added.
  - Later SubCAD capability maturation targets for 100k: side-face/oriented profile machining, robust retained multi-island planning, shells/thin walls, turning/revolves, sweeps, lofts, and original-STEP verification at scale.
- GNN feature recognition and LLM fine-tuning should wait for execution-scored data.
- RL remains later-stage research after simulator fidelity is validated.
