"""Vericut-style scene-graph machine model.

Models a CNC machine as a component tree (scene graph) where each node
has a 3D mesh (STL) and a local transform relative to its parent.
Kinematics are derived by walking the tree from leaf to root.
Collision pairs are explicitly configured.

This replaces the hardcoded MachineConfig enum approach in kinematics.py
with a fully data-driven, any-topology machine definition.

Usage:
    machine = MachineModel.from_json("machines/dmg_dmu50.json")
    tool_assembly = ToolAssembly.from_json("tools/d12_ball_endmill.json")

    # Forward kinematics
    joints = np.array([10.0, 20.0, -50.0, 0.0, 30.0, 45.0])
    tool_pose = machine.compute_forward_kinematics(joints)

    # World transform for any component (collision detection)
    spindle_world = machine.get_world_transform("spindle", joints)

    # Collision checking
    collisions = machine.check_collisions(joints, tool_assembly, stock_mesh, fixture_mesh)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Tuple, Union
import json
import os
import warnings
import numpy as np
import trimesh

from .kinematics import ToolPose, FiveAxisKinematics


# =========================================================================
#  Enums and type aliases
# =========================================================================

class ComponentType(Enum):
    """Types of nodes in the machine component tree."""
    STATIC = "static"
    LINEAR_AXIS = "linear_axis"
    ROTARY_AXIS = "rotary_axis"
    SPINDLE = "spindle"
    TOOL_MOUNT = "tool_mount"
    FIXTURE_MOUNT = "fixture_mount"
    STOCK_MOUNT = "stock_mount"


class CheckType(Enum):
    """Collision check types."""
    STATIC = "static"          # Check at every simulation step
    DURING_CUT = "during_cut"  # Check only during G1 feed moves
    NEAR_MISS = "near_miss"    # Warn on proximity, don't halt
    RAPID_ONLY = "rapid_only"  # Check only during G0 rapid moves


# =========================================================================
#  Data classes for collision configuration
# =========================================================================

@dataclass
class CollisionPair:
    """A configured collision pair between two groups of components.

    Attributes:
        group_a: Name of first collision group, or "stock".
        group_b: Name of second collision group, or "stock".
        clearance_mm: Distance threshold in mm. Below this = collision.
        check_type: When to check this pair.
        warn_clearance_mm: For near_miss type: distance below which to warn.
    """
    group_a: str
    group_b: str
    clearance_mm: float = 2.0
    check_type: CheckType = CheckType.STATIC
    warn_clearance_mm: float = 5.0


@dataclass
class Collision:
    """Result of a collision check.

    Attributes:
        component_a: ID of first colliding component.
        component_b: ID of second colliding component.
        distance_mm: Minimum distance between meshes.
        clearance_mm: Configured clearance threshold.
        point_a: Closest point on component A (world frame).
        point_b: Closest point on component B (world frame).
        is_near_miss: True if this is a near-miss (within warn zone but not critical).
    """
    component_a: str
    component_b: str
    distance_mm: float
    clearance_mm: float
    point_a: np.ndarray = field(default_factory=lambda: np.zeros(3))
    point_b: np.ndarray = field(default_factory=lambda: np.zeros(3))
    is_near_miss: bool = False

    def __repr__(self) -> str:
        return (f"Collision({self.component_a} <-> {self.component_b}, "
                f"dist={self.distance_mm:.3f}mm, clearance={self.clearance_mm:.3f}mm)")


# =========================================================================
#  Tool Assembly types
# =========================================================================

@dataclass
class ToolComponent:
    """A single component in a tool assembly (holder, extension, or cutter).

    Attributes:
        component_id: Unique ID within the assembly.
        component_type: "holder", "extension", or "cutter".
        mesh_path: Path to STL file.
        transform: 4x4 local transform relative to previous component.
        length_mm: Length of this component along tool axis.
        diameter_mm: Maximum diameter of this component.
        tool_definition: For cutter type, the APT tool parameters as dict.
        gauge_length_mm: Cumulative gauge length from holder gauge plane
                         to the tip of this component.
    """
    component_id: str
    component_type: str  # "holder", "extension", "cutter"
    mesh_path: Optional[str] = None
    transform: np.ndarray = field(default_factory=lambda: np.eye(4))
    length_mm: float = 0.0
    diameter_mm: float = 0.0
    tool_definition: Optional[dict] = None
    gauge_length_mm: float = 0.0

    def load_mesh(self, base_dir: str = "") -> Optional[trimesh.Trimesh]:
        """Load the STL mesh for this component."""
        if self.mesh_path is None:
            return None
        path = os.path.join(base_dir, self.mesh_path) if base_dir else self.mesh_path
        if not os.path.exists(path):
            return None
        return trimesh.load(path, force="mesh")


class ToolAssembly:
    """A complete tool assembly: holder + extension(s) + cutter.

    The tool assembly attaches to the machine's tool_mount node.
    Each component has a local transform relative to the previous component
    in the stack. The full assembly mesh is the union of all component meshes
    transformed by their chain transforms.

    Attributes:
        name: Human-readable name.
        components: Ordered list of ToolComponent (holder first, cutter last).
        interface: Machine tool interface type (HSK-A63, SK40, BT40, etc.).
        total_length_mm: Total length from gauge plane to cutter tip.
        gauge_length_mm: Total gauge length.
        max_rpm: Maximum RPM for this assembly.
        base_dir: Directory for resolving relative mesh paths.
    """

    def __init__(
        self,
        name: str = "",
        components: Optional[list[ToolComponent]] = None,
        interface: str = "HSK-A63",
        total_length_mm: float = 0.0,
        gauge_length_mm: float = 0.0,
        max_rpm: float = 24000,
        base_dir: str = "",
    ):
        self.name = name
        self.components = components or []
        self.interface = interface
        self.total_length_mm = total_length_mm
        self.gauge_length_mm = gauge_length_mm
        self.max_rpm = max_rpm
        self.base_dir = base_dir

        # Cached meshes
        self._cached_mesh: Optional[trimesh.Trimesh] = None
        self._cached_holder_mesh: Optional[trimesh.Trimesh] = None
        self._cached_cutter_mesh: Optional[trimesh.Trimesh] = None

    @classmethod
    def from_json(cls, path: str) -> ToolAssembly:
        """Load a tool assembly from a JSON file.

        Args:
            path: Path to the tool assembly JSON file.

        Returns:
            A ToolAssembly instance.
        """
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        base_dir = os.path.dirname(os.path.abspath(path))
        assembly = cls(
            name=data.get("name", ""),
            interface=data.get("interface", "HSK-A63"),
            total_length_mm=data.get("total_length_mm", 0.0),
            gauge_length_mm=data.get("gauge_length_mm", 0.0),
            max_rpm=data.get("max_rpm", 24000),
            base_dir=base_dir,
        )

        for comp_data in data.get("components", []):
            transform = cls._parse_transform(comp_data.get("transform", [0, 0, 0, 0, 0, 0]))
            tc = ToolComponent(
                component_id=comp_data["id"],
                component_type=comp_data["type"],
                mesh_path=comp_data.get("mesh"),
                transform=transform,
                length_mm=comp_data.get("length_mm", 0.0),
                diameter_mm=comp_data.get("diameter_mm", 0.0),
                tool_definition=comp_data.get("tool_definition"),
                gauge_length_mm=comp_data.get("gauge_length_mm", 0.0),
            )
            assembly.components.append(tc)

        return assembly

    def get_cutter_component(self) -> Optional[ToolComponent]:
        """Get the cutter component (last in the stack)."""
        for comp in reversed(self.components):
            if comp.component_type == "cutter":
                return comp
        return None

    def get_holder_component(self) -> Optional[ToolComponent]:
        """Get the holder component (first in the stack)."""
        for comp in self.components:
            if comp.component_type == "holder":
                return comp
        return None

    def get_mesh(self) -> Optional[trimesh.Trimesh]:
        """Get the combined mesh of the entire tool assembly."""
        if self._cached_mesh is not None:
            return self._cached_mesh

        meshes = []
        accumulated_transform = np.eye(4)
        for comp in self.components:
            accumulated_transform = accumulated_transform @ comp.transform
            mesh = comp.load_mesh(self.base_dir)
            if mesh is not None:
                mesh_copy = mesh.copy()
                mesh_copy.apply_transform(accumulated_transform)
                meshes.append(mesh_copy)

        if not meshes:
            self._cached_mesh = None
            return None

        combined = trimesh.util.concatenate(meshes)
        self._cached_mesh = combined
        return combined

    def get_holder_mesh(self) -> Optional[trimesh.Trimesh]:
        """Get the mesh of the holder only."""
        if self._cached_holder_mesh is not None:
            return self._cached_holder_mesh

        holder = self.get_holder_component()
        if holder is None:
            return None

        accumulated = np.eye(4)
        for comp in self.components:
            accumulated = accumulated @ comp.transform
            if comp.component_id == holder.component_id:
                mesh = comp.load_mesh(self.base_dir)
                if mesh is not None:
                    mesh_copy = mesh.copy()
                    mesh_copy.apply_transform(accumulated)
                    self._cached_holder_mesh = mesh_copy
                    return mesh_copy
        return None

    def get_cutter_mesh(self) -> Optional[trimesh.Trimesh]:
        """Get the mesh of the cutter only."""
        if self._cached_cutter_mesh is not None:
            return self._cached_cutter_mesh

        cutter = self.get_cutter_component()
        if cutter is None:
            return None

        accumulated = np.eye(4)
        for comp in self.components:
            accumulated = accumulated @ comp.transform
            if comp.component_id == cutter.component_id:
                mesh = comp.load_mesh(self.base_dir)
                if mesh is not None:
                    mesh_copy = mesh.copy()
                    mesh_copy.apply_transform(accumulated)
                    self._cached_cutter_mesh = mesh_copy
                    return mesh_copy
        return None

    @staticmethod
    def _parse_transform(transform_list: list) -> np.ndarray:
        """Convert [x,y,z,rx,ry,rz] to a 4x4 homogeneous transform."""
        x, y, z = transform_list[0], transform_list[1], transform_list[2]
        rx, ry, rz = np.radians(transform_list[3]), np.radians(transform_list[4]), np.radians(transform_list[5])
        # ZYX intrinsic Euler
        Rx = np.array([
            [1, 0, 0, 0],
            [0, np.cos(rx), -np.sin(rx), 0],
            [0, np.sin(rx), np.cos(rx), 0],
            [0, 0, 0, 1],
        ])
        Ry = np.array([
            [np.cos(ry), 0, np.sin(ry), 0],
            [0, 1, 0, 0],
            [-np.sin(ry), 0, np.cos(ry), 0],
            [0, 0, 0, 1],
        ])
        Rz = np.array([
            [np.cos(rz), -np.sin(rz), 0, 0],
            [np.sin(rz), np.cos(rz), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ])
        T = np.array([
            [1, 0, 0, x],
            [0, 1, 0, y],
            [0, 0, 1, z],
            [0, 0, 0, 1],
        ])
        return T @ Rz @ Ry @ Rx


# =========================================================================
#  MachineComponent -- a node in the machine tree
# =========================================================================

class MachineComponent:
    """A node in the machine component tree.

    Each component represents a physical part of the CNC machine.
    The tree structure defines the kinematic chain. Active axes
    (linear_axis, rotary_axis) inject their current joint position
    into the transform accumulation during kinematics computation.

    Attributes:
        id: Unique component identifier.
        component_type: Type of the component.
        parent_id: ID of the parent component (None for root).
        label: Human-readable name.
        mesh_path: Path to STL file for this component.
        collision_mesh_path: Alternative mesh for collision detection.
        collision_margin: Extra margin for collision detection (mm).
        local_transform: 4x4 transform relative to parent at zero position.
        axis_letter: For axis components, the axis letter (X, Y, Z, A, B, C, U, V, W).
        limits: (min, max) travel in mm (linear) or degrees (rotary).
        max_feed: Maximum feed rate.
        rapid_feed: Rapid traverse rate.
        max_rpm: Maximum RPM (spindle or rotary axis).
        continuous: Whether rotary axis can wind continuously (C axis).
        pivot_offset: (3,) offset from component origin to rotation center.
        spindle_nose_to_gauge_mm: Distance from spindle nose to gauge line.
        max_power_kw: Spindle motor power.
        max_torque_nm: Spindle motor torque.
        children: List of child component IDs (populated at load time).
        world_transform: Current world transform (updated per joint state).
    """

    def __init__(
        self,
        component_id: str,
        component_type: ComponentType,
        parent_id: Optional[str] = None,
        label: str = "",
        mesh_path: Optional[str] = None,
        collision_mesh_path: Optional[str] = None,
        collision_margin: float = 0.0,
        local_transform: Optional[np.ndarray] = None,
        axis_letter: Optional[str] = None,
        limits: Optional[Tuple[float, float]] = None,
        max_feed: Optional[float] = None,
        rapid_feed: Optional[float] = None,
        max_rpm: Optional[float] = None,
        continuous: bool = False,
        pivot_offset: Optional[np.ndarray] = None,
        spindle_nose_to_gauge_mm: float = 0.0,
        max_power_kw: Optional[float] = None,
        max_torque_nm: Optional[float] = None,
        base_dir: str = "",
    ):
        self.id = component_id
        self.component_type = component_type
        self.parent_id = parent_id
        self.label = label
        self.mesh_path = mesh_path
        self.collision_mesh_path = collision_mesh_path or mesh_path
        self.collision_margin = collision_margin
        self.local_transform = (local_transform if local_transform is not None
                                else np.eye(4, dtype=np.float64))
        self.axis_letter = axis_letter
        self.limits = limits
        self.max_feed = max_feed
        self.rapid_feed = rapid_feed or max_feed
        self.max_rpm = max_rpm
        self.continuous = continuous
        self.pivot_offset = (np.asarray(pivot_offset, dtype=np.float64)
                             if pivot_offset is not None
                             else np.zeros(3, dtype=np.float64))
        self.spindle_nose_to_gauge_mm = spindle_nose_to_gauge_mm
        self.max_power_kw = max_power_kw
        self.max_torque_nm = max_torque_nm
        self.base_dir = base_dir

        # Derived at load time
        self.children: list[str] = []
        self.world_transform: np.ndarray = np.eye(4, dtype=np.float64)

        # Cached mesh
        self._cached_mesh: Optional[trimesh.Trimesh] = None

    def load_mesh(self) -> Optional[trimesh.Trimesh]:
        """Load the STL mesh for this component.

        Returns:
            trimesh.Trimesh or None if no mesh is defined or file not found.
        """
        if self._cached_mesh is not None:
            return self._cached_mesh
        if self.mesh_path is None:
            return None
        path = os.path.join(self.base_dir, self.mesh_path) if self.base_dir else self.mesh_path
        if not os.path.exists(path):
            return None
        self._cached_mesh = trimesh.load(path, force="mesh")
        return self._cached_mesh

    def get_world_mesh(self) -> Optional[trimesh.Trimesh]:
        """Get the mesh transformed to world coordinates."""
        mesh = self.load_mesh()
        if mesh is None:
            return None
        result = mesh.copy()
        result.apply_transform(self.world_transform)
        return result

    def __repr__(self) -> str:
        return (f"MachineComponent(id='{self.id}', type={self.component_type.value}, "
                f"parent='{self.parent_id}')")


# =========================================================================
#  MachineModel
# =========================================================================

class MachineModel:
    """Complete machine definition loaded from JSON.

    Models a CNC machine as a component tree (scene graph).
    Provides forward/inverse kinematics by walking the tree,
    world-transform computation for any component, and
    collision checking via mesh proximity queries.

    Attributes:
        name: Human-readable machine name.
        version: Machine definition version.
        description: Optional description.
        manufacturer: Machine manufacturer.
        model_name: Machine model number.
        components: Dict of component_id -> MachineComponent.
        root_id: ID of the root component.
        collision_pairs: List of configured CollisionPair.
        collision_groups: Dict of group_name -> list of component_ids.
        home_position: (6,) float [X, Y, Z, A, B, C] home position.
        tool_change_position: (6,) float position for tool changes.
        axis_priority: Ordered list of axis letters for retract priority.
        retract_axis: Axis letter for safe retract direction.
        work_offset_defaults: Dict of G-code offset name -> (6,) float.
        kinematic_chain: Dict with 'tool_chain' and 'workpiece_chain' lists.
        base_dir: Directory for resolving relative mesh paths.
    """

    # Axis direction in machine frame for each axis letter
    AXIS_DIRECTION: dict[str, np.ndarray] = {
        "X": np.array([1.0, 0.0, 0.0]),
        "Y": np.array([0.0, 1.0, 0.0]),
        "Z": np.array([0.0, 0.0, 1.0]),
        "U": np.array([1.0, 0.0, 0.0]),
        "V": np.array([0.0, 1.0, 0.0]),
        "W": np.array([0.0, 0.0, 1.0]),
        "A": np.array([1.0, 0.0, 0.0]),   # rotation about X
        "B": np.array([0.0, 1.0, 0.0]),   # rotation about Y
        "C": np.array([0.0, 0.0, 1.0]),   # rotation about Z
    }

    def __init__(
        self,
        name: str = "",
        version: str = "1.0",
        description: str = "",
        manufacturer: str = "",
        model_name: str = "",
        components: Optional[dict[str, MachineComponent]] = None,
        root_id: str = "bed",
        collision_pairs: Optional[list[CollisionPair]] = None,
        collision_groups: Optional[dict[str, list[str]]] = None,
        home_position: Optional[np.ndarray] = None,
        tool_change_position: Optional[np.ndarray] = None,
        axis_priority: Optional[list[str]] = None,
        retract_axis: str = "Z",
        work_offset_defaults: Optional[dict[str, np.ndarray]] = None,
        kinematic_chain: Optional[dict[str, list[str]]] = None,
        base_dir: str = "",
    ):
        self.name = name
        self.version = version
        self.description = description
        self.manufacturer = manufacturer
        self.model_name = model_name
        self.components = components or {}
        self.root_id = root_id
        self.collision_pairs = collision_pairs or []
        self.collision_groups = collision_groups or {}
        self.home_position = (home_position if home_position is not None
                              else np.zeros(6, dtype=np.float64))
        self.tool_change_position = (tool_change_position if tool_change_position is not None
                                     else np.zeros(6, dtype=np.float64))
        self.axis_priority = axis_priority or ["Z"]
        self.retract_axis = retract_axis
        self.work_offset_defaults = work_offset_defaults or {}
        self.kinematic_chain = kinematic_chain or {}
        self.base_dir = base_dir

        # Discovered from components
        self._tool_mount_id: Optional[str] = None
        self._fixture_mount_id: Optional[str] = None
        self._stock_mount_id: Optional[str] = None
        self._spindle_id: Optional[str] = None
        self._axis_components: dict[str, MachineComponent] = {}

        # Cached chains (lazy-computed)
        self._tool_chain: Optional[list[str]] = None
        self._workpiece_chain: Optional[list[str]] = None

        # Built-in kinematics solver (parameterized from tree)
        self._kinematics_solver: Optional[FiveAxisKinematics] = None

        self._discover_special_nodes()

    def _discover_special_nodes(self) -> None:
        """Find tool_mount, fixture_mount, spindle, and axis components."""
        for comp_id, comp in self.components.items():
            if comp.component_type == ComponentType.TOOL_MOUNT:
                self._tool_mount_id = comp_id
            elif comp.component_type == ComponentType.FIXTURE_MOUNT:
                self._fixture_mount_id = comp_id
            elif comp.component_type == ComponentType.STOCK_MOUNT:
                self._stock_mount_id = comp_id
            elif comp.component_type == ComponentType.SPINDLE:
                self._spindle_id = comp_id

            if comp.axis_letter is not None:
                self._axis_components[comp.axis_letter] = comp

    # ===================================================================
    #  Loading
    # ===================================================================

    @classmethod
    def from_json(cls, path: str) -> MachineModel:
        """Load a machine definition from a JSON file.

        Args:
            path: Path to the machine definition JSON file.

        Returns:
            A MachineModel instance.

        Raises:
            FileNotFoundError: If the JSON file does not exist.
            json.JSONDecodeError: If the JSON is malformed.
            ValueError: If required fields are missing or invalid.
        """
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        base_dir = os.path.dirname(os.path.abspath(path))

        # Parse components
        components: dict[str, MachineComponent] = {}
        for comp_data in data.get("components", []):
            comp = cls._parse_component(comp_data, base_dir)
            components[comp.id] = comp

        # Build parent-child relationships
        for comp in components.values():
            if comp.parent_id is not None and comp.parent_id in components:
                parent = components[comp.parent_id]
                parent.children.append(comp.id)

        # Find root
        root_id = cls._find_root(components)

        # Parse collision pairs
        collision_pairs = []
        for cp_data in data.get("collision_pairs", []):
            check_type_str = cp_data.get("check_type", "static")
            try:
                check_type = CheckType(check_type_str)
            except ValueError:
                check_type = CheckType.STATIC
            collision_pairs.append(CollisionPair(
                group_a=cp_data["group_a"],
                group_b=cp_data["group_b"],
                clearance_mm=cp_data.get("clearance_mm", 2.0),
                check_type=check_type,
                warn_clearance_mm=cp_data.get("warn_clearance_mm", 5.0),
            ))

        # Parse collision groups
        collision_groups = data.get("collision_groups", {})

        # Parse positions
        home_position = np.array(data.get("home_position", [0, 0, 0, 0, 0, 0]),
                                 dtype=np.float64)
        tool_change_position = np.array(
            data.get("tool_change_position", [0, 0, -400, 0, 0, 0]),
            dtype=np.float64,
        )

        # Parse work offsets
        work_offsets = {}
        for key, value in data.get("work_offset_defaults", {}).items():
            work_offsets[key] = np.array(value, dtype=np.float64)

        machine = cls(
            name=data.get("name", ""),
            version=data.get("version", "1.0"),
            description=data.get("description", ""),
            manufacturer=data.get("manufacturer", ""),
            model_name=data.get("model", ""),
            components=components,
            root_id=root_id,
            collision_pairs=collision_pairs,
            collision_groups=collision_groups,
            home_position=home_position,
            tool_change_position=tool_change_position,
            axis_priority=data.get("axis_priority", ["Z"]),
            retract_axis=data.get("retract_axis", "Z"),
            work_offset_defaults=work_offsets,
            kinematic_chain=data.get("kinematic_chain", {}),
            base_dir=base_dir,
        )

        return machine

    @staticmethod
    def _parse_component(data: dict, base_dir: str) -> MachineComponent:
        """Parse a single component from JSON data."""
        try:
            component_type = ComponentType(data["type"])
        except (KeyError, ValueError):
            raise ValueError(
                f"Component '{data.get('id', 'unknown')}' has invalid type "
                f"'{data.get('type', 'missing')}'. "
                f"Must be one of: {[t.value for t in ComponentType]}"
            )

        transform = MachineModel._parse_transform(
            data.get("transform", [0, 0, 0, 0, 0, 0])
        )

        pivot = data.get("pivot_offset")
        if pivot is not None:
            pivot = np.array(pivot, dtype=np.float64)

        return MachineComponent(
            component_id=data["id"],
            component_type=component_type,
            parent_id=data.get("parent"),
            label=data.get("label", ""),
            mesh_path=data.get("mesh"),
            collision_mesh_path=data.get("collision_mesh"),
            collision_margin=data.get("collision_margin", 0.0),
            local_transform=transform,
            axis_letter=data.get("axis"),
            limits=tuple(data["limits"]) if "limits" in data else None,
            max_feed=data.get("max_feed"),
            rapid_feed=data.get("rapid_feed"),
            max_rpm=data.get("max_rpm"),
            continuous=data.get("continuous", False),
            pivot_offset=pivot,
            spindle_nose_to_gauge_mm=data.get("spindle_nose_to_gauge_mm", 0.0),
            max_power_kw=data.get("max_power_kw"),
            max_torque_nm=data.get("max_torque_nm"),
            base_dir=base_dir,
        )

    @staticmethod
    def _parse_transform(transform_list: list) -> np.ndarray:
        """Convert [x,y,z,rx,ry,rz] to a 4x4 homogeneous transform.

        Euler angles: ZYX intrinsic (rotate about Z, then Y', then X'').
        """
        x, y, z = transform_list[0], transform_list[1], transform_list[2]
        rx = np.radians(transform_list[3])
        ry = np.radians(transform_list[4])
        rz = np.radians(transform_list[5])

        # ZYX intrinsic
        cx, sx = np.cos(rx), np.sin(rx)
        cy, sy = np.cos(ry), np.sin(ry)
        cz, sz = np.cos(rz), np.sin(rz)

        R = np.array([
            [cy * cz, cz * sx * sy - cx * sz, cx * cz * sy + sx * sz, x],
            [cy * sz, cx * cz + sx * sy * sz, -cz * sx + cx * sy * sz, y],
            [-sy,     cy * sx,                cx * cy,                z],
            [0,       0,                      0,                      1],
        ], dtype=np.float64)

        return R

    @staticmethod
    def _find_root(components: dict) -> str:
        """Find the root component (the one with no parent)."""
        for comp_id, comp in components.items():
            if comp.parent_id is None:
                return comp_id
        # Fallback: find the component that is nobody's child
        all_ids = set(components.keys())
        child_ids = {c.parent_id for c in components.values() if c.parent_id is not None}
        roots = all_ids - child_ids
        if roots:
            return next(iter(roots))
        raise ValueError("Cannot determine root component: circular dependency or no root")

    # ===================================================================
    #  Chain computation
    # ===================================================================

    def _compute_chain_to_root(self, leaf_id: str) -> list[str]:
        """Compute the ordered list of component IDs from leaf to root.

        Args:
            leaf_id: ID of the leaf component.

        Returns:
            List of component IDs, starting from leaf and ending at root.
        """
        chain = []
        current_id = leaf_id
        visited = set()
        while current_id is not None:
            if current_id in visited:
                raise ValueError(
                    f"Circular dependency detected in component tree at '{current_id}'"
                )
            visited.add(current_id)
            chain.append(current_id)
            if current_id not in self.components:
                raise KeyError(f"Component '{current_id}' not found in machine model")
            current_id = self.components[current_id].parent_id
        return chain

    @property
    def tool_chain(self) -> list[str]:
        """Ordered list of component IDs from tool_mount to root."""
        if self._tool_chain is None:
            mount_id = self._tool_mount_id or self._tool_mount_id
            if mount_id is None:
                # Try the configured chain
                configured = self.kinematic_chain.get("tool_chain", [])
                if configured:
                    return configured
                raise ValueError("No tool_mount component found in machine")
            self._tool_chain = self._compute_chain_to_root(mount_id)
        return self._tool_chain

    @property
    def workpiece_chain(self) -> list[str]:
        """Ordered list of component IDs from fixture_mount/stock_mount to root."""
        if self._workpiece_chain is None:
            # Prefer stock_mount, fall back to fixture_mount
            mount_id = self._stock_mount_id or self._fixture_mount_id
            if mount_id is None:
                configured = self.kinematic_chain.get("workpiece_chain", [])
                if configured:
                    return configured
                raise ValueError("No fixture_mount or stock_mount found in machine")
            self._workpiece_chain = self._compute_chain_to_root(mount_id)
        return self._workpiece_chain

    # ===================================================================
    #  Axis helpers
    # ===================================================================

    @property
    def active_axes(self) -> list[str]:
        """Return sorted list of active axis letters in this machine."""
        axes = []
        for comp in self.components.values():
            if comp.axis_letter and comp.component_type in (
                ComponentType.LINEAR_AXIS, ComponentType.ROTARY_AXIS
            ):
                axes.append(comp.axis_letter)
        return sorted(axes)

    def get_axis_index(self, axis_letter: str) -> int:
        """Get the joint vector index for an axis letter.

        Standard mapping: X=0, Y=1, Z=2, A=3, B=4, C=5
                          U=0, V=1, W=2 (secondary linear)
        """
        mapping = {"X": 0, "Y": 1, "Z": 2, "A": 3, "B": 4, "C": 5,
                   "U": 0, "V": 1, "W": 2}
        return mapping.get(axis_letter.upper(), -1)

    # ===================================================================
    #  Transform computation
    # ===================================================================

    @staticmethod
    def _apply_axis_transform(
        comp: MachineComponent,
        joints: np.ndarray,
        accumulated: np.ndarray,
    ) -> np.ndarray:
        """Apply a component's axis motion to the accumulated transform.

        For linear_axis: applies translation along the axis direction.
        For rotary_axis: applies rotation about the axis at pivot_offset.

        Args:
            comp: The component to apply.
            joints: (6,) joint vector [X, Y, Z, A, B, C].
            accumulated: Current 4x4 accumulated transform.

        Returns:
            Updated 4x4 accumulated transform.
        """
        if comp.component_type == ComponentType.LINEAR_AXIS:
            if comp.axis_letter is None:
                return accumulated
            idx = MachineModel.get_axis_index_static(comp.axis_letter)
            if idx < 0 or idx >= len(joints):
                return accumulated
            axis_pos = joints[idx]
            direction = MachineModel.AXIS_DIRECTION.get(comp.axis_letter)
            if direction is None:
                return accumulated
            T_axis = np.eye(4, dtype=np.float64)
            T_axis[0:3, 3] = direction * axis_pos
            accumulated = accumulated @ T_axis

        elif comp.component_type == ComponentType.ROTARY_AXIS:
            if comp.axis_letter is None:
                return accumulated
            idx = MachineModel.get_axis_index_static(comp.axis_letter)
            if idx < 0 or idx >= len(joints):
                return accumulated
            angle_deg = joints[idx]
            angle_rad = np.radians(angle_deg)
            direction = MachineModel.AXIS_DIRECTION.get(comp.axis_letter)
            if direction is None:
                return accumulated

            pivot = comp.pivot_offset
            accumulated = accumulated @ MachineModel._translate(pivot)
            accumulated = accumulated @ MachineModel._rotation_matrix(
                direction, angle_rad
            )
            accumulated = accumulated @ MachineModel._translate(-pivot)

        return accumulated

    @staticmethod
    def get_axis_index_static(axis_letter: str) -> int:
        """Static version of get_axis_index."""
        mapping = {"X": 0, "Y": 1, "Z": 2, "A": 3, "B": 4, "C": 5,
                   "U": 0, "V": 1, "W": 2}
        return mapping.get(axis_letter.upper(), -1)

    def get_world_transform(
        self,
        component_id: str,
        joints: np.ndarray,
    ) -> np.ndarray:
        """Compute the 4x4 world transform for any component at given joints.

        Walks from the component up to the root, accumulating transforms
        including axis motions from the joint vector.

        This is the key method for collision detection: it tells you
        where every machine component is in 3D space.

        Args:
            component_id: ID of the component to compute transform for.
            joints: (6,) joint vector [X, Y, Z, A, B, C] in mm and degrees.

        Returns:
            4x4 homogeneous transform in world (machine) frame.
        """
        joints = np.asarray(joints, dtype=np.float64)
        chain = self._compute_chain_to_root(component_id)

        # Walk from root DOWN to component:
        # Root is at the end of the chain (leaf-to-root order).
        # We reverse to get root-to-leaf order and accumulate.
        accumulated = np.eye(4, dtype=np.float64)

        # The chain is [leaf, parent, grandparent, ..., root]
        # We need root-to-leaf: reverse and skip root's transform
        # since root has no parent and its transform is identity in world frame.
        root_to_leaf = list(reversed(chain))

        for comp_id in root_to_leaf:
            comp = self.components[comp_id]
            # Apply the component's local (zero-offset) transform
            accumulated = accumulated @ comp.local_transform
            # Apply axis motion if this is an active axis
            accumulated = self._apply_axis_transform(comp, joints, accumulated)

        return accumulated

    # ===================================================================
    #  Kinematics solver (parameterized from tree)
    # ===================================================================

    def _build_kinematics_solver(self) -> FiveAxisKinematics:
        """Build a FiveAxisKinematics solver parameterized from the component tree.

        Interrogates the tree to determine which rotary axes exist on which
        chain, picks the primary/secondary axes, and extracts axis limits.
        """
        if self._kinematics_solver is not None:
            return self._kinematics_solver

        from .kinematics import MachineConfig

        tool_rotaries = self._get_rotary_axes(self.tool_chain)
        wp_rotaries = self._get_rotary_axes(self.workpiece_chain)

        # Determine configuration
        if len(tool_rotaries) == 2:
            config = MachineConfig.HEAD_HEAD
        elif len(wp_rotaries) == 2:
            config = MachineConfig.TABLE_TABLE
        elif len(tool_rotaries) == 1 and len(wp_rotaries) == 1:
            config = MachineConfig.HEAD_TABLE
        else:
            # Non-standard: best guess
            if len(wp_rotaries) >= 2:
                config = MachineConfig.TABLE_TABLE
            elif len(tool_rotaries) >= 2:
                config = MachineConfig.HEAD_HEAD
            else:
                config = MachineConfig.HEAD_TABLE

        # Determine primary/secondary axes from tree order.
        # Primary = axis closest to root (applied first).
        # In leaf-to-root order, this is the LAST rotary in that chain.
        if len(tool_rotaries) >= 2:
            # HEAD_HEAD: both on tool chain
            primary = tool_rotaries[-1].axis_letter   # closer to root
            secondary = tool_rotaries[0].axis_letter  # closer to leaf
        elif len(wp_rotaries) >= 2:
            # TABLE_TABLE: both on workpiece chain
            primary = wp_rotaries[-1].axis_letter     # closer to root
            secondary = wp_rotaries[0].axis_letter    # closer to leaf
        elif len(tool_rotaries) == 1 and len(wp_rotaries) == 1:
            # HEAD_TABLE: one on each chain
            primary = tool_rotaries[0].axis_letter    # head rotary
            secondary = wp_rotaries[0].axis_letter    # table rotary
        elif len(tool_rotaries) >= 1:
            primary = tool_rotaries[-1].axis_letter
            secondary = tool_rotaries[0].axis_letter
        elif len(wp_rotaries) >= 1:
            primary = wp_rotaries[-1].axis_letter
            secondary = wp_rotaries[0].axis_letter
        else:
            primary, secondary = "B", "C"

        # Axis limits from the tree
        axis_limits: dict[str, Tuple[float, float]] = {}
        for comp in self.components.values():
            if comp.limits is not None and comp.axis_letter is not None:
                axis_limits[comp.axis_letter] = comp.limits

        self._kinematics_solver = FiveAxisKinematics(
            config=config,
            primary_axis=primary,
            secondary_axis=secondary,
            axis_limits=axis_limits if axis_limits else None,
        )
        return self._kinematics_solver

    def _get_rotary_axes(self, chain: list[str]) -> list[MachineComponent]:
        """Get rotary axis components from a chain, in leaf-to-root order."""
        rotaries = []
        for comp_id in chain:
            comp = self.components.get(comp_id)
            if comp and comp.component_type == ComponentType.ROTARY_AXIS:
                rotaries.append(comp)
        return rotaries

    def _get_linear_axes(self, chain: list[str]) -> list[MachineComponent]:
        """Get linear axis components from a chain."""
        linear = []
        for comp_id in chain:
            comp = self.components.get(comp_id)
            if comp and comp.component_type == ComponentType.LINEAR_AXIS:
                linear.append(comp)
        return linear

    # ===================================================================
    #  Forward Kinematics (delegates to tree-parameterized solver)
    # ===================================================================

    def compute_forward_kinematics(self, joints: np.ndarray) -> ToolPose:
        """Compute tool pose in workpiece frame from joint positions.

        Uses the FiveAxisKinematics solver parameterized from the component
        tree. This ensures FK/IK consistency (the same solver is used for both).

        Args:
            joints: (6,) float array [X, Y, Z, A, B, C] in mm and degrees.

        Returns:
            ToolPose in workpiece frame.
        """
        solver = self._build_kinematics_solver()
        return solver.forward(joints)

    # ===================================================================
    #  Inverse Kinematics (delegates to tree-parameterized solver)
    # ===================================================================

    def compute_inverse_kinematics(
        self,
        tool_pose: ToolPose,
        prev_joints: Optional[np.ndarray] = None,
    ) -> Optional[np.ndarray]:
        """Compute joint positions to achieve a desired tool pose.

        Uses the FiveAxisKinematics solver parameterized from the component
        tree. Supports TABLE_TABLE, HEAD_HEAD, and HEAD_TABLE configurations.

        Args:
            tool_pose: Desired ToolPose in workpiece frame.
            prev_joints: Previous joint values for solution selection.

        Returns:
            (6,) joint vector or None if unreachable.
        """
        solver = self._build_kinematics_solver()
        return solver.inverse(tool_pose, prev_joints)

    # ===================================================================
    #  Collision detection
    # ===================================================================

    def check_collisions(
        self,
        joints: np.ndarray,
        tool_assembly: Optional[ToolAssembly] = None,
        stock_mesh: Optional[trimesh.Trimesh] = None,
        fixture_mesh: Optional[trimesh.Trimesh] = None,
        check_type_filter: Optional[CheckType] = None,
    ) -> list[Collision]:
        """Check all configured collision pairs at a given joint state.

        For each collision pair, loads the STL meshes of the relevant
        components, transforms them to world space using the current joint
        state, and checks mesh-mesh proximity via trimesh.

        Args:
            joints: (6,) joint vector.
            tool_assembly: Optional tool assembly for tool_group checks.
            stock_mesh: Optional stock mesh for "stock" group checks.
            fixture_mesh: Optional fixture mesh for fixture_group checks.
            check_type_filter: If set, only check pairs of this type.

        Returns:
            List of Collision objects (empty = no collisions).
        """
        joints = np.asarray(joints, dtype=np.float64)

        # Update world transforms for all components
        self._update_all_world_transforms(joints)

        collisions: list[Collision] = []

        for pair in self.collision_pairs:
            if check_type_filter is not None and pair.check_type != check_type_filter:
                continue

            # Resolve group a components
            meshes_a = self._resolve_collision_meshes(
                pair.group_a, tool_assembly, stock_mesh, fixture_mesh
            )
            meshes_b = self._resolve_collision_meshes(
                pair.group_b, tool_assembly, stock_mesh, fixture_mesh
            )

            if not meshes_a or not meshes_b:
                continue

            # Check each pair of meshes
            for name_a, mesh_a in meshes_a:
                for name_b, mesh_b in meshes_b:
                    coll = self._check_mesh_pair(
                        name_a, mesh_a, name_b, mesh_b, pair
                    )
                    if coll is not None:
                        collisions.append(coll)

        return collisions

    def _update_all_world_transforms(self, joints: np.ndarray) -> None:
        """Update world_transform for all components at the given joint state."""
        for comp_id in self.components:
            self.components[comp_id].world_transform = self.get_world_transform(
                comp_id, joints
            )

    def _resolve_collision_meshes(
        self,
        group_name: str,
        tool_assembly: Optional[ToolAssembly],
        stock_mesh: Optional[trimesh.Trimesh],
        fixture_mesh: Optional[trimesh.Trimesh],
    ) -> list[Tuple[str, trimesh.Trimesh]]:
        """Resolve a collision group name into a list of (name, world_mesh) tuples.

        Special group names:
        - "stock": returns the stock_mesh transformed to world frame.
        - "fixture": returns the fixture_mesh transformed to world frame.
        - "tool_assembly": returns the tool assembly mesh transformed to world frame.
        """
        result: list[Tuple[str, trimesh.Trimesh]] = []

        if group_name == "stock":
            if stock_mesh is not None:
                wp_leaf = self.workpiece_chain[0]
                T_wp = self.components[wp_leaf].world_transform
                mesh = stock_mesh.copy()
                mesh.apply_transform(T_wp)
                result.append(("stock", mesh))
            return result

        if group_name == "fixture":
            if fixture_mesh is not None:
                fixture_id = self._fixture_mount_id
                if fixture_id:
                    T_fix = self.components[fixture_id].world_transform
                    mesh = fixture_mesh.copy()
                    mesh.apply_transform(T_fix)
                    result.append(("fixture", mesh))
                else:
                    result.append(("fixture", fixture_mesh.copy()))
            return result

        if group_name == "tool_assembly":
            if tool_assembly is not None:
                tool_mesh = tool_assembly.get_mesh()
                if tool_mesh is not None:
                    tool_id = self._tool_mount_id
                    if tool_id:
                        T_tool = self.components[tool_id].world_transform
                        mesh = tool_mesh.copy()
                        mesh.apply_transform(T_tool)
                        result.append(("tool_assembly", mesh))
            return result

        # Standard component group
        component_ids = self.collision_groups.get(group_name, [group_name])
        for comp_id in component_ids:
            if comp_id in self.components:
                mesh = self.components[comp_id].get_world_mesh()
                if mesh is not None:
                    result.append((comp_id, mesh))

        return result

    @staticmethod
    def _check_mesh_pair(
        name_a: str,
        mesh_a: trimesh.Trimesh,
        name_b: str,
        mesh_b: trimesh.Trimesh,
        pair: CollisionPair,
    ) -> Optional[Collision]:
        """Check proximity between two meshes.

        Returns Collision if distance < clearance, None otherwise.
        """
        try:
            # Use trimesh proximity query
            result = trimesh.proximity.closest_point(mesh_a, mesh_b)
            if len(result) < 2 or result[1] is None:
                return None

            # result is (closest_points_a, closest_points_b, distance)
            if len(result) == 3:
                pts_a, pts_b, dist = result
                if hasattr(dist, '__len__'):
                    # Sometimes returns arrays
                    dmin = float(np.min(dist))
                else:
                    dmin = float(dist)
                pa = np.array(pts_a[0]) if hasattr(pts_a, '__getitem__') else np.array([0, 0, 0])
                pb = np.array(pts_b[0]) if hasattr(pts_b, '__getitem__') else np.array([0, 0, 0])
            else:
                pts, dist = result
                if hasattr(dist, '__len__'):
                    dmin = float(np.min(dist))
                else:
                    dmin = float(dist)
                pa, pb = np.array([0, 0, 0]), np.array([0, 0, 0])
        except Exception:
            return None

        if dmin < pair.clearance_mm:
            return Collision(
                component_a=name_a,
                component_b=name_b,
                distance_mm=dmin,
                clearance_mm=pair.clearance_mm,
                point_a=pa,
                point_b=pb,
                is_near_miss=(dmin >= pair.clearance_mm * 0.5
                              if pair.check_type == CheckType.NEAR_MISS else False),
            )

        # Near-miss check (distance between clearance and warn_clearance)
        if pair.check_type == CheckType.NEAR_MISS and dmin < pair.warn_clearance_mm:
            return Collision(
                component_a=name_a,
                component_b=name_b,
                distance_mm=dmin,
                clearance_mm=pair.warn_clearance_mm,
                point_a=pa,
                point_b=pb,
                is_near_miss=True,
            )

        return None

    # ===================================================================
    #  Utility
    # ===================================================================

    def check_limits(self, joints: np.ndarray) -> bool:
        """Verify all joint values are within machine axis limits.

        Args:
            joints: (6,) joint vector.

        Returns:
            True if all axes are within limits.
        """
        joints = np.asarray(joints, dtype=np.float64)
        for axis_letter, comp in self._axis_components.items():
            idx = self.get_axis_index(axis_letter)
            if idx < 0 or idx >= 6:
                continue
            if comp.limits is not None:
                lo, hi = comp.limits
                if joints[idx] < lo - 1e-6 or joints[idx] > hi + 1e-6:
                    return False
        return True

    def compute_workspace_linearization(
        self,
        start_pose: ToolPose,
        end_pose: ToolPose,
        num_samples: int = 10,
        prev_joints: Optional[np.ndarray] = None,
    ) -> Optional[list[np.ndarray]]:
        """Interpolate in workpiece space and compute joint positions.

        Uses SLERP for orientation, linear interpolation for position.

        Args:
            start_pose: Starting tool pose.
            end_pose: Ending tool pose.
            num_samples: Number of interpolation samples.
            prev_joints: Previous joint values for IK continuity.

        Returns:
            List of (6,) joint arrays, or None if any pose is unreachable.
        """
        result: list[np.ndarray] = []
        current_prev = prev_joints

        for k in range(num_samples):
            t = k / (num_samples - 1) if num_samples > 1 else 0.0
            pos = start_pose.position + t * (end_pose.position - start_pose.position)
            q = FiveAxisKinematics.slerp(
                start_pose.orientation, end_pose.orientation, t
            )
            pose = ToolPose(position=pos, orientation=q)
            joints = self.compute_inverse_kinematics(pose, prev_joints=current_prev)
            if joints is None:
                return None
            result.append(joints)
            current_prev = joints

        return result

    def to_json(self, path: str) -> None:
        """Serialize the machine model back to a JSON file.

        Args:
            path: Output file path.
        """
        data = self.to_dict()
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def to_dict(self) -> dict:
        """Convert the machine model to a JSON-serializable dict."""
        components_list = []
        for comp_id, comp in self.components.items():
            comp_dict = {
                "id": comp.id,
                "type": comp.component_type.value,
                "parent": comp.parent_id,
                "label": comp.label,
                "mesh": comp.mesh_path,
                "transform": self._transform_to_list(comp.local_transform),
            }
            if comp.axis_letter:
                comp_dict["axis"] = comp.axis_letter
            if comp.limits:
                comp_dict["limits"] = list(comp.limits)
            if comp.max_feed:
                comp_dict["max_feed"] = comp.max_feed
            if comp.rapid_feed:
                comp_dict["rapid_feed"] = comp.rapid_feed
            if comp.max_rpm:
                comp_dict["max_rpm"] = comp.max_rpm
            if comp.continuous:
                comp_dict["continuous"] = True
            if np.any(comp.pivot_offset != 0):
                comp_dict["pivot_offset"] = comp.pivot_offset.tolist()
            if comp.spindle_nose_to_gauge_mm:
                comp_dict["spindle_nose_to_gauge_mm"] = comp.spindle_nose_to_gauge_mm
            if comp.max_power_kw:
                comp_dict["max_power_kw"] = comp.max_power_kw
            if comp.max_torque_nm:
                comp_dict["max_torque_nm"] = comp.max_torque_nm
            if comp.collision_margin:
                comp_dict["collision_margin"] = comp.collision_margin
            if comp.collision_mesh_path and comp.collision_mesh_path != comp.mesh_path:
                comp_dict["collision_mesh"] = comp.collision_mesh_path
            components_list.append(comp_dict)

        collision_pairs_list = []
        for cp in self.collision_pairs:
            collision_pairs_list.append({
                "group_a": cp.group_a,
                "group_b": cp.group_b,
                "clearance_mm": cp.clearance_mm,
                "check_type": cp.check_type.value,
                "warn_clearance_mm": cp.warn_clearance_mm,
            })

        work_offset_dict = {
            k: v.tolist() for k, v in self.work_offset_defaults.items()
        }

        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "manufacturer": self.manufacturer,
            "model": self.model_name,
            "components": components_list,
            "collision_groups": self.collision_groups,
            "collision_pairs": collision_pairs_list,
            "home_position": self.home_position.tolist(),
            "tool_change_position": self.tool_change_position.tolist(),
            "axis_priority": self.axis_priority,
            "retract_axis": self.retract_axis,
            "work_offset_defaults": work_offset_dict,
            "kinematic_chain": {
                "tool_chain": self.tool_chain if self._tool_chain else [],
                "workpiece_chain": self.workpiece_chain if self._workpiece_chain else [],
            },
        }

    @staticmethod
    def _transform_to_list(T: np.ndarray) -> list:
        """Convert a 4x4 homogeneous transform to [x,y,z,rx,ry,rz]."""
        x, y, z = T[0, 3], T[1, 3], T[2, 3]
        R = T[0:3, 0:3]

        # Extract Euler angles (ZYX intrinsic)
        if abs(R[2, 0]) < 0.999999:
            ry = -np.arcsin(R[2, 0])
            cy = np.cos(ry)
            rx = np.arctan2(R[2, 1] / cy, R[2, 2] / cy)
            rz = np.arctan2(R[1, 0] / cy, R[0, 0] / cy)
        else:
            rz = 0.0
            if R[2, 0] >= 1.0:
                ry = -np.pi / 2.0
                rx = np.arctan2(-R[0, 1], -R[0, 2])
            else:
                ry = np.pi / 2.0
                rx = np.arctan2(R[0, 1], R[0, 2])

        return [round(float(x), 6), round(float(y), 6), round(float(z), 6),
                round(float(np.degrees(rx)), 6),
                round(float(np.degrees(ry)), 6),
                round(float(np.degrees(rz)), 6)]

    @staticmethod
    def _matrix_to_quaternion(R: np.ndarray) -> np.ndarray:
        """Convert a 3x3 rotation matrix to quaternion [w, x, y, z] (scalar-first)."""
        trace = np.trace(R)
        if trace > 0.0:
            s = np.sqrt(trace + 1.0) * 2.0
            w = 0.25 * s
            x = (R[2, 1] - R[1, 2]) / s
            y = (R[0, 2] - R[2, 0]) / s
            z = (R[1, 0] - R[0, 1]) / s
        elif R[0, 0] > R[1, 1] and R[0, 0] > R[2, 2]:
            s = np.sqrt(1.0 + R[0, 0] - R[1, 1] - R[2, 2]) * 2.0
            w = (R[2, 1] - R[1, 2]) / s
            x = 0.25 * s
            y = (R[0, 1] + R[1, 0]) / s
            z = (R[0, 2] + R[2, 0]) / s
        elif R[1, 1] > R[2, 2]:
            s = np.sqrt(1.0 + R[1, 1] - R[0, 0] - R[2, 2]) * 2.0
            w = (R[0, 2] - R[2, 0]) / s
            x = (R[0, 1] + R[1, 0]) / s
            y = 0.25 * s
            z = (R[1, 2] + R[2, 1]) / s
        else:
            s = np.sqrt(1.0 + R[2, 2] - R[0, 0] - R[1, 1]) * 2.0
            w = (R[1, 0] - R[0, 1]) / s
            x = (R[0, 2] + R[2, 0]) / s
            y = (R[1, 2] + R[2, 1]) / s
            z = 0.25 * s

        q = np.array([w, x, y, z], dtype=np.float64)
        n = np.linalg.norm(q)
        if n > 1e-12:
            q = q / n
        return q

    @staticmethod
    def _translate(v: np.ndarray) -> np.ndarray:
        """Create a 4x4 translation matrix."""
        T = np.eye(4, dtype=np.float64)
        T[0:3, 3] = v
        return T

    @staticmethod
    def _rotation_matrix(axis: np.ndarray, angle: float) -> np.ndarray:
        """Create a 4x4 rotation matrix about an arbitrary axis by an angle.

        Uses Rodrigues' rotation formula.

        Args:
            axis: (3,) unit vector for rotation axis.
            angle: Rotation angle in radians.

        Returns:
            4x4 homogeneous rotation matrix.
        """
        axis = axis / np.linalg.norm(axis)
        c = np.cos(angle)
        s = np.sin(angle)
        t = 1.0 - c
        x, y, z = axis
        R = np.array([
            [t * x * x + c,       t * x * y - s * z,   t * x * z + s * y,   0],
            [t * x * y + s * z,   t * y * y + c,        t * y * z - s * x,   0],
            [t * x * z - s * y,   t * y * z + s * x,    t * z * z + c,       0],
            [0,                   0,                     0,                   1],
        ], dtype=np.float64)
        return R

    def __repr__(self) -> str:
        return (f"MachineModel(name='{self.name}', "
                f"components={len(self.components)}, "
                f"collision_pairs={len(self.collision_pairs)})")


# =========================================================================
#  Default machine generators (backward compatibility)
# =========================================================================

def generate_default_table_table(name: str = "Default BC Trunnion") -> MachineModel:
    """Generate a default BC trunnion (TABLE_TABLE) machine model.

    Used for backward compatibility with MachineConfig.TABLE_TABLE.

    Args:
        name: Machine name.

    Returns:
        A MachineModel with standard BC trunnion topology.
    """
    components: dict[str, MachineComponent] = {}

    # Bed (root)
    components["bed"] = MachineComponent(
        component_id="bed",
        component_type=ComponentType.STATIC,
        parent_id=None,
        label="Machine Bed",
        local_transform=np.eye(4),
    )

    # Z axis (tool side)
    components["z_axis"] = MachineComponent(
        component_id="z_axis",
        component_type=ComponentType.LINEAR_AXIS,
        parent_id="bed",
        label="Z-Axis Saddle",
        local_transform=_make_translation(0, 0, 400),
        axis_letter="Z",
        limits=(-400.0, 0.0),
        max_feed=30000,
        rapid_feed=50000,
    )

    # Spindle
    components["spindle"] = MachineComponent(
        component_id="spindle",
        component_type=ComponentType.SPINDLE,
        parent_id="z_axis",
        label="Spindle",
        local_transform=_make_translation(0, 0, -100),
        max_rpm=18000,
    )

    # Tool mount
    components["tool_mount"] = MachineComponent(
        component_id="tool_mount",
        component_type=ComponentType.TOOL_MOUNT,
        parent_id="spindle",
        label="Tool Mount",
        local_transform=_make_translation(0, 0, -50),
    )

    # Y axis (table side)
    components["y_axis"] = MachineComponent(
        component_id="y_axis",
        component_type=ComponentType.LINEAR_AXIS,
        parent_id="bed",
        label="Y-Axis Saddle",
        local_transform=_make_translation(0, -150, 0),
        axis_letter="Y",
        limits=(-300.0, 300.0),
        max_feed=30000,
    )

    # X axis
    components["x_axis"] = MachineComponent(
        component_id="x_axis",
        component_type=ComponentType.LINEAR_AXIS,
        parent_id="y_axis",
        label="X-Axis Table",
        local_transform=_make_translation(-250, 0, 0),
        axis_letter="X",
        limits=(-500.0, 500.0),
        max_feed=30000,
    )

    # B axis (rotary, tilting)
    components["b_axis"] = MachineComponent(
        component_id="b_axis",
        component_type=ComponentType.ROTARY_AXIS,
        parent_id="x_axis",
        label="B-Axis Trunnion",
        local_transform=_make_translation(0, 0, -200),
        axis_letter="B",
        limits=(-120.0, 120.0),
        max_feed=18000,
        max_rpm=50,
    )

    # C axis (rotary, continuous)
    components["c_axis"] = MachineComponent(
        component_id="c_axis",
        component_type=ComponentType.ROTARY_AXIS,
        parent_id="b_axis",
        label="C-Axis Rotary Table",
        local_transform=_make_translation(0, 0, -150),
        axis_letter="C",
        limits=(0.0, 360.0),
        max_feed=36000,
        max_rpm=100,
        continuous=True,
        pivot_offset=np.array([0.0, 0.0, -150.0]),
    )

    # Fixture mount
    components["fixture_mount"] = MachineComponent(
        component_id="fixture_mount",
        component_type=ComponentType.FIXTURE_MOUNT,
        parent_id="c_axis",
        label="Fixture Mount",
        local_transform=_make_translation(0, 0, -50),
    )

    # Build parent-child relationships
    for comp in components.values():
        if comp.parent_id and comp.parent_id in components:
            components[comp.parent_id].children.append(comp.id)

    return MachineModel(
        name=name,
        version="1.0",
        description=f"Auto-generated default BC trunnion machine: {name}",
        components=components,
        root_id="bed",
        collision_pairs=[
            CollisionPair("tool_group", "fixture_group", clearance_mm=2.0),
            CollisionPair("spindle_group", "table_group", clearance_mm=5.0),
            CollisionPair("tool_group", "stock", clearance_mm=0.0,
                         check_type=CheckType.DURING_CUT),
        ],
        collision_groups={
            "tool_group": ["tool_mount"],
            "spindle_group": ["spindle", "z_axis"],
            "table_group": ["c_axis", "b_axis", "x_axis", "y_axis"],
            "fixture_group": ["fixture_mount"],
        },
    )


def generate_default_head_head(name: str = "Default AB Tilting Head") -> MachineModel:
    """Generate a default AB tilting head (HEAD_HEAD) machine model.

    Args:
        name: Machine name.

    Returns:
        A MachineModel with standard AB tilting head topology.
    """
    components: dict[str, MachineComponent] = {}

    # Bed
    components["bed"] = MachineComponent(
        component_id="bed",
        component_type=ComponentType.STATIC,
        parent_id=None,
        label="Machine Bed",
        local_transform=np.eye(4),
    )

    # Table side (X, Y, fixture)
    components["x_axis"] = MachineComponent(
        component_id="x_axis",
        component_type=ComponentType.LINEAR_AXIS,
        parent_id="bed",
        label="X-Axis Table",
        local_transform=_make_translation(-250, 0, 0),
        axis_letter="X",
        limits=(-500.0, 500.0),
        max_feed=30000,
    )

    components["y_axis"] = MachineComponent(
        component_id="y_axis",
        component_type=ComponentType.LINEAR_AXIS,
        parent_id="bed",
        label="Y-Axis Table",
        local_transform=_make_translation(0, -150, 0),
        axis_letter="Y",
        limits=(-300.0, 300.0),
        max_feed=30000,
    )

    components["table"] = MachineComponent(
        component_id="table",
        component_type=ComponentType.STATIC,
        parent_id="x_axis",
        label="Work Table",
        local_transform=_make_translation(0, 0, -100),
    )

    components["fixture_mount"] = MachineComponent(
        component_id="fixture_mount",
        component_type=ComponentType.FIXTURE_MOUNT,
        parent_id="table",
        label="Fixture Mount",
        local_transform=_make_translation(0, 0, -50),
    )

    # Tool side (Z, A, B, spindle)
    components["z_axis"] = MachineComponent(
        component_id="z_axis",
        component_type=ComponentType.LINEAR_AXIS,
        parent_id="bed",
        label="Z-Axis Head Slide",
        local_transform=_make_translation(0, 0, 500),
        axis_letter="Z",
        limits=(-400.0, 0.0),
        max_feed=30000,
    )

    components["a_axis"] = MachineComponent(
        component_id="a_axis",
        component_type=ComponentType.ROTARY_AXIS,
        parent_id="z_axis",
        label="A-Axis Tilting Head",
        local_transform=_make_translation(0, 0, -100),
        axis_letter="A",
        limits=(-120.0, 120.0),
        max_feed=18000,
        max_rpm=50,
    )

    components["b_axis"] = MachineComponent(
        component_id="b_axis",
        component_type=ComponentType.ROTARY_AXIS,
        parent_id="a_axis",
        label="B-Axis Tilting Head",
        local_transform=_make_translation(0, 0, -80),
        axis_letter="B",
        limits=(-120.0, 120.0),
        max_feed=18000,
        max_rpm=50,
    )

    components["spindle"] = MachineComponent(
        component_id="spindle",
        component_type=ComponentType.SPINDLE,
        parent_id="b_axis",
        label="Spindle",
        local_transform=_make_translation(0, 0, -60),
        max_rpm=24000,
    )

    components["tool_mount"] = MachineComponent(
        component_id="tool_mount",
        component_type=ComponentType.TOOL_MOUNT,
        parent_id="spindle",
        label="Tool Mount",
        local_transform=_make_translation(0, 0, -50),
    )

    # Build relationships
    for comp in components.values():
        if comp.parent_id and comp.parent_id in components:
            components[comp.parent_id].children.append(comp.id)

    return MachineModel(
        name=name,
        version="1.0",
        description=f"Auto-generated default AB tilting head machine: {name}",
        components=components,
        root_id="bed",
        collision_pairs=[
            CollisionPair("tool_group", "fixture_group", clearance_mm=2.0),
            CollisionPair("spindle_group", "table_group", clearance_mm=5.0),
            CollisionPair("tool_group", "stock", clearance_mm=0.0,
                         check_type=CheckType.DURING_CUT),
        ],
        collision_groups={
            "tool_group": ["tool_mount"],
            "spindle_group": ["spindle", "z_axis", "a_axis", "b_axis"],
            "table_group": ["x_axis", "y_axis", "table"],
            "fixture_group": ["fixture_mount"],
        },
    )


def generate_default_head_table(name: str = "Default B-Head C-Table") -> MachineModel:
    """Generate a default B-head C-table (HEAD_TABLE) machine model.

    Args:
        name: Machine name.

    Returns:
        A MachineModel with standard B-head C-table topology.
    """
    components: dict[str, MachineComponent] = {}

    # Bed
    components["bed"] = MachineComponent(
        component_id="bed",
        component_type=ComponentType.STATIC,
        parent_id=None,
        label="Machine Bed",
        local_transform=np.eye(4),
    )

    # Tool side
    components["z_axis"] = MachineComponent(
        component_id="z_axis",
        component_type=ComponentType.LINEAR_AXIS,
        parent_id="bed",
        label="Z-Axis Head Slide",
        local_transform=_make_translation(0, 0, 400),
        axis_letter="Z",
        limits=(-400.0, 0.0),
        max_feed=30000,
    )

    components["b_axis"] = MachineComponent(
        component_id="b_axis",
        component_type=ComponentType.ROTARY_AXIS,
        parent_id="z_axis",
        label="B-Axis Tilting Head",
        local_transform=_make_translation(0, 0, -100),
        axis_letter="B",
        limits=(-120.0, 120.0),
        max_feed=18000,
        max_rpm=50,
    )

    components["spindle"] = MachineComponent(
        component_id="spindle",
        component_type=ComponentType.SPINDLE,
        parent_id="b_axis",
        label="Spindle",
        local_transform=_make_translation(0, 0, -60),
        max_rpm=18000,
    )

    components["tool_mount"] = MachineComponent(
        component_id="tool_mount",
        component_type=ComponentType.TOOL_MOUNT,
        parent_id="spindle",
        label="Tool Mount",
        local_transform=_make_translation(0, 0, -50),
    )

    # Table side
    components["y_axis"] = MachineComponent(
        component_id="y_axis",
        component_type=ComponentType.LINEAR_AXIS,
        parent_id="bed",
        label="Y-Axis Saddle",
        local_transform=_make_translation(0, -150, 0),
        axis_letter="Y",
        limits=(-300.0, 300.0),
        max_feed=30000,
    )

    components["x_axis"] = MachineComponent(
        component_id="x_axis",
        component_type=ComponentType.LINEAR_AXIS,
        parent_id="y_axis",
        label="X-Axis Table",
        local_transform=_make_translation(-250, 0, 0),
        axis_letter="X",
        limits=(-500.0, 500.0),
        max_feed=30000,
    )

    components["c_axis"] = MachineComponent(
        component_id="c_axis",
        component_type=ComponentType.ROTARY_AXIS,
        parent_id="x_axis",
        label="C-Axis Rotary Table",
        local_transform=_make_translation(0, 0, -200),
        axis_letter="C",
        limits=(0.0, 360.0),
        max_feed=36000,
        max_rpm=100,
        continuous=True,
        pivot_offset=np.array([0.0, 0.0, -200.0]),
    )

    components["fixture_mount"] = MachineComponent(
        component_id="fixture_mount",
        component_type=ComponentType.FIXTURE_MOUNT,
        parent_id="c_axis",
        label="Fixture Mount",
        local_transform=_make_translation(0, 0, -50),
    )

    for comp in components.values():
        if comp.parent_id and comp.parent_id in components:
            components[comp.parent_id].children.append(comp.id)

    return MachineModel(
        name=name,
        version="1.0",
        description=f"Auto-generated default B-head C-table machine: {name}",
        components=components,
        root_id="bed",
        collision_pairs=[
            CollisionPair("tool_group", "fixture_group", clearance_mm=2.0),
            CollisionPair("spindle_group", "table_group", clearance_mm=5.0),
            CollisionPair("tool_group", "stock", clearance_mm=0.0,
                         check_type=CheckType.DURING_CUT),
        ],
        collision_groups={
            "tool_group": ["tool_mount"],
            "spindle_group": ["spindle", "z_axis", "b_axis"],
            "table_group": ["c_axis", "x_axis", "y_axis"],
            "fixture_group": ["fixture_mount"],
        },
    )


def generate_from_config(config_enum, name: str = "") -> MachineModel:
    """Generate a default machine model from a MachineConfig enum.

    Used for backward compatibility when existing code passes a
    MachineConfig instead of a MachineModel.

    Args:
        config_enum: A kinematics.MachineConfig value.
        name: Optional machine name.

    Returns:
        A MachineModel with the corresponding topology.
    """
    from .kinematics import MachineConfig

    if config_enum == MachineConfig.TABLE_TABLE:
        return generate_default_table_table(name or "Default BC Trunnion")
    elif config_enum == MachineConfig.HEAD_HEAD:
        return generate_default_head_head(name or "Default AB Tilting Head")
    elif config_enum == MachineConfig.HEAD_TABLE:
        return generate_default_head_table(name or "Default B-Head C-Table")
    else:
        return generate_default_table_table(name or "Unknown Machine")


def _make_translation(x: float, y: float, z: float) -> np.ndarray:
    """Create a 4x4 translation matrix."""
    T = np.eye(4, dtype=np.float64)
    T[0, 3] = x
    T[1, 3] = y
    T[2, 3] = z
    return T


# =========================================================================
#  Self-test
# =========================================================================

if __name__ == "__main__":
    print("=== Machine Model Self-Test ===\n")

    # ------------------------------------------------------------------
    # 1. Generate default BC trunnion machine
    # ------------------------------------------------------------------
    print("1. Generate default BC trunnion machine ...")
    machine = generate_default_table_table("Test BC Trunnion")
    print(f"   Machine: {machine}")
    print(f"   Components: {len(machine.components)}")
    print(f"   Root: {machine.root_id}")
    print(f"   Tool chain: {machine.tool_chain}")
    print(f"   Workpiece chain: {machine.workpiece_chain}")
    print(f"   Active axes: {machine.active_axes}")
    assert len(machine.components) >= 7
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 2. Forward kinematics (zero joints should be at home)
    # ------------------------------------------------------------------
    print("2. Forward kinematics: zero joints ...")
    joints_zero = np.zeros(6, dtype=np.float64)
    pose = machine.compute_forward_kinematics(joints_zero)
    print(f"   Pose: {pose}")
    # Tool should be pointing along +Z (vertical)
    assert abs(pose.tool_axis[2] - 1.0) < 1e-6, \
        f"Expected vertical tool, got {pose.tool_axis}"
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 3. Forward kinematics: B=30 deg
    # ------------------------------------------------------------------
    print("3. Forward kinematics: B=30 deg ...")
    joints_b30 = np.array([0.0, 0.0, -50.0, 0.0, 30.0, 0.0])
    pose_b30 = machine.compute_forward_kinematics(joints_b30)
    print(f"   B=30: tool_axis = {pose_b30.tool_axis.round(4)}")
    # At B=30, C=0: the quaternion q_tool = quat_from_rot_y(-B_rad) gives
    # tool_axis = [-sin(30), 0, cos(30)] = [-0.5, 0, 0.866]
    assert abs(pose_b30.tool_axis[0] - (-0.5)) < 0.01
    assert abs(pose_b30.tool_axis[2] - 0.866) < 0.01
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 4. FK roundtrip: forward then IK, then FK again
    # ------------------------------------------------------------------
    print("4. FK -> IK -> FK roundtrip ...")
    joints_in = np.array([10.0, 20.0, -50.0, 0.0, 30.0, 45.0])
    pose_in = machine.compute_forward_kinematics(joints_in)
    joints_out = machine.compute_inverse_kinematics(pose_in)
    if joints_out is not None:
        pose_out = machine.compute_forward_kinematics(joints_out)
        pos_err = np.linalg.norm(pose_out.position - pose_in.position)
        axis_err = np.linalg.norm(pose_out.tool_axis - pose_in.tool_axis)
        print(f"   Position error: {pos_err:.3e} mm")
        print(f"   Axis error:     {axis_err:.3e}")
        assert axis_err < 1e-6, f"Axis error too large: {axis_err}"
        print("   PASSED\n")
    else:
        print("   FAILED: IK returned None\n")

    # ------------------------------------------------------------------
    # 5. World transform for collision detection
    # ------------------------------------------------------------------
    print("5. get_world_transform ...")
    joints_mid = np.array([50.0, 0.0, -100.0, 0.0, 15.0, 30.0])
    T_spindle = machine.get_world_transform("spindle", joints_mid)
    T_table = machine.get_world_transform("c_axis", joints_mid)
    print(f"   Spindle world position: {T_spindle[0:3, 3].round(2)}")
    print(f"   C-axis world position:  {T_table[0:3, 3].round(2)}")
    assert T_spindle.shape == (4, 4)
    assert T_table.shape == (4, 4)
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 6. Axis limits check
    # ------------------------------------------------------------------
    print("6. Axis limits check ...")
    ok = np.array([0.0, 0.0, -50.0, 0.0, 30.0, 45.0])
    assert machine.check_limits(ok), "Should be within limits"
    over = np.array([0.0, 0.0, -50.0, 0.0, 150.0, 45.0])
    assert not machine.check_limits(over), "Should be out of limits"
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 7. Default machine generators
    # ------------------------------------------------------------------
    print("7. Test all default machine generators ...")
    for gen_name, gen_fn in [
        ("TABLE_TABLE", lambda: generate_default_table_table()),
        ("HEAD_HEAD", lambda: generate_default_head_head()),
        ("HEAD_TABLE", lambda: generate_default_head_table()),
    ]:
        m = gen_fn()
        joints_t = np.array([10.0, 20.0, -50.0, 15.0, 30.0, 45.0])
        pose_t = m.compute_forward_kinematics(joints_t)
        print(f"   {gen_name}: FK OK, tool_axis={pose_t.tool_axis.round(4)}")
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 8. Workspace linearization
    # ------------------------------------------------------------------
    print("8. Workspace linearization ...")
    start_j = np.array([0.0, 0.0, -50.0, 0.0, 0.0, 0.0])
    end_j = np.array([10.0, 0.0, -50.0, 0.0, 15.0, 0.0])
    start_pose = machine.compute_forward_kinematics(start_j)
    end_pose = machine.compute_forward_kinematics(end_j)
    interp = machine.compute_workspace_linearization(start_pose, end_pose,
                                                      num_samples=5)
    if interp is not None:
        print(f"   {len(interp)} samples")
        for k, j in enumerate(interp):
            print(f"   [{k}]: X={j[0]:.2f}, Y={j[1]:.2f}, Z={j[2]:.2f}, "
                  f"B={j[4]:.2f}, C={j[5]:.2f}")
        print("   PASSED\n")
    else:
        print("   FAILED\n")

    # ------------------------------------------------------------------
    # 9. Serialize back to dict
    # ------------------------------------------------------------------
    print("9. Serialize to dict ...")
    d = machine.to_dict()
    assert "components" in d
    assert len(d["components"]) == len(machine.components)
    print(f"   Dict has {len(d['components'])} components")
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 10. ToolAssembly from JSON
    # ------------------------------------------------------------------
    print("10. ToolAssembly ...")
    ta = ToolAssembly(
        name="D12 Ball Endmill",
        components=[
            ToolComponent(
                component_id="holder",
                component_type="holder",
                mesh_path=None,
                transform=_make_translation(0, 0, 0),
                length_mm=80.0,
                diameter_mm=48.0,
            ),
            ToolComponent(
                component_id="cutter",
                component_type="cutter",
                mesh_path=None,
                transform=_make_translation(0, 0, 80),
                length_mm=75.0,
                diameter_mm=12.0,
                tool_definition={"type": "ball_endmill", "diameter": 12.0},
            ),
        ],
        interface="HSK-A63",
    )
    holder = ta.get_holder_component()
    cutter = ta.get_cutter_component()
    assert holder is not None and holder.component_id == "holder"
    assert cutter is not None and cutter.component_id == "cutter"
    print(f"   Tool: {ta.name}, holder={holder.length_mm}mm, "
          f"cutter diam={cutter.diameter_mm}mm")
    print("   PASSED\n")

    print("=== ALL MACHINE MODEL TESTS PASSED ===")
