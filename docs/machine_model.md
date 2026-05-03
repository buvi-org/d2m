# Machine Model: Scene-Graph Based CNC Machine Definition

## 1. Overview

### 1.1 Why This Exists

The current `kinematics.py` hardcodes three machine configurations (TABLE_TABLE, HEAD_HEAD, HEAD_TABLE) via an enum. This is inadequate because:

- A DMG DMU 50 and a Haas UMC-750 are both BC trunnion tables, but they have different **dimensions** (axis travels, table sizes), different **STL geometry** (casting shape, column design), and different **collision risks** (spindle nose vs. trunnion, tool holder vs. fixture).
- It cannot represent non-standard architectures: gantry mills, horizontal boring mills, hexapods, 6-axis robots, or swiss lathes with live tooling.
- Collision pair configuration is baked into assumptions rather than being an explicit, configurable part of the machine definition.
- Adding a new machine requires modifying Python source code and writing new arithmetic for each kinematic chain.

This document defines a **scene-graph machine model** -- the approach used by Vericut, NCSIMUL, and real CAM post-processors. A machine is a **tree of components**, each with a 3D mesh and a transform relative to its parent. Kinematics are derived by walking the tree. Collision pairs are explicitly configured. The G-code controller is a separate configuration file.

### 1.2 Key Concepts

| Concept | Description |
|---------|-------------|
| **Component Tree (Scene Graph)** | A rooted tree where each node is a physical machine component. The tree defines the kinematic chain. |
| **Walk-Up FK** | Forward kinematics: walk from a leaf node to the root, accumulating transforms. Active axes inject their current position into the accumulated transform. |
| **Explicit Collision Pairs** | Collision relationships are configured as pairs of collision groups (sets of component IDs). The simulation checks mesh-mesh proximity at every timestep. |
| **Controller Separation** | The machine defines the physical hardware; the controller defines the G-code dialect, macro mappings, and control logic. These are separate files. |
| **Tool Assembly Stack** | Tools are not monolithic; a ToolAssembly is a stack of holder + extension(s) + cutter, each with its own STL and transform. |

## 2. The Component Tree (Scene Graph)

### 2.1 Basic Concept

A CNC machine is modeled as a rooted tree where:
- The **root** is the machine base (bed/casting/frame).
- **Linear axes** are translation-only nodes.
- **Rotary axes** are rotation-only nodes.
- **Static nodes** are fixed structural elements.
- **Special nodes** (spindle, tool_mount, fixture_mount, stock_mount) define semantic attachment points.

Each node has:
- A **parent reference** (tree edge).
- A **local transform** (offset from parent when the axis is at its zero position).
- An **STL mesh** reference (for 3D visualization and collision detection).
- **Axis parameters** (if it is an active axis): travel limits, feed/speed limits, pivot offset.

### 2.2 Tree for a 5-Axis BC Trunnion Machine (DMG DMU 50)

```
                         ┌──────────────────────┐
                         │        Bed           │  (root, static)
                         │    "bed"             │
                         └──────┬───────┬───────┘
                                │       │
              ┌─────────────────┘       └──────────────────┐
              │                                             │
    ┌─────────▼──────────┐                      ┌──────────▼─────────┐
    │   Y Axis (linear)  │                      │  Z Axis (linear)   │
    │   "y_axis"         │                      │  "z_axis"          │
    │   axis: Y          │                      │  axis: Z           │
    │   limits: [-300,300]│                     │  limits: [-400,0]  │
    └─────────┬──────────┘                      └──────────┬─────────┘
              │                                             │
    ┌─────────▼──────────┐                      ┌──────────▼─────────┐
    │   X Axis (linear)  │                      │  Spindle (spindle) │
    │   "x_axis"         │                      │  "spindle"         │
    │   axis: X          │                      │  max_rpm: 18000    │
    │   limits: [-500,500]│                     └──────────┬─────────┘
    └─────────┬──────────┘                                │
              │                               ┌───────────▼─────────┐
    ┌─────────▼──────────┐                    │  Tool Mount         │
    │   B Axis (rotary)  │                    │  "tool_mount"       │
    │   "b_axis"         │                    │  type: tool_mount   │
    │   axis: B          │                    └─────────────────────┘
    │   limits: [-120,120]│                             │
    │   pivot_offset: [0,0,0]│              (ToolAssembly attached here)
    └─────────┬──────────┘
              │
    ┌─────────▼──────────┐
    │   C Axis (rotary)  │
    │   "c_axis"         │
    │   axis: C          │
    │   limits: [0,360]  │
    │   continuous: true │
    │   pivot_offset: [0,0,-150]│
    └─────────┬──────────┘
              │
    ┌─────────▼──────────┐
    │   Fixture Mount    │
    │   "fixture_mount"  │
    │   type: fixture_mount│
    └────────────────────┘
              │
        (Fixture mesh + Stock mesh attached here)
```

The tree yields two kinematic chains:

- **Tool chain**: `tool_mount -> spindle -> z_axis -> bed`
- **Workpiece chain**: `fixture_mount -> c_axis -> b_axis -> x_axis -> y_axis -> bed`

### 2.3 Tree for a 5-Axis Tilting-Head / Rotary-Table (HEAD_TABLE, e.g. Mazak Variaxis)

```
    Bed (root)
      ├── Z Axis (linear) -> B Axis (rotary head) -> Spindle -> Tool Mount
      ├── Y Axis (linear) -> X Axis (linear) -> C Axis (rotary table) -> Fixture Mount
      └── (Column / frame static parts)
```

### 2.4 Tree for a 3-Axis Vertical Mill

```
    Bed (root)
      ├── Y Axis -> X Axis -> Table -> Fixture Mount
      └── Z Axis -> Spindle -> Tool Mount
```

### 2.5 Tree for a Gantry Mill

```
    Bed (root)
      ├── X Axis (gantry bridge) -> Y Axis (cross-slide) -> Z Axis -> Spindle -> Tool Mount
      └── Table (fixed, may have optional rotary) -> Fixture Mount
```

## 3. Node Types

### 3.1 Enumeration

| Type | Description | Has Axis? | Special Behavior |
|------|-------------|-----------|------------------|
| `static` | Non-moving structural element. Attached to parent with a fixed transform. | No | Pure visual/collision geometry. Does not contribute to kinematic accumulation. |
| `linear_axis` | A translation axis (X, Y, Z, U, V, W). | Yes | Injects a translation into the kinematic chain. `axis` field gives the direction (always machine-aligned). |
| `rotary_axis` | A rotation axis (A, B, C). | Yes | Injects a rotation about its local axis into the kinematic chain. `axis` letter determines rotation axis convention. |
| `spindle` | The rotating spindle cartridge/housing. | No (rotates but does not change tool position) | Has max_rpm, max_power_kw. The spindle nose offset (`spindle_nose_to_gauge_mm`) defines the gauge line. |
| `tool_mount` | The interface where the tool assembly attaches (HSK, SK, BT, CAT taper). | No | The parent of the tool assembly attachment point. Transform from here defines gauge line to tool tip relationship. |
| `fixture_mount` | The interface where the fixture/vise attaches to the machine. | No | The parent of the fixture and stock in the workpiece chain. |
| `stock_mount` | The attachment point for the raw stock material. | No | Typically a child of fixture_mount. The stock mesh is placed relative to this node. |

### 3.2 Directional Convention

The direction of linear axis motion is always along the axis letter direction in the **machine coordinate system**:

- `X`: positive direction is to the right (looking from operator position)
- `Y`: positive direction is away from the operator
- `Z`: positive direction is upward (toward spindle)

For rotary axes:
- `A`: rotation about the X-axis (right-hand rule)
- `B`: rotation about the Y-axis (right-hand rule)
- `C`: rotation about the Z-axis (right-hand rule)

### 3.3 Why Separate `spindle` from `tool_mount`

In a real machine:
- The **spindle** is the motorized cartridge -- it has mass, geometry (can collide), RPM limits, and power limits.
- The **tool_mount** is the taper interface (HSK-A63, SK40, BT40, CAT50). It defines where the tool assembly attaches.

Separating them allows:
- Tool changes do not require modifying the machine tree -- only changing which ToolAssembly is attached to `tool_mount`.
- Spindle collision with the table/trunnion is checked independently of tool collision with the fixture.
- Different spindle cartridges can be swapped on some machines.

## 4. Node Properties

### 4.1 Common Properties (All Node Types)

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | string | Yes | Unique identifier within the machine. Must be a valid Python identifier / JSON key. |
| `type` | string | Yes | One of: `static`, `linear_axis`, `rotary_axis`, `spindle`, `tool_mount`, `fixture_mount`, `stock_mount`. |
| `parent` | string or null | Yes | ID of the parent component. `null` for the root node. |
| `mesh` | string or null | No | Path to STL file (relative to the machine JSON directory, or absolute). `null` means no geometry (pure transform node). |
| `transform` | [x, y, z, rx, ry, rz] | Yes | 6-DOF transform relative to parent when axis is at zero. `[x, y, z]` in mm, `[rx, ry, rz]` in degrees (Euler angles, ZYX intrinsic). This is the **zero-offset** -- the position of the node when its axis value is 0. |

### 4.2 Axis-Specific Properties (`linear_axis` and `rotary_axis`)

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `axis` | string | Yes | Axis letter: 'X', 'Y', 'Z' for linear; 'A', 'B', 'C' for rotary. 'U', 'V', 'W' for secondary linear axes. |
| `limits` | [min, max] | Yes | Travel limits in mm (linear) or degrees (rotary). For rotary axes, `min` and `max` define the allowed angular range. |
| `max_feed` | float | Yes | Maximum feed rate in mm/min (linear) or deg/min (rotary). |
| `rapid_feed` | float | No | Rapid traverse rate. Defaults to `max_feed`. |
| `max_rpm` | float | No | Maximum rotational speed (only for rotary axes, not linear). |
| `continuous` | bool | No | For rotary axes: if `true`, the axis can wind continuously (no wrap-around at 360). E.g., C-axis on most 5-axis machines. Default: `false`. |
| `pivot_offset` | [x, y, z] | No | (rotary_axis only) Offset from the component's local origin to the center of rotation. Default: `[0, 0, 0]`. Critical for correct FK/IK. |

### 4.3 Spindle-Specific Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `max_rpm` | float | Yes | Maximum spindle RPM. |
| `max_power_kw` | float | No | Maximum spindle motor power in kW. |
| `max_torque_nm` | float | No | Maximum spindle torque in Nm. |
| `spindle_nose_to_gauge_mm` | float | No | Distance from spindle nose face to the gauge line (tool length reference plane). Default: 0. Typical: 50mm for HSK-A63. |

### 4.4 Collision-Related Properties (All Node Types)

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `collision_mesh` | string or null | No | Alternative mesh for collision detection (simplified/convex hull for performance). If `null`, uses `mesh`. |
| `collision_margin` | float | No | Per-component collision margin in mm. Expands the mesh by this amount for proximity queries. Default: 0.0. |

## 5. Kinematics Derivation

### 5.1 Forward Kinematics: Tree Walking

Forward kinematics computes the **tool pose in the workpiece frame** given a joint vector (axis positions).

**Algorithm:**

```
Input: joints = [X, Y, Z, A, B, C]  (active axis positions)
Output: ToolPose (position + orientation in workpiece frame)

1. TOOL CHAIN:
   Start at tool_mount, walk UP to root.
   At each node:
     - Multiply transform by node's local_transform (4x4 matrix from 6-DOF)
     - If node is an active axis, apply its current joint value:
       * linear_axis: apply translation along axis letter direction
       * rotary_axis: apply rotation about axis letter direction (at pivot_offset)
   Result: T_tool_world = 4x4 matrix of tool origin in world/machine coordinates.

2. WORKPIECE CHAIN:
   Start at stock_mount (or fixture_mount if no separate stock_mount), walk UP to root.
   Same accumulation, but for the workpiece side.
   Result: T_workpiece_world = 4x4 matrix of workpiece origin in world coordinates.

3. TOOL IN WORKPIECE FRAME:
   T_tool_in_workpiece = inv(T_workpiece_world) @ T_tool_world

4. Decompose T_tool_in_workpiece into position + quaternion for ToolPose.
```

**Key insight:** The bed (root) is the common ancestor. The two chains meet at the root. The tool-to-workpiece transform is the relative transform between the two chains, expressed by inverting one side.

### 5.2 Detailed Transform Accumulation

For each node in the chain (walking toward root):

```python
def accumulate_transform(node, parent_world, joints):
    # Start with parent's world transform
    T = parent_world @ node.local_transform

    if node.type == "linear_axis":
        axis_val = joints.get(node.axis)  # current position
        T = T @ translation(axis_direction(node.axis) * axis_val)

    elif node.type == "rotary_axis":
        axis_val = radians(joints.get(node.axis))
        pivot = node.pivot_offset
        T = T @ translation(pivot) @ rotation(axis_direction, axis_val) @ translation(-pivot)

    return T
```

### 5.3 Inverse Kinematics

Inverse kinematics computes joint values from a desired tool pose in the workpiece frame.

The approach depends on the machine topology, but for standard 5-axis machines, analytic closed-form solutions exist:

**General strategy:**

1. Identify the two chains: tool chain (T) and workpiece chain (W).
2. The tool pose in workpiece frame is: `P_wp = inv(T_w) @ T_t` where `T_w` is the workpiece chain transform and `T_t` is the tool chain transform.
3. Separate the knowns (desired P_wp) from the unknowns (joint values).
4. For TABLE_TABLE: rotary axes are on the workpiece side. Solve for B, C from the tool axis orientation, then solve for X, Y, Z from the position.
5. For HEAD_HEAD: rotary axes are on the tool side. Solve for A, B from the tool axis, then solve for X, Y, Z.
6. For HEAD_TABLE: one rotary on each side. Solve for B (head), then C (table), then position.

**Tree-based generalization:**

The IK code can interrogate the tree to determine:
- Which rotary axes exist on the tool chain vs workpiece chain
- The pivot offsets for each rotary
- The kinematic chain order (which rotary is primary/secondary)
- The axis limits for each axis

This makes IK truly machine-independent. The same solver works for any 5-axis configuration by reading the tree.

### 5.4 singularity Handling

Singularities occur when:
- Two rotary axes align (e.g., B=0 in BC trunnion, where C rotation does not change tool orientation)
- A rotary axis reaches its limit

The solver detects near-singularity conditions (when `sin(axis_angle) < epsilon`) and uses the previous joint state to disambiguate. For continuous axes, it tracks accumulated angle beyond [0, 360).

### 5.5 `get_world_transform` -- The Collision Enabler

This method computes the 4x4 world transform for **any** component at a given joint state:

```python
def get_world_transform(component_id, joints):
    """Walk from component_id up to root, accumulating transforms."""
    T = identity
    current = components[component_id]
    while current is not None:
        T = apply_axis_transform(current, joints) @ current.local_transform @ T
        current = components[current.parent_id]
    return T
```

This is the foundation of collision detection: it tells us where the spindle head, holder, table, trunnion, and fixture are in 3D space at any moment.

## 6. Collision System

### 6.1 Collision Groups

A **collision group** is a named set of component IDs. Groups abstract away individual components so that collision pairs are configured at a logical level.

```json
"collision_groups": {
    "tool_group":     ["tool_mount"],
    "spindle_group":  ["spindle", "z_axis"],
    "table_group":    ["c_axis", "b_axis", "x_axis", "y_axis"],
    "fixture_group":  ["fixture_mount"],
    "head_group":     ["spindle", "tool_mount", "z_axis"]
}
```

### 6.2 Collision Pairs

A **collision pair** declares that every component in `group_a` should be checked against every component in `group_b`. The special value `"stock"` refers to the current stock mesh (dynamic), not a fixed component.

```json
"collision_pairs": [
    {
        "group_a": "tool_group",
        "group_b": "fixture_group",
        "clearance_mm": 2.0,
        "check_type": "static"
    },
    {
        "group_a": "spindle_group",
        "group_b": "table_group",
        "clearance_mm": 5.0,
        "check_type": "static"
    },
    {
        "group_a": "tool_group",
        "group_b": "stock",
        "clearance_mm": 0.0,
        "check_type": "during_cut"
    }
]
```

### 6.3 Check Types

| Type | Description |
|------|-------------|
| `static` | Check at every simulation step (G0 and G1 moves). For machine-machine clearance. |
| `during_cut` | Check only during G1 (feed) moves. For tool-stock proximity (contact is expected during cutting). |
| `near_miss` | Check but only warn if clearance is below threshold. Does not halt simulation. |
| `rapid_only` | Check only during G0 (rapid traverse) moves. For tool-fixture approach safety. |

### 6.4 Collision Detection Algorithm

```
For each collision pair (group_a, group_b, clearance, check_type):
    For each component_id_a in group_a:
        T_a_world = get_world_transform(component_id_a, joints)
        mesh_a_world = load_mesh(component_id_a).apply_transform(T_a_world)

        For each component_id_b in group_b:
            T_b_world = get_world_transform(component_id_b, joints)
            mesh_b_world = load_mesh(component_id_b).apply_transform(T_b_world)

            distance = trimesh.proximity.closest_point(mesh_a_world, mesh_b_world)[1]
            if distance < clearance:
                report Collision(component_a, component_b, distance, clearance)
```

For the special `"stock"` group: the stock mesh is transformed by the workpiece chain transform (from fixture_mount up to root) at the current joint state.

### 6.5 Near-Miss Zones

A near-miss zone is a clearance range `[warn_clearance, critical_clearance]`. If the distance falls in this range, a warning is reported but simulation continues. If below `critical_clearance`, it is a collision.

### 6.6 Swept-Path Collision Checking

For collision pairs with `check_type: "swept"`, instead of checking at discrete poses, the swept volume of the moving component between `start_joints` and `end_joints` is computed and checked against the static components. This catches collisions that occur between sampled poses (e.g., a fixture clamp intersecting the tool holder mid-move).

Swept-path checking is enabled per collision pair and uses the `swept_volume` module's sampling.

### 6.7 Performance Considerations

- Use **bounding volume hierarchies (BVH)** for mesh-mesh proximity queries (trimesh provides this).
- Use **convex hull simplifications** for collision meshes (faster than full STL).
- Cache world transforms between simulation steps -- many components don't move.
- **Broad phase**: AABB check before mesh-mesh proximity.
- **Narrow phase**: trimesh.proximity with ProximityQuery.

## 7. JSON Machine Definition Format

### 7.1 Complete Specification

```json
{
  "$schema": "https://buvi-org.github.io/d2m/schemas/machine_model_v1.json",
  "name": "Machine Name",
  "version": "1.0",
  "description": "Optional human-readable description",
  "manufacturer": "Manufacturer Name",
  "model": "Model Number",

  "components": [
    { /* component objects, see below */ }
  ],

  "collision_groups": {
    "group_name": ["component_id", "..."],
    "...": ["..."]
  },

  "collision_pairs": [
    {
      "group_a": "group_name_or_stock",
      "group_b": "group_name_or_stock",
      "clearance_mm": 2.0,
      "check_type": "static"
    }
  ],

  "home_position": [0, 0, 0, 0, 0, 0],
  "tool_change_position": [0, 0, -400, 0, 0, 0],

  "axis_priority": ["Z"],
  "retract_axis": "Z",

  "work_offset_defaults": {
    "G54": [250, 150, 50, 0, 0, 0],
    "G55": [0, 0, 0, 0, 0, 0]
  },

  "kinematic_chain": {
    "tool_chain": ["tool_mount", "spindle", "z_axis", "bed"],
    "workpiece_chain": ["stock_mount", "fixture_mount", "c_axis", "b_axis", "x_axis", "y_axis", "bed"]
  }
}
```

### 7.2 Component Object Schema

```json
{
  "id": "unique_component_id",
  "type": "linear_axis | rotary_axis | static | spindle | tool_mount | fixture_mount | stock_mount",
  "parent": "parent_component_id_or_null",
  "label": "Human-readable name (e.g., 'Z-Axis Saddle')",

  "mesh": "path/to/component.stl",
  "collision_mesh": "path/to/component_collision.stl",
  "collision_margin": 0.0,

  "transform": [x, y, z, rx, ry, rz],

  "axis": "X | Y | Z | A | B | C | U | V | W",
  "limits": [min, max],
  "max_feed": 30000,
  "rapid_feed": 50000,
  "max_rpm": 100,
  "continuous": false,
  "pivot_offset": [0, 0, 0],

  "spindle_nose_to_gauge_mm": 50,
  "max_power_kw": 25,
  "max_torque_nm": 100
}
```

Not all fields apply to all component types. The loader should validate required fields per type.

### 7.3 Transform Convention

The `transform` field is `[x, y, z, rx, ry, rz]`:
- `x, y, z`: translation in mm
- `rx, ry, rz`: Euler angles in degrees, intrinsic ZYX order (rotate about Z, then Y', then X'')

This yields a 4x4 homogeneous transform:
```
T = T(x,y,z) * Rz(rz) * Ry(ry) * Rx(rx)
```

This transform positions the component **relative to its parent** when the component's axis is at its **zero position** (home). Axis motion adds additional transforms on top of this.

### 7.4 Example: Full DMG DMU 50 Definition

```json
{
  "name": "DMG DMU 50",
  "version": "1.0",
  "description": "DMG MORI DMU 50 5-axis vertical machining center. BC trunnion table configuration. Travels: X=500, Y=450, Z=400. Table diameter: 630mm. Spindle: HSK-A63, 18,000 RPM, 25 kW.",
  "manufacturer": "DMG MORI",
  "model": "DMU 50",

  "components": [
    {
      "id": "bed",
      "type": "static",
      "parent": null,
      "label": "Machine Bed / Base Casting",
      "mesh": "dmg_dmu50/bed.stl",
      "transform": [0, 0, 0, 0, 0, 0]
    },
    {
      "id": "column",
      "type": "static",
      "parent": "bed",
      "label": "Vertical Column",
      "mesh": "dmg_dmu50/column.stl",
      "transform": [0, -300, 0, 0, 0, 0]
    },
    {
      "id": "z_axis",
      "type": "linear_axis",
      "parent": "column",
      "label": "Z-Axis Head Slide",
      "mesh": "dmg_dmu50/z_saddle.stl",
      "transform": [0, 0, 600, 0, 0, 0],
      "axis": "Z",
      "limits": [-400, 0],
      "max_feed": 30000,
      "rapid_feed": 50000
    },
    {
      "id": "spindle",
      "type": "spindle",
      "parent": "z_axis",
      "label": "Spindle Cartridge",
      "mesh": "dmg_dmu50/spindle_head.stl",
      "transform": [0, 0, -100, 0, 0, 0],
      "max_rpm": 18000,
      "max_power_kw": 25,
      "max_torque_nm": 130,
      "spindle_nose_to_gauge_mm": 50
    },
    {
      "id": "tool_mount",
      "type": "tool_mount",
      "parent": "spindle",
      "label": "HSK-A63 Tool Interface",
      "mesh": null,
      "transform": [0, 0, -50, 0, 0, 0]
    },
    {
      "id": "y_axis",
      "type": "linear_axis",
      "parent": "bed",
      "label": "Y-Axis Saddle",
      "mesh": "dmg_dmu50/y_saddle.stl",
      "transform": [0, -225, 0, 0, 0, 0],
      "axis": "Y",
      "limits": [-225, 225],
      "max_feed": 30000,
      "rapid_feed": 50000
    },
    {
      "id": "x_axis",
      "type": "linear_axis",
      "parent": "y_axis",
      "label": "X-Axis Table Slide",
      "mesh": "dmg_dmu50/x_table.stl",
      "transform": [-250, 0, 0, 0, 0, 0],
      "axis": "X",
      "limits": [-250, 250],
      "max_feed": 30000,
      "rapid_feed": 50000
    },
    {
      "id": "b_axis",
      "type": "rotary_axis",
      "parent": "x_axis",
      "label": "B-Axis Trunnion (Tilting Table)",
      "mesh": "dmg_dmu50/b_trunnion.stl",
      "transform": [0, 0, -250, 0, 0, 0],
      "axis": "B",
      "limits": [-115, 115],
      "max_feed": 18000,
      "max_rpm": 50,
      "pivot_offset": [0, 0, 0]
    },
    {
      "id": "c_axis",
      "type": "rotary_axis",
      "parent": "b_axis",
      "label": "C-Axis Rotary Table",
      "mesh": "dmg_dmu50/c_table.stl",
      "transform": [0, 0, -200, 0, 0, 0],
      "axis": "C",
      "limits": [0, 360],
      "max_feed": 36000,
      "max_rpm": 100,
      "continuous": true,
      "pivot_offset": [0, 0, -200]
    },
    {
      "id": "fixture_mount",
      "type": "fixture_mount",
      "parent": "c_axis",
      "label": "Fixture Mounting Surface",
      "mesh": null,
      "transform": [0, 0, -75, 0, 0, 0]
    }
  ],

  "collision_groups": {
    "tool_group": ["tool_mount"],
    "spindle_group": ["spindle", "z_axis", "column"],
    "head_group": ["spindle", "z_axis", "tool_mount"],
    "table_group": ["c_axis", "b_axis", "x_axis", "y_axis"],
    "trunnion_group": ["b_axis", "c_axis"],
    "fixture_group": ["fixture_mount"]
  },

  "collision_pairs": [
    {
      "group_a": "tool_group",
      "group_b": "fixture_group",
      "clearance_mm": 2.0,
      "check_type": "near_miss"
    },
    {
      "group_a": "spindle_group",
      "group_b": "table_group",
      "clearance_mm": 5.0,
      "check_type": "static"
    },
    {
      "group_a": "head_group",
      "group_b": "trunnion_group",
      "clearance_mm": 10.0,
      "check_type": "static"
    },
    {
      "group_a": "tool_group",
      "group_b": "stock",
      "clearance_mm": 0.0,
      "check_type": "during_cut"
    },
    {
      "group_a": "spindle_group",
      "group_b": "stock",
      "clearance_mm": 5.0,
      "check_type": "static"
    }
  ],

  "home_position": [0, 0, 0, 0, 0, 0],
  "tool_change_position": [0, 225, -400, 0, 0, 0],

  "axis_priority": ["Z"],
  "retract_axis": "Z",

  "work_offset_defaults": {
    "G54": [250, 150, 75, 0, 0, 0]
  },

  "kinematic_chain": {
    "tool_chain": ["tool_mount", "spindle", "z_axis", "column", "bed"],
    "workpiece_chain": ["fixture_mount", "c_axis", "b_axis", "x_axis", "y_axis", "bed"]
  }
}
```

## 8. Controller Definition

### 8.1 Separation of Concerns

The **machine** defines the physical hardware (geometry, axes, limits). The **controller** defines the G-code interpretation:
- Which G-code dialect (Fanuc, Heidenhain, Siemens, Haas, Okuma)
- Macro/variable mappings
- Canned cycle implementations
- Tool change macro behavior
- Probing cycle definitions
- Coordinate system management
- High-speed machining (look-ahead) settings

### 8.2 Controller JSON Format

```json
{
  "name": "Siemens 840D sl",
  "version": "1.0",
  "dialect": "siemens_840d",

  "gcode_mappings": {
    "G00": "rapid_traverse",
    "G01": "linear_feed",
    "G02": "circular_cw",
    "G03": "circular_ccw",
    "G17": "plane_xy",
    "G18": "plane_zx",
    "G19": "plane_yz",
    "G54": "work_offset_1",
    "G55": "work_offset_2"
  },

  "mcode_mappings": {
    "M03": "spindle_cw",
    "M04": "spindle_ccw",
    "M05": "spindle_stop",
    "M06": "tool_change",
    "M08": "coolant_on",
    "M09": "coolant_off",
    "M30": "program_end"
  },

  "canned_cycles": {
    "G81": "drilling",
    "G83": "peck_drilling",
    "G84": "tapping"
  },

  "variable_mappings": {
    "#500": "work_offset_x_g54",
    "#501": "work_offset_y_g54",
    "#502": "work_offset_z_g54"
  },

  "kinematic_transforms": {
    "TRAORI": "5axis_transform_on",
    "TRAFOOF": "5axis_transform_off",
    "ORIWKS": "orientation_workpiece_frame",
    "ORIMKS": "orientation_machine_frame"
  },

  "look_ahead_lines": 200,
  "nan_smoothing": false,
  "default_feed_rate": 5000
}
```

### 8.3 Dialect Profiles

| Dialect | Key Characteristics |
|---------|---------------------|
| `fanuc_30i` | G43.4/G43.5 for TCP, G68.2 for tilted work planes, macros via #variables |
| `siemens_840d` | TRAORI/TRAFOOF for 5-axis, CYCLE800 for swivel, frames (TRANS, ROT) |
| `heidenhain_tnc` | M128 for TCP, PLANE functions, CYCL DEF, conversational or DIN/ISO |
| `haas_ngc` | G234 for TCP, G254 for DWO, simplified macro set |
| `okuma_osp` | G131/G130 for TCP, CALL statements, different coordinate system conventions |
| `linuxcnc` | Open-source, supports multiple interpreters, highly configurable |

## 9. Tool Assembly Format

### 9.1 Concept

A tool is not a single entity. It is a **stack** of components:
- **Holder** (HSK/SK/BT/CAT taper with flange and pull stud)
- **Extension(s)** (collet chuck, shrink-fit extension, hydraulic holder)
- **Cutter** (the actual cutting tool: endmill, drill, etc.)

Each component has its own STL mesh and dimensions. This enables:
- Accurate collision detection for the entire tool assembly, not just the cutter
- Tool length calculation from holder gauge line
- Checking holder-fixture and extension-workpiece collisions
- Simulating different tool setups with the same cutter

### 9.2 Tool Assembly JSON Format

```json
{
  "name": "D12 Ball Endmill Assembly",
  "description": "D12 ball endmill in HSK-A63 shrink-fit holder",

  "interface": "HSK-A63",

  "components": [
    {
      "id": "holder",
      "type": "holder",
      "label": "HSK-A63 Shrink Fit Holder D12",
      "mesh": "holders/hsk_a63_shrink_d12.stl",
      "length_mm": 80.0,
      "diameter_mm": 48.0,
      "gauge_length_mm": 80.0,
      "transform": [0, 0, 0, 0, 0, 0]
    },
    {
      "id": "extension",
      "type": "extension",
      "label": "D12 Collet Extension 50mm",
      "mesh": "extensions/collet_ext_d12_50mm.stl",
      "length_mm": 50.0,
      "diameter_mm": 25.0,
      "transform": [0, 0, 80, 0, 0, 0]
    },
    {
      "id": "cutter",
      "type": "cutter",
      "label": "D12 Ball Endmill R6 4-Flute Carbide",
      "tool_definition": {
        "type": "ball_endmill",
        "diameter": 12.0,
        "flute_length": 24.0,
        "length": 75.0
      },
      "mesh": "cutters/ball_d12_fl24.stl",
      "transform": [0, 0, 130, 0, 0, 0],
      "stickout_mm": 35.0
    }
  ],

  "total_length_mm": 205.0,
  "gauge_length_mm": 205.0,
  "max_rpm": 24000,
  "max_feed_per_tooth_mm": 0.15
}
```

### 9.3 Tool Component Types

| Type | Description |
|------|-------------|
| `holder` | The tool holder body (taper + flange + body). Defines the machine interface type. |
| `extension` | Optional extension between holder and cutter. Multiple extensions can be stacked. |
| `cutter` | The actual cutting tool. Contains a `tool_definition` referencing the APT 7-parameter tool model for material removal simulation. |

### 9.4 Derived Properties

- **Gauge length**: Total distance from the holder's gauge plane (spindle nose face + `spindle_nose_to_gauge_mm`) to the cutter tip.
- **Stickout**: Distance from the last holder/extension face to the cutter tip. Affects tool rigidity and max cutting parameters.
- **Assembly mesh**: Union of all component meshes, transformed by their chain. Used for collision detection.

## 10. Comparison to Current Approach

### 10.1 Current Approach (kinematics.py)

```
Strengths:
  + Simple: enum + 3 hardcoded kinematic chains
  + Fast to implement for known configurations
  + No external files needed

Weaknesses:
  - New machine = new Python code (write new FK, IK, singularity handling)
  - Cannot model non-standard architectures (gantry, horizontal, hexapod)
  - Collision checking is not integrated -- no mesh-based collision pairs
  - Tool offset is a single float (tool_pivot_length), not a full assembly
  - Axis limits are generic defaults, not machine-specific
  - No STL meshes for visualization or collision detection
  - Work offsets (G54-G59) are not tied to the machine
  - Cannot swap tool holders or check holder collision
```

### 10.2 New Approach (Scene Graph MachineModel)

```
Strengths:
  + Any machine configuration: just write a JSON file
  + No code changes to add a new machine
  + Explicit collision pairs with mesh-based proximity checking
  + Full tool assembly with holder + extension + cutter STL meshes
  + Machine-specific axis limits, speeds, dimensions
  + Supports gantry, horizontal, hexapod, robot, swiss lathe, etc.
  + Visual preview of machine with actual geometries
  + Controller dialect is a separate configuration
  + Tool change position, home position, work offsets all in machine file
  + FK/IK derived from tree, not hardcoded per config

Weaknesses:
  - Requires STL files for each machine component (can be placeholders)
  - More complex initial setup (write JSON + collect STL files)
  - IK for arbitrary tree topologies may need numeric fallback (not always analytic)
  - Performance overhead from mesh collision checking (mitigated by BVH + convex hull)
```

### 10.3 Migration Path

1. **Phase 2**: Implement `MachineModel` and `MachineComponent` classes with tree-based FK/IK.
2. **Phase 3**: Wire `MachineModel` into `FiveAxisSimulator`. Keep backward compatibility: when given a `MachineConfig` enum, auto-generate a default `MachineModel`. Mark old kinematics paths as deprecated.
3. **Phase 4**: Create sample machine library (DMG DMU 50, Haas UMC-750, generic 3-axis).
4. **Future**: Full removal of `MachineConfig` enum and hardcoded kinematics once all callers migrate.

## 11. Implementation Details

### 11.1 Mesh Loading

- Use `trimesh.load()` for STL files.
- Cache loaded meshes in a dictionary keyed by path.
- `collision_mesh` overrides `mesh` for collision detection (use simplified convex hull).
- If `mesh` is `null`, the component is a pure transform node (no geometry).

### 11.2 Transform Chain Computation

The core operation is walking from a leaf node to the root:

```python
def compute_chain(component_id: str) -> list[str]:
    """Return the ordered list of component IDs from leaf to root."""
    chain = []
    current = component_id
    while current is not None:
        chain.append(current)
        current = components[current].parent_id
    return chain
```

For FK, two chains are computed (tool side + workpiece side). For `get_world_transform`, a single chain from the target component to root.

### 11.3 Axis Direction Vectors

| Axis Letter | Direction Vector (Machine Frame) |
|-------------|----------------------------------|
| X           | [1, 0, 0] |
| Y           | [0, 1, 0] |
| Z           | [0, 0, 1] |
| U           | [1, 0, 0] (secondary X) |
| V           | [0, 1, 0] (secondary Y) |
| W           | [0, 0, 1] (secondary Z) |
| A           | [1, 0, 0] (rotation about X) |
| B           | [0, 1, 0] (rotation about Y) |
| C           | [0, 0, 1] (rotation about Z) |

### 11.4 Homogeneous Transform Convention

All transforms use 4x4 homogeneous matrices:

```
T = | R   t |
    | 0   1 |

where R is 3x3 rotation, t is 3x1 translation.
```

Composition: `T_world = T_parent_world @ T_local` (parent-to-world times local-to-parent).

## 12. Future Extensions

- **Robotic arms**: The component tree naturally extends to 6-DOF serial manipulators. Each joint is a `rotary_axis`. IK for 6-DOF uses iterative numeric methods (e.g., Jacobian pseudoinverse or CCD).
- **Parallel kinematics**: Hexapods require solving the inverse kinematics of the parallel mechanism (leg lengths from platform pose). This would be a special `parallel_mechanism` component type.
- **Multi-channel machines**: Machines with dual spindles or dual turrets have multiple independent tool chains. The tree supports this by having multiple `tool_mount` leaf nodes.
- **Automatic collision pair generation**: For machines with many components, auto-generate all-pairs or neighbor-pairs collision groups from the tree.
- **Machine builder UI**: A GUI that lets users drag-and-drop components into a tree, assign STL files, and auto-generate the JSON definition.
