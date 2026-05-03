"""5-axis machine kinematics: forward/inverse kinematics, singularity handling.

Supports table-table (e.g., BC trunnion), head-head, and head-table
configurations. All kinematics are closed-form analytic solutions.

Reference: "Kinematic Modeling of 5-Axis Machine Tools" (standard textbook derivations)
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import numpy as np


class MachineConfig(Enum):
    """5-axis machine kinematic configuration."""
    TABLE_TABLE = "table_table"  # Both rotary axes on table (e.g., BC trunnion)
    HEAD_HEAD = "head_head"      # Both rotary axes in spindle head
    HEAD_TABLE = "head_table"    # One rotary in head, one on table


@dataclass
class ToolPose:
    """Tool position and orientation in the workpiece frame.

    Attributes:
        position: (3,) float array, tool tip position in mm (x, y, z).
        orientation: (4,) float array, unit quaternion [w, x, y, z]
                     representing tool orientation. The tool axis in
                     workpiece coordinates is rotate([0,0,1], orientation).
    """
    position: np.ndarray
    orientation: np.ndarray  # quaternion [w, x, y, z]

    @property
    def tool_axis(self) -> np.ndarray:
        """Tool axis direction in workpiece frame (normalized)."""
        # Rotate [0,0,1] by the orientation quaternion
        q = self.orientation
        # q * [0,0,1] * q_conj, simplified for z-axis
        x = 2 * (q[1] * q[3] + q[2] * q[0])
        y = 2 * (q[2] * q[3] - q[1] * q[0])
        z = 1 - 2 * (q[1]**2 + q[2]**2)
        return np.array([x, y, z])

    @classmethod
    def from_axis_angle(cls, position: np.ndarray, axis: np.ndarray, angle: float) -> "ToolPose":
        """Create ToolPose with tool axis rotated from +Z by axis-angle.

        This is the natural representation for 5-axis: the tool is aligned
        with +Z by default, and rotated by angle about axis.
        """
        axis = axis / np.linalg.norm(axis)
        half = angle / 2.0
        q = np.array([np.cos(half),
                      axis[0] * np.sin(half),
                      axis[1] * np.sin(half),
                      axis[2] * np.sin(half)])
        return cls(position=position, orientation=q)


class FiveAxisKinematics:
    """Models the kinematic chain of a 5-axis CNC machine.

    Supports forward kinematics (joints -> tool pose) and inverse kinematics
    (tool pose -> joints) for three common machine configurations.

    The joint vector is [X, Y, Z, A, B, C] where:
    - X, Y, Z are linear axis positions (mm)
    - A, B, C are rotary axis angles (degrees): A about X, B about Y, C about Z
    - Only 2 of [A, B, C] are active depending on machine config

    Attributes:
        config: Machine configuration type.
        primary_axis: Primary rotary axis letter ('A', 'B', or 'C').
        secondary_axis: Secondary rotary axis letter ('A', 'B', or 'C').
        axis_limits: Dict mapping axis letter to (min, max) tuples.
        tool_pivot_length: Distance from spindle gauge line to tool tip (mm).
        table_pivot_offset: Offset of rotary center from machine zero (3,).
    """

    # Default axis limits for a typical 5-axis machine
    DEFAULT_LIMITS = {
        "X": (-500.0, 500.0),
        "Y": (-300.0, 300.0),
        "Z": (-400.0, 0.0),
        "A": (-120.0, 120.0),
        "B": (-120.0, 120.0),
        "C": (0.0, 360.0),
    }

    def __init__(
        self,
        config: MachineConfig = MachineConfig.TABLE_TABLE,
        primary_axis: str = "B",
        secondary_axis: str = "C",
        axis_limits: Optional[dict] = None,
        tool_pivot_length: float = 0.0,
        table_pivot_offset: Optional[np.ndarray] = None,
    ):
        self.config = config
        self.primary_axis = primary_axis.upper()
        self.secondary_axis = secondary_axis.upper()
        self.axis_limits = axis_limits if axis_limits else dict(self.DEFAULT_LIMITS)
        self.tool_pivot_length = tool_pivot_length
        self.table_pivot_offset = (
            table_pivot_offset if table_pivot_offset is not None
            else np.zeros(3)
        )

    def forward(self, joints: np.ndarray) -> ToolPose:
        """Compute tool pose from joint positions.

        For TABLE_TABLE BC:
        - B rotates about machine Y axis
        - C rotates about machine Z axis (which itself rotates with B)
        - The part is on the table; the tool is fixed in orientation

        Joint vector: [X, Y, Z, A_or_B, B_or_C, extra] in mm and degrees.

        Args:
            joints: (6,) float array [X, Y, Z, A, B, C] in mm and degrees.

        Returns:
            ToolPose with tool tip position and quaternion orientation
            in the workpiece (table) frame.
        """
        # Placeholder -- implement in Phase 4
        position = joints[:3].copy()
        orientation = np.array([1.0, 0.0, 0.0, 0.0])  # identity quaternion
        return ToolPose(position=position, orientation=orientation)

    def inverse(self, pose: ToolPose, prev_joints: Optional[np.ndarray] = None) -> Optional[np.ndarray]:
        """Compute joint positions from a desired tool pose.

        Closed-form solution. Returns two solutions (B positive, B negative)
        and picks the one that satisfies axis limits.

        For TABLE_TABLE BC:
        1. Tool axis direction in machine frame: O_m = [Ox, Oy, Oz]
        2. B = -asin(Ox), C = atan2(Oy, Oz)
        3. Alternative: B' = pi - B, C' = C + pi
        4. Solve linear axes from rotation

        Args:
            pose: Desired tool pose in workpiece frame.
            prev_joints: Previous joint values for singularity handling.

        Returns:
            (6,) float array [X, Y, Z, A, B, C] or None if unreachable.
        """
        # Placeholder -- implement in Phase 4
        pass

    def interpolate(self, start_joints: np.ndarray, end_joints: np.ndarray,
                    feed_rate: float, num_samples: int = 10) -> list[np.ndarray]:
        """Linear interpolation in workpiece space with synchronized axes.

        Interpolates the tool pose (position + orientation via SLERP) and
        computes joint positions at each sample point.

        Args:
            start_joints: (6,) starting joint positions.
            end_joints: (6,) ending joint positions.
            feed_rate: Feed rate in mm/min (informational).
            num_samples: Number of intermediate sample points.

        Returns:
            List of (6,) joint arrays from start to end (inclusive).
        """
        # Placeholder -- implement in Phase 4
        pass

    def check_limits(self, joints: np.ndarray) -> bool:
        """Verify all joint values are within machine limits.

        Args:
            joints: (6,) float array of joint positions.

        Returns:
            True if all joints are within limits.
        """
        axis_names = ["X", "Y", "Z", "A", "B", "C"]
        for i, name in enumerate(axis_names):
            if name in self.axis_limits:
                lo, hi = self.axis_limits[name]
                if joints[i] < lo or joints[i] > hi:
                    return False
        return True

    def handle_singularity(self, pose: ToolPose,
                           prev_joints: Optional[np.ndarray] = None) -> np.ndarray:
        """Handle kinematic singularity (e.g., B=0 for table-table BC).

        When B approaches 0, the C axis becomes undefined because both
        rotary axes are aligned. Use the previous C value if available.

        Args:
            pose: Desired tool pose.
            prev_joints: Previous joint values for continuity.

        Returns:
            (6,) float array of joint positions with singularity-resolved
            rotary angles.
        """
        # Placeholder -- implement in Phase 4
        pass

    @staticmethod
    def slerp(q1: np.ndarray, q2: np.ndarray, t: float) -> np.ndarray:
        """Spherical linear interpolation between two quaternions.

        Args:
            q1: Start quaternion [w, x, y, z].
            q2: End quaternion [w, x, y, z].
            t: Interpolation parameter in [0, 1].

        Returns:
            Interpolated unit quaternion.
        """
        dot = np.clip(np.dot(q1, q2), -1.0, 1.0)
        if dot < 0:
            q2 = -q2
            dot = -dot
        if dot > 0.9995:
            result = q1 + t * (q2 - q1)
            return result / np.linalg.norm(result)
        theta_0 = np.arccos(dot)
        sin_theta_0 = np.sin(theta_0)
        theta = theta_0 * t
        sin_theta = np.sin(theta)
        s1 = sin_theta / sin_theta_0
        s0 = np.cos(theta) - dot * s1
        return s0 * q1 + s1 * q2

    @staticmethod
    def quaternion_angular_distance(q1: np.ndarray, q2: np.ndarray) -> float:
        """Angular distance between two quaternions in radians."""
        dot = np.abs(np.dot(q1, q2))
        dot = np.clip(dot, -1.0, 1.0)
        return 2.0 * np.arccos(dot)
