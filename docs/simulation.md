# d2m — Digital Simulation Infrastructure

## Overview

The simulation layer validates that AI-generated process plans are physically feasible and provides reward signals for future RL fine-tuning. It must answer: *"Will this plan actually work on a real machine?"*

For the current 100k STEP-to-SubCAD dataset objective, simulation is supporting
evidence rather than the acceptance authority. A pair counts only after pure
SubCAD execution and trusted comparison of the generated STEP against the
original Zero-to-CAD STEP target. Simulation warnings, collision checks, and
timing/cost estimates travel with accepted rows as quality metadata.

No single existing tool meets all needs. The simulation layer is a **custom integration of multiple libraries** with substantial new code for validation and RL reward computation.

## Multi-Fidelity Architecture

The core architecture pattern is **three-tier simulation**, trading off accuracy against speed:

```
                    ┌─────────────────────────────────┐
                    │        LLM PLANNER               │
                    │   Generates process plan (JSON)   │
                    └───────────────┬─────────────────┘
                                    │
            ┌───────────────────────┼───────────────────────┐
            ▼                       ▼                       ▼
┌───────────────────────┐ ┌──────────────────┐ ┌──────────────────────┐
│ TIER 1: Rule-Based    │ │ TIER 2: Voxel    │ │ TIER 3: Full Physics │
│ Heuristics            │ │ Simulation       │ │ Simulation           │
│                       │ │                  │ │                      │
│ Speed: microseconds   │ │ Speed: 1-10 sec  │ │ Speed: min-hrs       │
│ Fidelity: categorical │ │ Fidelity: medium │ │ Fidelity: high       │
│                       │ │                  │ │                      │
│ • Wall thickness      │ │ • Material       │ │ • CFD molding fill   │
│ • Draft angles        │ │   removal via    │ │ • FEA thermal/       │
│ • Tool constraints    │ │   voxel subtract  │ │   warpage            │
│ • Material compat.    │ │ • Swept volume   │ │ • Cutting forces     │
│ • Tolerance rules     │ │ • Collision check│ │ • Tool deflection    │
│                       │ │ • Cycle time     │ │ • Surface finish     │
│                       │ │                  │ │                      │
│ USE: Reject-sampling  │ │ USE: RL reward   │ │ USE: Final validation│
│ (discard obviously    │ │ shaping (primary │ │ & fine-tuning        │
│ bad plans instantly)  │ │ training loop)   │ │ (spot-check)         │
└───────────────────────┘ └──────────────────┘ └──────────────────────┘
```

**Why multi-fidelity?** RL needs thousands of simulation rollouts. Physics-grade simulation (CFD/FEA) takes hours per run. Voxel simulation takes seconds and the reward signal still correlates with plan quality. High-fidelity validation runs only on the final candidate plans.

## Tier 1: Rule-Based Heuristics (Milliseconds)

Implemented entirely in Python. No external simulators needed. Catches ~70% of common issues before any geometry simulation runs.

### CNC Heuristics
| Check | Rule | Source |
|-------|------|--------|
| Tool diameter vs feature | Tool Ø < pocket width; Tool Ø > min corner radius × 2 | Machinery's Handbook |
| Depth-to-diameter ratio | DOC ≤ 2.5× tool Ø for side milling; L/D ≤ 4× for drills (no peck) | Standard machining |
| Tolerance capability | ±0.01mm → need reamer/boring; drill alone = ±0.1mm | ISO 286 |
| Thread feasibility | Tap drill = major Ø − pitch; blind hole depth ≥ thread depth + 2× pitch | ISO 724 |
| Reachability | Tool reach > feature depth (accounting for holder clearance) | Geometry check |

### Injection Molding Heuristics
| Check | Rule | Source |
|-------|------|--------|
| Wall thickness range | 0.5mm–4mm for thermoplastics; uniform within 25% variation | Bralla DFM |
| Flow length ratio | Flow length / wall thickness < 150:1 (typical unfilled) | Moldflow guidelines |
| Draft angle | ≥0.5° (polished), ≥2° (textured surfaces) | Standard DFM |
| Gate placement | Gate at thickest section; avoid weld lines near stress points | Heuristic |
| Undercut detection | Requires side-action or lifter if present | Geometry check |
| Sink mark risk | Local thickness > 1.5× adjacent → sink risk | Thickness gradient |

These are instant geometric queries on the CAD mesh using **Trimesh**:
- `trimesh.ray.intersects_location` for thickness analysis
- `trimesh.curvature` for draft angle estimation
- Mesh section analysis for wall uniformity

## Tier 2: Voxel-Based Material Removal (Seconds)

The workhorse for RL training. Fast enough for thousands of rollouts, accurate enough for useful reward signals.

### Recommended Stack

```
trimesh (voxel module)     # Voxel grid operations on CAD geometry
manifold3d                  # Fast mesh boolean for tool swept volumes
gcodeparser                 # Parse G-code into structured operations
numpy                       # Array operations on voxel grids
pybullet (optional)         # Collision detection for tool-holder-body
```

### How It Works

```python
# Core simulation loop (simplified)

class VoxelCNCSimulator:
    def __init__(self, stock_mesh, resolution_mm=0.5):
        self.stock = trimesh.load(stock_mesh)
        self.voxels = self.stock.voxelized(pitch=resolution_mm)
        self.resolution = resolution_mm
        self.collisions = []

    def simulate_operation(self, op: ToolOperation) -> SimulationResult:
        # 1. Generate tool swept volume for this op's toolpath
        tool_mesh = build_tool_mesh(op.tool)
        swept = sweep_volume(tool_mesh, op.toolpath)  # via manifold3d booleans

        # 2. Voxelize the swept volume at same resolution
        swept_vox = swept.voxelized(pitch=self.resolution)

        # 3. Subtract from stock (numpy boolean mask)
        removed_mask = swept_vox.encoding.dense & self.voxels.encoding.dense
        self.voxels.encoding.dense &= ~removed_mask

        # 4. Check for gouges (tool removing material below finished surface)
        if self._detect_gouge(removed_mask, op.finish_surface):
            return SimulationResult(success=False, issue="gouge_detected")

        # 5. Compute metrics
        volume_removed = np.sum(removed_mask) * (self.resolution ** 3)
        uncut_volume = self._compute_uncut(op.target_geometry)

        return SimulationResult(
            success=True,
            volume_removed=volume_removed,
            uncut_volume=uncut_volume,
            cycle_time=estimate_cycle_time(op.toolpath, op.feeds),
            collisions=[]
        )
```

### Performance

| Resolution | Voxels (100mm³ part) | Operation time | Memory |
|-----------|---------------------|----------------|--------|
| 1.0mm | 1,000,000 | ~50ms | ~8MB |
| 0.5mm | 8,000,000 | ~200ms | ~64MB |
| 0.25mm | 64,000,000 | ~2s | ~512MB |

0.5mm resolution is the recommended starting point — adequate for most features, fast enough for RL.

## Tier 3: Full Physics Simulation (Minutes to Hours)

Used only for final validation of top-ranked plans, not during RL training.

### CNC: High-Fidelity Options

| Tool | Approach | When to Use |
|------|----------|-------------|
| **Manifold3d (high-res mesh)** | Mesh boolean at 0.1mm tolerance | Final artifact check before production |
| **OpenCASCADE BREP** | Exact geometric boolean | Ultimate accuracy verification |
| **FreeCAD CAM Simulator** | BREP-based stock subtract | Visual validation of critical features |
| **CAMotics** | Voxel-based G-code sim | Quick G-code visual check |

### Injection Molding: High-Fidelity Options

| Tool | Approach | When to Use |
|------|----------|-------------|
| **openInjMoldSim** | OpenFOAM-based CFD for fill/pack/cool | Phase 2+; best open-source option |
| **injectionMoldingFoam** | OpenFOAM solver for fiber-reinforced | If fiber-filled plastics needed |
| **Salome Platform** | CAD-to-mesh preprocessing | Companion tool for openInjMoldSim |

**Warning**: openInjMoldSim requires CFD expertise. Setup involves:
1. Import CAD into Salome → generate volume mesh
2. Define material properties (viscosity curves, PVT data, thermal conductivity)
3. Configure solver (injection location, pressure, temperature)
4. Run simulation (hours)
5. Post-process with ParaView/PyFoam

This is NOT plug-and-play. Plan 2-3 weeks to get the first simulation running.

## Collision Detection

PyBullet is the recommended engine for collision checking. It's fast, Python-native, and Gymnasium-compatible.

```python
class CollisionChecker:
    """Detect tool-holder collisions with part, fixture, and machine."""
    def __init__(self):
        self.client = pybullet.connect(pybullet.DIRECT)  # headless

    def load_setup(self, part_mesh, fixture_mesh, machine_model):
        self.part_id = self._load_mesh(part_mesh)
        self.fixture_id = self._load_mesh(fixture_mesh)
        self.machine_id = self._load_mesh(machine_model)

    def check_toolpath(self, tool_mesh, holder_mesh, positions: list[Matrix4]):
        for pos in positions:
            tool_id = self._load_mesh_at(tool_mesh, pos)
            holder_id = self._load_mesh_at(holder_mesh, pos)

            # Check tool-workpiece (this is cutting, not collision)
            tool_part = pybullet.getClosestPoints(tool_id, self.part_id, distance=0)

            # Check holder-part (this IS a collision)
            holder_part = pybullet.getClosestPoints(holder_id, self.part_id, distance=1.0)
            if holder_part:
                return CollisionResult(collision=True, body="holder", target="part")

            # Check tool-fixture
            tool_fixture = pybullet.getClosestPoints(tool_id, self.fixture_id, distance=0)
            if tool_fixture:
                return CollisionResult(collision=True, body="tool", target="fixture")

        return CollisionResult(collision=False)
```

## RL Environment Integration

The simulator is wrapped in a standard Gymnasium environment:

```python
class CAPPEnv(gymnasium.Env):
    """
    Observation: Encoded process plan (operations, tools, parameters, features)
    Action: Plan modification (tool swap, parameter adjustment, sequence reorder)
    Reward: volume_removed_efficiency - collision_penalty - time_penalty
            + constraint_satisfaction_bonus - tool_wear_penalty
    """
    def __init__(self, cad_path, material, target_plan):
        self.tier1 = RuleValidator()          # fast heuristics
        self.tier2 = VoxelCNCSimulator()      # material removal
        self.tier3 = None                      # full physics (lazy init)

    def step(self, action):
        plan = self._apply_action(action)
        reward = 0.0
        done = False
        info = {}

        # Tier 1: Instant rule check (reject obviously bad)
        t1_result = self.tier1.validate(plan)
        if t1_result.violations:
            return self.observation, -10.0, True, {"tier": 1, "violations": t1_result.violations}

        # Tier 2: Voxel simulation
        t2_result = self.tier2.simulate(plan)
        reward += t2_result.volume_removed_efficiency * 5.0
        reward -= len(t2_result.collisions) * 3.0
        reward -= t2_result.uncut_volume_ratio * 10.0
        reward += t2_result.constraint_satisfaction * 2.0
        info["tier"] = 2
        info["sim_result"] = t2_result

        # Tier 3: Optional high-fidelity spot check (expensive)
        # Only run on top plans, not every RL step

        return self.observation, reward, t2_result.is_complete, info
```

**RL algorithm**: PPO via Stable-Baselines3 for single-GPU training. Switch to RLlib (Ray) if distributed training is needed.

## Existing Tools Landscape

### Open-Source CNC Simulators

| Tool | Language | Capability | Python API | RL-Ready | Verdict |
|------|----------|-----------|------------|----------|---------|
| **CAMotics** | C++/Qt | 3-axis G-code sim, voxel removal | Partial (C bindings) | No | Good for visuals, not headless |
| **FreeCAD CAM** | C++/Python | 3-axis CAM + simulation, BREP-based | Yes (fragile headless) | No | Powerful but API unstable |
| **PyCAM** | Python | 3-axis toolpath gen, basic sim | Native | No | Dead since 2017 |
| **CQ-CAM** | Python | CadQuery-based 3-axis CAM | Native | No | Early stage, promising |

### Geometry Kernels (for custom simulators)

| Library | Speed | Accuracy | Python | License | Best For |
|---------|-------|----------|--------|---------|----------|
| **Manifold** | Very fast | High (mesh) | Yes | Apache 2.0 | **Primary choice** |
| **Trimesh** | Fast | Medium (mesh) | Yes | MIT | **Voxel + analysis** |
| **MeshLib** | Very fast | High (GPU accel) | Yes | Free tier | Performance leader |
| **OpenCASCADE** | Slow | Very high (BREP) | Yes (pythonOCC) | LGPL | Final verification |

### Injection Molding Simulators

| Tool | Approach | Speed | Accuracy | Python | Phase |
|------|----------|-------|----------|--------|-------|
| **openInjMoldSim** | OpenFOAM CFD | Hours | High | Pre/post only | Phase 2+ |
| **injectionMoldingFoam** | OpenFOAM | Hours | High | Pre/post only | Phase 2+ |
| **Salome Platform** | CAD→Mesh prep | Minutes | N/A | Full scripting | Companion |

### Multi-Physics Frameworks

| Framework | Strength | Speed | GPU Parallel | Best Use |
|-----------|----------|-------|-------------|----------|
| **PyBullet** | Collision detection | Very fast | No | Collision + kinematics |
| **MuJoCo (MJX)** | Contact dynamics + GPU | Very fast | Yes (100s parallel) | Massively parallel RL |
| **Isaac Sim** | Full physics + rendering | Slow | Yes | Digital twin (Phase 2+) |
| **Gazebo** | ROS integration | Moderate | No | Not recommended |

### G-Code Parsers

| Library | Install | Capability |
|---------|---------|------------|
| **gcodeparser** | `pip install gcodeparser` | Parse to objects, modal state tracking |
| **pygcode** | `pip install pygcode` | Full interpreter with machine state |
| **python-gcode** | `pip install python-gcode` | Lightweight parsing |

**Recommendation**: `gcodeparser` for MVP (simplest, best-maintained).

## Injection Molding: Simplified Models (No CFD)

For Phase 0/MVP, use heuristic checks that catch ~80% of molding issues without any CFD:

```
Rule Engine (Python + Trimesh)
│
├── Wall thickness analysis
│   ├── Ray-cast through mesh to find min/max thickness
│   ├── Flag: <0.5mm (short shot risk), >4mm (sink/shrink)
│   └── Flag: thickness variation >25% within 10mm radius
│
├── Draft angle check
│   ├── Surface normal analysis on vertical faces
│   └── Flag: <0.5° (ejection difficulty)
│
├── Flow length estimation
│   ├── Shortest-path distance from gate to extremities
│   └── Flag: length/wall_thickness > 150
│
├── Undercut detection
│   ├── Check for features that prevent straight-pull ejection
│   └── Flag: requires side-action, lifter, or unscrewing core
│
└── Gate/weld line heuristics
    ├── Identify natural weld line locations (where flows meet)
    └── Flag: weld line at high-stress feature
```

All checks run in milliseconds on the triangulated mesh via Trimesh.

## Key Gaps & Limitations

### What Open-Source Tools Cannot Do

1. **5-axis CNC simulation**: No open-source tool implements dexel/tridexel-based 5-axis material removal at production speed. CAMotics is 3-axis only.

2. **Cutting forces & tool deflection**: Requires physics-based material modeling (Johnson-Cook, etc.). Only commercial tools (Vericut, Third Wave AdvantEdge) do this.

3. **Thermal effects in machining**: Heat generation, coolant effects, thermal expansion — all require coupled FEA. Not available open-source.

4. **Full injection molding warpage**: openInjMoldSim handles fill but not coupled warpage/cooling/shrinkage prediction at Moldflow quality.

5. **Multi-process chain**: No tool tracks stock state across casting → machining → heat treating → finishing in a unified model. Each step restarts from nominal CAD.

6. **Machine-specific kinematics**: Open-source simulators model generic 3-axis orthogonal mills. Commercial tools model specific machines (trunnion, swivel head, hexapod) and check axis limits and singularities.

7. **Material databases**: No unified open-source database comparing to Moldflow's 25k+ materials. Cutting force coefficients require per-pair calibration.

### Accuracy vs. Speed for RL

| Approach | Accuracy | Speed/op | RL-Suitable |
|----------|----------|----------|-------------|
| Rule-based heuristics | Low (pass/fail) | <1ms | Initial screening |
| Voxel (1mm) | Medium | ~50ms | Primary reward signal |
| Voxel (0.5mm) | Medium-High | ~200ms | Primary reward signal |
| Mesh boolean (Manifold) | High | 5-60s | Batch fine-tuning |
| BREP boolean (OpenCASCADE) | Very high | Min-hrs | No |
| CFD (OpenFOAM) | High | Hrs/setup | No |
| FEA (CalculiX) | High | Hrs/setup | No |

**Critical insight**: RL does not need perfect physics. It needs a reward signal that *correlates* with actual quality. A voxel sim that reports "30% less collision volume = better plan" is useful even if absolute collision volume is off by 15%.

## Recommended Phase 0 Stack

All pip-installable Python packages:

```
trimesh              # CAD import, mesh operations, voxel support
manifold3d           # Fast mesh boolean operations
gcodeparser          # G-code parsing
pybullet             # Collision detection, kinematics
numpy                # Array operations on voxel grids
gymnasium            # RL environment API
stable-baselines3    # RL algorithms (PPO, DQN)
```

**Total added complexity**: ~7 Python packages. No external dependencies beyond `pip install`.

## Build vs. Integrate

| Component | Decision | Tool | Rationale |
|-----------|----------|------|-----------|
| G-code parser | **Integrate** | gcodeparser | Mature, pip-installable, well-maintained |
| CAD import | **Integrate** | trimesh | Best Python CAD import library, voxel support |
| CNC material removal | **Build** | on trimesh voxel + manifold3d | No existing tool has RL-compatible API |
| Collision detection | **Integrate** | PyBullet (headless) | Fast, Python-native, Gymnasium-compatible |
| Injection molding checks | **Build** | on trimesh analysis | Rule-based; no package exists |
| Molding CFD | **Defer** | openInjMoldSim (Phase 2+) | Too heavy for Phase 0 |
| Visualization | **Integrate** | Trimesh scene + PyVista | Trimesh for export, PyVista for advanced |
| RL framework | **Integrate** | SB3 (single-GPU) or RLlib (distributed) | Mature, well-documented |
| Machine kinematics | **Build** | custom chain model | Simple for 3-axis; defer 5-axis |

## Directory Structure (Simulation Module)

```
src/simulation/
├── __init__.py
├── env.py                    # Gymnasium CAPPEnv
├── tier1_rules.py            # Heuristic rule validators
├── tier2_voxel.py            # Voxel-based CNC simulation
├── tier3_physics.py          # High-fidelity integration (Phase 2+)
├── collision.py              # PyBullet collision detection wrapper
├── toolpath.py               # Tool swept volume generation
├── gcode.py                  # G-code parser wrapper
├── rewards.py                # Reward function definitions
├── molding_rules.py          # Injection molding heuristics
├── material_db.py            # Material property lookup tables
└── visualization.py          # Simulation result visualization
```

## Development Roadmap

Status note: this roadmap is a design target for the broader simulator/RL
program. The current repository has passing simulation bridge tests and browser
review assets, while RL and high-fidelity physics remain deferred until the
verified STEP-to-SubCAD corpus and comparison loop are reliable.

### Phase 0 (MVP — 2-3 months solo)
- [x] Architecture design (this document)
- [ ] 3-axis voxel CNC simulator (trimesh + manifold3d)
- [ ] G-code parser integration (gcodeparser)
- [ ] Rule-based injection molding checks
- [ ] Basic collision detection (PyBullet)
- [ ] Gymnasium environment wrapper
- [ ] RL loop with SB3 PPO
- [ ] Material DB: 6061, 7075, 4140 steel, ABS, PP, nylon

### Phase 1 (3-6 months)
- [ ] Multi-fidelity pipeline (Tier 1 → Tier 2 → Tier 3)
- [ ] 3-axis machine kinematics model
- [ ] Expanded material database (15+ materials)
- [ ] Hierarchical RL for plan structure + parameter tuning
- [ ] RLlib integration for distributed training
- [ ] Tool engagement analysis for feed/speed validation

### Phase 2 (6-12 months)
- [ ] openInjMoldSim integration for molding CFD
- [ ] Limited 5-axis kinematic support
- [ ] Simplified FEA for thermal distortion (CalculiX)
- [ ] Digital twin visualization (PyVista / Omniverse render)
- [ ] Multi-process chain validation (cast → machine → heat treat → finish)
