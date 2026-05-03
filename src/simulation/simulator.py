"""Main 5-axis CNC simulator orchestrator.

The FiveAxisSimulator is the primary entry point.  It wires together:
- TriDexelModel       (workpiece representation)
- MaterialRemovalEngine (material subtraction)
- MachineModel         (scene-graph machine kinematics + collision)
- Surface extraction   (tri-dexel to mesh)
- Validation           (gouge / collision checking)

Usage (new, recommended):
    machine = MachineModel.from_json("machines/dmg_dmu50.json")
    sim = FiveAxisSimulator(stock_mesh, target_mesh, machine)

Usage (legacy, backward-compatible):
    sim = FiveAxisSimulator(stock_mesh, target_mesh, MachineConfig.TABLE_TABLE)
    # Auto-generates a default MachineModel internally.

The simulator now uses the scene-graph MachineModel for:
- Forward/inverse kinematics (parameterized from the component tree)
- Collision detection (mesh proximity between configured collision pairs)
- Axis limits checking (machine-specific, from the tree)
- World-transform computation for visualization and debugging
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Union
import time
import re
import numpy as np
import trimesh

from .tri_dexel import TriDexelModel, AABB
from .tools import Tool, BallEndmill
from .kinematics import ToolPose, MachineConfig, FiveAxisKinematics
from .material_removal import (
    MaterialRemovalEngine, RemovalResult, Gouge, Collision,
)
from .surface import tri_dexel_to_mesh, compare_to_target, detect_gouges
from .machine import (
    MachineModel, MachineComponent, ComponentType,
    ToolAssembly, ToolComponent, CollisionPair, Collision as MachineCollision,
    CheckType,
    generate_from_config,
)


# =========================================================================
#  Result types
# =========================================================================

@dataclass
class MoveResult:
    """Result of executing a single tool move.

    Attributes:
        success:      True if the move executed without fatal errors.
        block_number: G-code block number (0 if from direct API).
        start_pose:   Starting tool pose.
        end_pose:     Ending tool pose.
        removal:      Material removal statistics.
        collisions:   Any collisions detected.
        warnings:     Non-fatal warnings.
    """
    success: bool = True
    block_number: int = 0
    start_pose: Optional[ToolPose] = None
    end_pose: Optional[ToolPose] = None
    removal: RemovalResult = field(default_factory=RemovalResult)
    collisions: list[Collision] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass
class SimulationResult:
    """Complete result of a simulation run.

    Attributes:
        success:              True if completed without fatal errors.
        moves_executed:       Number of tool moves simulated.
        total_volume_removed: Total mm^3 removed.
        total_time_ms:        Total simulation wall-clock time.
        collisions:           All detected collisions.
        gouges:               All detected gouges.
        warnings:             Non-fatal warnings.
        stock_mesh:           Final stock mesh.
        deviation_map:        Per-vertex signed deviation (mm).
    """
    success: bool = True
    moves_executed: int = 0
    total_volume_removed: float = 0.0
    total_time_ms: float = 0.0
    collisions: list[Collision] = field(default_factory=list)
    gouges: list[Gouge] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    stock_mesh: Optional[trimesh.Trimesh] = None
    deviation_map: Optional[np.ndarray] = None


# =========================================================================
#  Simple G-code parser
# =========================================================================

class GCodeParser:
    """Minimal G-code parser for common 5-axis codes.

    Supports: G00, G01, G02, G03 with X, Y, Z, A, B, C, F parameters.
    Maintains modal state so that axes not specified in a block remain
    at their previous value.
    """

    def __init__(self):
        self.reset()

    def reset(self) -> None:
        """Reset modal state."""
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.a = 0.0
        self.b = 0.0
        self.c = 0.0
        self.f = 500.0   # feed rate mm/min
        self.motion = 0   # current motion mode (G0 or G1)

    def parse_block(self, line: str) -> Optional[dict]:
        """Parse a single G-code line.

        Args:
            line: A G-code line string.

        Returns:
            Dict with parsed values, or None for comment/empty lines.
        """
        line = line.strip()
        if not line or line.startswith(';') or line.startswith('('):
            return None

        # Extract the block
        parts = line.upper().split()
        if not parts:
            return None

        result = {"motion": self.motion, "f": self.f}

        for token in parts:
            letter = token[0]
            try:
                value = float(token[1:])
            except ValueError:
                continue

            if letter == 'G':
                gcode = int(value)
                if gcode in (0, 1, 2, 3):
                    result["motion"] = gcode
                    self.motion = gcode
                    # G00 and G01 are modal
            elif letter == 'X':
                result["x"] = value
                self.x = value
            elif letter == 'Y':
                result["y"] = value
                self.y = value
            elif letter == 'Z':
                result["z"] = value
                self.z = value
            elif letter == 'A':
                result["a"] = value
                self.a = value
            elif letter == 'B':
                result["b"] = value
                self.b = value
            elif letter == 'C':
                result["c"] = value
                self.c = value
            elif letter == 'F':
                result["f"] = value
                self.f = value

        return result

    def to_joints(self, parsed: dict) -> np.ndarray:
        """Convert a parsed G-code dict to a joint vector.

        Uses modal state for any axes not specified.

        Args:
            parsed: Dict from parse_block().

        Returns:
            (6,) float array [X, Y, Z, A, B, C].
        """
        return np.array([
            parsed.get("x", self.x),
            parsed.get("y", self.y),
            parsed.get("z", self.z),
            parsed.get("a", self.a),
            parsed.get("b", self.b),
            parsed.get("c", self.c),
        ], dtype=np.float64)


# =========================================================================
#  FiveAxisSimulator
# =========================================================================

class FiveAxisSimulator:
    """Main orchestrator for 5-axis CNC material removal simulation.

    Wires together the tri-dexel model, material removal engine,
    machine kinematics (via MachineModel), surface extraction,
    and validation (gouge + collision checking).

    Can be constructed with either:
    - A MachineModel instance (new, recommended)
    - A MachineConfig enum (legacy, auto-generates default MachineModel)

    Attributes:
        stock_mesh:      Starting stock mesh.
        target_mesh:     Target (desired) CAD mesh.
        machine:         MachineModel instance (scene-graph machine definition).
        resolution:      Dexel grid resolution in mm.
        tri_dexel:       Current stock as TriDexelModel.
        removal_engine:  MaterialRemovalEngine.
        current_tool:    Currently loaded tool.
        tool_assembly:   Optional ToolAssembly for collision checking.
    """

    def __init__(
        self,
        stock_mesh: trimesh.Trimesh,
        target_mesh: trimesh.Trimesh,
        machine: Union[MachineModel, MachineConfig, str] = MachineConfig.TABLE_TABLE,
        resolution: float = 0.1,
        primary_axis: str = "B",
        secondary_axis: str = "C",
        tool_assembly: Optional[ToolAssembly] = None,
        fixture_mesh: Optional[trimesh.Trimesh] = None,
    ):
        """Initialize the simulator.

        Args:
            stock_mesh: Starting stock as a trimesh.
            target_mesh: Target (desired) CAD mesh.
            machine: One of:
                - MachineModel instance (new, recommended)
                - MachineConfig enum (legacy, auto-generates default model)
                - str path to a machine JSON file
            resolution: Dexel grid resolution in mm.
            primary_axis: Primary rotary axis (legacy, used only if machine is MachineConfig).
            secondary_axis: Secondary rotary axis (legacy, used only if machine is MachineConfig).
            tool_assembly: Optional ToolAssembly for collision detection.
            fixture_mesh: Optional fixture mesh for collision detection.
        """
        self.stock_mesh = stock_mesh
        self.target_mesh = target_mesh
        self.resolution = float(resolution)
        self.tool_assembly = tool_assembly
        self.fixture_mesh = fixture_mesh

        # Resolve machine model (new scene-graph or legacy enum)
        if isinstance(machine, MachineModel):
            self.machine = machine
            self._uses_legacy_config = False
        elif isinstance(machine, MachineConfig):
            self.machine = generate_from_config(machine)
            self._uses_legacy_config = True
        elif isinstance(machine, str):
            # Path to a machine JSON file
            self.machine = MachineModel.from_json(machine)
            self._uses_legacy_config = False
        else:
            raise TypeError(
                f"machine must be MachineModel, MachineConfig, or str path, "
                f"got {type(machine).__name__}"
            )

        # Kinematics: use the machine's built-in solver
        # (parameterized from the component tree)
        self._kinematics = self.machine._build_kinematics_solver()

        # For backward compatibility: expose the legacy config
        if self._uses_legacy_config:
            self.machine_config = machine
        else:
            self.machine_config = None

        # Store legacy params for reference
        self._legacy_primary = primary_axis
        self._legacy_secondary = secondary_axis

        # Tri-dexel model from stock
        self.tri_dexel = TriDexelModel.from_mesh(stock_mesh, resolution=resolution)

        # Material removal engine
        self.removal_engine = MaterialRemovalEngine(
            tri_dexel=self.tri_dexel,
            linear_resolution=resolution,
        )

        self.current_tool: Optional[Tool] = None
        self._move_history: list[MoveResult] = []
        self._current_joints: np.ndarray = np.zeros(6, dtype=np.float64)
        self._current_pose: Optional[ToolPose] = None

    # -----------------------------------------------------------------
    #  Tool management
    # -----------------------------------------------------------------

    def load_tool(self, tool: Tool) -> None:
        """Load (mount) a tool for subsequent moves.

        Args:
            tool: A Tool subclass instance.
        """
        self.current_tool = tool

    # -----------------------------------------------------------------
    #  Move execution
    # -----------------------------------------------------------------

    def execute_move(
        self,
        start_pose: ToolPose,
        end_pose: ToolPose,
        tool: Optional[Tool] = None,
        run_collision_check: bool = True,
    ) -> MoveResult:
        """Execute a single tool move between two poses.

        If start and end pose are identical, treats it as a single-position
        engagement (drilling, plunging).  Otherwise computes the swept volume.

        After material removal, runs collision checking on all configured
        collision pairs (machine-machine and tool-stock).

        Args:
            start_pose: Start tool pose in workpiece frame.
            end_pose:   End tool pose in workpiece frame.
            tool:       Tool (defaults to self.current_tool).
            run_collision_check: If True, check collision pairs after the move.

        Returns:
            MoveResult with statistics.
        """
        active_tool = tool if tool is not None else self.current_tool
        if active_tool is None:
            return MoveResult(
                success=False,
                warnings=["No tool loaded"],
            )

        warnings: list[str] = []

        # Check if it's actually a move or just a single position
        pos_dist = float(np.linalg.norm(end_pose.position - start_pose.position))
        ang_dist = FiveAxisKinematics.quaternion_angular_distance(
            start_pose.orientation, end_pose.orientation,
        )

        if pos_dist < 1e-9 and ang_dist < 1e-6:
            # Single-pose engagement
            removal = self.removal_engine.remove_tool_at_pose(active_tool, end_pose)
        else:
            # Swept volume removal
            removal = self.removal_engine.remove_tool_swept(
                active_tool, start_pose, end_pose,
            )

        # Collision checking using the machine model
        collisions: list[Collision] = []
        if run_collision_check:
            machine_collisions = self._check_machine_collisions_at_end_pose(end_pose)
            for mc in machine_collisions:
                if not mc.is_near_miss:
                    collisions.append(Collision(
                        body_a=mc.component_a,
                        body_b=mc.component_b,
                        penetration=abs(mc.clearance_mm - mc.distance_mm),
                        position=mc.point_a,
                    ))
                else:
                    warnings.append(
                        f"Near-miss: {mc.component_a} <-> {mc.component_b} "
                        f"({mc.distance_mm:.2f} mm, clearance {mc.warn_clearance_mm:.2f} mm)"
                    )

        if collisions:
            warnings.append(f"{len(collisions)} collision(s) detected")

        result = MoveResult(
            success=len(collisions) == 0,
            start_pose=start_pose.copy(),
            end_pose=end_pose.copy(),
            removal=removal,
            collisions=collisions,
            warnings=warnings,
        )
        self._move_history.append(result)
        return result

    def _check_machine_collisions_at_end_pose(
        self, pose: ToolPose,
    ) -> list[MachineCollision]:
        """Run collision checking at a given tool pose.

        Computes joint positions from the tool pose via inverse kinematics,
        then checks all configured collision pairs.

        Args:
            pose: Tool pose in workpiece frame.

        Returns:
            List of MachineCollision objects.
        """
        # Compute joint positions from the pose
        joints = self.machine.compute_inverse_kinematics(
            pose, prev_joints=self._current_joints,
        )
        if joints is None:
            return []

        return self.machine.check_collisions(
            joints=joints,
            tool_assembly=self.tool_assembly,
            stock_mesh=self.current_stock_mesh,
            fixture_mesh=self.fixture_mesh,
        )

    # -----------------------------------------------------------------
    #  G-code execution
    # -----------------------------------------------------------------

    def execute_gcode(self, gcode: str) -> SimulationResult:
        """Execute a G-code program.

        Parses each line and simulates the tool motion.
        Supports G00 (rapid), G01 (linear feed), and modal state.

        G00 moves:  Rapid traverse, no material removal (retract only).
        G01 moves:  Linear feed with material removal + collision checking.

        Note: G02/G03 arcs are currently linearized.

        Args:
            gcode: G-code program as a string.

        Returns:
            SimulationResult with aggregates.
        """
        t_start = time.perf_counter()
        parser = GCodeParser()
        parser.reset()

        total_vol = 0.0
        moves = 0
        collisions: list[Collision] = []
        all_warnings: list[str] = []

        prev_joints: Optional[np.ndarray] = None

        for line_no, line in enumerate(gcode.strip().split('\n'), start=1):
            parsed = parser.parse_block(line)
            if parsed is None:
                continue

            joints = parser.to_joints(parsed)
            motion = parsed.get("motion", 0)

            # Check axis limits using the machine model (machine-specific limits)
            if not self.machine.check_limits(joints):
                all_warnings.append(
                    f"Line {line_no}: joint values {np.round(joints, 1)} exceed machine limits"
                )

            # Compute tool pose from joints using the machine model's FK
            pose = self.machine.compute_forward_kinematics(joints)

            if prev_joints is not None and motion in (0, 1):
                prev_pose = self.machine.compute_forward_kinematics(prev_joints)

                if motion == 1:
                    # G01: feed move with material removal + collision check
                    move_result = self.execute_move(prev_pose, pose, run_collision_check=True)
                    if move_result.success:
                        total_vol += move_result.removal.volume_removed
                        moves += 1
                        all_warnings.extend(move_result.warnings)
                    else:
                        all_warnings.extend(move_result.warnings)
                    collisions.extend(move_result.collisions)
                elif motion == 0:
                    # G00: rapid -- check collisions but no material removal
                    rapid_collisions = self._check_rapid_collisions(prev_joints, joints)
                    for mc in rapid_collisions:
                        collisions.append(Collision(
                            body_a=mc.component_a,
                            body_b=mc.component_b,
                            penetration=abs(mc.clearance_mm - mc.distance_mm),
                            position=mc.point_a,
                        ))
                    if rapid_collisions:
                        all_warnings.append(
                            f"Line {line_no}: {len(rapid_collisions)} collision(s) during rapid move"
                        )

            prev_joints = joints.copy()
            self._current_joints = joints.copy()
            self._current_pose = pose

        t_elapsed = (time.perf_counter() - t_start) * 1000.0

        # Post-simulation validation
        gouges = detect_gouges(self.tri_dexel, self.target_mesh)

        return SimulationResult(
            success=len(all_warnings) == 0 or all("error" not in w.lower() for w in all_warnings),
            moves_executed=moves,
            total_volume_removed=total_vol,
            total_time_ms=t_elapsed,
            collisions=collisions,
            gouges=gouges,
            warnings=all_warnings,
        )

    def _check_rapid_collisions(
        self, start_joints: np.ndarray, end_joints: np.ndarray,
    ) -> list[MachineCollision]:
        """Check collisions during rapid (G00) moves.

        Checks at both start and end positions. For critical pairs,
        samples intermediate positions as well.

        Args:
            start_joints: Starting joint positions.
            end_joints: Ending joint positions.

        Returns:
            List of MachineCollision objects.
        """
        all_collisions: list[MachineCollision] = []

        # Check at end position
        end_collisions = self.machine.check_collisions(
            joints=end_joints,
            tool_assembly=self.tool_assembly,
            stock_mesh=self.current_stock_mesh,
            fixture_mesh=self.fixture_mesh,
            check_type_filter=CheckType.RAPID_ONLY,
        )
        all_collisions.extend(end_collisions)

        # Also check static pairs at end position
        static_collisions = self.machine.check_collisions(
            joints=end_joints,
            tool_assembly=self.tool_assembly,
            stock_mesh=self.current_stock_mesh,
            fixture_mesh=self.fixture_mesh,
            check_type_filter=CheckType.STATIC,
        )
        all_collisions.extend(static_collisions)

        return all_collisions

    # -----------------------------------------------------------------
    #  Properties
    # -----------------------------------------------------------------

    @property
    def current_stock_mesh(self) -> trimesh.Trimesh:
        """Current stock as a triangle mesh."""
        return tri_dexel_to_mesh(self.tri_dexel)

    @property
    def deviation_map(self) -> np.ndarray:
        """Per-vertex signed deviation from current stock to target.

        Returns:
            (V,) float array.  Positive = uncut, negative = gouge.
        """
        return compare_to_target(self.tri_dexel, self.target_mesh)

    @property
    def gouges(self) -> list[Gouge]:
        """Gouges detected in the current stock state."""
        return detect_gouges(self.tri_dexel, self.target_mesh)

    @property
    def stock_volume(self) -> float:
        """Current material volume in mm^3."""
        return self.tri_dexel.volume()

    @property
    def move_history(self) -> list[MoveResult]:
        return list(self._move_history)

    def reset(self) -> None:
        """Reset simulation to the original stock."""
        self.tri_dexel = TriDexelModel.from_mesh(
            self.stock_mesh, resolution=self.resolution,
        )
        self.removal_engine = MaterialRemovalEngine(
            tri_dexel=self.tri_dexel,
            linear_resolution=self.resolution,
        )
        self._move_history.clear()
        self._current_joints = np.zeros(6, dtype=np.float64)
        self._current_pose = None

    # -----------------------------------------------------------------
    #  Backward-compatibility properties
    # -----------------------------------------------------------------

    @property
    def kinematics(self) -> FiveAxisKinematics:
        """Legacy kinematics accessor.

        Returns the FiveAxisKinematics solver used internally.
        For new code, prefer using self.machine methods directly.
        """
        return self._kinematics

    @property
    def machine_config(self) -> Optional[MachineConfig]:
        """Legacy machine config accessor. None if using MachineModel directly."""
        return self._machine_config

    @machine_config.setter
    def machine_config(self, value: Optional[MachineConfig]) -> None:
        self._machine_config = value

    # -----------------------------------------------------------------
    #  Machine model accessors
    # -----------------------------------------------------------------

    def get_component_world_transform(
        self, component_id: str, joints: Optional[np.ndarray] = None,
    ) -> np.ndarray:
        """Get the 4x4 world transform for a machine component.

        Uses the scene-graph tree walk to compute where a component is
        in 3D space at the given joint positions.

        Args:
            component_id: ID of the machine component.
            joints: (6,) joint vector. Uses current joints if None.

        Returns:
            4x4 homogeneous transform.
        """
        if joints is None:
            joints = self._current_joints
        return self.machine.get_world_transform(component_id, joints)

    def load_tool_assembly(self, assembly: ToolAssembly) -> None:
        """Load a tool assembly for collision detection.

        Args:
            assembly: A ToolAssembly instance.
        """
        self.tool_assembly = assembly


# =========================================================================
#  Self-test
# =========================================================================

if __name__ == "__main__":
    print("=== FiveAxisSimulator Self-Test ===\n")
    import trimesh
    from .tools import BallEndmill

    # ------------------------------------------------------------------
    # 1. Basic simulator: plunge a tool into a box
    # ------------------------------------------------------------------
    print("1. Simulator: plunge ball endmill into box ...")
    stock = trimesh.creation.box(extents=[20.0, 20.0, 20.0])
    target = trimesh.creation.box(extents=[20.0, 20.0, 18.0])  # 2mm shallower

    sim = FiveAxisSimulator(
        stock, target,
        machine=MachineConfig.TABLE_TABLE,  # legacy mode
        resolution=0.5,
    )
    sim.load_tool(BallEndmill(diameter=6.0, flute_length=30.0))

    vol_before = sim.stock_volume
    print(f"   Stock volume before: {vol_before:.1f} mm^3")

    # Plunge at center to z=-3
    start = ToolPose(
        position=np.array([0.0, 0.0, 1.0]),
        orientation=np.array([1.0, 0.0, 0.0, 0.0]),
    )
    end = ToolPose(
        position=np.array([0.0, 0.0, -3.0]),
        orientation=np.array([1.0, 0.0, 0.0, 0.0]),
    )

    result = sim.execute_move(start, end)
    vol_after = sim.stock_volume

    print(f"   Volume removed:      {result.removal.volume_removed:.1f} mm^3")
    print(f"   Stock volume after:  {vol_after:.1f} mm^3")
    print(f"   Time:                {result.removal.time_ms:.1f} ms")
    assert result.success, "Move failed"
    assert result.removal.volume_removed > 0, "No material removed"
    assert result.removal.time_ms < 2000, f"Too slow: {result.removal.time_ms}ms"
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 2. G-code execution
    # ------------------------------------------------------------------
    print("2. G-code execution ...")
    sim2 = FiveAxisSimulator(
        stock, target,
        machine=MachineConfig.TABLE_TABLE,  # legacy mode
        resolution=0.5,
    )
    sim2.load_tool(BallEndmill(diameter=6.0, flute_length=30.0))

    gcode = """
G00 X0 Y0 Z5
G01 Z-2 F500
G01 X10 F1000
G01 Y10
G01 X0
G01 Y0
G00 Z5
"""
    result2 = sim2.execute_gcode(gcode.strip())
    vol_removed = result2.total_volume_removed
    print(f"   Moves executed:      {result2.moves_executed}")
    print(f"   Volume removed:      {vol_removed:.1f} mm^3")
    print(f"   Total time:          {result2.total_time_ms:.1f} ms")
    print(f"   Gouges detected:     {len(result2.gouges)}")
    assert result2.moves_executed > 0, "No moves executed"
    assert vol_removed > 0, "No material removed"
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 3. Reset
    # ------------------------------------------------------------------
    print("3. Reset simulation ...")
    vol_before_reset = sim2.stock_volume
    sim2.reset()
    vol_after_reset = sim2.stock_volume
    print(f"   Volume before reset: {vol_before_reset:.1f}")
    print(f"   Volume after reset:  {vol_after_reset:.1f}")
    assert abs(vol_after_reset - 8000.0) < 100.0, "Reset did not restore stock"
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 4. MachineModel construction (new API)
    # ------------------------------------------------------------------
    print("4. MachineModel construction (new API) ...")
    from .machine import generate_default_table_table, ToolAssembly, ToolComponent
    machine = generate_default_table_table("Test DMG DMU 50")
    sim3 = FiveAxisSimulator(
        stock, target,
        machine=machine,  # new API: pass MachineModel directly
        resolution=0.5,
    )
    sim3.load_tool(BallEndmill(diameter=6.0, flute_length=30.0))
    print(f"   Machine: {sim3.machine.name}")
    print(f"   Components: {len(sim3.machine.components)}")
    print(f"   Active axes: {sim3.machine.active_axes}")
    assert sim3.machine.name == "Test DMG DMU 50"
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 5. World transform accessor
    # ------------------------------------------------------------------
    print("5. Component world transform ...")
    joints_mid = np.array([50.0, 0.0, -100.0, 0.0, 15.0, 30.0])
    T_spindle = sim3.get_component_world_transform("spindle", joints_mid)
    print(f"   Spindle world position: {T_spindle[0:3, 3].round(2)}")
    assert T_spindle.shape == (4, 4)
    print("   PASSED\n")

    print("=== ALL SIMULATOR TESTS PASSED ===")
