"""Main 5-axis CNC simulator orchestrator.

The FiveAxisSimulator is the primary entry point for external code.
It wires together:
- TriDexelModel (workpiece representation)
- MaterialRemovalEngine (material subtraction)
- FiveAxisKinematics (machine kinematics)
- Surface extraction (tri-dexel to mesh)
- Validation (gouge/collision checking)

Usage:
    sim = FiveAxisSimulator(stock_mesh, target_mesh, MachineConfig.TABLE_TABLE)
    sim.load_tool(BallEndmill(diameter=10.0))
    result = sim.execute_gcode("G01 X50 Y20 Z-5 B15 C30 F500")
    sim.current_stock_mesh.show()
"""

from dataclasses import dataclass, field
from typing import Optional
import numpy as np
import trimesh

from .tri_dexel import TriDexelModel, AABB
from .tools import Tool, BallEndmill
from .kinematics import ToolPose, MachineConfig, FiveAxisKinematics
from .material_removal import MaterialRemovalEngine, RemovalResult, Gouge, Collision
from .surface import tri_dexel_to_mesh, compare_to_target, detect_gouges


@dataclass
class MoveResult:
    """Result of executing a single tool move.

    Attributes:
        success: Whether the move executed without fatal errors.
        start_pose: Starting tool pose in workpiece frame.
        end_pose: Ending tool pose in workpiece frame.
        removal: Removal statistics from material removal.
        collisions: Any collisions detected during the move.
        warnings: Non-fatal warnings (near limits, etc.).
    """
    success: bool = True
    start_pose: Optional[ToolPose] = None
    end_pose: Optional[ToolPose] = None
    removal: RemovalResult = field(default_factory=RemovalResult)
    collisions: list[Collision] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass
class SimulationResult:
    """Complete result of a simulation run.

    Attributes:
        success: True if simulation completed without fatal errors.
        moves_executed: Number of tool moves simulated.
        total_volume_removed: Total material removed in mm^3.
        total_time_ms: Total simulation time in milliseconds.
        collisions: All collisions detected.
        gouges: All gouges detected.
        warnings: Non-fatal warnings.
        stock_mesh: Final stock mesh after simulation.
        deviation_map: Per-vertex signed deviation to target (mm).
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


class FiveAxisSimulator:
    """Main orchestrator for 5-axis CNC material removal simulation.

    Wires together the tri-dexel model, material removal engine,
    5-axis kinematics, surface extraction, and validation.

    Attributes:
        stock_mesh: The starting stock mesh.
        target_mesh: The target (desired) CAD mesh.
        machine_config: Machine kinematic configuration.
        resolution: Dexel grid resolution in mm.
        kinematics: FiveAxisKinematics for the machine.
        tri_dexel: TriDexelModel of the current stock.
        removal_engine: MaterialRemovalEngine for subtraction.
        current_tool: The currently loaded tool.
    """

    def __init__(self, stock_mesh: trimesh.Trimesh,
                 target_mesh: trimesh.Trimesh,
                 machine_config: MachineConfig = MachineConfig.TABLE_TABLE,
                 resolution: float = 0.1):
        self.stock_mesh = stock_mesh
        self.target_mesh = target_mesh
        self.machine_config = machine_config
        self.resolution = resolution

        # Initialize kinematics
        self.kinematics = FiveAxisKinematics(config=machine_config)

        # Initialize tri-dexel model from stock
        self.tri_dexel = TriDexelModel.from_mesh(stock_mesh, resolution=resolution)

        # Initialize removal engine
        self.removal_engine = MaterialRemovalEngine(
            tri_dexel=self.tri_dexel,
            linear_resolution=resolution,
        )

        self.current_tool: Optional[Tool] = None
        self._move_history: list[MoveResult] = []

    def load_tool(self, tool: Tool) -> None:
        """Load a tool for subsequent moves.

        Args:
            tool: A Tool subclass instance (e.g., BallEndmill(diameter=10.0)).
        """
        self.current_tool = tool

    def execute_gcode(self, gcode: str) -> SimulationResult:
        """Execute a G-code program on the simulator.

        Parses the G-code string and simulates each move sequentially.
        Supports basic G-code: G00, G01, G02, G03 with X, Y, Z, A, B, C,
        and F parameters.

        Note: For a full G-code interpreter, use the gcodeparser library.
        This implementation handles common 5-axis codes.

        Args:
            gcode: G-code program as a string.

        Returns:
            SimulationResult with aggregates.
        """
        # Placeholder -- implement in Phase 5
        return SimulationResult()

    def execute_move(self, start_pose: ToolPose, end_pose: ToolPose,
                     tool: Optional[Tool] = None) -> MoveResult:
        """Execute a single tool move between two poses.

        If start and end pose are identical, treats it as a single-position
        tool engagement (drilling, plunging). Otherwise, computes the swept
        volume along the path.

        Args:
            start_pose: Starting tool pose.
            end_pose: Ending tool pose.
            tool: Tool to use (defaults to self.current_tool).

        Returns:
            MoveResult with removal statistics and any warnings.
        """
        # Placeholder -- implement in Phase 5
        return MoveResult()

    @property
    def current_stock_mesh(self) -> trimesh.Trimesh:
        """Extract and return the current stock as a triangle mesh."""
        return tri_dexel_to_mesh(self.tri_dexel)

    @property
    def deviation_map(self) -> np.ndarray:
        """Per-vertex signed deviation from current stock to target.

        Returns:
            (V,) float array. Positive = uncut material, negative = gouge.
        """
        return compare_to_target(self.tri_dexel, self.target_mesh)

    @property
    def gouges(self) -> list[Gouge]:
        """List of gouges detected (material removed below target surface)."""
        return detect_gouges(self.tri_dexel, self.target_mesh)

    @property
    def stock_volume(self) -> float:
        """Current material volume in mm^3."""
        return self.tri_dexel.volume()

    def reset(self) -> None:
        """Reset the simulation to the original stock."""
        self.tri_dexel = TriDexelModel.from_mesh(self.stock_mesh,
                                                  resolution=self.resolution)
        self.removal_engine = MaterialRemovalEngine(
            tri_dexel=self.tri_dexel,
            linear_resolution=self.resolution,
        )
        self._move_history = []
