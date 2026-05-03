# Tri-Dexel 5-Axis CNC Simulation Core -- Design Document

## 1. Algorithm Choice: Why Tri-Dexel

The core question for any material removal simulator is: **how do you represent the workpiece in memory such that subtracting a moving tool is fast, accurate, and handles arbitrary tool orientations?**

### Tradeoff Table

| Representation | Memory | Speed (single op) | Accuracy | 5-Axis Capability | Implementation Complexity |
|---|---|---|---|---|---|
| Uniform Voxel (3D grid) | O(n^3) | O(affected cells) -- fast | Resolution-limited (staircase) | Rotation requires resampling | Low |
| Octree (sparse voxel) | O(surface area) ~ n^2 | O(log n) per cell lookup | Adaptive resolution | Rotation requires resampling | Medium |
| BREP (exact geometry) | O(number of faces) | Slow -- boolean ops are O(n^3) on BREP | Exact (within float) | Full | Very High (needs kernel like OpenCASCADE) |
| Analytic Swept Volume | O(1) formula per move | Instant (formula eval) | Exact | Constrained to simple paths | Extreme (unsolved problem for general 5-axis) |
| **Tri-Dexel** | O(3 * nx * ny * avg_intervals) | Fast batch ray subtraction | Sub-resolution (interval endpoints are float) | Natural -- any ray direction supported | Medium-High |

### Why Tri-Dexel Wins for 5-Axis Simulation

1. **Direction-independent subtraction**: A single dexel grid along Z works well for 3-axis (tool axis is always Z). For 5-axis, the tool can approach from any direction. A different ray direction is needed for each tool orientation. **Three orthogonal dexel grids** cover all directions without resampling.

2. **Algebraic operations on intervals**: Subtraction, union, and intersection on sorted interval lists are O(n) operations. No mesh intersection, no BREP boolean kernel, no voxel resampling.

3. **Memory proportional to surface area**: A uniform voxel grid stores O(n^3) cells. Tri-dexel stores intervals only along rays that intersect the workpiece -- approximately O(3 * n^2 * k) where k is the average number of intervals per column. For a solid block, k=1 (one continuous interval); for complex geometry, k is proportional to feature count.

4. **Float-precision endpoints**: Interval [start, end] uses float64. This is NOT limited to grid resolution -- it is sub-resolution accurate. The grid spacing determines which rays are cast, but the start/end of each interval along that ray is float-precise.

5. **Published algorithm**: The tri-dexel approach is published in academic literature and used in commercial systems (Vericut uses a related dexel approach for its speed).

### Limitations (Honest Assessment)

- **Curved surface approximation**: Surfaces not aligned with dexel directions are staircase-approximated at the dexel spacing. At 0.1mm resolution, this is machining-tolerance-acceptable.
- **Memory for very large parts**: A 500mm^3 part at 0.1mm requires 3 * 5000^2 = 75M dexels, or ~600MB. Acceptable for modern workstations.
- **Not a replacement for BREP verification**: For final gauge R&R verification (micron-level), a BREP boolean is still needed.

---

## 2. Data Structure Design

### DexelInterval

```python
@dataclass(slots=True)
class DexelInterval:
    start: float   # Distance from ray origin to entry point
    end: float     # Distance from ray origin to exit point
    material_id: int = 0  # Reserved for multi-material support
```

Frozen once created. `slots=True` avoids dict overhead -- important when millions of these exist.

### DexelColumn

A **sorted, non-overlapping** list of `DexelInterval` objects. The sorting and non-overlap invariants are enforced on every mutation.

```python
class DexelColumn:
    _intervals: list[DexelInterval]
```

**Key operations** (all O(n) where n = interval count in column):

- `subtract(sub_start, sub_end)`: Remove material from [sub_start, sub_end]. Splits any interval that overlaps the subtraction range.
- `union(other)`: Merge two columns, combining overlapping intervals.
- `intersect(start, end)`: Extract only intervals within [start, end].
- `material_volume()`: Sum of (end - start) for all intervals.

**Memory layout**: The column stores a Python `list` of `DexelInterval` objects. For GPU-friendliness, we also support a "flat" representation:

```python
def to_flat(self) -> np.ndarray:
    """Return (N,2) float64 array of [start, end] pairs for batch ops."""
    return np.array([[i.start, i.end] for i in self._intervals], dtype=np.float64)
```

### DexelGrid

A 2D array of `DexelColumn` objects representing rays cast along one axis direction through a grid in the plane of the other two axes.

```
DexelGrid with axis='Z':
  - Grid plane: XY
  - Each cell [i][j] is a DexelColumn of intervals along Z
  - i indexes X position, j indexes Y position
  - Ray for cell [i][j] originates at (origin_x + i*res, origin_y + j*res, 0)
    and points in the +Z direction
```

```python
class DexelGrid:
    axis: str                          # 'x', 'y', or 'z' (dexel ray direction)
    origin: tuple[float, float, float] # Workspace origin of the grid
    resolution: float                  # Grid spacing in mm
    nu_cells: int                      # Number of cells in the first orthogonal axis
    nv_cells: int                      # Number of cells in the second orthogonal axis
    _columns: list[list[DexelColumn]]  # [nu][nv] array
```

**Axis mapping convention:**

| Grid | Ray Direction | Grid Plane | nu (first index) maps to | nv (second index) maps to |
|---|---|---|---|---|
| `axis='z'` | +Z | XY | X (columns) | Y (rows) |
| `axis='x'` | +X | YZ | Y (columns) | Z (rows) |
| `axis='y'` | +Y | XZ | X (columns) | Z (rows) |

**Initialization from mesh**:
```python
def init_from_mesh(self, mesh: trimesh.Trimesh) -> None:
    """Cast rays through the mesh to populate dexel columns.
    Uses trimesh.ray.intersects_location for ray-mesh intersection.
    Each ray produces a sorted list of (entry, exit) distance pairs.
    """
```

### TriDexelModel

Three orthogonal `DexelGrid` instances representing the same workpiece:

```python
class TriDexelModel:
    dexel_z: DexelGrid  # Rays along Z, grid in XY
    dexel_x: DexelGrid  # Rays along X, grid in YZ
    dexel_y: DexelGrid  # Rays along Y, grid in XZ
    bounds: AABB         # Bounding box of the workpiece
    resolution: float    # Grid resolution (same for all three grids)
```

**Why three grids?** A single dexel grid represents surfaces well when the surface normal has a positive dot product with the dexel direction. When the surface is nearly parallel to the dexel direction, it is poorly represented (rays graze the surface). Three orthogonal grids ensure that for any surface orientation, at least one grid has rays nearly perpendicular to it.

### Resolution Choice

- **Default**: 0.1mm (acceptable for roughing/finishing simulation)
- **Fine**: 0.05mm (precision finishing, tight tolerance features)
- **Coarse**: 0.5mm (rapid roughing overview, RL training)

The resolution translates directly to:
- Number of cells per grid: `(part_size / resolution)^2`
- Memory: `3 * n_cells * avg_intervals_per_column * sizeof(interval)`

For a 200mm^3 stock at 0.1mm: 3 * (2000)^2 * 1.5 * 16 bytes ~= 288MB (typical)

---

## 3. Interval Arithmetic Specification

This is the **hot path** of the entire system. Every material removal operation calls `DexelColumn.subtract()`. It must be correct and fast.

### Union Algorithm

Combine two sorted interval lists into one non-overlapping sorted list.

```
Input:  A = [[a0_start, a0_end], [a1_start, a1_end], ...]  (sorted, non-overlapping)
        B = [[b0_start, b0_end], [b1_start, b1_end], ...]  (sorted, non-overlapping)
Output: C = sorted, non-overlapping merged intervals

Algorithm:
1. Merge A and B by start value (like merge-sort merge step)
2. While merging, if current.start <= last.end, extend last.end = max(last.end, current.end)
3. Else append current as new interval
Complexity: O(n + m)
```

### Subtraction Algorithm (THE HOT PATH)

```
Input:  column = [[c0_start, c0_end], ...]  (sorted intervals of existing material)
        sub_start, sub_end                   (interval to remove)
Output: column is mutated in-place

Algorithm:
For each interval [c_start, c_end] in column:
    Case 1: sub completely covers interval     → remove interval entirely
        [ sub_start ... [c_start..c_end] ... sub_end ]  → delete
        
    Case 2: sub is completely inside interval  → split into two
        [ c_start ... [sub_start..sub_end] ... c_end ]  → [c_start, sub_start], [sub_end, c_end]
        
    Case 3: sub overlaps left side of interval → trim left
        [ sub_start ... [c_start ... sub_end] ... c_end ] → [sub_end, c_end]
        
    Case 4: sub overlaps right side of interval → trim right
        [ c_start ... [sub_start ... c_end] ... sub_end ] → [c_start, sub_start]
        
    Case 5: sub and interval are disjoint       → keep interval unchanged
        sub completely before: sub_end < c_start
        sub completely after:  sub_start > c_end

Optimization: Early exit when sub_end < first_interval[0].start (sub is before all material)
Complexity: O(n) single pass, in-place mutation with minimal allocation
```

**Performance notes for the hot path:**
- Use `list` operations (append, pop, slice assignment). Avoid `del column[i]` in the middle of a list -- it is O(n). Instead, build a new list of surviving intervals.
- Pre-allocate result list with capacity = len(column) + 1 (in case of split).
- In the common case (tool removes material from the top), the subtraction range covers the tail of the column and we can early-exit.

### Intersection Algorithm

```
Input:  column as sorted intervals, query range [q_start, q_end]
Output: list of intervals within query range, clipped to [q_start, q_end]

Algorithm:
For each interval in column:
    if interval.end < q_start: continue
    if interval.start > q_end: break  (sorted, so all subsequent are past range)
    result.append([max(interval.start, q_start), min(interval.end, q_end)])
Complexity: O(n)
```

### Batch Subtraction (Numpy Vectorization)

For bulk operations (e.g., subtracting the same tool shape from 1000 columns):

```python
def batch_subtract(columns_flat: list[np.ndarray], sub_start: np.ndarray, sub_end: np.ndarray) -> list[np.ndarray]:
    """
    columns_flat: list of (N_i, 2) arrays of interval pairs
    sub_start, sub_end: (K,) arrays of subtraction ranges (one per column)
    
    Uses numpy boolean indexing:
    - For each column, compute which intervals overlap the subtraction range
    - Apply the 5 cases above using array operations
    - Reconstruct each column from surviving interval fragments
    """
```

This is the path that gets accelerated by CuPy later -- the numpy operations map directly to CUDA kernels.

---

## 4. Tool Model

### APT Standard 7-Parameter Tool Definition

APT (Automatically Programmed Tools, ANSI/ISO 4343) defines cutting tools by 7 geometric parameters:

```
Parameter | Symbol | Description
----------|--------|-------------
Diameter  | D      | Cutting diameter (mm)
Corner radius | R  | Radius at the corner between side and bottom (mm)
Length    | L      | Total tool length (mm)
Flute length | FL   | Length of the cutting portion (mm)
Taper angle | A    | Side taper angle (degrees, 0 = straight)
Tip angle | B      | Bottom angle (degrees, 0 = flat, 180 = full radius)
Tip diameter | d    | Diameter at the tip (for drills, chamfers)
```

### Supported Tool Types

#### Flat Endmill (flat_endmill)
```
Shape: Cylinder of diameter D + flat bottom disc
D > 0, R = 0, A = 0, B = 0
```
- **Cylinder**: Infinite cylinder of radius D/2 from z=0 to z=FL (oriented along tool axis, tip at origin)
- **Bottom disc**: Circle of radius D/2 at z=0
- Ray-cylinder intersection: `|(P - O) - ((P - O).d)*d| = R` where d is cylinder axis direction
  - Quadratic: `|dir_perp|^2 * t^2 + 2*(dir_perp . (O - C_perp))*t + |(O - C_perp)|^2 - R^2 = 0`
  - Only keep solutions where the intersection point is within [0, FL]
- Ray-disc intersection: Ray-plane intersection at z=0, then check if point is within radius D/2

#### Ball Endmill (ball_endmill)
```
Shape: Cylinder of diameter D + hemisphere of radius D/2 at tip
D > 0, R = D/2, A = 0, B = 90
```
- **Cylinder**: Same as flat endmill (above the hemisphere)
- **Hemisphere**: Sphere of radius D/2 centered at (0,0,D/2) from tip
  - Ray-sphere: `|O + t*dir - C|^2 = R^2`
  - Quadratic: `|dir|^2 * t^2 + 2*dir.(O-C)*t + |O-C|^2 - R^2 = 0`
  - Keep solutions where z <= 0 (tip = hemisphere, material is below the sphere equator)
- The union of cylinder and hemisphere intervals gives the full tool intersection

#### Bull Nose Endmill (bull_nose)
```
Shape: Cylinder of diameter D + torus at corner
D > 0, 0 < R < D/2, A = 0, B = 0
```
- **Cylinder**: Radius D/2 for the main body
- **Flat bottom**: Radius (D/2 - R) for the flat portion
- **Torus corner**: Major radius = R, minor radius = (D/2 - R), centered at corner
  - Ray-torus intersection: 4th-degree polynomial (quartic)
  - Approximate: Sample the torus as many small sphere segments and union their results
  - More precisely: Solve the quartic using numpy roots for each ray (computationally expensive, use bounding box cull first)

#### Drill
```
Shape: Cone (tip angle B) + cylinder of diameter D
D > 0, A = 0, B = 118 (typical), d = 0
```
- **Cylinder**: Same as endmill cylinder
- **Cone**: From tip (0,0,0) to height where cone diameter = D
  - Cone angle: tan(B/2) = D/(2*h_cone), so h_cone = D/(2*tan(B/2))
  - Ray-cone: Quadratic equation in t
  - Cone apex at (0,0,0), half-angle = B/2
  - Check: intersection point z-coordinate is within [0, h_cone] and distance from axis <= D/2 at that z

#### Chamfer Tool
```
Shape: Truncated cone (chamfer angle A)
D > 0, A = chamfer angle, d = tip diameter
```
- **Truncated cone**: Radius varies linearly from d/2 at z=0 to D/2 at z=h
  - Ray-cone intersection with truncation planes at z=0 and z=h
  - Same quadratic as cone, plus plane clipping

#### Thread Mill
```
Shape: Cylinder with thread profile ridges
```
- Approximate as cylinder for material removal (thread form is too fine for dexel resolution)
- Thread validation is done in Tier 1 rules, not geometry simulation

#### Dovetail Cutter
```
Shape: Reverse taper (diameter increases with depth)
A = negative taper (typically 45-60 degrees)
```
- **Reverse taper cone**: Radius = r_base + z*tan(A) where A is the dovetail angle from vertical
- Ray-cone intersection with opposite sign

### Ray-Tool Intersection -- General Approach

All tool types share the same interface:

```python
class Tool(ABC):
    diameter: float
    length: float
    
    @abstractmethod
    def ray_intersection(self, ray_origin: np.ndarray, ray_direction: np.ndarray) -> DexelColumn:
        """
        Compute intersection intervals of this tool with a ray.
        
        The tool is positioned with its tip at origin, oriented along +Z (tool axis).
        The ray is transformed into the tool's local coordinate system before calling.
        
        Args:
            ray_origin: (3,) float array, origin of the ray in tool-local coordinates
            ray_direction: (3,) float array, direction of the ray (normalized)
            
        Returns:
            DexelColumn with sorted intervals where the ray enters and exits the tool volume
        """
```

**Implementation for ball endmill** (most common in 5-axis):

```python
def ray_intersection(self, ray_origin, ray_direction):
    intervals = []
    
    # 1. Ray-cylinder intersection (tool body)
    # Cylinder axis = +Z, centered at (0,0), radius = D/2
    # Length from z = D/2 to z = FL (the cylinder starts at the hemisphere equator)
    cylinder_hits = self._ray_cylinder_intersect(ray_origin, ray_direction, 
                                                   radius=D/2, 
                                                   z_min=D/2, z_max=self.length)
    intervals.extend(cylinder_hits)
    
    # 2. Ray-sphere intersection (hemisphere tip)
    # Sphere center at (0, 0, D/2), radius = D/2
    # Only keep points where z <= D/2 (below equator = tip hemisphere)
    sphere_hits = self._ray_sphere_intersect(ray_origin, ray_direction,
                                              center=(0, 0, D/2), radius=D/2,
                                              z_max=D/2)
    intervals.extend(sphere_hits)
    
    # 3. Merge and sort
    return DexelColumn.from_intervals(intervals).sort_and_merge()
```

### Swept Volume Bounding Box

```python
def swept_volume_bbox(self, start_pose: ToolPose, end_pose: ToolPose) -> AABB:
    """Bounding box of the volume swept by the tool moving from start to end pose.
    
    Expands the tool's bounding box at each pose and takes the convex hull of the two.
    For 5-axis, adds the maximal swept arc (the tool tip traces an arc in space).
    """
```

---

## 5. Material Removal Algorithm

### Core Algorithm

For each tool position and orientation:

```
Algorithm: remove_tool_at_pose(tool, pose)
1. For each dexel grid (Z, X, Y):
   a. Transform tool into the grid's local coordinate system
      - Tool is defined in its own frame: tip at origin, axis along +Z_local
      - Transform = pose.inverse() * grid.transform
   b. Compute affected column range:
      - Project tool bounding box onto the grid plane (XY for Z-grid, etc.)
      - Compute [i_min, i_max] and [j_min, j_max] in grid coordinates
      - This is the bounding box cull -- we skip most columns
   c. For each affected column (i, j):
      - Get the ray for this column: ray_origin = grid origin + (i*res, j*res, 0)
      - Transform ray into tool-local frame: ray_local = tool_transform * ray
      - Compute tool.ray_intersection(ray_local.origin, ray_local.direction)
      - Transform intersection distances back to grid-space distances
      - Call column.subtract(entry_dist, exit_dist)
2. Return RemovalResult(count_columns_modified, total_volume_removed)
```

### 5-Axis Swept Volume

For a tool moving from pose A to pose B in a 5-axis movement:

```
Algorithm: remove_tool_swept(tool, start_pose, end_pose)
1. Compute number of samples:
   - Translational component: arc_length / resolution (at least 2)
   - Rotational component: max angular change / angular_resolution (e.g., 5 degrees)
   - n_samples = max(translational_samples, rotational_samples, 2)
   
2. Sample intermediate poses:
   - Translation: linear interpolation in workpiece frame
   - Rotation: SLERP (spherical linear interpolation) for quaternion rotation
   - For each sample i: pose_i = interpolate(start, end, i/(n-1))
   
3. For each dexel grid, compute union of affected column ranges across all samples
   (This is the swept volume bounding box cull -- skip columns definitely not touched)

4. For each affected column:
   a. For each sample pose:
      - Compute ray-tool intersection at that pose
      - Add intervals to a running union
   b. Subtract the union of all intervals from the column
   
5. Return RemovalResult with aggregate statistics
```

**Sample count formula:**

```python
def n_samples_for_move(start_pose, end_pose, resolution=0.1, angular_resolution=np.radians(5)):
    translational_dist = np.linalg.norm(end_pose.position - start_pose.position)
    angular_dist = quaternion_angular_distance(start_pose.orientation, end_pose.orientation)
    
    n_trans = max(int(translational_dist / resolution) + 2, 2)
    n_angular = max(int(angular_dist / angular_resolution) + 2, 2)
    
    return max(n_trans, n_angular)
```

**Error bound**: The swept volume sampling error is bounded by the resolution parameter. A tool moving 1mm at 0.1mm sampling has at most 0.1mm of unsampled volume at the midpoint. For 5-axis rotation, 5-degree angular steps keep the swept arc within the resolution tolerance.

### Three-Grid Consistency

After material removal, all three dexel grids are updated independently. They may have slight inconsistencies (a column in one grid might show a tiny material sliver that the other grids disagree on). This is acceptable because:

1. The surface extraction step reconciles all three grids.
2. Deviations are bounded by the grid resolution.
3. Conservative approach: when in doubt, material is present (avoid false gouge detection).

---

## 6. 5-Axis Kinematics

### Transformation Chain Model

A 5-axis machine is modeled as a chain of rigid transformations. The tool tip position in world coordinates is:

```
T_tool_world = T_machine * T_rotary_primary(angle1) * T_rotary_secondary(angle2) * T_linear(X,Y,Z) * T_tool_offset
```

where `T_machine` is the fixed machine frame to world transformation.

### Machine Configurations

#### TABLE_TABLE (e.g., BC trunnion table)

Both rotary axes are on the table side. The part rotates; the tool is fixed in orientation.

```
Chain: world → table_base → B_axis(rotate about Y) → C_axis(rotate about rotated Z) → part
       world → machine_column → Z_axis → Y_axis → X_axis → spindle → tool
```

**Forward kinematics** (BC trunnion):
```
Given joints [X, Y, Z, B, C] in machine coordinates:
1. Part orientation: R_part = R_y(B) * R_z(C)   (B rotates about machine Y, C about part Z)
2. Tool tip position in part frame:
   P_tool_in_part = R_part.T * (P_spindle(X,Y,Z) - P_part_zero)
   
Where P_spindle(X,Y,Z) = [X, Y, Z] is the linear axis position
and P_part_zero is the machine zero of the rotary table center

Tool orientation in part frame:
   O_tool_in_part = R_part.T * [0, 0, 1]   (tool axis is always machine Z for table-table)
```

**Inverse kinematics** (BC trunnion):
```
Given desired tool position P_wp and orientation O_wp in workpiece frame:

Tool axis direction in machine frame: O_machine = [Ox_m, Oy_m, Oz_m]
From O_machine, compute B and C:
   B = -arcsin(Ox_m)       (B rotates about Y, affects X component)
   C = atan2(Oy_m, Oz_m)   (C rotates about Z)

Alternative solution: B' = pi - B, C' = C + pi

Tool position inverse:
   R_machine = Ry(B) * Rz(C)
   P_spindle = R_machine * P_wp + P_table_center
   X = P_spindle[0], Y = P_spindle[1], Z = P_spindle[2]
```

**Singularity at B=0**: When B=0, the C axis rotation does not change the tool orientation (both rotate the tool axis around itself). C becomes undefined. Solution: use the previous C value (or a preferred configuration), and handle with small epsilon for near-singularity.

#### HEAD_HEAD (both rotary axes in spindle head)

```
Chain: world → machine → linear axes → A_axis(tilt) → B_axis(pan) → spindle → tool
       world → part (fixed)
```

The tool orientation changes but the part is fixed. This is simpler for inverse kinematics but the machine head is heavier and less rigid.

#### HEAD_TABLE (one in head, one on table)

```
Chain: world → table → C_axis(rotate) → part
       world → machine → linear → B_axis(tilt) → spindle → tool
```

Common configuration: B on head (tilting spindle), C on table (rotary table).

### Forward Kinematics (unified)

```python
def forward(self, joints: np.ndarray) -> ToolPose:
    """
    joint vector = [X, Y, Z, A, B, C] in machine coordinates (mm, degrees)
    Returns tool tip position and orientation in the workpiece frame.
    
    For table-table: [X,Y,Z] position the tool tip relative to table center.
                     [A,B,C] are rotary table angles (A about X, B about Y, C about Z).
                     Only 2 of [A,B,C] are used depending on machine config.
    """
```

### Inverse Kinematics (unified, closed-form)

```python
def inverse(self, pose: ToolPose) -> Optional[np.ndarray]:
    """
    Given desired tool pose in workpiece frame, compute joint values.
    Returns None if pose is unreachable (outside machine envelope or limit violation).
    
    For table-table BC:
    1. Extract tool axis direction from pose orientation
    2. Compute B = -arcsin(tool_axis.x), C = atan2(tool_axis.y, tool_axis.z)
    3. Check both B solutions (B and pi-B) and pick within limits
    4. Compute [X,Y,Z] from rotation and translation equations
    
    For head-head:
    1. Tool axis = pose.orientation * [0,0,1]
    2. A = atan2(tool_axis.y, tool_axis.z) or similar mapping
    3. Solve for linear axes
    """
```

### Singularity Handling

At B=0 (table-table) or A=0 (head-head), one rotary axis loses meaning because the two rotary axes are aligned. The inverse kinematics has infinite solutions.

```python
def handle_singularity(self, pose: ToolPose, prev_joints: Optional[np.ndarray] = None) -> np.ndarray:
    """
    When near a singularity (e.g., |B| < 1e-6 degrees for table-table):
    1. If prev_joints is available, use the previous C value
    2. If no previous, use C = 0 as preferred solution
    3. The positional axes are unaffected by the singularity
    4. For small B, apply a minimum B to stay out of exact singularity
    """
```

### Axis Limit Validation

```python
def check_limits(self, joints: np.ndarray) -> bool:
    """Verify all joint values are within machine limits."""
    
AXIS_LIMITS = {
    "X": (-500, 500),    # mm
    "Y": (-300, 300),
    "Z": (-400, 0),      # Z is typically negative (toward table)
    "A": (-120, 120),    # degrees
    "B": (-120, 120),
    "C": (0, 360),       # or continuous
}
```

---

## 7. Surface Extraction

### Modified Marching Cubes for Tri-Dexel

Standard marching cubes operates on a 3D scalar field (e.g., voxel grid of signed distance values). For tri-dexel, we have three 2D grids of intervals -- not a scalar field. The approach:

#### Step 1: Extract Surface Points from Each Grid

For each dexel grid, material transitions (present-to-absent or absent-to-present) define surface points:

```
For each column:
    For each interval in column:
        Entry point: (grid coord, interval.start along ray) → 3D point, normal points inward
        Exit point:  (grid coord, interval.end along ray) → 3D point, normal points outward
        
For axis='Z' grid: 
    Point = (x_origin + i*res, y_origin + j*res, z_origin + interval.start/end)
    Normal = (0, 0, ±1)  (approximate -- ray is along Z)
```

This gives us three point clouds with approximated normals:
- Z-dexel surface points: normals roughly aligned with ±Z
- X-dexel surface points: normals roughly aligned with ±X
- Y-dexel surface points: normals roughly aligned with ±Y

#### Step 2: Merge and Filter

Merge all surface points from all three grids. For points close together (within resolution), keep the one with the highest-quality normal (i.e., the one whose dexel direction is closest to the surface normal).

**Normal quality heuristic**: A dexel ray gives a good surface estimate when the surface normal is nearly parallel to the ray direction. The entry/exit distance is accurately captured. When the surface is nearly perpendicular to the ray direction, the dexel doesn't see it well. For each surface point, compute how grazing the surface is to its dexel direction:

```
quality = |surface_normal . dexel_direction|  (1.0 = perfect, 0.0 = grazing)
```

Keep the point with the highest quality from any grid.

#### Step 3: Triangulation

Option A (fast): **Ball-pivoting or Poisson reconstruction** on the merged point cloud.
Option B (more accurate): **Running marching cubes on a derived signed distance field**.

For Option B:
1. From the merged point cloud, estimate signed distances at each point (using normals)
2. Interpolate onto a regular 3D grid at resolution/2
3. Run standard marching cubes on this grid
4. The result is a triangulated mesh

#### Step 4: Mesh Post-Processing

- Remove degenerate triangles (zero area)
- Fix non-manifold edges
- Optional: Laplacian smoothing (1-2 iterations) to reduce staircase artifacts

### Deviation Mapping

```python
def compare_to_target(simulated: TriDexelModel, target_mesh: trimesh.Trimesh) -> np.ndarray:
    """
    For each vertex of the target mesh:
    - Ray-cast through the simulated tri-dexel model
    - Compute signed distance: positive = uncut material remains, negative = gouge
    
    Returns (N,) array of signed distances in mm.
    """
```

### Gouge Detection

A gouge is detected when material was removed below the target surface:

```python
def detect_gouges(tri_dexel: TriDexelModel, target_mesh: trimesh.Trimesh, 
                  tolerance: float = 0.01) -> list[Gouge]:
    """
    Sample the target surface at resolution spacing.
    For each sample point:
    - Check if material exists at that point in tri_dexel
    - If no material found where target expects it → potential gouge
    - Verify by checking if the point is below the target surface
    
    Returns list of Gouge(position, depth, severity).
    """
```

---

## 8. Performance Targets

### Target Metrics

| Operation | 3-Axis | 5-Axis | Resolution | Part Size |
|---|---|---|---|---|
| Single tool pose subtraction | <50ms | <200ms | 0.1mm | 200mm^3 |
| Swept volume (10-sample move) | <100ms | <500ms | 0.1mm | 200mm^3 |
| Surface extraction (to mesh) | <2s | <2s | 0.1mm | 200mm^3 |
| Deviation mapping | <500ms | <500ms | 0.1mm | 200mm^3 |
| Full G-code simulation (100 ops) | <30s | <2min | 0.1mm | 200mm^3 |

### Profiling Hot Paths

The hot paths, in order of optimization priority:

1. **`DexelColumn.subtract()`** -- called for every affected column for every tool pose. Must be O(n) with minimal allocation.
2. **`Tool.ray_intersection()`** -- called for every affected column. Quadratic equation solves are fast but the per-column overhead matters.
3. **`DexelGrid.affected_columns()`** -- bounding box cull. Must be fast (integer arithmetic only).
4. **Swept volume sampling** -- number of samples directly multiplies the workload.

### GPU Acceleration Plan

**Phase 1 (current): Numpy vectorization**
- Batch tool-ray intersection using numpy array operations
- Batch interval subtraction using boolean indexing
- Pre-allocate arrays to avoid GC pressure

**Phase 2: CuPy drop-in**
- Replace `import numpy as np` with `import cupy as np` for GPU arrays
- Numpy's array API is directly compatible -- minimal code changes
- Expected speedup: 10-50x for batch operations (latency-bound per operation, but throughput scales)
- Limitation: PCIe transfer of large arrays between CPU and GPU adds latency

**Phase 3: Numba CUDA kernels**
- Write custom CUDA kernels for the interval subtraction hot path
- One CUDA thread per dexel column
- No Python overhead in the inner loop
- Expected: 50-200x over CPU for large batches

### Memory Budget

| Component | Formula | Example (200mm^3 at 0.1mm) |
|---|---|---|
| DexelGrid Z | (Lx/res + 1) * (Ly/res + 1) * 32 bytes | 2000 * 2000 * 32 = 128MB |
| DexelGrid X | (Ly/res + 1) * (Lz/res + 1) * 32 bytes | 128MB |
| DexelGrid Y | (Lx/res + 1) * (Lz/res + 1) * 32 bytes | 128MB |
| **Total** | | **~384MB** |

Column overhead assumes `DexelColumn` with average 1.5 intervals per column and 32 bytes per interval (two float64 values + material_id integer + overhead).

For 0.05mm resolution, quadruple the memory (~1.5GB). For 0.5mm resolution, 1/25th (~15MB).

---

## 9. Phase Roadmap

### Phase 1 (this phase): Folder Structure, Plan & Design Decisions
- Create directory structure under `src/simulation/`
- Write this design document
- Dependencies: none
- Test criteria: Document reviewed, all design decisions justified

### Phase 2: Core Data Structures
- Implement `tri_dexel.py`: DexelInterval, DexelColumn, DexelGrid, TriDexelModel
- Implement `tools.py`: APT standard tools with ray-tool intersection
- Dependencies: numpy, trimesh (for mesh import)
- Test criteria:
  - DexelColumn.subtract() produces correct intervals for all 5 cases
  - TriDexelModel.from_mesh() correctly voxelizes a sphere (check volume error < 5% at 0.1mm)
  - BallEndmill.ray_intersection() intersects a known ray within 1e-6
  - Each file has `if __name__ == "__main__":` with runnable self-test

### Phase 3: Material Removal Engine
- Implement `swept_volume.py`: swept volume sampling + bounding box computation
- Implement `material_removal.py`: MaterialRemovalEngine with pose and swept removal
- Dependencies: Phase 2
- Test criteria:
  - Remove a ball endmill at a known pose from a rectangular stock → correct cutout shape
  - Swept volume removal along a linear move → continuous slot
  - Volume conservation: volume_removed ≤ tool_volume * (1 + epsilon)
  - Performance: <50ms for single 3-axis pose subtraction

### Phase 4: 5-Axis Kinematics
- Implement `kinematics.py`: FiveAxisKinematics with all configs
- Dependencies: Phase 2 (ToolPose)
- Test criteria:
  - Forward kinematics for table-table BC: known joint angles → expected tool pose
  - Inverse kinematics: forward(inverse(pose)) == pose within 1e-6
  - Singularity handling: near B=0, returns valid solution
  - Axis limit check correctly rejects out-of-bounds positions

### Phase 5: Surface Extraction
- Implement `surface.py`: tri-dexel to mesh conversion, deviation mapping
- Implement `simulator.py`: FiveAxisSimulator orchestrator
- Dependencies: Phase 2, 3, 4
- Test criteria:
  - Simulated sphere: extracted mesh volume matches expected within 5%
  - Deviation map on a simulated pocket: detects uncut corners
  - Full G-code simulation of simple 3-axis program produces expected mesh

### Phase 6: Visualization & Validation
- Implement `visualizer.py`: 3D rendering of tri-dexel state, deviations, gouges
- Implement `validator.py`: comprehensive gouge/collision/constraint checking
- Dependencies: Phase 5
- Test criteria:
  - Visualizer renders stock + tool + deviation heatmap
  - Validator catches gouge, collision, over-travel scenarios

### Future Phases (beyond initial scope)
- CuPy/Numba GPU acceleration
- Real G-code parser integration (gcodeparser)
- Machine-specific kinematics library (Haas, DMG Mori, Hurco)
- BREP boolean verification pass (via pythonOCC)
- Multi-material support (material_id in DexelInterval)
- Tool wear model integration
- Cutting force estimation from engagement angle analysis

---

## Appendix A: Key Mathematical Formulas

### Ray-Cylinder Intersection

Cylinder of radius R along axis direction d (normalized), passing through point C on the axis.
Ray: O + t * dir (|dir| = 1).

Let w = O - C
Let w_perp = w - (w . d) * d       (component of w perpendicular to cylinder axis)
Let dir_perp = dir - (dir . d) * d  (component of ray direction perpendicular to cylinder axis)

Quadratic: a*t^2 + 2*b*t + c = 0
where:
  a = |dir_perp|^2
  b = dir_perp . w_perp
  c = |w_perp|^2 - R^2

Discriminant: delta = b^2 - a*c
If delta < 0: no intersection
If delta >= 0: t = (-b ± sqrt(delta)) / a

For finite cylinder: filter t values where the intersection point's projection onto the axis
is within [0, h] (or [z_min, z_max] in tool coordinates).

### Ray-Sphere Intersection

Sphere: center C, radius R.
Ray: O + t * dir.

Let w = O - C
Quadratic: a*t^2 + 2*b*t + c = 0
where:
  a = |dir|^2 = 1 (if dir is normalized)
  b = dir . w
  c = |w|^2 - R^2

Discriminant: delta = b^2 - a*c
If delta < 0: no intersection
t = (-b ± sqrt(delta)) / a

### Quaternion SLERP (for 5-axis tool pose interpolation)

```python
def slerp(q1: np.ndarray, q2: np.ndarray, t: float) -> np.ndarray:
    """Spherical linear interpolation between two quaternions."""
    dot = np.clip(np.dot(q1, q2), -1.0, 1.0)
    if dot < 0:
        q2 = -q2
        dot = -dot
    if dot > 0.9995:
        # Near-parallel: use linear interpolation
        result = q1 + t * (q2 - q1)
        return result / np.linalg.norm(result)
    theta_0 = np.arccos(dot)
    sin_theta_0 = np.sin(theta_0)
    theta = theta_0 * t
    sin_theta = np.sin(theta)
    s0 = np.cos(theta) - dot * sin_theta / sin_theta_0
    s1 = sin_theta / sin_theta_0
    return s0 * q1 + s1 * q2
```

### Quaternion Angular Distance

```python
def quaternion_angular_distance(q1, q2):
    """Angular distance between two quaternions in radians."""
    dot = np.abs(np.dot(q1, q2))
    dot = np.clip(dot, -1.0, 1.0)
    return 2 * np.arccos(dot)
```

## Appendix B: API Reference (Planned)

### TriDexelModel

```python
@classmethod
def from_mesh(cls, mesh: trimesh.Trimesh, resolution: float = 0.1) -> TriDexelModel

def to_mesh(self) -> trimesh.Trimesh

def get_material_at(self, point: np.ndarray) -> bool
    """Test if a 3D point contains material. Checks all three grids (consensus: 2/3)."""

def volume(self) -> float
    """Total material volume from all three dexel grids (averaged)."""
```

### FiveAxisSimulator

```python
class FiveAxisSimulator:
    def __init__(self, stock_mesh: trimesh.Trimesh, target_mesh: trimesh.Trimesh,
                 machine_config: MachineConfig, resolution: float = 0.1)
    
    def load_tool(self, tool: Tool) -> None
    
    def execute_gcode(self, gcode: str) -> SimulationResult
    
    def execute_move(self, start_pose: ToolPose, end_pose: ToolPose, 
                     tool: Tool) -> MoveResult
    
    @property
    def current_stock_mesh(self) -> trimesh.Trimesh
    
    @property
    def deviation_map(self) -> np.ndarray
    
    @property
    def gouges(self) -> list[Gouge]
```

### SimulationResult

```python
@dataclass
class SimulationResult:
    success: bool
    moves_executed: int
    total_volume_removed: float      # mm^3
    total_time: float                # seconds (cycle time)
    collisions: list[Collision]
    gouges: list[Gouge]
    warnings: list[str]
    stock_mesh: trimesh.Trimesh
    deviation_map: np.ndarray        # per-vertex signed distance to target
```

## Appendix C: Coordinate Frame Conventions

All coordinate systems use the **right-hand rule**:

- **Workpiece frame (WP)**: The part or stock. Origin at a convenient reference (e.g., top center of stock).
- **Tool frame (T)**: Tool tip at origin, tool axis along +Z. This is the standard APT tool coordinate system.
- **Machine frame (M)**: Origin at machine home. XYZ axes aligned with machine slides.
- **World frame (W)**: Fixed reference frame. For simulation, W = WP.

Tool orientation is represented as a unit quaternion `[w, x, y, z]` (scalar-first convention) or a 3x3 rotation matrix. The Z-axis of the tool frame maps to the tool axis direction in the world frame.
