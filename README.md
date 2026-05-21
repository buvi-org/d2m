# d2m — Design to Manufacturing AI

An AI-powered **Computer-Aided Process Planning (CAPP)** project for turning CAD designs into manufacturing process plans. The long-term target is: upload a STEP file with material and volume specs, and d2m outputs ranked, rule-compliant process plans — sequence of operations, machines, tools, cost estimates, and DFM (Design for Manufacturability) feedback.

This repository is currently a prototype/research codebase. Some foundational pieces are implemented and tested; the full end-to-end AI planning product is not yet complete.

## What It Does

1. **Ingest CAD** — Accept STEP files and metadata (material, tolerances, production volume)
2. **Generate/translate subtractive CAD** — SubCAD represents machining operations as executable subtractive programs
3. **Compare outputs** — Candidate geometry can be compared against reference STEP geometry with global and localized metrics
4. **Simulate machining** — A tri-dexel/five-axis simulation stack is under active development
5. **Plan with AI** — Agentic CadQuery -> SubCAD translation exists for LLM-driven code generation, with execution feedback

Initial implemented scope is concentrated on **CNC/subtractive manufacturing**. Injection molding, casting, 3D printing, sheet metal, RL fine-tuning, and production UI are aspirational roadmap items.

## Current Reality

Current STEP-to-SubCAD objective: build a training/evaluation set of at least
100,000 original-STEP-verified Zero-to-CAD pairs for a model/workflow that
generates executable pure SubCAD from STEP evidence. The accepted-pair count is
22; the pure planner can currently queue 86,923 plannable rows out of 100,516
local rows. Planner coverage is not success. A row counts only after generated
pure SubCAD executes, emits the manufacturing artifacts, and its generated STEP
matches the original Zero-to-CAD `model.step` under the trusted comparison
policy. Hybrid/imported opaque geometry, direct CadQuery reconstruction, and
skipped unsupported features are rejected for verified pairs.

Implemented and tested:

- Phase 1 synthetic dataset generation: 9,994 labeled parts are available in `synthetic_10k_samples.7z`.
- SubCAD fluent API for subtractive machining operations, STEP/STL export, process-plan JSON, fixtures, tool assemblies, and multi-setup metadata.
- Agentic CadQuery -> SubCAD translator infrastructure, including LLM provider abstraction, prompt builders, convergence controller, REPL execution, geometry comparison, and optional localized/feature-aware feedback paths.
- Corrected Zero-to-CAD live benchmark runner that saves each original dataset STEP as the target, compares generated SubCAD output against that original STEP, and records trusted match policy artifacts.
- Mesh comparison utilities for per-vertex signed deviation and Z-slice feedback.

SubCAD Shop-Floor v1 is now treated as complete for the current prototype contract:

- Schema v1 process plans use `subcad.shop_floor.v1` while preserving legacy plan fields used by the current tests.
- Neutral toolpaths describe motion intent without committing to a controller-specific G-code dialect.
- Setup-sheet exports include stock, material, tools, operations, setups, work offsets, validation warnings, and a clear note that production G-code posting is deferred.
- Validation produces actionable errors/warnings before simulation or downstream CAM handoff.

**Phase 2 toolpaths are now complete and passing for the current prototype contract**:

- Every Phase 2 operation emits a non-empty neutral toolpath suitable for preview, estimating, validation, and simulation handoff.
- Process plans include useful toolpath summaries for Phase 2 operations.
- A preview-only G-code adapter renders controller-neutral intent for review and warns that production postprocessing remains deferred.
- Validation and time estimation use authored toolpath data, including malformed-path checks and path-length-based cycle-time estimates.

**Fixture and tool inventory v1 is now complete for the current prototype contract**:

- Versioned catalog files describe shop-floor fixtures and available tools as structured data, rather than treating them as arbitrary generated objects.
- Fixtures now carry semantic dimensions, clamping/clearance zones, setup context, and visualization payloads for the browser review workflow.
- Tools now preserve selected catalog identity, tool assembly metadata, holder/stickout/flute data, and backward-compatible flat fields in process plans.
- The browser viewer can show fixture bodies, clamp zones, setup context, neutral toolpaths, and cutter/shank/holder geometry for review.

Recently fixed blocker:

- The previous tri-dexel zero-volume failure has been fixed. `test_sim_bridge.py` now verifies nonzero stock volume, modified columns, and positive material removal. Simulation is still a prototype, but the core volume/material-removal path is no longer blocked.

**Manufacturing Trust v1 has its first implementation slice in place**: inventory-aware tool selection, realistic pass planning for core operations, sampled fixture/tool-holder clearance, benchmark comparison cases, and review visualization that exposes tools, holders, passes, timing, and warnings.

**Manufacturing Economics v1 has its first implementation slice in place**: local machine/material/tool cost catalogs, tool-change time, setup/load-unload time, material cost, tool wear cost, total time/cost estimates, setup-sheet economics output, visualization metadata, and ranked program comparison by fastest, cheapest, weighted score, and Pareto status.

## What SubCAD Can Do Now

SubCAD can currently be used as a CadQuery-backed subtractive machining representation for prototype workflows:

- Author machining programs with the fluent `Stock` API, including core operations, Phase 2 operations, pure STEP-coverage operation families, fixtures, setups, work offsets, and tool/material metadata.
- Export STEP/STL geometry plus JSON process plans using the `subcad.shop_floor.v1` schema.
- Preserve neutral toolpaths for shop-floor review, estimation, validation, preview-only G-code rendering, browser playback, and simulation handoff.
- Export Markdown/JSON setup sheets with stock, material, selected tools, tool assemblies, fixtures, operations, setup/work-offset data, validation messages, and deferred-production-G-code notes.
- Review fixture bodies, clamp zones, selected tools, holder/cutter assemblies, operation timelines, and stock states in the browser visualization workflow.
- Estimate engineering time/cost from local catalogs, including cutting time, tool-change time, setup/load-unload time, material, machine, setup, and tooling cost.
- Compare alternate SubCAD programs by time/cost tradeoff and Pareto ranking.
- Run local validation and integration tests for SubCAD, fixturing, shop-floor schema v1, Phase 2 toolpaths, translator infrastructure, and the simulation bridge.

SubCAD is not yet a production CAM/postprocessor or quoting system. Controller-certified G-code, industrial CAM strategy coverage, formal ERP/shop quoting, a full upload-to-plan product UI, large-scale live translation success claims, and validated simulation/RL workflows remain future work.

Current translator benchmark reality: the corrected runner compares against the original Zero-to-CAD STEP, not a self-generated STEP. The compatibility gate is now a typed pure-operation planner rather than a blocked-term filter, so 86,923 of 100,516 local train/val/test rows are plannable into operation families after inaccessible closed shells are rejected. That is planner coverage, not verified 100k success: each saved pair still must execute and pass original-STEP geometry comparison. Guarded live pilots currently have 30 accepted original-STEP-verified pairs.

Training readiness requires versioned accepted-pair manifests that preserve
source split/row/UUID, original STEP hash/path, generated SubCAD and generated
STEP hashes/paths, feature-family tags, comparison policy, validation/economics
artifacts, runner command, prompt/model id, SubCAD/process-plan schema version,
and git commit. Failed attempts and self-generated SubCAD -> STEP pairs remain
separate from the primary verified split.

### Visualization workflow

The primary visualization direction is browser-based Three.js with Python exporting the session assets. This keeps CadQuery/trimesh/simulation logic in Python while using the browser for interactive inspection.

```python
from src.subcad import Stock

part = (
    Stock.rectangular(60, 40, 16)
    .face_mill(depth=1)
    .pocket(width=18, length=24, depth=4)
)

part.visualization_package("web/sessions/latest", target=part)
economics = part.estimate_cost(machine="generic_3axis_mill", quantity=5)
part.visualization_package("web/sessions/latest", target=part, economics=economics)
```

Then serve `web/` and open the session viewer:

```bash
cd web
python -m http.server 8080
```

Open `http://localhost:8080/visualization.html?session=sessions/latest/scene.json`.

The viewer loads stock/target STL assets, neutral toolpaths, selected tool/holder metadata, fixture/clamp-zone data, comparison JSON, and diff markers. WebGPU remains the longer-term path for browser-side material removal; the current reliable path is Python export plus Three.js review.

Economics is available as an engineering estimate:

```python
from src.subcad import compare_programs

estimate = part.estimate_cost(machine="generic_3axis_mill", quantity=10)
print(estimate["time_breakdown"]["total_time_per_part_min"])
print(estimate["cost_breakdown"]["total_cost"])

comparison = compare_programs([program_a, program_b], weights={"time": 0.6, "cost": 0.4})
print(comparison["fastest_index"], comparison["cheapest_index"], comparison["weighted_best_index"])
```

These values are for engineering tradeoff review only, not production quotes.

Recent local test status:

| Test | Status |
|------|--------|
| `python test_agentic_translator.py` | PASS, 121/121. Includes corrected Zero-to-CAD runner policy tests; live LLM runs are separate. |
| `python test_subcad_integration.py` | PASS, 39/39 |
| `python test_fixturing_integration.py` | PASS, 19/19 |
| `python test_sim_bridge.py` | PASS, 51/51 |
| `python test_subcad_shopfloor_v1.py` | PASS. Acceptance test for completed SubCAD Shop-Floor v1 contract. |
| `python test_subcad_phase2_toolpaths.py` | PASS. Acceptance test for completed Phase 2 toolpaths, preview-only G-code adapter, validation, and estimation. |
| `python test_subcad_visualization.py` | PASS. Browser visualization package coverage, including current fixture/tool review metadata. |
| `python test_subcad_manufacturing_economics.py` | PASS. Engineering time/cost estimate and program-comparison coverage. |

## Architecture

```
CAD File (STEP) + Specs
    │
    ├─→ GNN Feature Extractor ──→ Structured Features JSON
    ├─→ 4-View Renderer ────────→ PNG Images (front, top, side, iso)
    │
    ▼
LLM (DeepSeek V4 Pro) + Knowledge Graph (Neo4j)
    │
    ▼
Process Plan JSON + DFM Notes + Explanations
    │
    ▼
Simulation Engine (optional) ──→ RL Feedback Loop
```

See [docs/architecture.md](docs/architecture.md) for full technical architecture.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| CAD/SubCAD Geometry | CadQuery-backed SubCAD operations, STEP/STL export, shop-floor schema v1, neutral toolpaths, fixture/tool catalogs |
| CAD Parsing | pythonOCC / CadQuery |
| Feature Recognition | Planned: PyTorch Geometric (GNN / GAT) |
| Knowledge Graph | Neo4j + custom Python rule engine |
| LLM Planning | Agentic translator scaffolding; fine-tuning is planned |
| Simulation | Tri-dexel/five-axis prototype; core volume/material-removal bridge tests now pass; neutral-toolpath preference/fallback is part of Shop-Floor v1 |
| UI | Browser review prototype under `web/` for stock, target, toolpaths, tools/holders, fixtures, clamp zones, and operation playback; product UI is planned |
| Deployment | Cloud GPU (Vast.ai / RunPod for training), Render / Hugging Face Spaces for hosting |

[see full architecture documentation](docs/architecture.md) with more details.

## Project Plan

Phased solo build using AI-assisted development (Claude Code, Cursor):

| Phase | Timeline | Scope | Cost (₹) |
|-------|----------|-------|----------|
| **0**: Prototype | Week 1-2 | Partially complete — core SubCAD, translator scaffolding, and rule/process-plan primitives exist; full upload-to-plan UX is not complete. | 0 |
| **1**: Synthetic Data | Week 2-3 | ✅ Complete — 9,994 labeled parts with STEP + JSON. CadQuery CSG engine + rule-based labeling. | 2,000-8,000 |
| **2**: Feature Recognition / Translation | Week 3-5 | Prototype hardening — typed pure-operation planner, translator scaffolding, and comparison utilities exist; feature-family verification is next. GNN feature recognition remains planned. | 8,000-15,000 |
| **2.5**: SubCAD Shop-Floor v1 | Complete | Schema v1, neutral toolpaths, setup-sheet export, validation buckets, and deferred production G-code contract. | TBD |
| **2.6**: Phase 2 Toolpaths | ✅ Complete | Non-empty neutral paths for Phase 2 ops, plan summaries, preview-only G-code adapter, malformed-path validation, and authored-path estimation. | TBD |
| **2.7**: Fixture + Tool Inventory v1 | ✅ Complete | Structured fixture/tool catalogs, selected tool assemblies, fixture/clamp visualization, and browser review metadata. | TBD |
| **3**: Manufacturing Trust v1 | Initial slice complete | Inventory-aware tool planning, realistic pass plans, sampled fixture/tool-holder clearance, stronger simulation comparison tests, and warning-focused visualization. | TBD |
| **3.1**: Manufacturing Economics v1 | Initial slice complete | Tool-change/setup/load-unload time, material/machine/setup/tooling cost, setup-sheet/viewer economics metadata, and time/cost program comparison. | TBD |
| **4**: LLM Fine-Tuning | Planned | Fine-tune/evaluate planning or code-generation model after reliable translated pairs and scoring. | 3,000-8,000 |
| **5**: Product Integration + UI | Planned | Full upload → plan → validation workflow and production UI. | 5,000-10,000 |
| **6**: Simulation + RL | Aspirational | RL loop after simulator is reliable and validated against real outcomes. | 15,000-40,000 |

**Total estimated training cost**: ₹40,000–1,20,000 ($480–$1,450)

See [docs/plan.md](docs/plan.md) for detailed phased roadmap with milestones and risk mitigations.

## Quick Start

```bash
# Clone with LFS
git clone https://github.com/buvi-org/d2m.git
cd d2m
git lfs pull

# Install
pip install -r requirements.txt

# Extract the 10K synthetic dataset (67 MB archive, ~1.1 GB extracted)
7z x synthetic_10k_samples.7z -odata/synthetic_10k
```

### Generate your own synthetic data

```bash
# Full 10K batch (multi-process, no renders for speed)
python generate_synthetic_data.py --count 10000 --output-dir ./data/synthetic --workers 8 --no-render

# With 4-view PNG renders (slower)
python generate_synthetic_data.py --count 100 --output-dir ./data/synthetic --workers 4

# Resume interrupted batch
python generate_synthetic_data.py --count 10000 --output-dir ./data/synthetic --resume

# Convert generated parts to JSONL training format
python convert_dataset.py --input-dir data/synthetic --output data/train.jsonl --val-split 0.1
```

### Tests and current validation

```bash
# Translator/SubCAD tests that currently pass locally
python test_agentic_translator.py
python test_subcad_integration.py
python test_fixturing_integration.py

# Simulation bridge test
python test_sim_bridge.py

# Shop-floor v1 acceptance test
python test_subcad_shopfloor_v1.py

# Phase 2 toolpath acceptance test
python test_subcad_phase2_toolpaths.py

# Visualization package coverage
python test_subcad_visualization.py

# Manufacturing economics coverage
python test_subcad_manufacturing_economics.py
```

## Status

**Completed** — Phase 1 synthetic dataset, SubCAD operation model, process-plan/export basics, fixture/setup metadata, SubCAD Shop-Floor v1, Phase 2 neutral toolpaths, fixture/tool inventory v1, Manufacturing Economics v1 initial slice, browser fixture/tool/economics review metadata, preview-only G-code adapter, authored-path validation/estimation, typed pure SubCAD operation planner, initial geometry-backed pure operations for selected-edge/profile/retained-boss features, and non-live agentic translator tests.

**Current hardening priority** — Forward Scan And Bucketization v1: run accepted-index guarded scans from the latest verified row, classify the next blocker before spending larger live batches, maintain per-family match metrics, and track the corpus-capacity gap between the 86,923 currently plannable rows and the 100k accepted-pair target.

**In progress / prototype** — Agentic CadQuery -> SubCAD translation against original STEP targets, localized/feature-aware comparison validation, feature-family benchmark reporting, and simulation feedback quality. The corrected live runner now uses original Zero-to-CAD STEP targets and can attempt most local rows through the pure planner, but 100k success still requires each family to execute and match the original STEP. See [docs/step_to_subcad_ai.md](docs/step_to_subcad_ai.md) for the current decision: STEP/B-Rep JSON is the source of truth, while images/video with projected dimensions are supporting evidence.

**Recently fixed** — Simulation bridge zero-volume failure. Core dexel volume and material-removal tests now pass, but simulation/RL claims should still be treated as roadmap until validated on representative real workflows.

**Planned** — Production controller-specific G-code postprocessing, GNN feature recognition, LLM fine-tuning, production UI, fully validated simulation feedback loop, and RL.

## License

MIT
