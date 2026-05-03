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
Multimodal LLM (Llama 4 / Qwen3-VL) + Knowledge Graph (Neo4j)
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
| LLM Planning | Llama 4 Scout (17B MoE) or Qwen3-VL-32B, fine-tuned via QLoRA (Unsloth) |
| Simulation | FreeCAD CAM / CadQuery collision checks |
| UI | Streamlit / Gradio (Phase 1), React (later) |
| Deployment | Cloud GPU (Vast.ai / RunPod for training), Render / Hugging Face Spaces for hosting |

[see full architecture documentation](docs/architecture.md) with more details.

## Project Plan

Phased solo build using AI-assisted development (Claude Code, Cursor, Grok):

| Phase | Timeline | Scope | Cost (₹) |
|-------|----------|-------|----------|
| **0**: Prototype | Week 1-2 | STEP parsing → LLM API → basic plan output. Zero training. | 0 |
| **1**: Synthetic Data | Week 2-3 | CadQuery script generating 10k+ labeled parts with STEP + JSON + renders | 2,000-8,000 |
| **2**: Feature Recognition | Week 3-5 | Train GNN on synthetic MFCAD++ data for feature extraction | 8,000-15,000 |
| **3**: LLM Fine-Tuning | Week 5-7 | Multimodal QLoRA fine-tune Llama 4 / Qwen3-VL on planning task | 5,000-12,000 |
| **4**: Integration + UI | Week 7-9 | Full pipeline + Streamlit UI + rule engine | 5,000-10,000 |
| **5**: Simulation + RL | Week 9-12 | Digital validation, RL fine-tuning loop | 15,000-40,000 |

**Total estimated training cost**: ₹40,000–1,20,000 ($480–$1,450)

See [docs/plan.md](docs/plan.md) for detailed phased roadmap with milestones and risk mitigations.

## Quick Start

```bash
# Clone
git clone https://github.com/buvi-org/d2m.git
cd d2m

# Install
pip install -r requirements.txt

# Generate synthetic training data
python scripts/generate_synthetic_data.py --num_parts 5000

# Train feature extractor
python scripts/train_gnn_features.py

# Fine-tune LLM planner
python scripts/train_llm_planner.py

# Run the app
streamlit run app/main.py
```

## Status

**Pre-MVP / Planning** — Building synthetic data pipeline and Phase 0 prototype.

## License

MIT
