// =============================================================================
// dexel_subtract.wgsl — Core Material Removal Compute Shader
//
// Ports the Python tri-dexel material removal engine to WebGPU compute shaders.
// Each thread processes one dexel column: computes ray-tool intersection
// intervals, then subtracts them from the column's existing material intervals.
//
// Python reference files (the spec):
//   src/simulation/tools.py           — ray-primitive + tool intersection
//   src/simulation/tri_dexel.py       — DexelColumn.subtract() interval ops
//   src/simulation/swept_volume.py    — world_to_tool, pose interpolation
//   src/simulation/material_removal.py — engine orchestration
// =============================================================================

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const MAX_COLUMN_INTERVALS: u32 = 64u;    // max [start,end] pairs per column
const MAX_TOOL_INTERVALS: u32 = 4u;       // max entry/exit pairs per tool shape
const BULLNOSE_SPHERE_SAMPLES: u32 = 8u;   // torus approximation spheres per quadrant

// Tool type enum (must match tools.py factory names + JavaScript engine)
const TOOL_BALL: u32      = 0u;
const TOOL_FLAT: u32      = 1u;
const TOOL_BULLNOSE: u32  = 2u;
const TOOL_DRILL: u32     = 3u;

// Axis enum for grid direction
const AXIS_Z: u32 = 0u;
const AXIS_X: u32 = 1u;
const AXIS_Y: u32 = 2u;

// ---------------------------------------------------------------------------
// Data Structures  (Python: tri_dexel.py DexelColumn, tools.py ToolParameters)
// ---------------------------------------------------------------------------

struct ToolParams {
    tool_type: u32,          // TOOL_BALL | TOOL_FLAT | TOOL_BULLNOSE | TOOL_DRILL
    diameter: f32,           // mm
    corner_radius: f32,      // mm (R_corner for bull nose, unused for others)
    flute_length: f32,       // mm, cutting flute length from tip
    // Tool pose in workpiece frame: tip position
    tool_pos_x: f32,
    tool_pos_y: f32,
    tool_pos_z: f32,
    // Tool axis direction in workpiece frame (unit vector, for 5-axis)
    tool_dir_x: f32,
    tool_dir_y: f32,
    tool_dir_z: f32,
};

// Grid parameters uniform
struct GridParams {
    axis: u32,               // AXIS_Z | AXIS_X | AXIS_Y
    resolution: f32,         // mm per cell
    nu_cells: u32,           // number of cells in first orthogonal direction
    nv_cells: u32,           // number of cells in second orthogonal direction
    origin_x: f32,           // mm, min corner of grid in workpiece coords
    origin_y: f32,
    origin_z: f32,
};

// =============================================================================
// Storage Buffer Bindings
//
// Buffer layout: Each column gets a fixed-size slot in the intervals buffer.
// slot_start = col_idx * MAX_COLUMN_INTERVALS * 2
// A column with N intervals uses indices [slot_start, slot_start + 2*N)
// =============================================================================

// Packed interval data: [s0, e0, s1, e1, ...] per column slot
@group(0) @binding(0) var<storage, read_write> intervals: array<f32>;

// Column metadata: one per column in the grid
struct DexelColumnMeta {
    interval_count: u32,    // number of active [s,e] pairs (0 if empty)
    padding: u32,           // alignment
};
@group(0) @binding(1) var<storage, read_write> columns: array<DexelColumnMeta>;

// Tool parameters for current pose
@group(0) @binding(2) var<storage, read> tool: ToolParams;

// Affected column indices (output of CPU bounding-box cull)
@group(0) @binding(3) var<storage, read> affected_cols: array<u32>;

// Grid parameters
@group(0) @binding(4) var<storage, read> grid_params: GridParams;

// Statistics counters (optional, for performance monitoring)
@group(0) @binding(5) var<storage, read_write> cols_modified: atomic<u32>;
@group(0) @binding(6) var<storage, read_write> total_removed: atomic<u32>;


// =============================================================================
// MATH UTILITIES
// Python: tools.py _solve_quadratic() line 24
// =============================================================================

/// Solve a*t^2 + 2*b*t + c = 0 for t.
/// Returns true if real roots exist. t0 <= t1.
/// Python: tools.py:24 _solve_quadratic
fn solve_quadratic(a: f32, b: f32, c: f32, t0: ptr<function, f32>, t1: ptr<function, f32>) -> bool {
    if abs(a) < 1e-20 {
        // Degenerate: linear equation 2*b*t + c = 0
        if abs(b) < 1e-20 {
            return false;
        }
        let t = -c / (2.0 * b);
        *t0 = t;
        *t1 = t;
        return true;
    }

    let disc = b * b - a * c;
    if disc < 0.0 {
        return false;
    }

    let sqrt_disc = sqrt(disc);
    *t0 = (-b - sqrt_disc) / a;
    *t1 = (-b + sqrt_disc) / a;

    if *t0 > *t1 {
        let tmp = *t0;
        *t0 = *t1;
        *t1 = tmp;
    }
    return true;
}

/// Clamp an interval [t_in, t_out] to t >= 0.
/// Returns false if the interval is entirely behind the ray origin.
/// Python: tools.py:73 _clip_positive
fn clip_positive(t_in: f32, t_out: f32, out_in: ptr<function, f32>, out_out: ptr<function, f32>) -> bool {
    if t_out < -1e-6 {
        return false;
    }
    *out_in = max(t_in, 0.0);
    *out_out = t_out;
    if *out_out < *out_in {
        return false;
    }
    return true;
}

/// 3x3 rotation matrix from unit quaternion [w, x, y, z] (scalar-first).
/// Python: swept_volume.py:33 quaternion_to_matrix
fn quat_to_mat3(qw: f32, qx: f32, qy: f32, qz: f32) -> mat3x3<f32> {
    let xx = qx * qx; let yy = qy * qy; let zz = qz * qz;
    let xy = qx * qy; let xz = qx * qz; let yz = qy * qz;
    let wx = qw * qx; let wy = qw * qy; let wz = qw * qz;

    return mat3x3<f32>(
        vec3<f32>(1.0 - 2.0*(yy + zz),  2.0*(xy + wz),       2.0*(xz - wy)),
        vec3<f32>(2.0*(xy - wz),         1.0 - 2.0*(xx + zz), 2.0*(yz + wx)),
        vec3<f32>(2.0*(xz + wy),         2.0*(yz - wx),       1.0 - 2.0*(xx + yy)),
    );
}

/// Multiplies mat3 * vec3
fn mat3_mul_vec3(m: mat3x3<f32>, v: vec3<f32>) -> vec3<f32> {
    return vec3<f32>(
        m[0].x * v.x + m[0].y * v.y + m[0].z * v.z,
        m[1].x * v.x + m[1].y * v.y + m[1].z * v.z,
        m[2].x * v.x + m[2].y * v.y + m[2].z * v.z,
    );
}

/// Transpose of mat3
fn mat3_transpose(m: mat3x3<f32>) -> mat3x3<f32> {
    return mat3x3<f32>(
        vec3<f32>(m[0].x, m[1].x, m[2].x),
        vec3<f32>(m[0].y, m[1].y, m[2].y),
        vec3<f32>(m[0].z, m[1].z, m[2].z),
    );
}

/// Build a quaternion from axis-angle. Rotation of `angle` about `axis`.
/// Python: kinematics.py:70 from_axis_angle
fn quat_from_axis_angle(axis: vec3<f32>, angle: f32) -> vec4<f32> {
    let half = angle * 0.5;
    let s = sin(half);
    return vec4<f32>(cos(half), axis.x * s, axis.y * s, axis.z * s);
}

/// Build a rotation matrix that rotates the tool from +Z to `tool_dir`.
/// Returns (matrix, ok_flag).
/// Python: swept_volume.py:53 world_to_tool, direction_to_tool
fn build_tool_to_world(tool_dir: vec3<f32>) -> mat3x3<f32> {
    // Build rotation from tool-local z-axis [0,0,1] to tool_dir
    let z_axis = vec3<f32>(0.0, 0.0, 1.0);
    let cross = cross(z_axis, tool_dir);
    let sin_angle = length(cross);
    let cos_angle = dot(z_axis, tool_dir);

    if sin_angle < 1e-9 {
        // tool_dir is nearly parallel to +Z -> identity
        if cos_angle > 0.0 {
            return mat3x3<f32>(
                vec3<f32>(1.0, 0.0, 0.0),
                vec3<f32>(0.0, 1.0, 0.0),
                vec3<f32>(0.0, 0.0, 1.0),
            );
        } else {
            // tool_dir is -Z -> 180-degree rotation about X
            return mat3x3<f32>(
                vec3<f32>(1.0,  0.0,  0.0),
                vec3<f32>(0.0, -1.0,  0.0),
                vec3<f32>(0.0,  0.0, -1.0),
            );
        }
    }

    let axis = cross / sin_angle;
    let angle = atan2(sin_angle, cos_angle);
    // Use Rodrigues' rotation formula for axis-angle to matrix
    let c = cos(angle);
    let s = sin(angle);
    let t = 1.0 - c;
    let x = axis.x; let y = axis.y; let z_ = axis.z;

    return mat3x3<f32>(
        vec3<f32>(t*x*x + c,     t*x*y - s*z_,   t*x*z_ + s*y),
        vec3<f32>(t*x*y + s*z_,  t*y*y + c,      t*y*z_ - s*x),
        vec3<f32>(t*x*z_ - s*y,  t*y*z_ + s*x,   t*z_*z_ + c),
    );
}

/// Transform a point from world frame to tool-local frame.
/// Tool-local: tip at origin, tool axis along +Z.
/// Python: swept_volume.py:53 world_to_tool
fn world_to_tool(world_pt: vec3<f32>, tool_pos: vec3<f32>, inv_rot: mat3x3<f32>) -> vec3<f32> {
    return mat3_mul_vec3(inv_rot, world_pt - tool_pos);
}

/// Transform a direction from world frame to tool-local frame.
/// Python: swept_volume.py:70 direction_to_tool
fn direction_to_tool(world_dir: vec3<f32>, inv_rot: mat3x3<f32>) -> vec3<f32> {
    return mat3_mul_vec3(inv_rot, world_dir);
}


// =============================================================================
// RAY-PRIMITIVE INTERSECTIONS
// All functions take ray origin O and direction D in tool-local coordinates.
// |D| should be 1 (unit length) for correct t values.
// Output: write entry/exit pairs into the provided array, return count.
// Python: tools.py ray_cylinder, ray_sphere, ray_cone, ray_disc
// =============================================================================

/// Intersect ray with right circular cylinder: x^2 + y^2 <= radius^2, z in [z_min, z_max].
/// Python: tools.py:58 _ray_cylinder
fn ray_cylinder(
    O: vec3<f32>, D: vec3<f32>,
    radius: f32, z_min: f32, z_max: f32,
    out_intervals: ptr<function, array<vec2<f32>, MAX_TOOL_INTERVALS>>,
) -> u32 {
    let a = D.x * D.x + D.y * D.y;
    let b = O.x * D.x + O.y * D.y;
    let c = O.x * O.x + O.y * O.y - radius * radius;

    var count: u32 = 0u;

    if abs(a) < 1e-20 {
        // Ray parallel to cylinder axis
        if c > 1e-10 {
            return 0u; // outside the cylinder entirely
        }
        // Inside infinite cylinder: intersect with z planes
        if abs(D.z) < 1e-20 {
            // Ray perpendicular AND inside -> degenerate, treat as full range
            var ti: f32; var to_: f32;
            if clip_positive(0.0, 1e10, &ti, &to_) {
                (*out_intervals)[count] = vec2<f32>(ti, to_);
                count += 1u;
            }
            return count;
        }
        let t_zmin = (z_min - O.z) / D.z;
        let t_zmax = (z_max - O.z) / D.z;
        var t0 = min(t_zmin, t_zmax);
        var t1 = max(t_zmin, t_zmax);
        var ti: f32; var to_: f32;
        if clip_positive(t0, t1, &ti, &to_) {
            (*out_intervals)[count] = vec2<f32>(ti, to_);
            count += 1u;
        }
        return count;
    }

    var t0: f32; var t1: f32;
    if !solve_quadratic(a, b, c, &t0, &t1) {
        return 0u;
    }

    let z0 = O.z + t0 * D.z;
    let z1 = O.z + t1 * D.z;

    let in_0 = z_min <= z0 && z0 <= z_max;
    let in_1 = z_min <= z1 && z1 <= z_max;

    if in_0 && in_1 {
        var ti: f32; var to_: f32;
        if clip_positive(t0, t1, &ti, &to_) {
            (*out_intervals)[count] = vec2<f32>(ti, to_);
            count += 1u;
        }
    } else if in_0 && !in_1 {
        let t_bound = select(
            (z_max - O.z) / D.z,
            (z_min - O.z) / D.z,
            z1 > z_max
        );
        var ti = min(t0, t_bound);
        var to_ = max(t0, t_bound);
        var ci: f32; var co_: f32;
        if clip_positive(ti, to_, &ci, &co_) {
            (*out_intervals)[count] = vec2<f32>(ci, co_);
            count += 1u;
        }
    } else if !in_0 && in_1 {
        let t_bound = select(
            (z_max - O.z) / D.z,
            (z_min - O.z) / D.z,
            z0 > z_max
        );
        var ti = min(t_bound, t1);
        var to_ = max(t_bound, t1);
        var ci: f32; var co_: f32;
        if clip_positive(ti, to_, &ci, &co_) {
            (*out_intervals)[count] = vec2<f32>(ci, co_);
            count += 1u;
        }
    } else {
        // Both outside -- check if ray passes through z-slab
        if (z0 < z_min && z1 > z_max) || (z0 > z_max && z1 < z_min) {
            let t_enter = select(
                (z_min - O.z) / D.z,
                (z_max - O.z) / D.z,
                z0 > z_max
            );
            let t_exit = select(
                (z_max - O.z) / D.z,
                (z_min - O.z) / D.z,
                z0 > z_max
            );
            var ti = min(t_enter, t_exit);
            var to_ = max(t_enter, t_exit);
            var ci: f32; var co_: f32;
            if clip_positive(ti, to_, &ci, &co_) {
                (*out_intervals)[count] = vec2<f32>(ci, co_);
                count += 1u;
            }
        }
    }

    return count;
}

/// Intersect ray with sphere at center C, radius R.
/// clip_z_max restricts to the lower hemisphere (z <= clip_z_max).
/// Python: tools.py:159 _ray_sphere
fn ray_sphere(
    O: vec3<f32>, D: vec3<f32>,
    center: vec3<f32>, radius: f32, clip_z_max: f32,
    out_intervals: ptr<function, array<vec2<f32>, MAX_TOOL_INTERVALS>>,
) -> u32 {
    var count: u32 = 0u;

    let w = O - center;
    let a_val = 1.0; // |D| = 1
    let b_val = dot(D, w);
    let c_val = dot(w, w) - radius * radius;

    var t0: f32; var t1: f32;
    if !solve_quadratic(a_val, b_val, c_val, &t0, &t1) {
        return 0u;
    }

    // Clip negative solutions
    if t1 < -1e-6 {
        return 0u;
    }
    if t0 < -1e-6 {
        t0 = 0.0;
    }

    // Clip to hemisphere if needed
    if clip_z_max < 1e10 {
        let z0 = O.z + t0 * D.z;
        let z1 = O.z + t1 * D.z;

        let in_0 = z0 <= clip_z_max + 1e-6;
        let in_1 = z1 <= clip_z_max + 1e-6;

        if !in_0 && !in_1 {
            return 0u;
        }
        if in_0 && !in_1 {
            if abs(D.z) > 1e-20 {
                let t_clip = (clip_z_max - O.z) / D.z;
                if t0 <= t_clip && t_clip <= t1 {
                    t1 = t_clip;
                } else {
                    return 0u;
                }
            }
        } else if !in_0 && in_1 {
            if abs(D.z) > 1e-20 {
                let t_clip = (clip_z_max - O.z) / D.z;
                if t0 <= t_clip && t_clip <= t1 {
                    t0 = t_clip;
                } else {
                    return 0u;
                }
            }
        }
    }

    (*out_intervals)[count] = vec2<f32>(t0, t1);
    count += 1u;
    return count;
}

/// Intersect ray with right circular cone.
/// Apex at `apex`, axis +Z, half-angle `half_angle`, height `height`.
/// If truncate_radius_min > 0, cone starts at minimum radius (frustum).
/// Python: tools.py:218 _ray_cone
fn ray_cone(
    O: vec3<f32>, D: vec3<f32>,
    apex: vec3<f32>, half_angle: f32, height: f32, truncate_radius_min: f32,
    out_intervals: ptr<function, array<vec2<f32>, MAX_TOOL_INTERVALS>>,
) -> u32 {
    var count: u32 = 0u;

    // Transform ray so apex is at origin
    let Ox = O.x - apex.x;
    let Oy = O.y - apex.y;
    let Oz = O.z - apex.z;

    let k2 = tan(half_angle) * tan(half_angle);

    let a_val = D.x * D.x + D.y * D.y - k2 * D.z * D.z;
    let b_val = Ox * D.x + Oy * D.y - k2 * Oz * D.z;
    let c_val = Ox * Ox + Oy * Oy - k2 * Oz * Oz;

    var t0: f32; var t1: f32;
    if !solve_quadratic(a_val, b_val, c_val, &t0, &t1) {
        return 0u;
    }

    // Check which roots are within height and radius bounds
    var hit_ts: array<f32, 2>;
    var hit_count: u32 = 0u;

    for (var i: u32 = 0u; i < 2u; i++) {
        let t_val = select(t0, t1, i == 1u);
        let z_t = Oz + t_val * D.z;
        let r_t = sqrt(k2) * z_t;

        if z_t >= 0.0 && z_t <= height + 1e-6 {
            if r_t >= truncate_radius_min - 1e-6 {
                hit_ts[hit_count] = t_val;
                hit_count += 1u;
            }
        }
    }

    if hit_count == 2u {
        var ti = min(hit_ts[0], hit_ts[1]);
        var to_ = max(hit_ts[0], hit_ts[1]);
        if to_ < -1e-6 { return 0u; }
        if ti < -1e-6 { ti = 0.0; }
        (*out_intervals)[count] = vec2<f32>(ti, to_);
        count += 1u;
    } else if hit_count == 1u {
        var t_val = hit_ts[0];
        if t_val < -1e-6 { return 0u; }
        (*out_intervals)[count] = vec2<f32>(0.0, t_val);
        count += 1u;
    }

    return count;
}

/// Intersect ray with flat disc at z=z_plane, radius R.
/// Returns t values where ray hits the disc.
/// Python: tools.py:278 _ray_disc
fn ray_disc(
    O: vec3<f32>, D: vec3<f32>,
    z_plane: f32, radius: f32,
) -> array<f32, 2> {
    var result: array<f32, 2>;
    result[0] = -1.0; // sentinel: no hit
    result[1] = -1.0;

    if abs(D.z) > 1e-20 {
        let t = (z_plane - O.z) / D.z;
        if t < -1e-6 {
            return result; // behind ray
        }
        let px = O.x + t * D.x;
        let py = O.y + t * D.y;
        if px * px + py * py <= radius * radius + 1e-6 {
            result[0] = t;
        }
    } else {
        // Ray parallel to disc plane
        if abs(O.z - z_plane) < 1e-6 {
            // Ray in disc plane: intersect with circle
            let a_val = D.x * D.x + D.y * D.y;
            let b_val = O.x * D.x + O.y * D.y;
            let c_val = O.x * O.x + O.y * O.y - radius * radius;
            var t0: f32; var t1: f32;
            if solve_quadratic(a_val, b_val, c_val, &t0, &t1) {
                result[0] = t0;
                result[1] = t1;
            }
        }
    }
    return result;
}


// =============================================================================
// TOOL-SPECIFIC RAY INTERSECTION
// Each function computes intersection intervals for a specific tool type
// and a given ray in tool-local coordinates.
// Returns the number of interval pairs (0 to MAX_TOOL_INTERVALS).
//
// Python reference:
//   tools.py:450 FlatEndmill.ray_intersection
//   tools.py:520 BallEndmill.ray_intersection
//   tools.py:587 BullNoseEndmill.ray_intersection
//   tools.py:673 Drill.ray_intersection
// =============================================================================

/// Ball endmill: cylinder (z >= R) + hemisphere (z <= R, center at (0,0,R)).
/// Python: tools.py:520 BallEndmill.ray_intersection
fn ray_ball_endmill(
    O: vec3<f32>, D: vec3<f32>,
    radius: f32, flute_length: f32,
    out_intervals: ptr<function, array<vec2<f32>, MAX_TOOL_INTERVALS>>,
) -> u32 {
    // Collect all t-values from both components
    var all_t: array<f32, 8>; // worst case: 2 from cylinder + 2 from sphere + disc edges
    var t_count: u32 = 0u;

    // 1. Cylinder: z in [radius, flute_length]
    var cyl_ivs: array<vec2<f32>, MAX_TOOL_INTERVALS>;
    let cyl_count = ray_cylinder(O, D, radius, radius, flute_length, &cyl_ivs);
    for (var i: u32 = 0u; i < cyl_count; i++) {
        all_t[t_count] = cyl_ivs[i].x; t_count += 1u;
        all_t[t_count] = cyl_ivs[i].y; t_count += 1u;
    }

    // 2. Sphere: center (0, 0, radius), hemisphere z <= radius
    var sph_ivs: array<vec2<f32>, MAX_TOOL_INTERVALS>;
    let sphere_center = vec3<f32>(0.0, 0.0, radius);
    let sph_count = ray_sphere(O, D, sphere_center, radius, radius, &sph_ivs);
    for (var i: u32 = 0u; i < sph_count; i++) {
        all_t[t_count] = sph_ivs[i].x; t_count += 1u;
        all_t[t_count] = sph_ivs[i].y; t_count += 1u;
    }

    if t_count < 2u {
        return 0u;
    }

    // For convex tool: first and last t are entry/exit
    // Simple selection sort over small array
    for (var i: u32 = 0u; i < t_count; i++) {
        for (var j: u32 = i + 1u; j < t_count; j++) {
            if all_t[j] < all_t[i] {
                let tmp = all_t[i];
                all_t[i] = all_t[j];
                all_t[j] = tmp;
            }
        }
    }

    (*out_intervals)[0] = vec2<f32>(all_t[0], all_t[t_count - 1u]);
    return 1u;
}

/// Flat endmill: cylinder (z >= 0) + bottom disc at z=0.
/// Python: tools.py:450 FlatEndmill.ray_intersection
fn ray_flat_endmill(
    O: vec3<f32>, D: vec3<f32>,
    radius: f32, flute_length: f32,
    out_intervals: ptr<function, array<vec2<f32>, MAX_TOOL_INTERVALS>>,
) -> u32 {
    var all_t: array<f32, 8>;
    var t_count: u32 = 0u;

    // 1. Cylinder: z in [0, flute_length]
    var cyl_ivs: array<vec2<f32>, MAX_TOOL_INTERVALS>;
    let cyl_count = ray_cylinder(O, D, radius, 0.0, flute_length, &cyl_ivs);
    for (var i: u32 = 0u; i < cyl_count; i++) {
        all_t[t_count] = cyl_ivs[i].x; t_count += 1u;
        all_t[t_count] = cyl_ivs[i].y; t_count += 1u;
    }

    // 2. Bottom disc at z=0
    let disc_ts = ray_disc(O, D, 0.0, radius);
    if disc_ts[0] >= -0.5 {
        all_t[t_count] = disc_ts[0]; t_count += 1u;
    }
    if disc_ts[1] >= -0.5 {
        all_t[t_count] = disc_ts[1]; t_count += 1u;
    }

    if t_count < 2u {
        return 0u;
    }

    // Sort
    for (var i: u32 = 0u; i < t_count; i++) {
        for (var j: u32 = i + 1u; j < t_count; j++) {
            if all_t[j] < all_t[i] {
                let tmp = all_t[i];
                all_t[i] = all_t[j];
                all_t[j] = tmp;
            }
        }
    }

    (*out_intervals)[0] = vec2<f32>(all_t[0], all_t[t_count - 1u]);
    return 1u;
}

/// Bull nose endmill: cylinder + torus corner + flat bottom.
/// Torus approximated as NxN spheres distributed along the corner arc.
/// Python: tools.py:587 BullNoseEndmill.ray_intersection
fn ray_bullnose_endmill(
    O: vec3<f32>, D: vec3<f32>,
    tool_radius: f32, corner_radius: f32, flute_length: f32,
    out_intervals: ptr<function, array<vec2<f32>, MAX_TOOL_INTERVALS>>,
) -> u32 {
    var all_intervals_local: array<vec2<f32>, 128>; // union of all primitive intervals
    var iv_count: u32 = 0u;

    let r_flat = tool_radius - corner_radius;
    let r_c = corner_radius;

    // 1. Cylinder above corner: z in [r_c, flute_length]
    var cyl_ivs: array<vec2<f32>, MAX_TOOL_INTERVALS>;
    let cyl_count = ray_cylinder(O, D, tool_radius, r_c, flute_length, &cyl_ivs);
    for (var i: u32 = 0u; i < cyl_count && iv_count < 128u; i++) {
        all_intervals_local[iv_count] = cyl_ivs[i]; iv_count += 1u;
    }

    // 2. Flat bottom disc at z=0, radius = r_flat
    let disc_ts = ray_disc(O, D, 0.0, r_flat);
    if disc_ts[0] >= -0.5 && iv_count < 128u {
        all_intervals_local[iv_count] = vec2<f32>(disc_ts[0], disc_ts[0]); iv_count += 1u;
    }

    // 3. Torus: sample the 90-degree corner arc as NxN spheres
    let N = BULLNOSE_SPHERE_SAMPLES;
    for (var k: u32 = 0u; k <= N && iv_count < 124u; k++) {
        let angle = (3.14159265359 * 0.5) * f32(k) / f32(N); // 0 to pi/2
        let cx = r_flat * cos(angle);
        let cz = r_c - r_c * sin(angle);
        let centre_base = vec3<f32>(cx, 0.0, cz);

        for (var m: u32 = 0u; m < N && iv_count < 124u; m++) {
            let phi = 2.0 * 3.14159265359 * f32(m) / f32(N);
            let c_rot = vec3<f32>(
                centre_base.x * cos(phi),
                centre_base.x * sin(phi),
                centre_base.z,
            );

            var sph_ivs: array<vec2<f32>, MAX_TOOL_INTERVALS>;
            let sph_count = ray_sphere(O, D, c_rot, r_c, 1e10, &sph_ivs);
            for (var i: u32 = 0u; i < sph_count && iv_count < 128u; i++) {
                all_intervals_local[iv_count] = sph_ivs[i]; iv_count += 1u;
            }
        }
    }

    // Merge overlapping intervals = collect all t values, sort, take min/max
    // (Conservative: for convex-ish tool, first entry + last exit is correct)
    if iv_count == 0u {
        return 0u;
    }

    var t_min: f32 = 1e10;
    var t_max: f32 = -1e10;
    for (var i: u32 = 0u; i < iv_count; i++) {
        t_min = min(t_min, all_intervals_local[i].x);
        t_max = max(t_max, all_intervals_local[i].y);
    }
    // Also check for holes: if there are gaps, we need more intervals
    // For now, emit the bounding interval (correct for convex tools,
    // approximate for bull nose)

    (*out_intervals)[0] = vec2<f32>(t_min, t_max);
    return 1u;
}

/// Drill: cone tip + cylinder body.
/// Python: tools.py:673 Drill.ray_intersection
fn ray_drill(
    O: vec3<f32>, D: vec3<f32>,
    radius: f32, tip_angle_rad: f32, flute_length: f32,
    out_intervals: ptr<function, array<vec2<f32>, MAX_TOOL_INTERVALS>>,
) -> u32 {
    let half_angle = tip_angle_rad * 0.5;
    let cone_height = radius / tan(half_angle);

    var all_intervals: array<vec2<f32>, MAX_TOOL_INTERVALS * 2>;
    var iv_count: u32 = 0u;

    // 1. Cylinder: z in [cone_height, flute_length]
    var cyl_ivs: array<vec2<f32>, MAX_TOOL_INTERVALS>;
    let cyl_count = ray_cylinder(O, D, radius, cone_height, flute_length, &cyl_ivs);
    for (var i: u32 = 0u; i < cyl_count && iv_count < 8u; i++) {
        all_intervals[iv_count] = cyl_ivs[i]; iv_count += 1u;
    }

    // 2. Cone: apex at origin, z in [0, cone_height]
    var cone_ivs: array<vec2<f32>, MAX_TOOL_INTERVALS>;
    let cone_count = ray_cone(O, D, vec3<f32>(0.0, 0.0, 0.0), half_angle, cone_height, 0.0, &cone_ivs);
    for (var i: u32 = 0u; i < cone_count && iv_count < 8u; i++) {
        all_intervals[iv_count] = cone_ivs[i]; iv_count += 1u;
    }

    if iv_count == 0u {
        return 0u;
    }

    // Merge: collect all t values
    var all_t: array<f32, 8>;
    var t_count: u32 = 0u;
    for (var i: u32 = 0u; i < iv_count && t_count < 8u; i++) {
        all_t[t_count] = all_intervals[i].x; t_count += 1u;
        all_t[t_count] = all_intervals[i].y; t_count += 1u;
    }

    // Sort
    for (var i: u32 = 0u; i < t_count; i++) {
        for (var j: u32 = i + 1u; j < t_count; j++) {
            if all_t[j] < all_t[i] {
                let tmp = all_t[i];
                all_t[i] = all_t[j];
                all_t[j] = tmp;
            }
        }
    }

    (*out_intervals)[0] = vec2<f32>(all_t[0], all_t[t_count - 1u]);
    return 1u;
}

/// Dispatch to the correct tool intersection based on tool_type.
/// Python: tools.py factory function + each tool's ray_intersection
fn compute_tool_intervals(
    O_local: vec3<f32>, D_local: vec3<f32>,
    tool_params: ToolParams,
    out_intervals: ptr<function, array<vec2<f32>, MAX_TOOL_INTERVALS>>,
) -> u32 {
    let R = tool_params.diameter * 0.5;
    let FL = tool_params.flute_length;

    switch tool_params.tool_type {
        case TOOL_BALL: {
            return ray_ball_endmill(O_local, D_local, R, FL, out_intervals);
        }
        case TOOL_FLAT: {
            return ray_flat_endmill(O_local, D_local, R, FL, out_intervals);
        }
        case TOOL_BULLNOSE: {
            return ray_bullnose_endmill(O_local, D_local, R, tool_params.corner_radius, FL, out_intervals);
        }
        case TOOL_DRILL: {
            // Default tip angle: 118 degrees
            let tip_angle = 118.0 * 3.14159265359 / 180.0;
            return ray_drill(O_local, D_local, R, tip_angle, FL, out_intervals);
        }
        default: {
            // Fallback: treat as ball endmill
            return ray_ball_endmill(O_local, D_local, R, FL, out_intervals);
        }
    }
}


// =============================================================================
// INTERVAL SUBTRACTION — The Hot Path
//
// Python: tri_dexel.py:107 DexelColumn.subtract()
//
// Handles 5 overlap cases for each existing interval [a, b] vs removal [s, e]:
//   Case 1: s <= a && b <= e  -> interval fully inside removal -> delete
//   Case 2: a < s && e < b     -> removal inside interval    -> split [a,s], [e,b]
//   Case 3: s <= a && a < e <= b -> removal overlaps left   -> [e, b]
//   Case 4: a <= s < b && b <= e -> removal overlaps right  -> [a, s]
//   Case 5: b <= s || a >= e    -> disjoint                  -> keep as-is
//
// Expected: one column can generate at most N+1 surviving intervals from N inputs
//           (case 2 splits one interval into two)
// =============================================================================

/// Subtract tool intervals from a dexel column's existing intervals.
/// Returns the number of surviving intervals.
fn subtract_intervals(
    col_idx: u32,
    tool_intervals: array<vec2<f32>, MAX_TOOL_INTERVALS>,
    tool_iv_count: u32,
) -> u32 {
    if tool_iv_count == 0u {
        // No tool intersection -> column unchanged
        return columns[col_idx].interval_count;
    }

    let slot_start = col_idx * MAX_COLUMN_INTERVALS * 2u;
    let old_count = columns[col_idx].interval_count;

    if old_count == 0u {
        // Empty column -> nothing to subtract
        return 0u;
    }

    // Read existing intervals into thread-local storage
    var existing: array<vec2<f32>, MAX_COLUMN_INTERVALS>;
    for (var i: u32 = 0u; i < old_count && i < MAX_COLUMN_INTERVALS; i++) {
        let idx = slot_start + i * 2u;
        existing[i] = vec2<f32>(intervals[idx], intervals[idx + 1u]);
    }

    // Build surviving intervals
    var result: array<vec2<f32>, MAX_COLUMN_INTERVALS>;
    var result_count: u32 = 0u;

    // For each existing interval, subtract each tool interval from it
    // This handles the general case of multiple tool intervals
    for (var ei: u32 = 0u; ei < old_count && ei < MAX_COLUMN_INTERVALS; ei++) {
        var a = existing[ei].x;
        var b = existing[ei].y;
        var consumed: bool = false;

        for (var ti: u32 = 0u; ti < tool_iv_count; ti++) {
            let s = tool_intervals[ti].x;
            let e = tool_intervals[ti].y;

            // Degenerate/zero-length removal -> skip
            if e <= s + 1e-12 {
                continue;
            }

            // Case 5a: interval entirely before removal range
            if b <= s + 1e-12 {
                break; // keep as-is (handled below)
            }

            // Case 5b: interval entirely after removal range
            if a >= e - 1e-12 {
                break; // keep as-is
            }

            // Case 1: interval completely covered by removal
            if s <= a + 1e-12 && b <= e + 1e-12 {
                consumed = true;
                break; // interval deleted
            }

            // Case 2: removal lies wholly inside interval -> split
            if a < s - 1e-12 && e < b - 1e-12 {
                // Left piece [a, s]
                if result_count < MAX_COLUMN_INTERVALS && s > a + 1e-12 {
                    result[result_count] = vec2<f32>(a, s);
                    result_count += 1u;
                }
                // Right piece [e, b]
                if result_count < MAX_COLUMN_INTERVALS && b > e + 1e-12 {
                    result[result_count] = vec2<f32>(e, b);
                    result_count += 1u;
                }
                consumed = true;
                break;
            }

            // Case 3: removal overlaps left portion
            if s <= a + 1e-12 && a < e - 1e-12 && e < b - 1e-12 {
                a = e; // trim left, continue with remaining
                // Continue checking other tool intervals against trimmed [a, b]
            }

            // Case 4: removal overlaps right portion
            else if a < s - 1e-12 && s < b - 1e-12 && b <= e + 1e-12 {
                b = s; // trim right, continue
            }

            // After trimming, if interval is degenerate -> consumed
            if b <= a + 1e-12 {
                consumed = true;
                break;
            }
        }

        // If not consumed, write the (possibly trimmed) surviving interval
        if !consumed && b > a + 1e-12 && result_count < MAX_COLUMN_INTERVALS {
            result[result_count] = vec2<f32>(a, b);
            result_count += 1u;
        }
    }

    // Write surviving intervals back to the buffer
    for (var i: u32 = 0u; i < result_count; i++) {
        let idx = slot_start + i * 2u;
        intervals[idx]      = result[i].x;
        intervals[idx + 1u] = result[i].y;
    }

    // Update column metadata
    columns[col_idx].interval_count = result_count;

    return result_count;
}


// =============================================================================
// GRID -> WORLD COORDINATE HELPERS
// Python: tri_dexel.py DexelGrid.ray_origin() (line 433)
// =============================================================================

/// Compute the ray origin for column (col_idx) in world coordinates.
/// col_idx is a linearized index into the 2D grid.
/// Python: tri_dexel.py:433 DexelGrid.ray_origin
fn compute_ray_origin(col_idx: u32) -> vec3<f32> {
    let nu = grid_params.nu_cells;
    let nv = grid_params.nv_cells;
    let i = col_idx / nv;  // first orthogonal axis index
    let j = col_idx % nv;  // second orthogonal axis index
    let res = grid_params.resolution;

    let ox = grid_params.origin_x;
    let oy = grid_params.origin_y;
    let oz = grid_params.origin_z;

    // Axis-dependent mapping (Python: tri_dexel.py _AXIS_MAP)
    //
    //   Axis Z: nu=X(0), nv=Y(1), ray_dir=(0,0,1)
    //     ray_origin = (ox + i*res, oy + j*res, oz)
    //
    //   Axis X: nu=Y(1), nv=Z(2), ray_dir=(1,0,0)
    //     ray_origin = (ox, oy + i*res, oz + j*res)
    //
    //   Axis Y: nu=X(0), nv=Z(2), ray_dir=(0,1,0)
    //     ray_origin = (ox + i*res, oy, oz + j*res)
    //
    // Cell center offset: (i + 0.5)*res, (j + 0.5)*res

    let fi = f32(i) + 0.5;
    let fj = f32(j) + 0.5;

    switch grid_params.axis {
        case AXIS_Z: {
            return vec3<f32>(ox + fi * res, oy + fj * res, oz);
        }
        case AXIS_X: {
            return vec3<f32>(ox, oy + fi * res, oz + fj * res);
        }
        default: { // AXIS_Y
            return vec3<f32>(ox + fi * res, oy, oz + fj * res);
        }
    }
}

/// Get the ray direction for the current grid axis.
/// Python: tri_dexel.py DexelGrid.ray_direction() (line 445)
fn compute_ray_direction() -> vec3<f32> {
    switch grid_params.axis {
        case AXIS_Z: { return vec3<f32>(0.0, 0.0, 1.0); }
        case AXIS_X: { return vec3<f32>(1.0, 0.0, 0.0); }
        default:     { return vec3<f32>(0.0, 1.0, 0.0); }
    }
}


// =============================================================================
// MAIN COMPUTE ENTRY POINT
//
// One thread per affected dexel column.
// Python: material_removal.py:144 _remove_at_pose_on_grid
// =============================================================================

@compute @workgroup_size(64)
fn main(@builtin(global_invocation_id) gid: vec3<u32>) {
    let thread_idx = gid.x;

    // Bounds check: each thread processes one affected column
    let num_affected = arrayLength(&affected_cols);
    if thread_idx >= num_affected {
        return;
    }

    let col_idx = affected_cols[thread_idx];

    // --- 1. Compute ray origin and direction in world frame ---
    let ray_origin_world = compute_ray_origin(col_idx);
    let ray_dir_world = compute_ray_direction();

    // --- 2. Build inverse rotation matrix (world -> tool-local) ---
    let tool_pos = vec3<f32>(tool.tool_pos_x, tool.tool_pos_y, tool.tool_pos_z);
    let tool_dir = vec3<f32>(tool.tool_dir_x, tool.tool_dir_y, tool.tool_dir_z);

    // Normalize tool_dir
    let dir_len = length(tool_dir);
    let tool_dir_n = select(tool_dir / dir_len, vec3<f32>(0.0, 0.0, 1.0), dir_len < 1e-9);

    let R_tool_to_world = build_tool_to_world(tool_dir_n);
    // World -> Tool: inverse rotation = transpose (orthonormal)
    let R_world_to_tool = mat3_transpose(R_tool_to_world);

    // --- 3. Transform ray to tool-local coordinates ---
    // Python: swept_volume.py:53 world_to_tool, :70 direction_to_tool
    let O_local = world_to_tool(ray_origin_world, tool_pos, R_world_to_tool);
    let D_local = direction_to_tool(ray_dir_world, R_world_to_tool);

    // Normalize D_local (rotation preserves length, but guard against precision)
    let D_len = length(D_local);
    let D_local_n = select(D_local / D_len, D_local, D_len < 1e-9);

    if D_len < 1e-9 {
        return; // degenerate direction
    }

    // --- 4. Compute ray-tool intersection in tool-local space ---
    var tool_intervals: array<vec2<f32>, MAX_TOOL_INTERVALS>;
    let tool_count = compute_tool_intervals(O_local, D_local_n, tool, &tool_intervals);

    if tool_count == 0u {
        return; // ray misses the tool entirely
    }

    // --- 5. Subtract tool intervals from column ---
    // Distance values are invariant under rotation since |D_local| = |D_world| = 1.
    // So t_local == t_world (Python: swept_volume.py documentation lines 268-275).
    let new_count = subtract_intervals(col_idx, tool_intervals, tool_count);

    // --- 6. Update statistics ---
    if columns[col_idx].interval_count != new_count || new_count == 0u {
        atomicAdd(&cols_modified, 1u);
        // Approximate volume removed: count changed intervals
        atomicAdd(&total_removed, 1u);
    }
}
