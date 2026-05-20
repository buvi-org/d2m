# Session Notes — 2026-05-19

## Status addendum — 2026-05-20

These notes originally captured the work from 2026-05-19. The repository has moved since then, so treat the original "Next Steps" section as historical context, not current status.

Current verified status:

| Area | Status |
|------|--------|
| Agentic translator non-live test suite | `python test_agentic_translator.py` passes 55/55. This validates imports, prompts, code extraction, REPL integration, geometry comparison, feedback formatting, and mocked rich-comparison propagation. It does not prove live LLM translation success. |
| SubCAD integration | `python test_subcad_integration.py` passes 39/39. Fluent chains, exports, process-plan JSON, volume monotonicity, immutability, threaded holes, and STEP round trip are covered. |
| Fixture/setup integration | `python test_fixturing_integration.py` passes 19/19. Fixture metadata, setup flip, clearance warning path, JSON round trip, and error handling are covered. |
| Simulation bridge | `python test_sim_bridge.py` now passes 51/51 after fixing tri-dexel mesh initialization and distance accounting. |

Current doc decision:

- SubCAD and the agentic translator should be described as implemented prototype infrastructure with passing non-live tests.
- Simulation should be described as a working prototype path with passing bridge tests, not yet a validated production machining simulator.
- Mesh and feature comparison are no longer just research recommendations; implementation files exist under `src/simulation/mesh_compare.py` and `src/simulation/feature_compare.py`, with translator hooks in `src/data/agentic_translator.py`.
- GNN feature recognition, fine-tuning, product UI, and RL remain roadmap items, not implemented product status.

Recommended current plan:

1. Validate existing mesh and feature comparison feedback on known translated samples.
2. Run live translator trials with comparison/simulation signals recorded for scoring.
3. Harden simulation beyond the bridge tests: real target meshes, representative toolpaths, gouge/deviation validation, and performance checks.
4. Build training/evaluation pairs from execution-scored translations.
5. Revisit GNN, fine-tuning, and RL after the executable feedback loop is reliable.

## What we built today

### 1. AI Agentic CadQuery->subCAD Translator (`src/data/agentic_translator.py`)

The core infrastructure for translating constructive CadQuery programs into subtractive subCAD programs using an LLM + execution feedback loop.

**Components:**

- **`LLMClient`** — unified client supporting DeepSeek (default), Anthropic, and OpenAI backends. Reads API keys from env vars (`DEEPSEEK_API_KEY`, `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`).

- **`AgenticTranslator`** — main translation class. The loop:
  1. Builds a prompt with CadQuery source, ops trace, STEP bbox, measures, and full subCAD API reference
  2. LLM generates subCAD code
  3. Code is executed in `run_subcad()` (the REPL)
  4. Output is compared to reference STEP via `compare_to_reference()`
  5. If mismatch, formatted feedback is sent back to LLM for refinement
  6. Repeats until convergence or stagnation

- **`ConvergenceController`** — replaces fixed `max_attempts` with a trend-tracking algorithm:

  | Decision | Trigger |
  |----------|---------|
  | `success` | Volume ratio within tolerance (default 5%) |
  | `continue` | Error shrinking — still converging toward target |
  | `stagnant` | 3 consecutive attempts with no improvement |
  | `diverging` | 2 consecutive attempts getting worse |
  | `execution_failing` | 3 consecutive syntax/exec errors |
  | `safety_cap` | 20 attempts absolute max |

- **Prompt builders** — `build_system_prompt()` (full subCAD API reference), `build_user_prompt()` (CadQuery code + ops trace + STEP data + measures), `build_iteration_prompt()` (targeted refinement feedback)

- **`extract_code()`** — robust code extraction from LLM responses (handles fenced blocks, bare code, malformed output)

- **`translate_exploration_sample()`** — convenience function: point at a sample directory and get a translation

- **`translate_batch()`** — batch processing with optional output saving

### 2. Fixed `compare_to_reference()` in subcad_repl.py

The function was using `trimesh.load()` for STEP files, which requires the `cascadio` module (not available). Changed to use CadQuery's built-in STEP importer (`geometry.import_step()` -> `geometry.to_mesh()`), with trimesh as fallback for non-STEP formats.

### 3. Test suite (`test_agentic_translator.py`)

42 tests covering:
- Module imports
- System prompt contents (all operations documented)
- Code extraction (fenced, unfenced, bare, malformed)
- User prompt building (CadQuery code, ops trace, stock dims)
- Iteration prompt building (feedback + previous code)
- REPL integration (valid code execution, volume, faces, STEP/STL export)
- REPL error handling (missing part, syntax errors)
- Geometry comparison (self-match, cross-part)
- Feedback formatting
- Function availability

## Research Results: Better Shape Comparison Metrics

The research agent explored 4 approaches for going beyond global volume ratio to feature-localized comparison:

### Approach 1: Cross-Sectional Slicing (recommended 2nd)
- Slice both meshes at regular Z intervals
- Compare cross-sectional area at each Z
- Catches: wrong pocket depth, missing holes at specific Z, profile errors
- Feedback: "At Z=-5.0mm: candidate has 15% MORE area — material uncut"
- APIs: `trimesh.Trimesh.section()`, `Path2D.area`
- ~150 lines

### Approach 2: Per-Vertex Signed Distance Field (recommended 1st)
- Sample reference mesh vertices, compute signed distance to candidate
- Cluster error regions spatially
- Catches: gouges, uncut material, localized shape deviations
- Feedback: "Overcut of 1.2mm near (10, 20, -5) affecting 45 surface points"
- APIs: `trimesh.proximity.closest_point()`, `scipy.spatial.cKDTree`
- ~120 lines
- Note: existing `/api/deviation/` endpoint already returns per-vertex heatmap data

### Approach 3: Feature-Aware Per-Operation Comparison (recommended 3rd, highest value)
- Use ops trace / process plan to know what features exist and where
- Extract sub-meshes around each feature region
- Compare per-feature: pocket depth, hole presence, chamfer width
- Feedback: "Hole at (30, 10): diameter 5.8mm instead of 6.0mm — MISSING"
- APIs: `cadquery.selectors.BoxSelector`, `trimesh.proximity`, AAG face classifiers
- ~200 lines
- Integrates with existing `pipeline.py` feature extraction and `validator.py`

### Approach 4: Projected Area / Silhouette (fastest screening)
- Project both meshes onto XY, XZ, YZ planes
- Compare binary projections
- Catches: missing holes, wrong outer profile, asymmetric cuts
- Feedback: "XY projection missing 3% material near (25, 5)"
- ~80 lines
- APIs: `scipy.ndimage`, `scipy.spatial.ConvexHull`

### Summary Matrix

| Approach | Localizes? | Lines | Best For |
|----------|-----------|-------|----------|
| 1. Z-slicing | By depth | ~150 | Pocket depth, hole-through detection |
| 2. Per-vertex SDF | 3D clusters | ~120 | Gouges, uncut, surface finish |
| 3. Feature-aware | Per operation | ~200 | Wrong dimensions, missing ops, positions |
| 4. Projections | 2D regions | ~80 | Missing holes, asymmetric profile |
| Volume only | NO | 1 | Nothing useful |

### Recommended order: #2 (SDF) -> #1 (Z-slicing) -> #3 (feature-aware)

## Files changed/created

| File | Action |
|------|--------|
| `src/data/agentic_translator.py` | **Created** — AI agentic translator with convergence controller |
| `src/data/subcad_repl.py` | **Fixed** — `compare_to_reference()` uses CadQuery STEP import |
| `test_agentic_translator.py` | **Created** — 42 self-tests |

## Historical Next Steps

The following list is retained to preserve the 2026-05-19 session history. It is not the current plan verbatim.

### Immediate (historical)
1. **Implement Approach 2 (Per-vertex SDF)** — now represented by `src/simulation/mesh_compare.py`; current work is validation and integration, not first implementation.
2. **Implement Approach 1 (Z-slicing)** — now represented by `src/simulation/mesh_compare.py`; current work is validation and integration, not first implementation.
3. **Wire richer comparison into agentic translator** — hooks now exist; current work is to validate feedback quality and avoid overclaiming translator success.

### Medium-term
4. **Implement Approach 3 (Feature-aware)** — integrate with `pipeline.py` feature extraction and `operations.py` serialization. This is the endgame: per-operation feedback that tells the LLM exactly which operation to fix.
5. **Run live translations** — set `DEEPSEEK_API_KEY` and translate the 5 exploration samples. Measure success rate, iteration count, and convergence behavior. The former simulation bridge blocker is now fixed; the remaining concern is whether the feedback metrics are meaningful on representative samples.
6. **Scale to dataset** — once success rate is solid on exploration samples, run `translate_batch()` on the ADSKAILab Zero-To-CAD-100k dataset to generate training pairs.

### Eventual
7. **RL fine-tuning** — use the REPL execution feedback as a reward signal for fine-tuning a code-generation model (Qwen2.5-Coder-7B or similar).
8. **Multi-setup translation** — handle parts that need flipping (machining from multiple faces).

## How to run

```python
# Set API key
import os
os.environ["DEEPSEEK_API_KEY"] = "sk-..."

# Translate a single sample
from src.data.agentic_translator import translate_exploration_sample
result = translate_exploration_sample(
    "data/zero_to_cad_exploration/sample_1",
    provider="deepseek",    # or "anthropic", "openai"
    tolerance=0.05,         # 5% volume match = success
    stagnation_limit=3,     # give up after 3 non-improving attempts
)

# Or run the tests
# python test_agentic_translator.py
```
