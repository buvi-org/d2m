# WebGPU Compute Shader Architecture for Tri-Dexel Simulation

## 1. What Runs Where

### Browser (ALL simulation compute)
- WebGPU compute shaders: dexel subtraction, marching cubes surface extraction, gouge/collision detection
- WebGL/Three.js: mesh rendering
- CPU JavaScript: orchestration, buffer management, G-code parsing (lightweight), bounding-box culling, tool pose interpolation

### Server (zero simulation compute)
- G-code parsing (Python, can optionally run in browser too)
- LLM process planning
- Initial stock STEP-to-dexel conversion (one-time preprocessing)
- Static file serving (HTML, JS, WGSL shaders)
- User authentication / project management

### Communication
- WebSocket sends parsed G-code blocks + tool definitions to browser
- Browser streams back: simulation progress, deviation stats, collision events
- Alternatively: self-contained static page with embedded G-code for demos

---

## 2. Memory Model

### GPU Buffer Layout

The tri-dexel data structure maps to GPU storage buffers as follows:

```
┌─────────────────────────────────────────────────────────────────┐
│  Z-Dexel Grid (XY plane, rays along +Z)                         │
│                                                                  │
│  @binding(0) intervals_z:  array<f32>   // packed [s0,e0,s1,e1..]│
│  @binding(1) columns_z:    array<DexelColumnMeta>               │
│                                                                  │
│  DexelColumnMeta {                                               │
│    interval_offset: u32,  // start index in intervals array      │
│    interval_count: u32,   // number of [start,end] pairs         │
│  }                                                               │
└─────────────────────────────────────────────────────────────────┘

Same layout replicated for X-grid (@binding(0,1) in group 1) and
Y-grid (@binding(0,1) in group 2).

### Buffer Sizing Rules

- Max intervals per column: 64 (covers complex multi-feature parts)
- Column buffer size: nu_cells * nv_cells * sizeof(DexelColumnMeta) = nx*ny*8 bytes
- Interval buffer size: nu_cells * nv_cells * 64 * 2 * 4 bytes = nx*ny*512 bytes
- For a 512x512 grid at 0.1mm resolution: ~128 MB per grid, ~384 MB total for tri-dexel
- Resizing: when interval count exceeds capacity, double the intervals buffer and re-pack

### Additional Buffers

```
@binding(2) tool_params:    ToolParams uniform buffer   (48 bytes per tool pose)
@binding(3) affected_cols:  array<u32>                   (output of CPU culling)
@binding(4) grid_params:    vec4<f32> uniform            (origin_x, origin_y, res, cols_per_row)
```

### Output Buffers (Marching Cubes)

```
@binding(0) vertex_buffer:   array<f32>  // x,y,z,nx,ny,nz per vertex
@binding(1) vertex_count:    atomic<u32>
@binding(2) index_buffer:    array<u32>
@binding(3) index_count:     atomic<u32>
```

---

## 3. Dispatch Strategy

### Per-Move Pipeline

For each tool move (G01 block):

1. **CPU**: Parse G-code -> tool pose start/end
2. **CPU**: Interpolate tool poses (SLERP + linear for 5-axis)
3. **CPU**: Compute swept bounding box, cull to affected column indices
4. **CPU**: Serialize tool params to uniform buffer, upload affected column list
5. **GPU Dispatch 1**: `dexel_subtract_z` (one thread per affected column)
6. **GPU Dispatch 2**: `dexel_subtract_x` (one thread per affected column)
7. **GPU Dispatch 3**: `dexel_subtract_y` (one thread per affected column)

For swept volumes (toolpaths longer than resolution):
- Sample N intermediate poses
- For each pose sample, dispatch subtract shaders
- The union happens naturally because each dispatch subtracts from the same buffers

### Workgroup Configuration

```
Workgroup size: 64 (WGSL @workgroup_size(64))
Dispatch count: ceil(affected_cols.length / 64)

For 512x512 grid, worst-case affected ≈ 262k columns
  = 4096 workgroups per dispatch
  = ~4M GPU threads per move (3 dispatches)
```

### Synchronization

- Each dispatch must complete before the next begins (GPU fence / pipeline barrier)
- Between Z/X/Y subtract dispatches: no dependency (they modify different buffer groups)
  - Can run in parallel if using separate bind groups

---

## 4. Shader Pipeline

### Shader 1: `dexel_subtract.wgsl`

**Purpose**: Core material removal. For each dexel column, compute ray-tool intersection intervals and subtract from existing intervals.

**Input**: Dexel interval buffer, column metadata, tool params, affected column indices, grid params

**Output**: Updated dexel interval buffer + column metadata (in-place)

**Key Functions** (mapped to Python source):
- `ray_ball_endmill_intersection()` -> Python `BallEndmill.ray_intersection()` (tools.py:520)
- `ray_flat_endmill_intersection()` -> Python `FlatEndmill.ray_intersection()` (tools.py:450)
- `ray_bullnose_intersection()` -> Python `BullNoseEndmill.ray_intersection()` (tools.py:587)
- `ray_drill_intersection()` -> Python `Drill.ray_intersection()` (tools.py:673)
- `subtract_intervals_in_place()` -> Python `DexelColumn.subtract()` (tri_dexel.py:107)
- `world_to_tool()` -> Python `world_to_tool()` (swept_volume.py:53)
- `ray_cylinder()` -> Python `_ray_cylinder()` (tools.py:58)
- `ray_sphere()` -> Python `_ray_sphere()` (tools.py:159)
- `ray_cone()` -> Python `_ray_cone()` (tools.py:218)
- `ray_disc()` -> Python `_ray_disc()` (tools.py:278)
- `solve_quadratic()` -> Python `_solve_quadratic()` (tools.py:24)

**Data flow per thread**:
1. Read `col_idx` from `affected_cols[gid.x]`
2. Read column metadata: `interval_offset`, `interval_count`
3. Compute ray origin in world coords from grid params + col_idx
4. Transform ray to tool-local via tool pose
5. Dispatch to tool-specific intersection function -> up to 4 entry/exit pairs
6. For each existing interval in column, apply 5-case subtraction
7. Write surviving intervals back to packed buffer
8. Update `interval_count` in column metadata

### Shader 2: `marching_cubes.wgsl`

**Purpose**: Extract surface mesh from dexel interval data.

**Algorithm**: 
- For each non-empty column in Z-grid, emit surface vertices at interval boundaries
- Entry point of first interval = surface facing -Z (ray origin side)
- Exit point of last interval = surface facing +Z
- Internal entry/exit pairs = internal cavities/walls
- Each vertex: position + normal (6 floats)
- Build index buffer connecting adjacent columns into triangles
- Merge vertices from X and Y grids (done on CPU after readback, for simplicity)

**Input**: Z dexel intervals + column metadata, X dexel intervals, Y dexel intervals

**Output**: Vertex buffer (position + normal interleaved), index buffer, atomic counters

### Shader 3: `collision_detect.wgsl`

**Purpose**: Detect tool-machine collisions using SDF distance checks.

**Input**: Tool pose, machine component SDFs in buffers

**Output**: Collision flag + penetration depth per collision pair

---

## 5. Data Flow

```
G-code file
    │
    ▼
┌──────────────────┐
│  CPU: G-code     │  JavaScript parser (web/sim/gcode.js)
│  Parser          │  Modal state tracking, returns parsed moves
└──────┬───────────┘
       │  [{motion: "G01", X:10, Y:20, Z:-5, A:0, B:30, C:0}, ...]
       ▼
┌──────────────────┐
│  CPU: Tool Pose  │  Interpolate start->end poses for swept volumes
│  Interpolation   │  Compute swept bounding box (AABB)
└──────┬───────────┘
       │  ToolParams + affected column indices
       ▼
┌──────────────────┐
│  GPU: Dexel      │  Compute shader dispatch (3x, one per axis)
│  Subtraction     │  Each thread: ray-tool intersect + interval subtract
└──────┬───────────┘
       │  Updated dexel buffers (on GPU)
       ▼
┌──────────────────┐
│  GPU: Marching   │  Surface extraction compute shader
│  Cubes           │  Emit vertex/index buffers
└──────┬───────────┘
       │  Vertex buffer + Index buffer (GPU -> CPU readback)
       ▼
┌──────────────────┐
│  CPU -> GPU:     │  Upload vertex/index buffers to WebGL
│  Three.js Render │  Render mesh, tool animation, deviation heatmap
└──────────────────┘
```

---

## 6. Performance Targets

| Operation | Target | Notes |
|-----------|--------|-------|
| 3-axis single move (no sweep) | <10ms GPU time | 512x512 grid, ball endmill |
| 5-axis single move (no sweep) | <30ms GPU time | Includes pose interpolation overhead |
| 5-axis swept move (10 samples) | <50ms GPU time | 10x dispatch overhead |
| Marching cubes (512x512 grid) | <20ms GPU time | Surface extraction + vertex/index generation |
| Total frame budget | <50ms | For interactive playback at 20fps |
| Buffer readback (2M vertices) | <5ms | GPU->CPU transfer for mesh update |

### Scaling Notes

- Workload scales linearly with grid resolution^2
- Each additional dexel direction adds ~33% compute
- Swept volumes scale linearly with sample count
- WebGPU overhead per dispatch: ~0.1-0.5ms (amortized over thousands of threads)

---

## 7. Error Handling & Debugging

### Shader Debugging
- `device.pushErrorScope('validation')` before each dispatch
- `device.popErrorScope()` after to catch shader compilation/validation errors
- WGSL `debugPrintf` (where available) for printf-style debugging
- Compare GPU output against Python reference for identical inputs

### Buffer Overflow Handling
- Pre-allocate generous interval capacity (64 intervals/column)
- On overflow: resize buffer, re-pack, re-dispatch
- Track max interval count per grid for adaptive sizing

### Fallback Paths
- If WebGPU unavailable: fall back to Architecture B (WASM) or Architecture A (server)
- If GPU OOM: reduce grid resolution, retry
- If shader compilation fails: report error to user with WGSL source
