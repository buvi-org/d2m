# Tri-Dexel in the Browser: WebGPU Compute + WebGL Render

## Summary

The tri-dexel simulation engine can run entirely in the browser, with WebGPU compute shaders handling the heavy math and WebGL rendering the result. This enables a Vericut-like 5-axis simulation experience with zero install, shareable URLs, and instant visual feedback — something Vericut's 1990s desktop architecture cannot do.

## Three Architectures

### A. Server-Side Compute, Stream Mesh → Browser

```
Server (Python + numpy/CuPy)
  ├── Tri-dexel engine runs on GPU
  ├── Marching cubes extracts surface mesh
  └── Stream mesh delta to browser via WebSocket

Browser (Three.js)
  └── Receives mesh as glTF binary, renders
```

- **Pros**: Uses full Python/CUDA stack. Server can have A100/H100.
- **Cons**: Latency per frame (mesh transfer). Full remesh per operation is heavy to stream. Doesn't scale to many concurrent users.
- **Latency budget**: Mesh serialization + transfer + deserialization ≈ 50-200ms for typical part.
- **Verdict**: Works today. Best for Phase 0 if we need a working UI fast. Not the long-term target.

### B. WebAssembly Compute, WebGL Render

```
Browser
  ├── WASM (Rust/C++): Tri-dexel engine on CPU threads
  ├── Web Workers: Marching cubes
  └── WebGL (Three.js): Render mesh
```

- **Pros**: Runs in browser without GPU requirements. Rust + wasm-bindgen + nalgebra is a mature toolchain.
- **Cons**: CPU-only. No GPU acceleration for dexel subtraction (which is embarrassingly parallel).
- **Performance**: Single dexel at 512² ≈ 5-10ms per operation. Tri-dexel ≈ 15-30ms. Acceptable for 3-axis, borderline for 5-axis at high resolution.
- **Verdict**: Fallback path for browsers without WebGPU support. Not the primary target.

### C. WebGPU Compute, WebGL Render (Target Architecture)

```
Browser
  ├── WebGPU Compute Shader: Tri-dexel subtraction on GPU
  ├── WebGPU Compute Shader: Marching cubes on GPU
  └── WebGL fallback (or WebGPU render): Display mesh
```

- **Pros**: Full GPU acceleration in browser. Dexel subtraction maps perfectly to compute shaders — each column is an independent work item. Same architecture as CUDA but targeting browser GPU. Chrome 113+ (May 2023) supports it. Edge, Opera same. Firefox Nightly.
- **Cons**: Safari support is behind (WebGPU in Safari Technology Preview). Requires WGSL shader language (different from CUDA/GLSL, though similar concepts).
- **Performance**: Comparable to CUDA for this workload. Embarrassingly parallel — thousands of dexel columns processed simultaneously.
- **Verdict**: The target architecture. Write the Python/numpy reference implementation first, port compute kernels to WGSL in Phase 2.

## WebGPU Compute Shader Design

The tri-dexel subtraction is naturally parallel — each dexel column is independent. The compute shader processes columns in workgroups:

```wgsl
// Dexel subtraction compute shader (single direction, e.g., Z-dexels)

struct ToolParams {
    tool_type: u32,        // 0=ball, 1=flat, 2=bull_nose
    diameter: f32,
    corner_radius: f32,
    tool_pos: vec3<f32>,   // tool tip position in workpiece frame
    tool_dir: vec3<f32>,   // tool axis direction (for 5-axis)
};

@group(0) @binding(0) var<storage, read_write> intervals: array<f32>;  // packed [start,end] pairs
@group(0) @binding(1) var<storage, read_write> interval_counts: array<u32>;  // count per column
@group(0) @binding(2) var<storage, read> tool: ToolParams;
@group(0) @binding(3) var<storage, read> affected_cols: array<u32>;  // column indices to process

@compute @workgroup_size(64)
fn main(@builtin(global_invocation_id) gid: vec3<u32>) {
    let idx = gid.x;
    if idx >= arrayLength(&affected_cols) { return; }

    let col_id = affected_cols[idx];

    // 1. Compute ray-tool intersection for this dexel column
    //    For Z-dexels: ray is vertical at (x_grid, y_grid)
    //    For 5-axis ball endmill: sphere + cylinder intersection with the ray
    let tool_intervals = compute_ray_tool_intersection(col_id, &tool);

    // 2. Subtract tool intervals from column's interval list
    //    In-place update of the packed intervals array
    subtract_intervals_in_place(col_id, &intervals, &interval_counts, &tool_intervals);
}

fn compute_ray_tool_intersection(col_id: u32, tool: &ToolParams) -> array<vec2<f32>, 4> {
    // Analytic ray-tool intersection
    // Ball endmill = cylinder + capped hemisphere
    // Returns up to 4 entry/exit pairs for complex tool shapes
    ...
}

fn subtract_intervals_in_place(
    col_id: u32,
    intervals: &array<f32>,
    counts: &array<u32>,
    to_remove: &array<vec2<f32>, 4>
) {
    // Standard interval subtraction: O(n) scan through existing intervals,
    // removing or splitting where to_remove overlaps.
    // This is the hot path — must be allocation-free.
    ...
}
```

The same pattern applies across all three dexel grids. For 5-axis moves, we sample intermediate tool poses and dispatch compute shaders per sample.

## Recommended Architecture: Hybrid Split

```
┌──────────────────────────────────────────────────────┐
│                     BROWSER                           │
│                                                       │
│  ┌──────────────────┐    ┌───────────────────────┐   │
│  │  WebGPU Compute   │    │  WebGL Renderer       │   │
│  │  (Tri-Dexel Core) │───▶│  (Three.js)           │   │
│  │                   │    │                       │   │
│  │  • Dexel subtract │    │  • Surface mesh       │   │
│  │  • March cubes    │    │  • Deviation heatmap  │   │
│  │  • Collision      │    │  • Tool animation     │   │
│  │  • Gouge detect   │    │  • Machine kinematics │   │
│  └──────────────────┘    └───────────────────────┘   │
│           │                                          │
│           │ WebSocket                                 │
└───────────┼──────────────────────────────────────────┘
            │
┌───────────▼──────────────────────────────────────────┐
│                     SERVER                             │
│                                                       │
│  • G-code parsing (Python)                            │
│  • LLM process plan generation                        │
│  • Knowledge graph validation                         │
│  • Initial stock conversion (STEP → tri-dexel init)   │
│  • Tool library serving                               │
│  • User authentication / project management           │
└──────────────────────────────────────────────────────┘
```

**Server does**: Heavy preprocessing (STEP → tri-dexel initialization), G-code parsing, LLM planning, knowledge graph queries.

**Browser does**: All simulation computation (dexel subtraction, surface extraction, collision detection) and rendering.

**Wire protocol**: WebSocket sends G-code blocks + tool definitions. Browser streams back simulation progress, deviation stats, collision events.

## Performance Expectations

| Scenario | WebGPU (browser) | Python/CuPy (server) | Native CUDA (C++) |
|----------|-----------------|---------------------|-------------------|
| 3-axis, 0.1mm res, 200mm³ part | 5-15ms per op | 10-30ms per op | 2-5ms per op |
| 5-axis, 0.1mm res, 200mm³ part | 20-50ms per op | 40-100ms per op | 10-25ms per op |
| Marching cubes (1M dexel grid) | 10-30ms | 20-50ms | 5-15ms |
| Mesh transfer (glTF binary) | N/A (local) | 50-200ms over network | N/A |

WebGPU is within 2-3x of native CUDA for this workload — entirely acceptable for interactive use.

## Implementation Path

1. **Now (Python reference)**: Tri-dexel engine in numpy. Validates the math, serves as the test oracle.
2. **Phase 2 (WebGPU port)**: Port dexel subtraction + marching cubes to WGSL compute shaders.
3. **Phase 3 (Full browser app)**: Three.js renderer, WebSocket protocol, complete VERICUT-like interaction model.

## Competitive Implications

Vericut's architecture is a 1990s desktop application — C++ with a Qt/OpenGL frontend, single-machine license server, GUI-first design. It cannot run in a browser. A WebGPU-based tri-dexel simulator:

- Zero install — share a URL, not a license dongle
- Offloads compute to user's GPU — scales infinitely
- WebSocket streaming enables real-time collaboration (multiple engineers watching the same simulation)
- Mobile-capable (WebGPU on Android Chrome, eventually iOS Safari)
- API-first design from day one (not bolted-on Python 2.7 API like Vericut)

This is not just "replacing Vericut" — it's leapfrogging their architectural ceiling entirely.
