# d2m — Architecture

## Overview

d2m is currently centered on a STEP -> pure SubCAD research workflow: generate
executable subtractive SubCAD, execute it, export a generated STEP, and compare
that generated STEP against the original source STEP before accepting a pair for
training or evaluation. The immediate dataset target is 100,000
original-STEP-verified Zero-to-CAD pairs. Current measured status is 501 unique
accepted pairs and 79,911 plannable rows out of 100,516 local rows; plannable rows are an
attempt queue, not verified success.

The architecture remains modular because manufacturing involves hard physical
rules, sparse expert data, and geometric reasoning. However, verified training
pairs must be pure SubCAD: no hybrid/imported opaque geometry, no direct CadQuery
reconstruction, and no skipped unsupported features. GNNs, multimodal inputs,
knowledge graphs, and RL remain staged or aspirational unless explicitly called
out as implemented elsewhere in this document.

## High-Level Pipeline

### Active Corpus-Generation Pipeline

This is the current path that gates training data:

```
Zero-to-CAD row
  ├─ original model.step          (immutable target)
  ├─ CadQuery source / ops trace  (feature evidence)
  ▼
Pure SubCAD planner + deterministic/agentic generator
  ▼
Executable pure SubCAD program
  ├─ process plan / setup sheet / validation / economics
  └─ generated STEP
  ▼
Trusted comparison against original model.step
  ▼
accepted manifest record or failed/unsupported/manual-review record
```

The older product architecture below remains useful as the long-term
upload-to-plan direction, but it is not the acceptance authority for the 100k
training corpus.

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
│  │  Knowledge Graph │    │  Text LLM             │                      │
│  │  (Neo4j)         │◄──►│  (DeepSeek V4 Pro)    │                      │
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

### 5. LLM Planner (Neural Layer)

**Responsibility**: High-level reasoning — process selection, sequencing, explanation generation.

- **Base Model**: DeepSeek V4 Pro — state-of-the-art reasoning, extremely cost-efficient
- **Input**: Text prompt (features JSON + material + constraints + structured geometry description)
- **4-view renders**: Generated for human review in the UI, but not required for LLM input
- **Output**: Full JSON process plan with:
  - Operation sequence with dependencies
  - Tool selection per operation
  - Machine assignment
  - Estimated cycle time & cost
  - DFM notes and warnings
  - Natural-language rationale for each decision
- **Fine-tuning**: DeepSeek managed fine-tuning API
  - 5,000-20,000 instruction-response pairs
  - No GPU provisioning needed
  - Cost: ₹3,000-8,000 per run
- **Inference**: DeepSeek API with fine-tuned model ID

**Why LLM**: Captures the "engineering judgment" that pure rule-based systems miss — trade-offs, edge cases, explanations in natural language.

**Why text-only**: DeepSeek V4 Pro is a text model. This is sufficient because:
- Manufacturing features are discrete and nameable (holes, pockets, slots, bosses)
- Dimensions, tolerances, and adjacency relationships are numeric — text is the natural representation
- 4-view renders are still generated for human review in the UI
- If visual reasoning proves necessary, renders can be added via a separate vision model or base64-encoded images if DeepSeek adds vision support

### 6. Optimization Layer

**Responsibility**: Multi-objective optimization of candidate plans.

- **Objectives**: Minimize cost, minimize time, maximize quality, minimize environmental impact
- **Methods**:
  - Genetic Algorithm (GA) for discrete optimization (tool sequences, machine assignment)
  - Reinforcement Learning for sequential decision-making (which op next?)
- **Integration**: Takes top-N plans from LLM, scores them against objectives, returns Pareto-optimal set

### 7. Simulation & RL Validation

**Responsibility**: Verify plans are physically feasible; provide reward signal for continual improvement.

Uses a **multi-fidelity architecture** — three tiers trading speed for accuracy:

| Tier | Method | Speed | Use |
|------|--------|-------|-----|
| Tier 1 | Rule-based heuristics (wall thickness, draft, tolerance, tool constraints) | <1ms | Reject-sampling (discard bad plans instantly) |
| Tier 2 | Voxel-based material removal (trimesh + manifold3d) | 1-10s | Primary RL reward signal |
| Tier 3 | Full physics (openInjMoldSim CFD, mesh boolean) | min-hrs | Final validation spot-check |

- **CNC simulation**: Custom voxel simulator on trimesh.voxel + manifold3d mesh booleans + PyBullet collision detection
- **Molding simulation**: Rule-based heuristics for MVP (wall thickness, draft, flow length); full CFD via openInjMoldSim deferred to Phase 2+
- **RL loop**: Gymnasium env wrapping the simulator; PPO via Stable-Baselines3; composite reward = volume_removed − collision_penalty − time_penalty + constraint_bonus
- **Key insight**: RL doesn't need perfect physics — a voxel sim that correlates with real outcomes is sufficient for learning feasible plans

See **[docs/simulation.md](simulation.md)** for the full simulation infrastructure documentation, including tool landscape, build-vs-integrate decisions, and phased roadmap.

### 8. Output & Integration Layer

- **Primary output**: JSON/XML process plan (operations, tools, machines, NC code stubs)
- **Visual output**: Highlighted CAD features, Gantt chart of operations sequence
- **API**: REST endpoints for CAD/CAM/ERP integration
- **UI**: Streamlit/Gradio for MVP, React SPA for production

## Knowledge Acquisition: How the System Learns

This section addresses a critical question: how does manufacturing knowledge — tool catalogs, material properties, process rules, operating parameters — actually get into the system? The answer is four distinct ingestion channels, each feeding different components.

### Channel 1: Structured Tool Catalogs → Knowledge Graph

The primary source of tool knowledge. Tool manufacturers (Sandvik, Kennametal, Iscar, OSG, Seco, etc.) publish catalogs as structured data — CSV exports, JSON APIs, or ISO 13399 XML.

**What gets ingested per tool:**

```
Tool: Ø10mm 4-flute carbide end mill, TiAlN coated
├── GEOMETRY:      diameter=10mm, LOC=25mm, OAL=75mm, helix=30°, corner_radius=0
├── SUBSTRATE:     solid carbide, TiAlN coated
├── WORKPIECES:    Aluminum ✓ | Steel ✓ | Stainless ✓ | Titanium ⚠ (reduced params) | Plastic ✓
├── PROCESSES:     facing, pocketing, profiling, slotting, helical_interpolation
├── PARAMS (6061): SFM=600, FPT=0.05mm, DOC_max=5mm, WOC_max=4mm
├── PARAMS (4140): SFM=200, FPT=0.03mm, DOC_max=2mm, WOC_max=2mm
├── TOLERANCE:     holds ±0.05mm milling; cannot achieve H7 alone
├── FITS_MACHINE:  CAT40 / HSK63 / BT40 spindles
├── COST:          ₹2,500 | LIFE: 4h (aluminum), 2h (steel)
└── CONSTRAINTS:   min_hole_dia=N/A, max_depth=2.5×D, needs_coolant: true
```

**Ingestion pipeline:**

```python
# Example: Ingest Sandvik ISO 13399 XML catalog into Neo4j
# Claude/Cursor writes this once per catalog format

def ingest_iso13399_catalog(xml_path: str, kg: KnowledgeGraph):
    for tool_elem in parse_iso13399(xml_path):
        tool = Tool(
            id=tool_elem.id,
            type=tool_elem.type,         # end_mill, drill, reamer, tap...
            geometry=tool_elem.geometry,
            substrate=tool_elem.substrate,
            coating=tool_elem.coating,
        )
        kg.merge_tool(tool)

        # Link to compatible workpiece materials
        for mat in tool_elem.compatible_materials:
            kg.link(tool, "COMPATIBLE_WITH", mat, properties={
                "sfm": mat.sfm, "feed_per_tooth": mat.fpt,
                "doc_max": mat.doc_max, "coolant_required": mat.coolant
            })

        # Link to processes this tool can perform
        for proc in tool_elem.processes:
            kg.link(tool, "EXECUTES", proc)

        # Link to machines this tool fits
        for machine in tool_elem.spindle_types:
            kg.link(tool, "FITS", machine)
```

**Catalog format landscape:**

| Manufacturer | Format | Accessibility |
|-------------|--------|---------------|
| Sandvik Coromant | ISO 13399 XML, CoroPlus API | Free with account |
| Kennametal | NOVO API, CSV export | Free with account |
| Iscar | IscarToolAdvisor JSON | Free |
| OSG | CSV cutting conditions tables | Public download |
| Seco | Suggest web API | Free with account |
| Generic | ISO 13399 standard | Standardized, tool-agnostic |

### Channel 2: Manufacturing Handbooks → Rule Engine + LLM Corpus

*Machinery's Handbook*, ISO tolerance guides, DFM handbooks, and process engineering textbooks encode the fundamental rules. These feed two subsystems:

**A) Hard rules extracted into the Python rule engine:**

```python
# rules.py — Excerpt of rules distilled from handbooks

def check_hole_process(hole: Feature, plan: ProcessPlan) -> list[Warning]:
    """Rules from Machinery's Handbook, 32nd ed., Hole Making section."""
    warnings = []

    # Rule: Any hole < H7 tolerance requires a reaming pass
    if hole.tolerance_grade and hole.tolerance_grade <= 7:
        if not any(op.tool.type == "reamer" for op in plan.operations):
            warnings.append(Warning(
                severity="error",
                message=f"Hole Ø{hole.dia}mm requires H{hole.tolerance_grade} tolerance. "
                        "Drill alone insufficient — add reamer after drill.",
                source="Machinery's Handbook §Hole Making"
            ))

    # Rule: Deep holes need peck drilling
    if hole.depth > hole.dia * 5:
        if not any("peck" in op.strategy for op in plan.operations):
            warnings.append(Warning(
                severity="warn",
                message=f"Deep hole (L/D={hole.depth/hole.dia:.1f}). "
                        "Use peck drilling cycle to clear chips.",
                source="Machinery's Handbook §Deep Hole Drilling"
            ))

    # Rule: Tap drill size = major diameter − pitch (metric)
    if hole.has_thread:
        expected_drill = hole.dia - hole.thread_pitch
        actual_drill = plan.get_drill_diameter(hole)
        if abs(actual_drill - expected_drill) > 0.05:
            warnings.append(Warning(
                severity="error",
                message=f"Tap drill should be Ø{expected_drill}mm for M{hole.dia}×{hole.thread_pitch}",
                source="ISO 724"
            ))

    return warnings


def check_wall_thickness(feature: Feature, material: Material) -> list[Warning]:
    """DFM rules from Bralla, Design for Manufacturability Handbook."""

    if material.type == "plastic" and feature.wall_thickness < 1.0:
        return [Warning(
            severity="error",
            message=f"Wall thickness {feature.wall_thickness}mm too thin for {material.name}. "
                    "Minimum 1.0mm for injection molding. Risk: short shot, warping.",
            suggestion="Increase wall to ≥1.0mm or add flow leaders."
        )]

    return []
```

**B) Handbook excerpts embedded in LLM fine-tuning data:**

These teach the LLM *why* a rule exists and how to handle edge cases:

```jsonl
{"instruction": "You are a senior manufacturing engineer. A Ø20mm through hole in 4140 steel must hold ±0.012mm tolerance. What tool sequence? Explain.", "output": "Sequence: center drill → Ø19.7mm twist drill → Ø19.95mm boring bar (semi-finish) → Ø20mm H7 reamer. Explanation: ±0.012mm on Ø20mm is IT6 (H6/H7). A twist drill alone produces IT11-IT13 (±0.13-0.33mm) — entirely inadequate. Even a reamer after a drill is marginal here because the drill wanders. The boring bar establishes straightness before the reamer sizes it. Total 4 operations: spot for location, drill for bulk removal, bore for straightness, ream for size."}
{"instruction": "Can I use a Ø6mm 2-flute HSS end mill for a 30mm deep pocket in 304 stainless?", "output": "No — and here's why. Max depth of cut for a Ø6mm end mill is ~2.5× diameter = 15mm when side-milling 304 SS. At 30mm depth, that tool will deflect, chatter, and likely snap. Solutions: (1) Use a larger end mill if corner radius allows. (2) If Ø6mm is required for internal corners, rough with a larger tool first, then finish with the Ø6mm taking only 0.5mm radial engagement. (3) Use a reduced-shank or necked tool with 6mm cutting diameter but thicker shank for rigidity."}
```

These are generated by prompting an LLM with handbook content and validated rules — Claude/Cursor writes the extractor once.

### Channel 3: Synthetic Data Generator → LLM Pattern Learning

The synthetic data generator doesn't assign tools randomly. It encodes real machining logic that the LLM absorbs as statistical patterns during fine-tuning.

```python
# Inside generate_synthetic_data.py — tool selection is rule-driven

def assign_tools_for_features(features: list, material: str) -> list[ToolStep]:
    """Encodes real machining logic. Output becomes LLM training labels."""
    steps = []

    for feat in features:
        if feat.type == "hole":
            steps.append(ToolStep(
                tool="Ø6mm center drill", op="spot_drill",
                depth=3, rpm=rpm_lookup("center_drill", 6, material)
            ))

            # Drill: leave 0.2-0.5mm for reaming if tolerance is tight
            allowance = 0.3 if feat.tolerance < 0.05 else 0
            drill_dia = feat.diameter - allowance
            steps.append(ToolStep(
                tool=f"Ø{drill_dia:.1f}mm twist drill", op="drill",
                depth=feat.depth,
                strategy="peck" if feat.depth > drill_dia * 4 else "standard",
                rpm=rpm_lookup("drill", drill_dia, material),
                feed=feed_lookup("drill", drill_dia, material)
            ))

            if feat.tolerance < 0.05:
                steps.append(ToolStep(
                    tool=f"Ø{feat.diameter}mm H7 reamer", op="ream",
                    rpm=rpm_lookup("ream", feat.diameter, material),
                    feed=feed_lookup("ream", feat.diameter, material),
                    note="Required for tolerance < ±0.05mm"
                ))

            if feat.has_thread:
                steps.append(ToolStep(
                    tool=f"M{feat.diameter}×{feat.pitch} machine tap",
                    op="tap",
                    rpm=rpm_lookup("tap", feat.diameter, material),
                    note=f"Tap drill was Ø{drill_dia:.1f}mm"
                ))

        elif feat.type == "pocket":
            steps.append(ToolStep(
                tool=f"Ø{feat.width * 0.6:.1f}mm roughing end mill",
                op="rough_pocket", strategy="adaptive",
                rpm=rpm_lookup("end_mill", feat.width * 0.6, material),
                stepover=feat.width * 0.6 * 0.4,
                note="Rough with large tool for MRR; finish with smaller if corners tight"
            ))

            # Finish pass with smaller tool if corners are tight
            if feat.min_corner_radius < feat.width * 0.3:
                finish_dia = feat.min_corner_radius * 2
                steps.append(ToolStep(
                    tool=f"Ø{finish_dia:.1f}mm finish end mill",
                    op="finish_pocket",
                    rpm=rpm_lookup("end_mill", finish_dia, material),
                    stepover=0.5,
                    note=f"Finish tool sized for R{feat.min_corner_radius}mm corners"
                ))

    return steps


def feeds_speeds_lookup(tool_type: str, dia: float, material: str) -> dict:
    """Lookup table populated from Machinery's Handbook + manufacturer data."""
    TABLE = {
        ("end_mill", "aluminum_6061"): {"sfm": 500, "fpt": 0.05},
        ("end_mill", "steel_4140"):    {"sfm": 180, "fpt": 0.03},
        ("end_mill", "stainless_304"): {"sfm": 120, "fpt": 0.025},
        ("drill", "aluminum_6061"):    {"sfm": 300, "fpt": 0.1},
        ("drill", "steel_4140"):       {"sfm": 90,  "fpt": 0.06},
        ("drill", "stainless_304"):    {"sfm": 60,  "fpt": 0.05},
        ("ream", "aluminum_6061"):     {"sfm": 150, "fpt": 0.08},
        ("ream", "steel_4140"):        {"sfm": 50,  "fpt": 0.04},
        # ... full table has 50+ entries per tool type / material combination
    }
    return TABLE.get((tool_type, material))
```

**What the LLM learns from 10,000+ such examples:**
- Tool diameter scales with feature size (not memorized, but proportional)
- Tight tolerance → reaming/boring pass added
- Deep features → peck drilling or reduced DOC
- Small internal corners → finish with smaller tool
- Harder materials → slower SFM, lighter feed, shallower DOC

The LLM never sees the `feeds_speeds_lookup` table. It sees 10,000 examples of "for a Ø12mm hole in 6061, drill at 3000 RPM and 0.15mm/rev" and learns the underlying mapping.

### Channel 4: User Feedback + Shop Outcomes → Continuous Learning

Once deployed, real-world outcomes close the learning loop:

```python
# Continuous learning feedback loop

class FeedbackCollector:
    def record_rejection(self, plan: ProcessPlan, reason: str, user: str):
        """User rejected a plan — learn the pattern."""
        self.db.insert({
            "event": "plan_rejected",
            "plan_id": plan.id,
            "features": plan.features,
            "tools": plan.tools,
            "reason": reason,   # e.g., "4mm end mill will deflect"
            "user": user,
            "timestamp": now()
        })
        # At next retraining: this plan becomes a NEGATIVE example
        # LLM learns: "don't pair deep pockets with small-diameter tools"

    def record_shop_outcome(self, plan: ProcessPlan, actual: ShopResult):
        """Real shop-floor data."""
        self.db.insert({
            "event": "plan_executed",
            "plan_id": plan.id,
            "actual_time": actual.cycle_time,       # vs predicted_time
            "actual_cost": actual.total_cost,        # vs predicted_cost
            "tool_wear": actual.tool_wear_pct,       # update tool life model
            "quality_pass": actual.inspection_pass,  # was the part good?
            "issues": actual.issues,                 # surface finish, chatter, etc.
        })
        # Update cost models, tool life estimates, parameter adjustments

    def generate_retraining_examples(self) -> list:
        """Before each retraining cycle, convert feedback into examples."""
        examples = []
        for rejection in self.db.get_rejections(since=last_training):
            examples.append({
                "instruction": build_instruction(rejection.features),
                "output": f"AVOID: {rejection.reason}. {rejection.suggested_fix}",
                "weight": 2.0  # upweight corrections
            })
        return examples
```

**Retraining trigger points:**
- Every 50 user corrections on the same issue pattern
- Every significant shop outcome divergence (actual time > 2× predicted)
- Monthly batch: incorporate all feedback since last cycle

### Knowledge Acquisition Pipeline: Summary

```
                      ┌─────────────────────────────┐
                      │    TOOL CATALOGS (ISO 13399) │
                      │    Sandvik, Kennametal, OSG   │
                      └─────────────┬───────────────┘
                                    │ parse & link
                                    ▼
┌──────────────────┐     ┌─────────────────────┐
│  HANDBOOKS       │     │   KNOWLEDGE GRAPH    │◄──── Initial manual curation
│  Machinery's Hbk │────▶│   (Neo4j)            │      by domain expert
│  DFM guides       │     │                      │
│  ISO standards    │     │  Tools + Materials   │
└──────────────────┘     │  + Processes + Rules  │
                          └──────────┬───────────┘
                                     │
              ┌──────────────────────┼──────────────────────┐
              │                      │                      │
              ▼                      ▼                      ▼
    ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
    │  RULE ENGINE     │  │  SYNTHETIC DATA │  │  LLM PROMPT     │
    │  Hard constraints│  │  GENERATOR      │  │  CONTEXT        │
    │  (never violated)│  │  Encodes rules  │  │  Handbook text  │
    │                  │  │  into examples  │  │  embedded       │
    └─────────────────┘  └────────┬────────┘  └─────────────────┘
                                  │
                                  ▼
                        ┌─────────────────┐
                        │  LLM FINE-TUNING │
                        │  Learns patterns │
                        │  from 10k+ ex.   │
                        └────────┬────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
              ▼                  ▼                  ▼
    ┌─────────────┐   ┌─────────────┐   ┌─────────────────┐
    │ USER FEEDBACK│   │ SHOP OUTCOMES│   │ SIMULATION      │
    │ Plan reject  │   │ Actual time │   │ Feasibility ✓/✗ │
    │ Corrections  │   │ Tool wear   │   │ Collision check  │
    └──────┬───────┘   └──────┬──────┘   └────────┬────────┘
           │                  │                    │
           └──────────────────┼────────────────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │  CONTINUOUS LEARN │
                    │  Retraining cycle │
                    │  (monthly / 50    │
                    │   corrections)     │
                    └───────────────────┘
```

### Key Design Principle

The LLM is allowed to be creative about tool selection — it can suggest novel combinations. But the **knowledge graph + rule engine act as the gatekeeper**: any tool in the final plan must exist in the graph and satisfy all constraints. This means:

- **LLM suggests** → "Use a Ø8mm ball end mill for this organic pocket"
- **KG validates** → "Ø8mm ball end mill exists? ✓ Compatible with 6061? ✓ Available on VF2? ✓"
- **Rules check** → "Pocket depth 20mm vs tool reach 18mm? ✗ REJECT"

The LLM provides engineering judgment; the symbolic layer ensures physical and shop-floor reality.

## Data Flow for Training

Current verified-pair flow:

```
Zero-to-CAD original STEP
  -> STEP/B-Rep and CadQuery feature evidence
  -> pure SubCAD generator
  -> SubCAD execution and generated STEP export
  -> trusted comparison against original STEP
  -> accepted train/eval manifest or rejected-attempt manifest
```

The synthetic/GNN/VLM flow below is retained as future/product training context,
not the active acceptance gate for the 100k verified SubCAD corpus.

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
            │                  │  Fine-Tuning      │
            │                  │  (DeepSeek V4 Pro)   │
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
| Multimodal over text-only | DeepSeek V4 Pro (text) | Manufacturing features are discrete and numeric — text is the natural representation. 4 renders still generated for human review. |
| QLoRA over full fine-tune | DeepSeek managed fine-tuning API | No GPU provisioning needed, cost-efficient, simple API |
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
│   └── simulation/           # Multi-fidelity validation (see docs/simulation.md)
│       ├── env.py            # Gymnasium CAPPEnv
│       ├── tier1_rules.py    # Heuristic rule validators
│       ├── tier2_voxel.py    # Voxel-based CNC simulation
│       ├── tier3_physics.py  # High-fidelity integration (Phase 2+)
│       ├── collision.py      # PyBullet collision detection
│       ├── toolpath.py       # Tool swept volume generation
│       ├── gcode.py          # G-code parser wrapper
│       ├── rewards.py        # Reward function definitions
│       ├── molding_rules.py  # Injection molding heuristics
│       ├── material_db.py    # Material property lookup tables
│       └── visualization.py  # Simulation result viz
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

Future product path, gated by the verified 100k corpus and reliable comparison
loop:

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
