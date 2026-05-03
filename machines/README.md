# Machine Library

This directory contains machine definition files for the d2m 5-axis CNC simulator. Each `.json` file defines a complete CNC machine using the Vericut-style scene-graph component tree format.

## Using a Machine Definition

```python
from src.simulation.machine import MachineModel
from src.simulation.simulator import FiveAxisSimulator

# Load a machine from its JSON definition
machine = MachineModel.from_json("machines/dmg_dmu50.json")

# Use it in the simulator
sim = FiveAxisSimulator(stock_mesh, target_mesh, machine)
```

## Available Machines

| File | Machine | Type | Travels (X/Y/Z) | Rotary |
|------|---------|------|-----------------|--------|
| `dmg_dmu50.json` | DMG MORI DMU 50 | 5-axis BC trunnion | 500/450/400 mm | B: -35 to +110 deg, C: 360 deg continuous |
| `haas_umc750.json` | Haas UMC-750 | 5-axis BC trunnion | 762/508/508 mm | B: -35 to +120 deg, C: 360 deg continuous |
| `generic_3axis.json` | Generic 3-Axis VMC | 3-axis vertical mill | 600/400/350 mm | None |

## Creating Your Own Machine Definition

### Step 1: Understand the Component Tree

A CNC machine is modeled as a **scene graph** (component tree). Each node represents a physical component of the machine. The tree structure defines the kinematic chain:

```
Bed (root)
  ├── Column -> Z Axis -> Spindle -> Tool Mount    (tool chain)
  └── Y Axis -> X Axis -> B Axis -> C Axis -> Fixture Mount  (workpiece chain)
```

### Step 2: Gather Machine Specifications

You need the following information about your machine:
- **Axis travels** (X, Y, Z limits in mm)
- **Rotary axis ranges** (A, B, C limits in degrees)
- **Rapid traverse speeds** (mm/min)
- **Spindle specs** (max RPM, power, torque, tool interface)
- **Physical dimensions** (for component offsets)
- **Tool change position** (absolute machine coordinates)
- **Home position** (where the machine powers up)
- **Work offset defaults** (typical G54 values)

### Step 3: Write the JSON File

Create a new `.json` file following this structure:

```json
{
  "name": "Your Machine Name",
  "version": "1.0",
  "description": "Brief description of the machine",
  "manufacturer": "Manufacturer Name",
  "model": "Model Number",

  "components": [
    {
      "id": "unique_component_id",
      "type": "static | linear_axis | rotary_axis | spindle | tool_mount | fixture_mount | stock_mount",
      "parent": "parent_component_id or null (for root)",
      "label": "Human-readable name",
      "mesh": "relative/path/to/component.stl or null",
      "transform": [x_mm, y_mm, z_mm, rx_deg, ry_deg, rz_deg],

      "_axis_specific (only for linear_axis/rotary_axis)": "",
      "axis": "X | Y | Z | A | B | C",
      "limits": [min, max],
      "max_feed": 30000,
      "rapid_feed": 50000,
      "max_rpm": 100,
      "continuous": false,
      "pivot_offset": [x, y, z],

      "_spindle_specific": "",
      "max_power_kw": 25,
      "max_torque_nm": 100,
      "spindle_nose_to_gauge_mm": 50
    }
  ],

  "collision_groups": {
    "group_name": ["component_id_1", "component_id_2"]
  },

  "collision_pairs": [
    {
      "group_a": "group_name_or_stock",
      "group_b": "group_name_or_stock",
      "clearance_mm": 2.0,
      "check_type": "static | during_cut | near_miss | rapid_only",
      "warn_clearance_mm": 5.0
    }
  ],

  "home_position": [x, y, z, a, b, c],
  "tool_change_position": [x, y, z, a, b, c],

  "axis_priority": ["Z"],
  "retract_axis": "Z",

  "work_offset_defaults": {
    "G54": [x, y, z, a, b, c]
  },

  "kinematic_chain": {
    "tool_chain": ["leaf_to_root_component_ids"],
    "workpiece_chain": ["leaf_to_root_component_ids"]
  }
}
```

### Step 4: Understand Component Types

| Type | Description | Required Fields |
|------|-------------|----------------|
| `static` | Non-moving structural part (bed, column, frame) | `id`, `type`, `parent` |
| `linear_axis` | Translation axis (X, Y, Z) | + `axis`, `limits`, `max_feed` |
| `rotary_axis` | Rotation axis (A, B, C) | + `axis`, `limits`, `max_feed` |
| `spindle` | Spindle cartridge/housing | + `max_rpm` |
| `tool_mount` | Tool holder interface (HSK, BT, SK) | None additional |
| `fixture_mount` | Fixture/vise attachment point | None additional |
| `stock_mount` | Raw stock attachment (optional) | None additional |

### Step 5: Determine Component Transforms

The `transform` field positions each component relative to its parent:
- `[x, y, z]`: Translation in mm
- `[rx, ry, rz]`: Euler rotation in degrees (ZYX intrinsic order)

Start at the bed (root, transform = [0, 0, 0, 0, 0, 0]) and work outward:
1. Column: offset from bed to column base
2. Z-axis: offset to the Z-axis head at its top position (Z=0 is fully retracted)
3. Spindle: offset from Z-axis saddle to spindle center
4. Tool mount: offset from spindle nose to tool interface gauge line
5. Y-axis: offset to Y-axis saddle center
6. X-axis: offset to X-axis table center (from Y-axis)
7. Rotary axes: offset to pivot center
8. Fixture mount: offset from rotary table surface to fixture reference plane

### Step 6: Set Up Collision Groups and Pairs

Collision groups are named sets of component IDs:
```json
{
  "tool_group": ["tool_mount"],
  "spindle_group": ["spindle", "z_axis", "column"],
  "table_group": ["c_axis", "b_axis", "x_axis", "y_axis"]
}
```

Collision pairs declare which groups should be checked against each other:
```json
[
  {"group_a": "spindle_group", "group_b": "table_group", "clearance_mm": 5.0, "check_type": "static"},
  {"group_a": "tool_group", "group_b": "stock", "clearance_mm": 0.0, "check_type": "during_cut"}
]
```

The special group name `"stock"` refers to the dynamic stock mesh during simulation.

### Step 7: Add STL Meshes (Optional but Recommended)

Place STL files in a subdirectory named after your machine:
```
machines/
  dmg_dmu50/
    bed.stl
    column.stl
    z_saddle.stl
    spindle_head.stl
    y_saddle.stl
    x_table.stl
    b_trunnion.stl
    c_table.stl
```

If `mesh` is `null`, the component has no geometry and is a pure transform node. This is typical for `tool_mount` and `fixture_mount` which are logical attachment points.

For collision detection performance, you can specify a simplified mesh:
```json
{
  "mesh": "spindle_head.stl",
  "collision_mesh": "spindle_head_convex.stl"
}
```

### Step 8: Verify Your Definition

Load the machine and run basic checks:
```python
machine = MachineModel.from_json("machines/my_machine.json")

# Check that all components form a valid tree
for comp in machine.components.values():
    print(f"{comp.id}: type={comp.component_type.value}, parent={comp.parent_id}")

# Verify FK works at home
pose = machine.compute_forward_kinematics(machine.home_position)
print(f"Home pose: {pose}")

# Run FK-IK roundtrip
joints = np.array([50.0, 0.0, -100.0, 0.0, 15.0, 30.0])
pose = machine.compute_forward_kinematics(joints)
recovered = machine.compute_inverse_kinematics(pose)
print(f"Roundtrip axis error: {np.linalg.norm(machine.compute_forward_kinematics(recovered).tool_axis - pose.tool_axis)}")
```

## Machine-Specific Notes

### DMG DMU 50
- The B-axis trunnion tilts from -35 to +110 degrees
- Table diameter: 630 mm
- Max workpiece: 630 x 400 mm
- Tool interface: HSK-A63
- Typical application: complex 5-axis workpieces, medical, aerospace
- Spindle nose to table center: ~280 mm (at B=0)
- Known to be "stiff" with good dynamic performance

### Haas UMC-750
- B-axis tilts from -35 to +120 degrees
- Table diameter: 500 mm
- Max table load: 300 kg
- Tool interface: BT40
- Typical application: job shop 5-axis work, mold bases
- Platter (C-axis table surface) is ~60 mm above the B-axis pivot
- Good value proposition for entry-level 5-axis

### Generic 3-Axis VMC
- No rotary axes (3 linear axes only)
- Standard C-frame vertical mill configuration
- Useful as a template for creating custom 3-axis machine definitions
- Can be modified to represent bridge mills, gantry mills, etc.

## Troubleshooting

**Q: My machine loads but FK gives wrong tool orientation.**
A: Check that the `kinematic_chain.tool_chain` and `kinematic_chain.workpiece_chain` list the correct component IDs in leaf-to-root order. Verify that your rotary axes have the correct `axis` letter (A/B/C).

**Q: Collision checking doesn't find any collisions.**
A: Verify that your `collision_groups` contain valid component IDs and that the components have `mesh` paths pointing to existing STL files.

**Q: IK returns None for a valid pose.**
A: The pose may be unreachable due to axis limits or the machine's kinematic configuration. Check your axis `limits` values and ensure all active axes are correctly declared.
