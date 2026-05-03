"""Tool swept volume computation for 5-axis CNC moves.

Computes the volume of space swept by a tool as it moves between two
poses. Uses sampled intermediate poses (SLERP for rotation, linear for
translation) and computes the union of tool intersections at each pose.

The sampling error is bounded by the grid resolution.
"""

from typing import Tuple
import numpy as np

from .tri_dexel import AABB, DexelColumn, DexelGrid, TriDexelModel
from .tools import Tool
from .kinematics import ToolPose, FiveAxisKinematics


class SweptVolumeSampler:
    """Samples tool poses along a 5-axis move and computes swept volume geometry.

    For each sampled pose, computes the tool's intersection with affected
    dexel columns. Returns the union of all intersection intervals for
    material removal.

    Attributes:
        linear_resolution: Maximum distance between pose samples (mm).
        angular_resolution: Maximum angular change between pose samples (radians).
    """

    def __init__(self, linear_resolution: float = 0.1,
                 angular_resolution_deg: float = 5.0):
        self.linear_resolution = linear_resolution
        self.angular_resolution = np.radians(angular_resolution_deg)

    def sample_poses(self, start_pose: ToolPose, end_pose: ToolPose) -> list[ToolPose]:
        """Generate interpolated tool poses between start and end.

        Number of samples determined by both translational and rotational
        components: n = max(translational_samples, rotational_samples).

        Translation: linear interpolation.
        Rotation: SLERP via FiveAxisKinematics.slerp.

        Args:
            start_pose: ToolPose at the start.
            end_pose: ToolPose at the end.

        Returns:
            List of ToolPose from start to end, inclusive.
        """
        # Placeholder -- implement in Phase 3
        n = 2  # at minimum, start and end
        if n < 2:
            n = 2

        result = []
        for i in range(n):
            t = i / (n - 1)
            pos = start_pose.position + t * (end_pose.position - start_pose.position)
            q = FiveAxisKinematics.slerp(start_pose.orientation, end_pose.orientation, t)
            result.append(ToolPose(position=pos, orientation=q))
        return result

    def swept_bbox(self, tool: Tool, start_pose: ToolPose, end_pose: ToolPose) -> AABB:
        """Compute bounding box of the entire swept volume.

        Expands the tool's local bbox at each pose and takes the union.

        Args:
            tool: The cutting tool.
            start_pose: Starting tool pose.
            end_pose: Ending tool pose.

        Returns:
            AABB containing the entire swept volume.
        """
        # Placeholder -- implement in Phase 3
        return AABB(min=np.zeros(3), max=np.zeros(3))

    def compute_swept_intervals(self, tool: Tool, start_pose: ToolPose,
                                 end_pose: ToolPose,
                                 grid: DexelGrid) -> dict:
        """Compute ray-tool intersection intervals for all affected columns.

        For each column in the swept volume's projected bounding box,
        compute the union of tool intersection intervals across all
        sampled poses.

        Args:
            tool: The cutting tool.
            start_pose: Starting tool pose.
            end_pose: Ending tool pose.
            grid: The DexelGrid to compute intersections for.

        Returns:
            Dict mapping (i, j) column indices to DexelColumn of
            intervals to subtract.
        """
        # Placeholder -- implement in Phase 3
        return {}
