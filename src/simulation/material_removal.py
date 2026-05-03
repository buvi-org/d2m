"""Material removal engine -- the core simulation algorithm.

Subtracts tool volumes from the tri-dexel workpiece representation.
This is the hot path of the entire simulation system.

Algorithm:
1. Transform tool into workpiece frame
2. For each dexel grid (Z, X, Y):
   a. Compute affected columns via bounding box cull
   b. For each affected column, compute ray-tool intersection intervals
   c. Subtract those intervals from the column's interval list
3. Return statistics (volume removed, columns modified)
"""

from dataclasses import dataclass, field
from typing import Optional
import numpy as np
import time

from .tri_dexel import TriDexelModel, DexelColumn, DexelGrid
from .tools import Tool
from .kinematics import ToolPose
from .swept_volume import SweptVolumeSampler


@dataclass
class RemovalResult:
    """Statistics from a material removal operation.

    Attributes:
        columns_modified: Number of dexel columns that were changed.
        volume_removed: Total volume removed in mm^3.
        time_ms: Time taken for the operation in milliseconds.
        grid_results: Per-grid statistics dict.
    """
    columns_modified: int = 0
    volume_removed: float = 0.0
    time_ms: float = 0.0
    grid_results: dict = field(default_factory=dict)


@dataclass
class Gouge:
    """A detected gouge (material removed below target surface).

    Attributes:
        position: (3,) float array of gouge location (mm).
        depth: Depth of gouge in mm (positive = below target).
        severity: 'minor' (<tolerance), 'moderate', or 'severe'.
    """
    position: np.ndarray
    depth: float
    severity: str = "minor"


@dataclass
class Collision:
    """A detected collision (tool/holder hitting part/fixture).

    Attributes:
        tool_position: (3,) float, tool position at collision (mm).
        collision_type: 'holder_part', 'tool_fixture', 'tool_clamp', etc.
        penetration: Overlap depth in mm.
    """
    tool_position: np.ndarray
    collision_type: str
    penetration: float = 0.0


class MaterialRemovalEngine:
    """Engine for subtracting tool volumes from a tri-dexel workpiece model.

    Performs material removal at single tool poses and along swept paths.
    Uses bounding box culling to minimize the number of columns checked.

    Attributes:
        tri_dexel: The TriDexelModel representing the workpiece.
        swept_sampler: SweptVolumeSampler for toolpath discretization.
    """

    def __init__(self, tri_dexel: TriDexelModel,
                 linear_resolution: float = 0.1,
                 angular_resolution_deg: float = 5.0):
        self.tri_dexel = tri_dexel
        self.swept_sampler = SweptVolumeSampler(
            linear_resolution=linear_resolution,
            angular_resolution_deg=angular_resolution_deg,
        )

    def remove_tool_at_pose(self, tool: Tool, pose: ToolPose) -> RemovalResult:
        """Subtract tool volume from all three dexel grids at a single pose.

        This is the primary material removal operation for single-point
        tool positions (e.g., drilling, plunging, G0 positions).

        Algorithm:
        1. For each dexel grid (Z, X, Y):
           a. Transform the tool from its local frame to the grid's frame
           b. Compute the tool's bounding box projection onto the grid plane
           c. For each column in the affected range:
              - Transform the ray to tool-local coordinates
              - Compute ray-tool intersection via tool.ray_intersection()
              - Subtract intersection intervals from the column

        Args:
            tool: The cutting tool.
            pose: ToolPose in workpiece coordinates.

        Returns:
            RemovalResult with statistics.
        """
        # Placeholder -- implement in Phase 3
        return RemovalResult()

    def remove_tool_swept(self, tool: Tool, start_pose: ToolPose,
                          end_pose: ToolPose) -> RemovalResult:
        """Subtract tool swept volume along a 5-axis move.

        Samples intermediate poses between start and end, computes
        the union of tool intersections at each pose, and subtracts
        from all three dexel grids.

        Args:
            tool: The cutting tool.
            start_pose: Starting tool pose.
            end_pose: Ending tool pose.

        Returns:
            RemovalResult with aggregate statistics.
        """
        # Placeholder -- implement in Phase 3
        return RemovalResult()

    def validate_no_gouge(self, target_vertices: np.ndarray,
                          target_faces: np.ndarray,
                          tolerance: float = 0.01) -> list[Gouge]:
        """Check if any material was removed below the target surface.

        Samples the target surface and compares against the current
        tri-dexel state. Negative deviation = gouge.

        Args:
            target_vertices: (V, 3) target mesh vertices.
            target_faces: (F, 3) target mesh face indices.
            tolerance: Allowed deviation in mm.

        Returns:
            List of Gouge objects for violations beyond tolerance.
        """
        # Placeholder -- implement in Phase 6
        return []

    def compute_uncut_volume(self, target_vertices: np.ndarray,
                             target_faces: np.ndarray) -> float:
        """Compute volume of material remaining above the target surface.

        This is the material that still needs to be removed.

        Args:
            target_vertices: (V, 3) target mesh vertices.
            target_faces: (F, 3) target mesh face indices.

        Returns:
            Volume in mm^3.
        """
        # Placeholder -- implement in Phase 6
        return 0.0
