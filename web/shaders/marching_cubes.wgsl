// =============================================================================
// marching_cubes.wgsl — Surface Mesh Extraction from Tri-Dexel Data
//
// Extracts a triangle mesh from the tri-dexel model by:
// 1. Emitting surface vertices at interval boundaries for each non-empty column
// 2. Building triangle indices connecting adjacent columns
// 3. Computing approximate normals from dexel axis directions
//
// Python reference:
//   src/simulation/surface.py — tri_dexel_to_mesh, _extract_surface_points
//   src/simulation/tri_dexel.py — DexelGrid, DexelColumn, TriDexelModel
// =============================================================================

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const MAX_COLUMN_INTERVALS: u32 = 64u;
const MAX_VERTICES: u32 = 1_000_000u;
const MAX_INDICES: u32 = 6_000_000u;

// ---------------------------------------------------------------------------
// Storage Buffer Bindings
// ---------------------------------------------------------------------------

// Z-dexel interval data (packed [s,e] pairs per column slot)
@group(0) @binding(0) var<storage, read> z_intervals: array<f32>;
@group(0) @binding(1) var<storage, read> z_columns: array<u32>; // [interval_count] per column

// X-dexel interval data
@group(0) @binding(2) var<storage, read> x_intervals: array<f32>;
@group(0) @binding(3) var<storage, read> x_columns: array<u32>;

// Y-dexel interval data
@group(0) @binding(4) var<storage, read> y_intervals: array<f32>;
@group(0) @binding(5) var<storage, read> y_columns: array<u32>;

// Grid parameters (same structure as dexel_subtract.wgsl)
struct GridParams {
    axis: u32,           // 0=Z, 1=X, 2=Y
    resolution: f32,
    nu_cells: u32,       // cells in first orthogonal direction
    nv_cells: u32,       // cells in second orthogonal direction
    origin_x: f32,
    origin_y: f32,
    origin_z: f32,
};
@group(0) @binding(6) var<storage, read> grid: GridParams;

// Output vertex buffer: interleaved position (xyz) + normal (xyz) = 6 floats/vertex
@group(0) @binding(7) var<storage, read_write> vertices: array<f32>;

// Atomic vertex count (incremented per vertex written)
@group(0) @binding(8) var<storage, read_write> vertex_count: atomic<u32>;

// Output index buffer: triangle indices
@group(0) @binding(9) var<storage, read_write> indices: array<u32>;

// Atomic index count
@group(0) @binding(10) var<storage, read_write> index_count: atomic<u32>;


// =============================================================================
// SURFACE POINT EXTRACTION
//
// For each non-empty column in a dexel grid, extract surface vertices:
//   - Entry point of first interval  -> surface facing -ray_dir
//   - Exit point of last interval    -> surface facing +ray_dir
//   - Internal entry/exit pairs      -> internal cavities
//
// Python: surface.py:25 _extract_surface_points
// =============================================================================

/// Compute ray origin for a column index in the Z-grid (XY plane).
fn z_ray_origin(col_idx: u32) -> vec3<f32> {
    let nv = grid.nv_cells;
    let i = col_idx / nv;
    let j = col_idx % nv;
    let fi = f32(i) + 0.5;
    let fj = f32(j) + 0.5;
    let res = grid.resolution;
    return vec3<f32>(grid.origin_x + fi * res, grid.origin_y + fj * res, grid.origin_z);
}

/// Compute ray origin for a column index in the X-grid (YZ plane).
fn x_ray_origin(col_idx: u32) -> vec3<f32> {
    let nv = grid.nv_cells; // nv = Z cells for X-grid
    let i = col_idx / nv;   // Y index
    let j = col_idx % nv;   // Z index
    let fi = f32(i) + 0.5;
    let fj = f32(j) + 0.5;
    let res = grid.resolution;
    return vec3<f32>(grid.origin_x, grid.origin_y + fi * res, grid.origin_z + fj * res);
}

/// Compute ray origin for a column index in the Y-grid (XZ plane).
fn y_ray_origin(col_idx: u32) -> vec3<f32> {
    let nv = grid.nv_cells; // nv = Z cells for Y-grid
    let i = col_idx / nv;   // X index
    let j = col_idx % nv;   // Z index
    let fi = f32(i) + 0.5;
    let fj = f32(j) + 0.5;
    let res = grid.resolution;
    return vec3<f32>(grid.origin_x + fi * res, grid.origin_y, grid.origin_z + fj * res);
}


// =============================================================================
// MAIN COMPUTE ENTRY POINT
//
// Each thread processes one column from all three grids sequentially.
// Extracts surface vertices and writes them to the output buffer.
//
// Strategy: Process columns in work-item order.
// Each work-item handles one column index across all three grids.
// =============================================================================

@compute @workgroup_size(64)
fn main(@builtin(global_invocation_id) gid: vec3<u32>) {
    let col_idx = gid.x;

    // Bounds check
    let total_z_cols = grid.nu_cells * grid.nv_cells;
    if col_idx >= total_z_cols {
        return;
    }

    // --- Process Z-Grid Column ---
    let z_slot = col_idx * MAX_COLUMN_INTERVALS * 2u;
    let z_count = z_columns[col_idx];

    if z_count > 0u {
        let ray_orig = z_ray_origin(col_idx);
        let ray_dir = vec3<f32>(0.0, 0.0, 1.0);
        let n_entry = vec3<f32>(0.0, 0.0, -1.0); // surface facing -Z
        let n_exit  = vec3<f32>(0.0, 0.0,  1.0); // surface facing +Z

        for (var k: u32 = 0u; k < z_count && k < MAX_COLUMN_INTERVALS; k++) {
            let idx = z_slot + k * 2u;
            let s = z_intervals[idx];
            let e = z_intervals[idx + 1u];

            if e > s + 1e-9 {
                // Entry vertex
                let entry_vtx = atomicAdd(&vertex_count, 1u);
                if entry_vtx < MAX_VERTICES {
                    let base = entry_vtx * 6u;
                    // Position
                    let p_entry = ray_orig + s * ray_dir;
                    vertices[base + 0u] = p_entry.x;
                    vertices[base + 1u] = p_entry.y;
                    vertices[base + 2u] = p_entry.z;
                    // Normal
                    vertices[base + 3u] = n_entry.x;
                    vertices[base + 4u] = n_entry.y;
                    vertices[base + 5u] = n_entry.z;
                }

                // Exit vertex
                let exit_vtx = atomicAdd(&vertex_count, 1u);
                if exit_vtx < MAX_VERTICES {
                    let base = exit_vtx * 6u;
                    let p_exit = ray_orig + e * ray_dir;
                    vertices[base + 0u] = p_exit.x;
                    vertices[base + 1u] = p_exit.y;
                    vertices[base + 2u] = p_exit.z;
                    vertices[base + 3u] = n_exit.x;
                    vertices[base + 4u] = n_exit.y;
                    vertices[base + 5u] = n_exit.z;
                }
            }
        }
    }

    // --- Process X-Grid Column (if within bounds) ---
    if col_idx < grid.nu_cells * grid.nv_cells {
        let x_slot = col_idx * MAX_COLUMN_INTERVALS * 2u;
        let x_count = x_columns[col_idx];

        if x_count > 0u {
            let ray_orig = x_ray_origin(col_idx);
            let ray_dir = vec3<f32>(1.0, 0.0, 0.0);
            let n_entry = vec3<f32>(-1.0, 0.0, 0.0);
            let n_exit  = vec3<f32>( 1.0, 0.0, 0.0);

            for (var k: u32 = 0u; k < x_count && k < MAX_COLUMN_INTERVALS; k++) {
                let idx = x_slot + k * 2u;
                let s = x_intervals[idx];
                let e = x_intervals[idx + 1u];

                if e > s + 1e-9 {
                    // Entry vertex
                    let entry_vtx = atomicAdd(&vertex_count, 1u);
                    if entry_vtx < MAX_VERTICES {
                        let base = entry_vtx * 6u;
                        let p_entry = ray_orig + s * ray_dir;
                        vertices[base + 0u] = p_entry.x;
                        vertices[base + 1u] = p_entry.y;
                        vertices[base + 2u] = p_entry.z;
                        vertices[base + 3u] = n_entry.x;
                        vertices[base + 4u] = n_entry.y;
                        vertices[base + 5u] = n_entry.z;
                    }

                    // Exit vertex
                    let exit_vtx = atomicAdd(&vertex_count, 1u);
                    if exit_vtx < MAX_VERTICES {
                        let base = exit_vtx * 6u;
                        let p_exit = ray_orig + e * ray_dir;
                        vertices[base + 0u] = p_exit.x;
                        vertices[base + 1u] = p_exit.y;
                        vertices[base + 2u] = p_exit.z;
                        vertices[base + 3u] = n_exit.x;
                        vertices[base + 4u] = n_exit.y;
                        vertices[base + 5u] = n_exit.z;
                    }
                }
            }
        }

        // --- Process Y-Grid Column ---
        let y_slot = col_idx * MAX_COLUMN_INTERVALS * 2u;
        let y_count = y_columns[col_idx];

        if y_count > 0u {
            let ray_orig = y_ray_origin(col_idx);
            let ray_dir = vec3<f32>(0.0, 1.0, 0.0);
            let n_entry = vec3<f32>(0.0, -1.0, 0.0);
            let n_exit  = vec3<f32>(0.0,  1.0, 0.0);

            for (var k: u32 = 0u; k < y_count && k < MAX_COLUMN_INTERVALS; k++) {
                let idx = y_slot + k * 2u;
                let s = y_intervals[idx];
                let e = y_intervals[idx + 1u];

                if e > s + 1e-9 {
                    // Entry vertex
                    let entry_vtx = atomicAdd(&vertex_count, 1u);
                    if entry_vtx < MAX_VERTICES {
                        let base = entry_vtx * 6u;
                        let p_entry = ray_orig + s * ray_dir;
                        vertices[base + 0u] = p_entry.x;
                        vertices[base + 1u] = p_entry.y;
                        vertices[base + 2u] = p_entry.z;
                        vertices[base + 3u] = n_entry.x;
                        vertices[base + 4u] = n_entry.y;
                        vertices[base + 5u] = n_entry.z;
                    }

                    // Exit vertex
                    let exit_vtx = atomicAdd(&vertex_count, 1u);
                    if exit_vtx < MAX_VERTICES {
                        let base = exit_vtx * 6u;
                        let p_exit = ray_orig + e * ray_dir;
                        vertices[base + 0u] = p_exit.x;
                        vertices[base + 1u] = p_exit.y;
                        vertices[base + 2u] = p_exit.z;
                        vertices[base + 3u] = n_exit.x;
                        vertices[base + 4u] = n_exit.y;
                        vertices[base + 5u] = n_exit.z;
                    }
                }
            }
        }
    }

    // --- Build Index Buffer ---
    // Connect adjacent surface vertices into triangles.
    // For each pair of adjacent non-empty columns in the grid,
    // connect their surface vertices to form quads (split into 2 triangles).
    //
    // This is done by checking the "right" neighbor (j+1) and "down" neighbor (i+1).
    // If both columns have intervals, we connect their first surface (entry) vertices.
    //
    // For simplicity, we use a separate dispatch pass for index generation,
    // or do it on the CPU after vertex readback. This shader focuses on vertex extraction.
    // A second dispatch (or CPU post-processing) builds indices by scanning
    // adjacent columns.
    //
    // Stub: Index construction is performed on CPU from the vertex buffer.
    // The vertex_count and vertex buffer are read back after this dispatch.
}
