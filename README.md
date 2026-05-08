# d2m — Design to Manufacturing AI

An AI-powered **Computer-Aided Process Planning (CAPP)** system that automatically generates manufacturing process plans from CAD designs. Upload a STEP file with material and volume specs, and d2m outputs ranked, rule-compliant process plans — sequence of operations, machines, tools, cost estimates, and DFM (Design for Manufacturability) feedback.

## What It Does

1. **Ingest CAD** — Accept STEP/IGES files + metadata (material, tolerances, production volume)
2. **Recognize Features** — GNN-based extraction of machinable features (holes, pockets, slots, bosses, chamfers, fillets)
3. **Generate Process Plans** — Multimodal LLM reasons over features + visual renders to produce full manufacturing plans
4. **Validate & Explain** — Rule engine checks DFM violations, explains why each process was chosen
5. **Simulate & Improve** — Digital simulation validates plans; RL fine-tuning improves accuracy over time

Initial scope targets **CNC machining (metals)** and **injection molding (plastics)**, expandable to casting, 3D printing, and sheet metal.

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
| CAD Parsing | pythonOCC / CadQuery |
| Feature Recognition | PyTorch Geometric (GNN / GAT) |
| Knowledge Graph | Neo4j + custom Python rule engine |
| LLM Planning | DeepSeek V4 Pro, fine-tuned via managed fine-tuning API |
| Simulation | Multi-fidelity: trimesh voxel + manifold3d + PyBullet (see [docs/simulation.md](docs/simulation.md)) |
| UI | Streamlit / Gradio (Phase 1), React (later) |
| Deployment | Cloud GPU (Vast.ai / RunPod for training), Render / Hugging Face Spaces for hosting |

[see full architecture documentation](docs/architecture.md) with more details.

## Project Plan

Phased solo build using AI-assisted development (Claude Code, Cursor):

| Phase | Timeline | Scope | Cost (₹) |
|-------|----------|-------|----------|
| **0**: Prototype | Week 1-2 | STEP parsing → LLM API → basic plan output. Zero training. | 0 |
| **1**: Synthetic Data | Week 2-3 | ✅ Complete — 9,994 labeled parts with STEP + JSON. CadQuery CSG engine + rule-based labeling. | 2,000-8,000 |
| **2**: Feature Recognition | Week 3-5 | Train GNN on synthetic MFCAD++ data for feature extraction | 8,000-15,000 |
| **3**: LLM Fine-Tuning | Week 5-7 | Fine-tune DeepSeek V4 Pro on planning task via managed API | 3,000-8,000 |
| **4**: Integration + UI | Week 7-9 | Full pipeline + Streamlit UI + rule engine | 5,000-10,000 |
| **5**: Simulation + RL | Week 9-12 | Digital validation, RL fine-tuning loop | 15,000-40,000 |

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

### Phase 2: GNN training (requires RTX 4090 or similar)

```bash
# Extract dataset first
7z x synthetic_10k_samples.7z -odata/synthetic_10k

# Convert to JSONL for LLM fine-tuning
python convert_dataset.py --input-dir data/synthetic_10k --output data/train_10k.jsonl --val-split 0.1

# Train GNN feature extractor (coming in Phase 2)
# python scripts/train_gnn_features.py
```

## Status

**Phase 0 complete** — Rule engine + LLM planner working via DeepSeek API.

**Phase 1 complete** — 9,994 labeled synthetic CAD parts generated (STEP + JSON + renders). Dataset available as `synthetic_10k_samples.7z` (67 MB via git-lfs).

## License

MIT
