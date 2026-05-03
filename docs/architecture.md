# d2m — Architecture

## Overview

d2m is a **hybrid AI system** combining neural networks, symbolic reasoning, and multimodal LLMs for automated manufacturing process planning. A monolithic model cannot work — manufacturing involves hard physical rules, sparse expert data, and geometric reasoning. The architecture is modular: each component does one thing well, and the pipeline composes them.

## High-Level Pipeline

```
┌──────────────────────────────────────────────────────────────────────┐
│                        INPUT LAYER                                    │
│  STEP/IGES CAD file + metadata (material, quantity, tolerances, PMI) │
└──────────────────────────────┬───────────────────────────────────────┘
                               │
          ┌────────────────────┼────────────────────┐
          ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│   CAD Parser    │  │  4-View Render  │  │  Material Info   │
│ (pythonOCC /    │  │  (CadQuery /    │  │  + Tolerances    │
│  CadQuery)      │  │   FreeCAD)      │  │  + Volume specs  │
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         │                    │                    │
         ▼                    │                    │
┌─────────────────┐           │                    │
│  B-Rep → AAG    │           │                    │
│  Conversion     │           │                    │
└────────┬────────┘           │                    │
         │                    │                    │
         ▼                    ▼                    ▼
┌──────────────────────────────────────────────────────────────────────┐
│                   FEATURE EXTRACTION (GNN)                            │
│                                                                       │
│  Graph Neural Network (AAGNet / MaProNet-style) processes            │
│  Attributed Adjacency Graph to identify machinable features:         │
│  holes, pockets, slots, bosses, chamfers, fillets, threads           │
│                                                                       │
│  Output: Structured feature list with dimensions, positions,         │
│          tolerances, and surface finish attributes                    │
└──────────────────────────────┬───────────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────────┐
│                     REASONING & PLANNING ENGINE                        │
│                                                                       │
│  ┌─────────────────┐    ┌─────────────────────┐                      │
│  │  Knowledge Graph │    │  Multimodal LLM      │                      │
│  │  (Neo4j)         │◄──►│  (Llama 4 / Qwen3)   │                      │
│  │                  │    │                      │                      │
│  │  • Materials     │    │  • Process selection  │                      │
│  │  • Tools/Machines│    │  • Sequencing         │                      │
│  │  • Process rules │    │  • Tool allocation    │                      │
│  │  • DFM constraints│   │  • Cost estimation    │                      │
│  │  • Cost models   │    │  • Natural-language   │                      │
│  │                  │    │    explanations       │                      │
│  └────────┬─────────┘    └──────────┬───────────┘                      │
│           │                         │                                  │
│           ▼                         ▼                                  │
│  ┌─────────────────────────────────────────────────────────────┐     │
│  │              Optimization Layer (GA / RL)                     │     │
│  │  Multi-objective: minimize cost, time; maximize quality       │     │
│  └─────────────────────────────────────────────────────────────┘     │
└──────────────────────────────┬───────────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    VALIDATION & SIMULATION                             │
│                                                                       │
│  • Rule engine checks all DFM constraints against proposed plan      │
│  • FreeCAD CAM simulation validates toolpaths and collision          │
│  • Molding simulation checks wall thickness, warping, fill            │
│  • Feedback loop: simulation results → reward signal for RL          │
└──────────────────────────────┬───────────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────────┐
│                        OUTPUT LAYER                                    │
│                                                                       │
│  • JSON process plan (operations, sequence, tools, machines, params) │
│  • Cost & time estimates                                              │
│  • DFM issue flags with explanations                                  │
│  • Ranked alternative plans                                           │
│  • Visual: highlighted features, Gantt chart of operations            │
│  • API endpoints for CAD/CAM/ERP integration                          │
└──────────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. CAD Parser & Representation

**Responsibility**: Convert vendor CAD formats into machine-readable geometry.

- **Input formats**: STEP (.stp), IGES (.igs), native CAD via plugins (.SLDPRT, .f3d)
- **Internal representation**: Boundary Representation (B-Rep) → Attributed Adjacency Graph (AAG)
  - B-Rep stores topological entities (faces, edges, vertices) and their geometric definitions
  - AAG captures face adjacency with edge attributes (convex/concave, angle)
- **Tooling**: pythonOCC (OpenCascade Python bindings), CadQuery
- **Why AAG**: Naturally represents design features — a pocket is a set of faces with specific adjacency patterns. GNNs operate directly on this graph structure.

### 2. 4-View Renderer

**Responsibility**: Generate standardized visual inputs for the multimodal LLM.

- Renders 4 orthographic + isometric PNG views per part:
  - Front (XY plane), Top (XZ plane), Side (YZ plane), Isometric
- Uses CadQuery's built-in STL export + vtk/plotly for rendering
- **Why visual input**: Complex geometries, surface finish issues, and assembly constraints are often obvious in images but hard to describe in text. Multimodal fusion improves edge-case accuracy.

### 3. Feature Extraction GNN

**Responsibility**: Identify and classify all machinable features from the AAG.

- **Architecture**: Graph Attention Network (GAT) or AAGNet variant
  - Input: AAG nodes (faces) with geometric features (area, curvature, normal vectors)
  - Output: Node classifications (face → feature type) + feature parameters
- **Training**: Supervised on MFCAD/MFCAD++ public datasets + synthetic data
  - >99% accuracy reported in recent work (2024-2025)
- **Technology**: PyTorch Geometric (PyG)
- **Training cost**: ₹2,000-8,000 on single RTX 4090 (2-8 hours)

### 4. Knowledge Graph (Symbolic Layer)

**Responsibility**: Store and enforce hard manufacturing rules.

**Schema** (Neo4j property graph):

```
(Process)-[:COMPATIBLE_WITH]->(Material)
(Process)-[:REQUIRES]->(Tool)
(Process)-[:PRECEDES]->(Process)    // dependency chain
(Feature)-[:MACHINABLE_BY]->(Process)
(Material)-[:HAS_PROPERTY]->(Property)
(Tool)-[:AVAILABLE_ON]->(Machine)
```

**Rule categories**:
- **Material-Process compatibility**: e.g., ABS → injection molding; Aluminum → CNC/die casting
- **Tolerance constraints**: ±0.01mm tolerance → CNC required, sand casting excluded
- **Feature dependencies**: "Drill after mill on same face", "Chamfer after pocket"
- **DFM rules**: Thin wall (<1mm in ABS) → warping risk → flag for redesign
- **Tool/Machine constraints**: Tool diameter must be less than pocket width

**Engine**: Python rule engine (custom, declarative) with graph queries for relationship checking.

### 5. Multimodal LLM Planner (Neural Layer)

**Responsibility**: High-level reasoning — process selection, sequencing, explanation generation.

- **Base Model**: Llama 4 Scout (17B MoE, natively multimodal) or Qwen3-VL-32B
- **Input**: Text prompt (features JSON + material + constraints) + 4 rendered views
- **Output**: Full JSON process plan with:
  - Operation sequence with dependencies
  - Tool selection per operation
  - Machine assignment
  - Estimated cycle time & cost
  - DFM notes and warnings
  - Natural-language rationale for each decision
- **Fine-tuning**: QLoRA (r=16, alpha=16) on synthetic data
  - 5,000-20,000 instruction-response pairs
  - 1-2 hours on single RTX 4090
  - Cost: ₹5,000-12,000 per run
- **Inference**: Merged LoRA weights, served via vLLM or llama.cpp

**Why LLM**: Captures the "engineering judgment" that pure rule-based systems miss — trade-offs, edge cases, explanations in natural language.

### 6. Optimization Layer

**Responsibility**: Multi-objective optimization of candidate plans.

- **Objectives**: Minimize cost, minimize time, maximize quality, minimize environmental impact
- **Methods**:
  - Genetic Algorithm (GA) for discrete optimization (tool sequences, machine assignment)
  - Reinforcement Learning for sequential decision-making (which op next?)
- **Integration**: Takes top-N plans from LLM, scores them against objectives, returns Pareto-optimal set

### 7. Simulation & RL Validation

**Responsibility**: Verify plans are physically feasible; provide reward signal for continual improvement.

- **CNC simulation**: FreeCAD CAM workbench or CadQuery for basic toolpath + collision check
- **Molding simulation**: PyBullet or simplified fill analysis for thin-wall / warping checks
- **RL loop**:
  - Agent: LLM planner (generates plan as action)
  - Environment: Simulator (returns success + cost as reward)
  - Algorithm: GRPO (Group Relative Policy Optimization) — 2026 standard for LLM RL
  - Additional cost: ₹15,000-40,000 (3-5 extra GPU runs)

### 8. Output & Integration Layer

- **Primary output**: JSON/XML process plan (operations, tools, machines, NC code stubs)
- **Visual output**: Highlighted CAD features, Gantt chart of operations sequence
- **API**: REST endpoints for CAD/CAM/ERP integration
- **UI**: Streamlit/Gradio for MVP, React SPA for production

## Data Flow for Training

```
                    ┌──────────────────────────┐
                    │  Synthetic Data Generator │
                    │  (CadQuery scripts)        │
                    └───────────┬──────────────┘
                                │
            ┌───────────────────┼───────────────────┐
            ▼                   ▼                   ▼
     STEP files           JSON labels          PNG renders
            │                   │                   │
            ▼                   │                   │
     B-Rep → AAG               │                   │
            │                   │                   │
            ▼                   ▼                   ▼
     ┌─────────────┐   ┌──────────────┐   ┌──────────────┐
     │ GNN Training │   │  Instruction │   │  Image tokens │
     │ (supervised) │   │   formatting │   │  for VLM      │
     └──────┬───────┘   └──────┬───────┘   └──────┬───────┘
            │                  │                   │
            │                  └─────────┬─────────┘
            │                            │
            │                  ┌─────────▼─────────┐
            │                  │  QLoRA Fine-Tuning │
            │                  │  (Llama 4/Qwen3)   │
            │                  └─────────┬─────────┘
            │                            │
            │                  ┌─────────▼─────────┐
            │                  │   RL via GRPO +    │
            │                  │   Simulation       │
            │                  └───────────────────┘
            ▼
     Trained Feature
     Extractor (GNN)
```

## Technology Choices & Rationale

| Decision | Choice | Why |
|----------|--------|-----|
| GNN over 3D CNN for features | Graph Attention Network | CAD topology (face adjacency) is naturally a graph; GNNs capture structural dependencies that CNNs miss |
| Hybrid symbolic + neural | Neo4j + LLM | Hard manufacturing rules (physics, material science) must never be violated; symbolic layer guarantees constraint enforcement |
| Multimodal over text-only | Llama 4 Scout / Qwen3-VL | Visual inspection catches surface finish, thin-wall, and assembly issues invisible to text |
| QLoRA over full fine-tune | Unsloth QLoRA | 10-100x cheaper, fits on single consumer GPU, negligible accuracy loss for this task |
| RL over pure SFT | GRPO | Simulation feedback fixes infeasible plans the model would otherwise hallucinate |
| Synthetic over real data | CadQuery scripts | Real CAD→plan datasets are proprietary and rare; synthetic data with engineered labels is near-free and covers more edge cases |

## Directory Structure

```
d2m/
├── app/
│   ├── main.py              # Streamlit/Gradio UI entry point
│   ├── pipeline.py           # Full inference pipeline orchestrator
│   └── api.py                # REST API (FastAPI)
├── src/
│   ├── cad_parser/           # STEP/IGES parsing (pythonOCC/CadQuery)
│   │   ├── parser.py         # B-Rep → AAG conversion
│   │   ├── renderer.py       # 4-view PNG generation
│   │   └── aag.py            # Attributed Adjacency Graph builder
│   ├── feature_extraction/   # GNN feature recognition
│   │   ├── model.py          # GAT/AAGNet architecture
│   │   ├── train.py          # Training script
│   │   └── inference.py      # Inference wrapper
│   ├── knowledge_graph/      # Neo4j + rules
│   │   ├── schema.py         # Graph schema & population
│   │   ├── rules.py          # DFM / process rules engine
│   │   └── queries.py        # Common Cypher queries
│   ├── planner/              # LLM planning
│   │   ├── train.py          # QLoRA fine-tuning script
│   │   ├── inference.py      # Plan generation
│   │   ├── dataset.py        # Synthetic data → training format
│   │   └── prompts.py        # Prompt templates
│   ├── optimization/         # Multi-objective optimization
│   │   ├── genetic.py        # GA for plan optimization
│   │   └── rl.py             # GRPO RL training
│   └── simulation/           # Validation & simulation
│       ├── cnc_sim.py        # Toolpath/collision simulation
│       └── molding_sim.py    # Plastic molding simulation
├── scripts/
│   ├── generate_synthetic_data.py  # Synthetic CAD data generator
│   └── convert_dataset.py    # JSON labels → LLM training format
├── data/                     # Generated datasets (gitignored)
├── models/                   # Trained model weights (gitignored)
├── docs/
│   ├── architecture.md
│   └── plan.md
├── requirements.txt
└── README.md
```

## Inference Flow (Production)

```
1. User uploads STEP + material + volume → stored in temp/
2. CAD parser validates file, extracts B-Rep
3. Renderer generates 4 PNG views
4. AAG builder creates graph representation
5. GNN inference extracts features → JSON
6. Feature JSON + images + material specs → formatted into LLM prompt
7. LLM generates candidate process plans (top-N, temp=0.7)
8. Knowledge graph validates each plan against rules; rejects violations
9. Optimizer ranks surviving plans by cost/time/quality
10. Optional simulation validates top plan physically
11. Response returned: ranked plans + DFM notes + explanations
12. User can ask follow-up questions or request alternatives
```

## Scalability Notes

- **Inference**: GNN inference (<1s on CPU), LLM generation (5-30s on GPU). Pipeline runs in ~30-60s end-to-end per part.
- **Batch mode**: Process multiple parts in parallel for quoting platforms
- **Online learning**: Store user corrections + simulation outcomes → periodic retraining
- **Model serving**: Single A100 serves 50+ concurrent inference requests via vLLM
