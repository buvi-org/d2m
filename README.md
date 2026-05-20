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

Implemented and tested:

- Phase 1 synthetic dataset generation: 9,994 labeled parts are available in `synthetic_10k_samples.7z`.
- SubCAD fluent API for subtractive machining operations, STEP/STL export, process-plan JSON, fixtures, and multi-setup metadata.
- Agentic CadQuery -> SubCAD translator infrastructure, including LLM provider abstraction, prompt builders, convergence controller, REPL execution, geometry comparison, and optional localized/feature-aware feedback paths.
- Mesh comparison utilities for per-vertex signed deviation and Z-slice feedback.

SubCAD Shop-Floor v1 is being integrated as the next contract layer:

- Schema v1 process plans use `subcad.shop_floor.v1` while preserving legacy plan fields used by the current tests.
- Neutral toolpaths describe motion intent without committing to a controller-specific G-code dialect.
- Setup-sheet exports are intended to include stock, material, tools, operations, setups, work offsets, validation warnings, and a clear note that G-code posting is deferred.
- Validation should produce actionable errors/warnings before simulation or downstream CAM handoff.

Recently fixed blocker:

- The previous tri-dexel zero-volume failure has been fixed. `test_sim_bridge.py` now verifies nonzero stock volume, modified columns, and positive material removal. Simulation is still a prototype, but the core volume/material-removal path is no longer blocked.

Recent local test status:

| Test | Status |
|------|--------|
| `python test_agentic_translator.py` | PASS, 55/55. Non-live tests only; no LLM API translation run. |
| `python test_subcad_integration.py` | PASS, 39/39 |
| `python test_fixturing_integration.py` | PASS, 19/19 |
| `python test_sim_bridge.py` | PASS, 51/51 |
| `python test_subcad_shopfloor_v1.py` | New acceptance test for SubCAD Shop-Floor v1; expected to pass after Agents 1-4 integrate schema/toolpath/setup-sheet APIs. |

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
| CAD/SubCAD Geometry | CadQuery-backed SubCAD operations, STEP/STL export, shop-floor schema v1 in progress |
| CAD Parsing | pythonOCC / CadQuery |
| Feature Recognition | Planned: PyTorch Geometric (GNN / GAT) |
| Knowledge Graph | Neo4j + custom Python rule engine |
| LLM Planning | Agentic translator scaffolding; fine-tuning is planned |
| Simulation | Tri-dexel/five-axis prototype; core volume/material-removal bridge tests now pass; neutral-toolpath preference/fallback is part of Shop-Floor v1 |
| UI | Browser simulation prototype under `web/`; product UI is planned |
| Deployment | Cloud GPU (Vast.ai / RunPod for training), Render / Hugging Face Spaces for hosting |

[see full architecture documentation](docs/architecture.md) with more details.

## Project Plan

Phased solo build using AI-assisted development (Claude Code, Cursor):

| Phase | Timeline | Scope | Cost (₹) |
|-------|----------|-------|----------|
| **0**: Prototype | Week 1-2 | Partially complete — core SubCAD, translator scaffolding, and rule/process-plan primitives exist; full upload-to-plan UX is not complete. | 0 |
| **1**: Synthetic Data | Week 2-3 | ✅ Complete — 9,994 labeled parts with STEP + JSON. CadQuery CSG engine + rule-based labeling. | 2,000-8,000 |
| **2**: Feature Recognition / Translation | Week 3-5 | In progress — translator and comparison utilities exist; GNN feature recognition remains planned. | 8,000-15,000 |
| **2.5**: SubCAD Shop-Floor v1 | Current integration | Schema v1, neutral toolpaths, setup-sheet export, validation buckets, and deferred G-code contract. | TBD |
| **3**: Simulation Reliability | Next priority | Harden the now-passing tri-dexel/material-removal bridge with real target meshes, deviation/gouge checks, and representative toolpaths. | TBD |
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

# Shop-floor v1 acceptance test after integration lands
python test_subcad_shopfloor_v1.py
```

## Status

**Completed** — Phase 1 synthetic dataset, SubCAD operation model, process-plan/export basics, fixture/setup metadata, and non-live agentic translator tests.

**In progress** — SubCAD Shop-Floor v1, agentic CadQuery -> SubCAD translation, localized/feature-aware comparison, and simulation reliability hardening.

**Recently fixed** — Simulation bridge zero-volume failure. Core dexel volume and material-removal tests now pass, but simulation/RL claims should still be treated as roadmap until validated on representative real workflows.

**Planned** — Controller-specific G-code posting, GNN feature recognition, LLM fine-tuning, production UI, validated simulation feedback loop, and RL.

## License

MIT
