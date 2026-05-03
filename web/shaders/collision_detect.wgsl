// =============================================================================
// collision_detect.wgsl — Tool-Machine Collision Detection via SDF Probes
//
// Checks for collisions between the tool and machine components (table,
// fixture, spindle housing) using signed distance field lookups.
//
// Algorithm:
// 1. Sample points along the tool surface (shank, holder, tip)
// 2. For each sample point, evaluate the SDF of each collision body
// 3. If signed distance < clearance threshold -> collision
// 4. Report deepest penetration per collision pair
//
// Python reference:
//   src/simulation/material_removal.py — Collision, validate_no_collision (stub)
// =============================================================================

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const MAX_SAMPLES: u32 = 256u;        // sample points along tool
const MAX_COLLISION_BODIES: u32 = 8u; // maximum machine components to check

// Collision pair type
const COLLISION_TOOL_FIXTURE: u32  = 0u;
const COLLISION_TOOL_TABLE: u32    = 1u;
const COLLISION_HOLDER_PART: u32   = 2u;
const COLLISION_HOLDER_FIXTURE: u32 = 3u;

// ---------------------------------------------------------------------------
// Data Structures
// ---------------------------------------------------------------------------

struct ToolParams {
    tool_type: u32,
    diameter: f32,
    corner_radius: f32,
    flute_length: f32,
    tool_pos_x: f32,
    tool_pos_y: f32,
    tool_pos_z: f32,
    tool_dir_x: f32,
    tool_dir_y: f32,
    tool_dir_z: f32,
    holder_diameter: f32,   // shank/holder diameter for collision checks
    holder_length: f32,      // length of holder above flute
};

// SDF of a collision body, stored as a uniform grid
struct CollisionBody {
    body_type: u32,          // 0=table, 1=fixture, 2=spindle_housing
    // SDF grid parameters
    sdf_offset: u32,         // offset into sdf_data buffer
    sdf_nx: u32,
    sdf_ny: u32,
    sdf_nz: u32,
    // Bounding box in world coordinates
    bbox_min_x: f32,
    bbox_min_y: f32,
    bbox_min_z: f32,
    bbox_max_x: f32,
    bbox_max_y: f32,
    bbox_max_z: f32,
    // Collision configuration
    clearance: f32,          // minimum allowed distance (mm)
    enabled: u32,            // 0=disabled, 1=enabled
    padding: u32,
};

struct CollisionResult {
    collision_type: u32,     // COLLISION_* enum
    body_index: u32,
    penetration: f32,        // mm of overlap (positive = collision)
    sample_point_x: f32,     // world position of deepest penetration
    sample_point_y: f32,
    sample_point_z: f32,
    padding: f32,
};


// =============================================================================
// STORAGE BUFFER BINDINGS
// =============================================================================

// Tool parameters for current pose
@group(0) @binding(0) var<storage, read> tool: ToolParams;

// Collision body descriptors
@group(0) @binding(1) var<storage, read> bodies: array<CollisionBody>;

// Packed SDF data (all bodies in one buffer)
@group(0) @binding(2) var<storage, read> sdf_data: array<f32>;

// Output collision results
@group(0) @binding(3) var<storage, read_write> results: array<CollisionResult>;

// Number of collisions detected (atomic counter)
@group(0) @binding(4) var<storage, read_write> collision_count: atomic<u32>;

// Global clearance threshold
@group(0) @binding(5) var<storage, read> global_clearance: f32;


// =============================================================================
// SDF EVALUATION
// =============================================================================

/// Trilinear interpolation of the SDF at a world-space point.
/// Returns the signed distance. Positive = outside, negative = inside.
fn evaluate_sdf(world_pt: vec3<f32>, body: CollisionBody) -> f32 {
    // Check if point is within the SDF bbox
    if world_pt.x < body.bbox_min_x || world_pt.x > body.bbox_max_x ||
       world_pt.y < body.bbox_min_y || world_pt.y > body.bbox_max_y ||
       world_pt.z < body.bbox_min_z || world_pt.z > body.bbox_max_z {
        // Outside bbox -> approximate distance to bbox surface
        let dx = max(body.bbox_min_x - world_pt.x, max(0.0, world_pt.x - body.bbox_max_x));
        let dy = max(body.bbox_min_y - world_pt.y, max(0.0, world_pt.y - body.bbox_max_y));
        let dz = max(body.bbox_min_z - world_pt.z, max(0.0, world_pt.z - body.bbox_max_z));
        return length(vec3<f32>(dx, dy, dz));
    }

    // Convert world position to SDF grid coordinates
    let sx = body.bbox_max_x - body.bbox_min_x;
    let sy = body.bbox_max_y - body.bbox_min_y;
    let sz = body.bbox_max_z - body.bbox_min_z;

    if sx < 1e-9 || sy < 1e-9 || sz < 1e-9 {
        return 1e10; // degenerate
    }

    let fx = (world_pt.x - body.bbox_min_x) / sx * f32(body.sdf_nx - 1u);
    let fy = (world_pt.y - body.bbox_min_y) / sy * f32(body.sdf_ny - 1u);
    let fz = (world_pt.z - body.bbox_min_z) / sz * f32(body.sdf_nz - 1u);

    // Integer and fractional parts
    let ix = u32(floor(fx));
    let iy = u32(floor(fy));
    let iz = u32(floor(fz));
    let dx = fx - floor(fx);
    let dy = fy - floor(fy);
    let dz = fz - floor(fz);

    // Clamp to valid range
    let cx = min(ix, body.sdf_nx - 2u);
    let cy = min(iy, body.sdf_ny - 2u);
    let cz = min(iz, body.sdf_nz - 2u);

    // Trilinear interpolation
    let stride_y = body.sdf_nx;
    let stride_z = body.sdf_ny * body.sdf_nx;

    let idx000 = body.sdf_offset + cz * stride_z + cy * stride_y + cx;
    let idx100 = idx000 + 1u;
    let idx010 = idx000 + stride_y;
    let idx110 = idx010 + 1u;
    let idx001 = idx000 + stride_z;
    let idx101 = idx001 + 1u;
    let idx011 = idx001 + stride_y;
    let idx111 = idx011 + 1u;

    let v000 = sdf_data[idx000];
    let v100 = sdf_data[idx100];
    let v010 = sdf_data[idx010];
    let v110 = sdf_data[idx110];
    let v001 = sdf_data[idx001];
    let v101 = sdf_data[idx101];
    let v011 = sdf_data[idx011];
    let v111 = sdf_data[idx111];

    // Interpolate along x
    let c00 = v000 * (1.0 - dx) + v100 * dx;
    let c01 = v001 * (1.0 - dx) + v101 * dx;
    let c10 = v010 * (1.0 - dx) + v110 * dx;
    let c11 = v011 * (1.0 - dx) + v111 * dx;

    // Interpolate along y
    let c0 = c00 * (1.0 - dy) + c10 * dy;
    let c1 = c01 * (1.0 - dy) + c11 * dy;

    // Interpolate along z
    return c0 * (1.0 - dz) + c1 * dz;
}


// =============================================================================
// TOOL SURFACE SAMPLING
// =============================================================================

/// Generate sample points along the tool surface (shank + holder).
/// world_pts: output array of world-space sample points
/// Returns: number of valid sample points
fn sample_tool_surface(
    out_pts: ptr<function, array<vec3<f32>, MAX_SAMPLES>>,
) -> u32 {
    var count: u32 = 0u;

    let tool_pos = vec3<f32>(tool.tool_pos_x, tool.tool_pos_y, tool.tool_pos_z);
    let tool_dir = vec3<f32>(tool.tool_dir_x, tool.tool_dir_y, tool.tool_dir_z);
    let tool_dir_n = normalize(tool_dir);

    let R_tool = tool.diameter * 0.5;
    let R_holder = tool.holder_diameter * 0.5;

    // Build local-to-world rotation (same as in dexel_subtract.wgsl)
    let z_axis = vec3<f32>(0.0, 0.0, 1.0);
    let cross_ax = cross(z_axis, tool_dir_n);
    let sin_angle = length(cross_ax);
    let cos_angle = dot(z_axis, tool_dir_n);

    var rot_col0 = vec3<f32>(1.0, 0.0, 0.0);
    var rot_col1 = vec3<f32>(0.0, 1.0, 0.0);
    var rot_col2 = vec3<f32>(0.0, 0.0, 1.0);

    if sin_angle > 1e-9 {
        let axis = cross_ax / sin_angle;
        let angle = atan2(sin_angle, cos_angle);
        let c = cos(angle); let s = sin(angle);
        let t = 1.0 - c;
        let ax = axis.x; let ay = axis.y; let az = axis.z;
        rot_col0 = vec3<f32>(t*ax*ax+c, t*ax*ay+s*az, t*ax*az-s*ay);
        rot_col1 = vec3<f32>(t*ax*ay-s*az, t*ay*ay+c, t*ay*az+s*ax);
        rot_col2 = vec3<f32>(t*ax*az+s*ay, t*ay*az-s*ax, t*az*az+c);
    } else if cos_angle < 0.0 {
        rot_col1 = vec3<f32>(0.0, -1.0, 0.0);
        rot_col2 = vec3<f32>(0.0, 0.0, -1.0);
    }

    // Sample points in rings along the tool axis
    let num_rings: u32 = 8u;
    let num_angular: u32 = 8u;
    let total_length = tool.flute_length + tool.holder_length;
    let ring_spacing = total_length / f32(num_rings);

    for (var ring: u32 = 0u; ring < num_rings && count < MAX_SAMPLES; ring++) {
        let z_local = f32(ring) * ring_spacing;
        // Determine radius at this z: tool shank below flute_length, holder above
        let r_local: f32 = select(R_holder, R_tool, z_local < tool.flute_length);

        for (var a_i: u32 = 0u; a_i < num_angular && count < MAX_SAMPLES; a_i++) {
            let angle = 2.0 * 3.14159265359 * f32(a_i) / f32(num_angular);
            let local_pt = vec3<f32>(
                r_local * cos(angle),
                r_local * sin(angle),
                z_local,
            );

            // Transform from tool-local to world
            let world_pt = tool_pos +
                rot_col0 * local_pt.x +
                rot_col1 * local_pt.y +
                rot_col2 * local_pt.z;

            (*out_pts)[count] = world_pt;
            count += 1u;
        }
    }

    return count;
}


// =============================================================================
// MAIN COMPUTE ENTRY POINT
// =============================================================================

@compute @workgroup_size(64)
fn main(@builtin(global_invocation_id) gid: vec3<u32>) {
    let body_idx = gid.x;

    // One thread per collision body
    let num_bodies = arrayLength(&bodies);
    if body_idx >= num_bodies {
        return;
    }

    let body = bodies[body_idx];
    if body.enabled == 0u {
        return;
    }

    // Sample points on the tool surface
    var sample_pts: array<vec3<f32>, MAX_SAMPLES>;
    let num_samples = sample_tool_surface(&sample_pts);

    // Check each sample point against this SDF body
    var min_distance: f32 = 1e10;
    var worst_point: vec3<f32> = vec3<f32>(0.0, 0.0, 0.0);

    for (var i: u32 = 0u; i < num_samples; i++) {
        let sd = evaluate_sdf(sample_pts[i], body);
        if sd < min_distance {
            min_distance = sd;
            worst_point = sample_pts[i];
        }
    }

    // Check if collision (distance < clearance)
    let effective_clearance = max(body.clearance, global_clearance);
    if min_distance < effective_clearance {
        let result_idx = atomicAdd(&collision_count, 1u);
        let max_results = arrayLength(&results);

        if result_idx < max_results {
            let pen = effective_clearance - min_distance;
            results[result_idx] = CollisionResult(
                body.body_type,
                body_idx,
                pen,
                worst_point.x,
                worst_point.y,
                worst_point.z,
                0.0, // padding
            );
        }
    }
}
