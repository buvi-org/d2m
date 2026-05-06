# d2m — Project Plan

## Overview

Solo build of an AI-powered CAPP (Computer-Aided Process Planning) system using AI-assisted development tools (Claude Code, Cursor, Grok). No ML engineers hired — the AI tools generate code, and the builder orchestrates.

**Goal**: Upload STEP file → receive ranked, rule-compliant manufacturing process plans with DFM feedback, cost/time estimates, and explanations.

**Initial scope**: CNC machining for metals (aluminum, steel) + injection molding for plastics (ABS, PA6, PP). Expandable to casting, 3D printing, sheet metal.

## Timeline & Phases

### Phase 0: Zero-Training Prototype
**Week 1-2 | Cost: ₹0 (subscriptions only)**

Build a working pipeline that uses off-the-shelf LLM APIs + hardcoded rules before any training.

**Deliverables**:
- [ ] STEP file parser (pythonOCC/CadQuery) extracting basic geometry
- [ ] Simple rule engine (material → process mapping + basic DFM checks)
- [ ] DeepSeek V4 Pro API integration for process plan generation from text features
- [ ] Streamlit UI: upload CAD → view plan
- [ ] Test on 10-20 real CAD parts

**Milestone**: System produces reasonable-looking process plans. Identify where it fails → informs training priorities.

**Key risk**: CAD parsing edge cases. Mitigation: Start with simple prismatic parts; expand geometry complexity later.

---

### Phase 1: Synthetic Data Generation
**Week 2-3 | Cost: ₹2,000-8,000 (GPU/CPU hours)**

Generate labeled training data via automated CadQuery scripts.

**Deliverables**:
- [ ] `generate_synthetic_data.py`: Creates 10,000+ parametric parts with randomized features
  - Prismatic base plate + combinations of: pockets, through holes, blind holes, slots, bosses, fillets, chamfers
  - 50/50 metal/plastic material split
  - Variable dimensions, positions, tolerances
- [ ] Each part exports: STEP file + JSON label + 4 PNG renders (front, top, side, isometric)
- [ ] JSON labels include: features list, material, tolerances, suggested processes, DFM notes, process dependencies
- [ ] Dataset conversion script: JSON labels → LLM instruction-response format

**Milestone**: 10,000+ labeled parts with multi-modal training data ready.

**Key risk**: Generated parts not realistic enough. Mitigation: Use real CAD templates as base shapes; validate with domain expert.

---

### Phase 2: GNN Feature Extraction Training
**Week 3-5 | Cost: ₹8,000-15,000**

Train a Graph Neural Network to automatically identify machinable features from CAD B-Rep.

**Deliverables**:
- [ ] AAG builder: STEP → B-Rep → Attributed Adjacency Graph
- [ ] GAT/AAGNet model implementation (PyTorch Geometric)
- [ ] Train on MFCAD/MFCAD++ public datasets + synthetic data
- [ ] Evaluate: >95% accuracy on held-out test set
- [ ] Inference wrapper: STEP file → features JSON in <1 second

**Milestone**: GNN reliably extracts features from unseen CAD parts.

**Training details**:
- Architecture: Graph Attention Network, 4-6 layers
- Input: Face nodes with geometric features (area, curvature, normals, position)
- Output: Per-node feature classification + feature parameter regression
- Hardware: Single RTX 4090 (2-8 hours)
- Dataset: MFCAD++ (~60k labeled STEP files) + synthetic augmentation

**Key risk**: GNN overfits to synthetic geometry patterns. Mitigation: Heavy augmentation + public dataset diversity.

---

### Phase 3: LLM Fine-Tuning (Text + Feature-Based Planner)
**Week 5-7 | Cost: ₹3,000-8,000**

Fine-tune DeepSeek V4 Pro for manufacturing process planning using text-based feature descriptions and structured geometry data.

**Deliverables**:
- [ ] Dataset formatting: synthetic JSON → Alpaca-style text prompts
  - Instruction: "Design a manufacturing process. Material: X. Features: [...]. Tolerances: ±Y."
  - Geometry described via structured text (feature types, dimensions, positions, adjacency)
  - Response: Full JSON process plan
- [ ] Fine-tuning via DeepSeek API fine-tuning endpoint
  - 5,000-20,000 instruction-response pairs
  - Managed fine-tuning — no GPU provisioning needed
- [ ] Evaluation: Compare LLM plans against ground-truth rules; >90% rule compliance
- [ ] Fine-tuned model ID saved for inference

**Milestone**: LLM generates rule-compliant, professional process plans from feature descriptions.

**Model choice**:
- **DeepSeek V4 Pro** — state-of-the-art reasoning, extremely cost-efficient inference, managed fine-tuning API
- Geometry conveyed through structured text (feature types, dimensions, tolerances, adjacency relationships) rather than images
- 4-view renders generated for optional human review in the UI, but not required for LLM input

**Key risk**: LLM hallucinates infeasible sequences. Mitigation: Knowledge graph post-validation catches violations before output.

---

### Phase 4: Integration, Rule Engine & UI
**Week 7-9 | Cost: ₹5,000-10,000**

Connect all components into a single pipeline with user interface.

**Deliverables**:
- [ ] Full inference pipeline: CAD upload → GNN features → LLM plan → rule validation → output
- [ ] Neo4j knowledge graph populated with material-process-tool rules
- [ ] Python rule engine for DFM constraint checking
- [ ] Streamlit/Gradio UI: drag-drop CAD, view plans, ask questions
- [ ] FastAPI backend for programmatic access
- [ ] Error handling, retry logic, logging

**Milestone**: End-to-end system usable for internal testing on real parts.

**UI features**:
- CAD file upload (drag & drop)
- Material/volume/tolerance input form
- Process plan output with:
  - Ranked alternatives (by cost, time, quality)
  - Highlighted features on CAD preview
  - DFM warnings with explanations
  - Natural-language Q&A about the plan

---

### Phase 5: Simulation & RL Fine-Tuning
**Week 9-12 | Cost: ₹15,000-40,000**

Add digital simulation for plan validation and reinforcement learning for continual improvement.

**Deliverables**:
- [ ] CNC toolpath simulation (FreeCAD CAM / CadQuery)
  - Collision detection, tool reachability, fixture interference
- [ ] Basic molding simulation (fill analysis, thin-wall check)
- [ ] Simulator → reward function: plan_success * (1 - normalized_cost)
- [ ] GRPO RL training: LLM generates plan, simulator scores it, model updates
  - 3-5 training iterations
- [ ] Before/after accuracy comparison

**Milestone**: System self-improves; simulation catches plans that look good on paper but fail physically.

**RL setup**:
- Agent: Fine-tuned LLM (Phase 3)
- Environment: Physics simulator (FreeCAD CAM / molding sim)
- Algorithm: GRPO (Group Relative Policy Optimization)
- Reward: Feasibility (binary) + cost efficiency + time efficiency
- Hardware: 1-2 GPUs, 3-5 runs

**Key risk**: Simulator fidelity vs. real world. Mitigation: Validate against 20-50 real shop-floor outcomes before relying on RL.

---

## Cost Summary

| Phase | Training Cost (₹) | Training Cost ($) |
|-------|-------------------|-------------------|
| 0: Prototype | 0 | 0 |
| 1: Synthetic Data | 2,000 – 8,000 | 24 – 96 |
| 2: GNN Feature Extraction | 8,000 – 15,000 | 96 – 180 |
| 3: DeepSeek Fine-Tuning | 3,000 – 8,000 | 36 – 96 |
| 4: Integration + UI | 5,000 – 10,000 | 60 – 120 |
| 5: Simulation + RL | 15,000 – 40,000 | 180 – 480 |
| **Total** | **33,000 – 79,000** | **$396 – $948** |

**Ongoing monthly costs** (post-launch): ₹5,000-15,000 ($60-180) for inference hosting + occasional retraining.

**AI tool subscriptions**: ~₹3,000-5,000/month ($36-60) for DeepSeek API + Cursor Pro.

## Development Methodology

AI-assisted solo development using the following workflow:

1. **Architecture**: Grok/Claude for high-level design decisions and technical research
2. **Code generation**: Claude Code (via Cursor or CLI) for all implementation
3. **Debugging**: Paste errors back to Claude for step-by-step debugging
4. **Testing**: AI-generated test scripts; manual validation on real CAD files
5. **Iteration**: Upload failed cases → ask AI "Why did this fail? Fix it."

**Golden rule**: Always ask AI for explanations alongside code. Understanding the "why" prevents cascading bugs.

## Risk Register

| Risk | Impact | Probability | Mitigation |
|------|--------|------------|------------|
| CAD parsing fails on real-world files | High | Medium | Start with STEP only; add formats incrementally. pythonOCC is battle-tested. |
| Synthetic data not representative | High | Medium | Validate with domain expert early; use real CAD templates as base shapes |
| LLM hallucinates infeasible plans | Medium | High | Knowledge graph post-validation; RL simulation feedback |
| GPU cost overrun | Low | Low | Use spot instances; limit experiments to 3-5 runs per phase |
| Feature extraction GNN poor generalization | Medium | Low | Transfer learning from MFCAD++; augment with synthetic data noise |
| Simulator fidelity gap | Medium | Medium | Validate sim outputs against 20-50 real shop outcomes before RL reliance |

## Success Criteria

1. **Phase 0**: System produces any process plan from STEP input (even if not optimal)
2. **Phase 1**: 10,000+ synthetic parts generated with valid STEP + labels
3. **Phase 2**: GNN achieves >95% feature recognition accuracy on held-out test set
4. **Phase 3**: LLM plans are >90% rule-compliant (validated by knowledge graph)
5. **Phase 4**: End-to-end pipeline runs in <60 seconds per part; UI is responsive
6. **Phase 5**: Simulation catches >80% of infeasible plans; RL improves plan quality by >10% over SFT baseline

## Post-MVP Roadmap (Beyond 12 Weeks)

- **Expand processes**: Add casting, 3D printing (FDM/SLA), sheet metal forming
- **Expand materials**: More metals (titanium, brass), engineering plastics (PEEK, PC), composites
- **ERP integration**: Connect to shop-floor scheduling, inventory, machine availability
- **Digital twin**: Real-time sensor feedback → plan adaptation
- **SaaS product**: Multi-tenant web app for manufacturing quoting platforms
- **CAD plugin**: Direct integration into Fusion 360 / SolidWorks
- **Batch quotation mode**: Process 100+ designs simultaneously for online manufacturing marketplaces
