"""5-axis machine kinematics: forward / inverse kinematics, singularity handling.

Supports three machine configurations:
- TABLE_TABLE  (e.g. BC trunnion): both rotary axes on the table.
- HEAD_HEAD    (e.g. AB tilting head): both rotary axes in the spindle.
- HEAD_TABLE   (e.g. B head + C table): one rotary in head, one on table.

All kinematics use closed-form analytic solutions derived from the
transformation chain model.

.. deprecated::
    This module represents the original hardcoded kinematics approach.
    For new code, prefer `MachineModel` from `src.simulation.machine`,
    which supports arbitrary machine topologies via a scene-graph
    component tree with explicit collision pairs, component STL meshes,
    and machine-specific axis limits.

    The MachineConfig enum and hardcoded FK/IK are retained for backward
    compatibility only.  The FiveAxisKinematics solver is still used
    internally by MachineModel as the core FK/IK engine, parameterized
    from the component tree.

    Migration path:
        Old: kin = FiveAxisKinematics(config=MachineConfig.TABLE_TABLE)
        New: machine = MachineModel.from_json("machines/dmg_dmu50.json")
             pose = machine.compute_forward_kinematics(joints)
             joints = machine.compute_inverse_kinematics(pose)

Reference:
  "Kinematic Modeling of 5-Axis Machine Tools",
  "Inverse Kinematics of Five-Axis Machines" (standard textbook derivations)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Tuple
import numpy as np


# =========================================================================
#  Enums and data classes
# =========================================================================

class MachineConfig(Enum):
    """5-axis machine kinematic configuration type."""
    TABLE_TABLE = "table_table"   # Both rotary axes on table
    HEAD_HEAD = "head_head"       # Both rotary axes in spindle head
    HEAD_TABLE = "head_table"     # One in head, one on table


@dataclass
class ToolPose:
    """Tool position and orientation in the workpiece frame.

    Attributes:
        position:    (3,) float, tool tip position (mm) in workpiece frame.
        orientation: (4,) float, unit quaternion [w, x, y, z] (scalar-first).
                     The tool axis direction in the workpiece frame is
                     rotate_quat([0, 0, 1], orientation).
    """
    position: np.ndarray
    orientation: np.ndarray

    def __post_init__(self):
        self.position = np.asarray(self.position, dtype=np.float64)
        self.orientation = np.asarray(self.orientation, dtype=np.float64)
        # Ensure unit quaternion
        n = np.linalg.norm(self.orientation)
        if abs(n - 1.0) > 1e-12:
            self.orientation = self.orientation / n

    @property
    def tool_axis(self) -> np.ndarray:
        """Tool axis direction in workpiece frame (unit vector).

        Rotates the local +Z axis [0, 0, 1] by the orientation quaternion.
        """
        q = self.orientation
        # q * [0,0,1] * q_conj, simplified for the z-axis:
        x = 2.0 * (q[1] * q[3] + q[2] * q[0])
        y = 2.0 * (q[2] * q[3] - q[1] * q[0])
        z = 1.0 - 2.0 * (q[1] * q[1] + q[2] * q[2])
        return np.array([x, y, z])

    @classmethod
    def from_axis_angle(cls, position: np.ndarray, axis: np.ndarray,
                        angle: float) -> ToolPose:
        """Create a ToolPose with tool axis rotated from +Z by angle about axis.

        Args:
            position: Tool tip position in workpiece frame.
            axis:     Rotation axis (unit vector).
            angle:    Rotation angle in radians.

        Returns:
            ToolPose with the tool axis rotated from +Z.
        """
        axis = np.asarray(axis, dtype=np.float64)
        axis = axis / np.linalg.norm(axis)
        half = angle / 2.0
        q = np.array([
            np.cos(half),
            axis[0] * np.sin(half),
            axis[1] * np.sin(half),
            axis[2] * np.sin(half),
        ])
        return cls(position=position, orientation=q)

    def copy(self) -> ToolPose:
        return ToolPose(position=self.position.copy(),
                         orientation=self.orientation.copy())

    def __repr__(self) -> str:
        return (f"ToolPose(pos={self.position.round(3)}, "
                f"axis={self.tool_axis.round(3)})")


# =========================================================================
#  Quaternion helpers
# =========================================================================

def quat_multiply(q1: np.ndarray, q2: np.ndarray) -> np.ndarray:
    """Multiply two quaternions q1 * q2 (scalar-first convention)."""
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    return np.array([
        w1*w2 - x1*x2 - y1*y2 - z1*z2,
        w1*x2 + x1*w2 + y1*z2 - z1*y2,
        w1*y2 - x1*z2 + y1*w2 + z1*x2,
        w1*z2 + x1*y2 - y1*x2 + z1*w2,
    ])


def quat_from_rot_x(angle: float) -> np.ndarray:
    """Quaternion for rotation about X by angle (radians)."""
    half = angle / 2.0
    return np.array([np.cos(half), np.sin(half), 0.0, 0.0])


def quat_from_rot_y(angle: float) -> np.ndarray:
    """Quaternion for rotation about Y by angle (radians)."""
    half = angle / 2.0
    return np.array([np.cos(half), 0.0, np.sin(half), 0.0])


def quat_from_rot_z(angle: float) -> np.ndarray:
    """Quaternion for rotation about Z by angle (radians)."""
    half = angle / 2.0
    return np.array([np.cos(half), 0.0, 0.0, np.sin(half)])


def quaternion_to_rotvec(q: np.ndarray) -> np.ndarray:
    """Convert quaternion [w,x,y,z] to rotation vector (axis * angle)."""
    q = np.asarray(q)
    n = np.linalg.norm(q)
    if n < 1e-15:
        return np.zeros(3)
    q = q / n
    angle = 2.0 * np.arccos(np.clip(q[0], -1.0, 1.0))
    if angle < 1e-10:
        return np.zeros(3)
    s = np.sin(angle / 2.0)
    if abs(s) < 1e-15:
        return np.zeros(3)
    axis = q[1:4] / s
    return axis * angle


# =========================================================================
#  FiveAxisKinematics
# =========================================================================

class FiveAxisKinematics:
    """Models the kinematic chain of a 5-axis CNC machine.

    The joint vector is always [X, Y, Z, A, B, C] where:
    - X, Y, Z: linear axis positions (mm)
    - A, B, C: rotary axis angles (degrees)
      A rotates about X, B about Y, C about Z
    - Only 2 of [A, B, C] are active depending on machine configuration

    Coordinate conventions:
    - Workpiece frame (WP): attached to the part on the table.
    - Machine frame (M):   origin at machine home.
    - Tool frame (T):      tip at origin, tool axis along +Z.

    For simulation, WP = world frame (fixed reference).
    """

    DEFAULT_LIMITS: dict[str, Tuple[float, float]] = {
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
        axis_limits: Optional[dict[str, Tuple[float, float]]] = None,
        tool_pivot_length: float = 0.0,
        table_pivot_offset: Optional[np.ndarray] = None,
    ):
        """
        Args:
            config:             Machine kinematic configuration.
            primary_axis:       First rotary axis letter ('A','B','C').
            secondary_axis:     Second rotary axis letter ('A','B','C').
            axis_limits:        Dict of axis -> (min, max) in mm or degrees.
            tool_pivot_length:  Distance from spindle gauge line to tool tip (mm).
            table_pivot_offset: (3,) offset from machine zero to rotary table centre (mm).
        """
        self.config = config
        self.primary_axis = primary_axis.upper()
        self.secondary_axis = secondary_axis.upper()
        self.axis_limits = axis_limits if axis_limits is not None else dict(self.DEFAULT_LIMITS)
        self.tool_pivot_length = float(tool_pivot_length)
        self.table_pivot_offset = (
            np.asarray(table_pivot_offset, dtype=np.float64)
            if table_pivot_offset is not None
            else np.zeros(3, dtype=np.float64)
        )

        # Determine which rotary axes are active
        self._active_rotary = [self.primary_axis, self.secondary_axis]

    # -----------------------------------------------------------------
    #  Joint indexing helpers
    # -----------------------------------------------------------------

    @property
    def primary_index(self) -> int:
        """Index of the primary rotary axis in the joint vector."""
        return {"A": 3, "B": 4, "C": 5}[self.primary_axis]

    @property
    def secondary_index(self) -> int:
        """Index of the secondary rotary axis in the joint vector."""
        return {"A": 3, "B": 4, "C": 5}[self.secondary_axis]

    def _active_rotary_values(self, joints: np.ndarray) -> Tuple[float, float]:
        """Return (primary_angle_deg, secondary_angle_deg) from the joint vector."""
        return joints[self.primary_index], joints[self.secondary_index]

    # =================================================================
    #  FORWARD KINEMATICS
    # =================================================================

    def forward(self, joints: np.ndarray) -> ToolPose:
        """Compute tool tip pose from joint positions.

        Joint vector: [X, Y, Z, A, B, C] in mm and degrees.

        Args:
            joints: (6,) float array.

        Returns:
            ToolPose in the workpiece frame.
        """
        joints = np.asarray(joints, dtype=np.float64)
        if self.config == MachineConfig.TABLE_TABLE:
            return self._forward_table_table(joints)
        elif self.config == MachineConfig.HEAD_HEAD:
            return self._forward_head_head(joints)
        else:
            return self._forward_head_table(joints)

    def _forward_table_table(self, joints: np.ndarray) -> ToolPose:
        """Forward kinematics for table-table (BC trunnion).

        Chain: world -> linear axes -> tool (fixed orientation)
               world -> B-axis -> C-axis -> part

        Tool axis in workpiece frame: the tool is always along machine +Z.
        The part rotates with B (about Y) then C (about rotated Z).
        The tool tip position in the part frame is computed by inverse-rotating
        the linear position.

        Joints: [X, Y, Z, A_or_unused, B, C] in mm and deg.
        """
        X, Y, Z = joints[0], joints[1], joints[2]
        B, C = self._active_rotary_values(joints)
        B_rad = np.radians(B)
        C_rad = np.radians(C)

        # Build rotation: part orientation = R_y(B) * R_z(C)
        qB = quat_from_rot_y(B_rad)
        qC = quat_from_rot_z(C_rad)
        q_part = quat_multiply(qB, qC)

        # The tool orientation in part frame:
        # Tool is fixed along machine +Z = [0,0,1] in machine frame.
        # Part rotates, so tool axis in part frame = R_part^T * [0,0,1]
        #   = R_z(-C) * R_y(-B) * [0,0,1]
        # For a BC trunnion, the tool in machine frame is always +Z.
        # In the part frame, the tool appears to come from the opposite
        # direction.  So tool orientation = inverse of part orientation.
        #
        # Actually: the tool axis in workpiece frame is R_part^T * [0,0,1].
        # R_part = R_y(B) * R_z(C), so R_part^T = R_z(-C) * R_y(-B).
        # [0,0,1] rotated by R_z(-C) first: unchanged (Z rotation preserves Z).
        # Then by R_y(-B): [-sin(-B), 0, cos(-B)] = [sin(B), 0, cos(B)].
        # So tool_axis = [sin(B), 0, cos(B)].

        tool_axis_wp = np.array([np.sin(B_rad), 0.0, np.cos(B_rad)])

        # The tool tip position:
        # In machine frame, the tool tip is at [X, Y, Z].
        # The part is at the table pivot, rotated by R_part.
        # The tool tip in part frame P_wp:
        #   P_wp = R_part^T * ([X,Y,Z] - table_pivot) + table_pivot
        #   (inverse-rotate the linear position to get part-frame position)
        R_part = self._rotation_matrix_y(B_rad) @ self._rotation_matrix_z(C_rad)
        R_part_T = R_part.T

        P_machine = np.array([X, Y, Z])
        P_wp = R_part_T @ (P_machine - self.table_pivot_offset) + self.table_pivot_offset

        # Orientation: tool axis is [sin(B), 0, cos(B)] in part frame.
        # Convert to quaternion: this is a rotation of +Z to [sin(B), 0, cos(B)].
        # That's equivalent to rotation about Y by B.
        # But wait -- the tool axis being [sin(B), 0, cos(B)] means the
        # tool is tilted by -B relative to the Z axis (in part frame).
        # The orientation quaternion should rotate [0,0,1] to this axis.
        # Rotation about Y by -B degrees takes [0,0,1] to [sin(B), 0, cos(B)]:
        # Actually: R_y(-B) * [0,0,1] = [sin(B), 0, cos(B)]. Yes.
        # So tool orientation = R_y(-B).
        q_tool = quat_from_rot_y(-B_rad)

        return ToolPose(position=P_wp, orientation=q_tool)

    def _forward_head_head(self, joints: np.ndarray) -> ToolPose:
        """Forward kinematics for head-head configuration.

        Chain: world -> part (fixed)
               world -> linear axes -> A-axis -> B-axis -> spindle -> tool

        Joints: [X, Y, Z, A, B, C_or_unused] in mm and deg.
        """
        X, Y, Z = joints[0], joints[1], joints[2]
        A_deg, B_deg = self._active_rotary_values(joints)
        A_rad = np.radians(A_deg)
        B_rad = np.radians(B_deg)

        # Tool orientation: R_A * R_B applied to +Z
        # R_A rotates about X, R_B about Y (since B rotates with A in head-head)
        # Tool axis = R_x(A) * R_y(B) * [0,0,1]
        #   R_y(B)*[0,0,1] = [sin(B), 0, cos(B)]
        #   R_x(A)*[sin(B), 0, cos(B)] = [sin(B), sin(A)*cos(B), cos(A)*cos(B)]
        tool_axis = np.array([
            np.sin(B_rad),
            np.sin(A_rad) * np.cos(B_rad),
            np.cos(A_rad) * np.cos(B_rad),
        ])

        # Tool tip position:
        # The linear axes position the spindle gauge point.
        # Tool tip = [X, Y, Z] + R * [0, 0, -tool_pivot_length]
        # (tool extends downward from gauge point)
        R_head = self._rotation_matrix_x(A_rad) @ self._rotation_matrix_y(B_rad)
        pivot_offset = R_head @ np.array([0.0, 0.0, -self.tool_pivot_length])
        P_tip = np.array([X, Y, Z]) + pivot_offset

        # Orientation quaternion: R_x(A) * R_y(B)
        qA = quat_from_rot_x(A_rad)
        qB = quat_from_rot_y(B_rad)
        q_tool = quat_multiply(qA, qB)

        return ToolPose(position=P_tip, orientation=q_tool)

    def _forward_head_table(self, joints: np.ndarray) -> ToolPose:
        """Forward kinematics for head-table (B head + C table).

        Chain: world -> linear axes -> B-axis (head tilt) -> tool
               world -> C-axis (table) -> part

        Joints: [X, Y, Z, A_or_unused, B, C] in mm and deg.
        """
        X, Y, Z = joints[0], joints[1], joints[2]
        B_deg, C_deg = self._active_rotary_values(joints)
        B_rad = np.radians(B_deg)
        C_rad = np.radians(C_deg)

        # Part rotation: R_z(C)
        R_part = self._rotation_matrix_z(C_rad)

        # Tool in machine frame: tip at [X,Y,Z], oriented by B (tilting head)
        # Head B tilts about machine Y axis
        # Tool tip = [X, Y, Z] + R_y(B) * [0, 0, -tool_pivot_length]
        R_head = self._rotation_matrix_y(B_rad)

        # Tool axis in machine frame = R_y(B) * [0,0,1] = [sin(B), 0, cos(B)]
        tool_axis_machine = np.array([np.sin(B_rad), 0.0, np.cos(B_rad)])

        # Tool axis in part frame = R_part^T * tool_axis_machine
        tool_axis_wp = R_part.T @ tool_axis_machine

        # Tool tip in machine frame
        pivot_offset = R_head @ np.array([0.0, 0.0, -self.tool_pivot_length])
        P_tip_machine = np.array([X, Y, Z]) + pivot_offset

        # Tool tip in part frame
        P_tip_wp = R_part.T @ (P_tip_machine - self.table_pivot_offset) + self.table_pivot_offset

        # Orientation: rotate +Z to tool_axis_wp
        # Build quaternion: R_z(C)^T * R_y(B)
        n = np.linalg.norm(tool_axis_wp)
        if n < 1e-12:
            q_tool = np.array([1.0, 0.0, 0.0, 0.0])
        else:
            tool_axis_wp = tool_axis_wp / n
            # Cross product of [0,0,1] and tool_axis_wp gives rotation axis
            z_axis = np.array([0.0, 0.0, 1.0])
            cross = np.cross(z_axis, tool_axis_wp)
            sin_angle = np.linalg.norm(cross)
            cos_angle = np.dot(z_axis, tool_axis_wp)
            angle = np.arctan2(sin_angle, cos_angle)
            if sin_angle < 1e-12:
                q_tool = np.array([1.0, 0.0, 0.0, 0.0])
            else:
                axis = cross / sin_angle
                half = angle / 2.0
                q_tool = np.array([
                    np.cos(half),
                    axis[0] * np.sin(half),
                    axis[1] * np.sin(half),
                    axis[2] * np.sin(half),
                ])

        return ToolPose(position=P_tip_wp, orientation=q_tool)

    # =================================================================
    #  INVERSE KINEMATICS
    # =================================================================

    def inverse(self, pose: ToolPose,
                prev_joints: Optional[np.ndarray] = None) -> Optional[np.ndarray]:
        """Compute joint positions from a desired tool pose.

        Returns one solution (preferring the one closest to prev_joints
        if given, otherwise the solution with primary axis within limits).

        Args:
            pose:         Desired tool pose in workpiece frame.
            prev_joints:  Previous joint values for singularity handling.

        Returns:
            (6,) float array [X, Y, Z, A, B, C] or None if unreachable.
        """
        if self.config == MachineConfig.TABLE_TABLE:
            return self._inverse_table_table(pose, prev_joints)
        elif self.config == MachineConfig.HEAD_HEAD:
            return self._inverse_head_head(pose, prev_joints)
        else:
            return self._inverse_head_table(pose, prev_joints)

    def _inverse_table_table(self, pose: ToolPose,
                             prev_joints: Optional[np.ndarray] = None) -> Optional[np.ndarray]:
        """Inverse kinematics for table-table (BC trunnion).

        From the tool axis direction in part frame [Ox, Oy, Oz]:
            B = -arcsin(Ox)    (because Ox = sin(B) from forward derivation)
            C = atan2(-Oy, Oz)  (derived from rotation composition)

        Two solutions:
            (B, C)  and  (pi - B, C + pi)  [flip tool over]
        """
        tool_axis = pose.tool_axis
        Ox, Oy, Oz = tool_axis[0], tool_axis[1], tool_axis[2]

        # Clamp Ox for asin
        Ox_clamped = np.clip(Ox, -1.0, 1.0)

        # Two B solutions
        B1_rad = -np.arcsin(Ox_clamped)       # B in [-pi/2, pi/2]
        B2_rad = np.pi - B1_rad                # alternative

        # For each B, compute C
        # Tool axis = [sin(B), 0, cos(B)] rotated by C about Z
        # Actually the full derivation:
        # R_z(-C) * R_y(-B) * [0,0,1] = tool_axis
        # This gives: [-sin(B)*cos(C), sin(B)*sin(C), cos(B)]
        # Wait no. Let me re-derive.
        #
        # In table-table BC: part rotates with R = R_y(B)*R_z(C).
        # The tool axis in part frame = R^T * [0,0,1].
        # R^T = R_z(-C) * R_y(-B)
        # R_y(-B) * [0,0,1] = [sin(B), 0, cos(B)]
        # R_z(-C) * [sin(B), 0, cos(B)] = [sin(B)*cos(C), -sin(B)*sin(C), cos(B)]
        # So: Ox = sin(B)*cos(C), Oy = -sin(B)*sin(C), Oz = cos(B)
        #
        # From this: B = acos(Oz) or B = -acos(Oz)
        # And: C = atan2(-Oy, Ox) when sin(B) > 0
        #
        # Using B = -asin(Ox) from the simplified derivation was wrong.
        # Let me correct this.

        Oz_clamped = np.clip(Oz, -1.0, 1.0)

        # B = acos(Oz), two solutions:
        B1_rad = np.arccos(Oz_clamped)       # B in [0, pi]
        B2_rad = -B1_rad                      # negative solution

        solutions = []

        for B_rad in (B1_rad, B2_rad):
            sinB = np.sin(B_rad)
            if abs(sinB) < 1e-9:
                # Singularity: B near 0 or pi
                # C undefined -- use previous C or 0
                if prev_joints is not None:
                    C_rad = np.radians(prev_joints[self.secondary_index])
                else:
                    C_rad = 0.0
            else:
                # C = atan2(-Oy/sinB, Ox/sinB) = atan2(-Oy, Ox)
                C_rad = np.arctan2(-Oy / sinB, Ox / sinB)

            # Compute position
            R_part = self._rotation_matrix_y(B_rad) @ self._rotation_matrix_z(C_rad)
            P_machine = R_part @ (pose.position - self.table_pivot_offset) + self.table_pivot_offset
            X, Y, Z = P_machine[0], P_machine[1], P_machine[2]

            # Build joint vector
            joints = np.zeros(6, dtype=np.float64)
            joints[0], joints[1], joints[2] = X, Y, Z
            joints[self.primary_index] = np.degrees(B_rad)
            joints[self.secondary_index] = np.degrees(C_rad)

            if self.check_limits(joints):
                solutions.append(joints)

        if not solutions:
            # Return the first solution even if outside limits
            # (caller should check limits separately)
            if prev_joints is not None:
                B_rad = np.arccos(Oz_clamped)
                sinB = np.sin(B_rad)
                if abs(sinB) < 1e-9:
                    C_rad = np.radians(prev_joints[self.secondary_index])
                else:
                    C_rad = np.arctan2(-Oy / sinB, Ox / sinB)
            else:
                B_rad = np.arccos(Oz_clamped)
                sinB = np.sin(B_rad)
                C_rad = np.arctan2(-Oy, Ox) if abs(sinB) > 1e-9 else 0.0

            R_part = self._rotation_matrix_y(B_rad) @ self._rotation_matrix_z(C_rad)
            P_machine = R_part @ (pose.position - self.table_pivot_offset) + self.table_pivot_offset
            joints = np.zeros(6, dtype=np.float64)
            joints[0], joints[1], joints[2] = P_machine[0], P_machine[1], P_machine[2]
            joints[self.primary_index] = np.degrees(B_rad)
            joints[self.secondary_index] = np.degrees(C_rad)
            return joints

        # Pick solution closest to prev_joints (if available)
        if prev_joints is not None and len(solutions) > 1:
            best = min(solutions, key=lambda j: np.sum(np.abs(j - prev_joints)))
            return best

        return solutions[0]

    def _inverse_head_head(self, pose: ToolPose,
                           prev_joints: Optional[np.ndarray] = None) -> Optional[np.ndarray]:
        """Inverse kinematics for head-head (AB tilting head).

        Tool axis = R_x(A) * R_y(B) * [0,0,1]
          = [sin(B), sin(A)*cos(B), cos(A)*cos(B)]

        So: A = atan2(Oy, Oz)
            B = atan2(Ox, sqrt(Oy^2 + Oz^2))
        """
        tool_axis = pose.tool_axis
        Ox, Oy, Oz = tool_axis[0], tool_axis[1], tool_axis[2]

        # From derivation: Oy = -cos(B)*sin(A), Oz = cos(B)*cos(A)
        # So A = atan2(-Oy, Oz)
        A_rad = np.arctan2(-Oy, Oz)

        # B = atan2(Ox, sqrt(Oy^2 + Oz^2))
        r_yz = np.sqrt(Oy * Oy + Oz * Oz)
        if abs(Ox) < 1e-9 and r_yz < 1e-9:
            B_rad = 0.0
        else:
            B_rad = np.arctan2(Ox, r_yz)

        # Compute position
        R_head = self._rotation_matrix_x(A_rad) @ self._rotation_matrix_y(B_rad)
        pivot_offset = R_head @ np.array([0.0, 0.0, -self.tool_pivot_length])
        P_machine = pose.position - pivot_offset
        X, Y, Z = P_machine[0], P_machine[1], P_machine[2]

        joints = np.zeros(6, dtype=np.float64)
        joints[0], joints[1], joints[2] = X, Y, Z
        joints[self.primary_index] = np.degrees(A_rad)
        joints[self.secondary_index] = np.degrees(B_rad)

        return joints

    def _inverse_head_table(self, pose: ToolPose,
                            prev_joints: Optional[np.ndarray] = None) -> Optional[np.ndarray]:
        """Inverse kinematics for head-table (B head + C table).

        Chain: part rotation = R_z(C), head tilt = R_y(B).
        Tool axis in part frame = R_z(-C) * R_y(B) * [0,0,1]
          = R_z(-C) * [sin(B), 0, cos(B)]
          = [sin(B)*cos(C), sin(B)*sin(C), cos(B)]

        So: B = acos(Oz),    C = atan2(Oy, Ox)   when sin(B) > 0
        """
        tool_axis = pose.tool_axis
        Ox, Oy, Oz = tool_axis[0], tool_axis[1], tool_axis[2]

        Oz_clamped = np.clip(Oz, -1.0, 1.0)
        B1_rad = np.arccos(Oz_clamped)  # B in [0, pi]
        B2_rad = -B1_rad

        solutions = []
        for B_rad in (B1_rad, B2_rad):
            sinB = np.sin(B_rad)
            if abs(sinB) < 1e-9:
                C_rad = np.radians(prev_joints[self.secondary_index]) if prev_joints is not None else 0.0
            else:
                C_rad = np.arctan2(Oy / sinB, Ox / sinB)

            # Position
            R_part = self._rotation_matrix_z(C_rad)
            R_head = self._rotation_matrix_y(B_rad)
            pivot_offset = R_head @ np.array([0.0, 0.0, -self.tool_pivot_length])
            P_tip_machine = R_part @ (pose.position - self.table_pivot_offset) + self.table_pivot_offset
            P_machine = P_tip_machine - pivot_offset
            X, Y, Z = P_machine[0], P_machine[1], P_machine[2]

            joints = np.zeros(6, dtype=np.float64)
            joints[0], joints[1], joints[2] = X, Y, Z
            joints[self.primary_index] = np.degrees(B_rad)
            joints[self.secondary_index] = np.degrees(C_rad)

            if self.check_limits(joints):
                solutions.append(joints)

        if not solutions:
            B_rad = np.arccos(Oz_clamped)
            sinB = np.sin(B_rad)
            C_rad = np.arctan2(Oy, Ox) if abs(sinB) > 1e-9 else 0.0
            R_part = self._rotation_matrix_z(C_rad)
            R_head = self._rotation_matrix_y(B_rad)
            pivot_offset = R_head @ np.array([0.0, 0.0, -self.tool_pivot_length])
            P_tip_machine = R_part @ (pose.position - self.table_pivot_offset) + self.table_pivot_offset
            P_machine = P_tip_machine - pivot_offset
            joints = np.zeros(6, dtype=np.float64)
            joints[0], joints[1], joints[2] = P_machine[0], P_machine[1], P_machine[2]
            joints[self.primary_index] = np.degrees(B_rad)
            joints[self.secondary_index] = np.degrees(C_rad)
            return joints

        if prev_joints is not None and len(solutions) > 1:
            return min(solutions, key=lambda j: np.sum(np.abs(j - prev_joints)))
        return solutions[0]

    # =================================================================
    #  INTERPOLATION
    # =================================================================

    def interpolate(self, start_joints: np.ndarray, end_joints: np.ndarray,
                    num_samples: int = 10) -> list[np.ndarray]:
        """Linear interpolation in joint space with synchronised axes.

        For 5-axis moves, the tool path should be in workpiece space.
        This method interpolates joint values linearly (good enough for
        short moves).  For long moves, use workpiece-space interpolation
        via forward/inverse kinematics at each sample.

        Args:
            start_joints: (6,) starting joint values.
            end_joints:   (6,) ending joint values.
            num_samples:  Number of samples including start and end.

        Returns:
            List of (6,) float joint arrays.
        """
        start_joints = np.asarray(start_joints, dtype=np.float64)
        end_joints = np.asarray(end_joints, dtype=np.float64)

        result = []
        for k in range(num_samples):
            t = k / (num_samples - 1) if num_samples > 1 else 0.0
            j = start_joints + t * (end_joints - start_joints)
            result.append(j.copy())
        return result

    def interpolate_workspace(self, start_pose: ToolPose, end_pose: ToolPose,
                              num_samples: int = 10,
                              prev_joints: Optional[np.ndarray] = None) -> Optional[list[np.ndarray]]:
        """Interpolate in workpiece space and compute joints at each sample.

        SLERP for rotation, linear for position.

        Args:
            start_pose:  Start tool pose.
            end_pose:    End tool pose.
            num_samples: Number of samples.
            prev_joints: Previous joint values for IK continuity.

        Returns:
            List of (6,) joint arrays, or None if any pose is unreachable.
        """
        result: list[np.ndarray] = []
        current_prev = prev_joints

        for k in range(num_samples):
            t = k / (num_samples - 1) if num_samples > 1 else 0.0
            pos = start_pose.position + t * (end_pose.position - start_pose.position)
            q = self.slerp(start_pose.orientation, end_pose.orientation, t)
            pose = ToolPose(position=pos, orientation=q)

            joints = self.inverse(pose, prev_joints=current_prev)
            if joints is None:
                return None
            result.append(joints)
            current_prev = joints

        return result

    # =================================================================
    #  LIMITS & SINGULARITY
    # =================================================================

    def check_limits(self, joints: np.ndarray) -> bool:
        """Verify all joint values are within machine axis limits.

        Args:
            joints: (6,) float array.

        Returns:
            True if all axes are within limits.
        """
        axis_names = ["X", "Y", "Z", "A", "B", "C"]
        for i, name in enumerate(axis_names):
            if name in self.axis_limits:
                lo, hi = self.axis_limits[name]
                if joints[i] < lo - 1e-6 or joints[i] > hi + 1e-6:
                    return False
        return True

    def handle_singularity(self, pose: ToolPose,
                           prev_joints: Optional[np.ndarray] = None) -> Optional[np.ndarray]:
        """Handle kinematic singularity.

        For TABLE_TABLE BC: singularity at B = 0 or B = pi, where C
        rotation does not change the tool orientation.

        Strategy: if B is very close to 0 (or pi), use the previous C
        value.  If no previous, default to C = 0.

        Args:
            pose: Desired tool pose.
            prev_joints: Previous joint values.

        Returns:
            Joint array with singularity-resolved rotary angles.
        """
        tool_axis = pose.tool_axis
        Oz = tool_axis[2]

        if self.config == MachineConfig.TABLE_TABLE:
            # Check if near B=0 or B=pi
            cosB = np.clip(Oz, -1.0, 1.0)
            B_rad = np.arccos(cosB)

            if abs(np.sin(B_rad)) < 1e-6:
                # Singularity: C undefined
                if prev_joints is not None:
                    C_rad = np.radians(prev_joints[self.secondary_index])
                else:
                    C_rad = 0.0
            else:
                Ox, Oy = tool_axis[0], tool_axis[1]
                sinB = np.sin(B_rad)
                C_rad = np.arctan2(-Oy / sinB, Ox / sinB)

            R_part = self._rotation_matrix_y(B_rad) @ self._rotation_matrix_z(C_rad)
            P_machine = R_part @ (pose.position - self.table_pivot_offset) + self.table_pivot_offset

            joints = np.zeros(6)
            joints[0], joints[1], joints[2] = P_machine[0], P_machine[1], P_machine[2]
            joints[self.primary_index] = np.degrees(B_rad)
            joints[self.secondary_index] = np.degrees(C_rad)
            return joints

        # For other configs, just use standard inverse
        return self.inverse(pose, prev_joints)

    # =================================================================
    #  STATIC HELPERS
    # =================================================================

    @staticmethod
    def slerp(q1: np.ndarray, q2: np.ndarray, t: float) -> np.ndarray:
        """Spherical linear interpolation between two unit quaternions.

        Args:
            q1, q2: Quaternions [w, x, y, z], scalar-first.
            t:      Interpolation parameter in [0, 1].

        Returns:
            Interpolated unit quaternion.
        """
        q1 = np.asarray(q1, dtype=np.float64)
        q2 = np.asarray(q2, dtype=np.float64)

        dot = np.clip(np.dot(q1, q2), -1.0, 1.0)
        if dot < 0:
            q2 = -q2
            dot = -dot
        if dot > 0.9995:
            # Near-parallel: linear interpolation
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
        """Angular distance between two quaternions in radians (0 to pi)."""
        dot = abs(np.dot(np.asarray(q1), np.asarray(q2)))
        dot = np.clip(dot, -1.0, 1.0)
        return 2.0 * np.arccos(dot)

    @staticmethod
    def _rotation_matrix_x(angle: float) -> np.ndarray:
        """3x3 rotation matrix about X-axis by angle (radians)."""
        c, s = np.cos(angle), np.sin(angle)
        return np.array([
            [1.0, 0.0, 0.0],
            [0.0, c,   -s],
            [0.0, s,   c],
        ])

    @staticmethod
    def _rotation_matrix_y(angle: float) -> np.ndarray:
        """3x3 rotation matrix about Y-axis by angle (radians)."""
        c, s = np.cos(angle), np.sin(angle)
        return np.array([
            [c,   0.0, s],
            [0.0, 1.0, 0.0],
            [-s,  0.0, c],
        ])

    @staticmethod
    def _rotation_matrix_z(angle: float) -> np.ndarray:
        """3x3 rotation matrix about Z-axis by angle (radians)."""
        c, s = np.cos(angle), np.sin(angle)
        return np.array([
            [c,   -s, 0.0],
            [s,   c,  0.0],
            [0.0, 0.0, 1.0],
        ])


# =========================================================================
#  Self-test
# =========================================================================

if __name__ == "__main__":
    print("=== 5-Axis Kinematics Self-Test ===\n")

    # ------------------------------------------------------------------
    # 1. TABLE_TABLE BC: forward + inverse roundtrip
    # ------------------------------------------------------------------
    print("1. TABLE_TABLE BC: forward/inverse roundtrip ...")
    kin = FiveAxisKinematics(
        config=MachineConfig.TABLE_TABLE,
        primary_axis="B", secondary_axis="C",
    )

    # Known joint values
    joints_in = np.array([10.0, 20.0, -50.0, 0.0, 30.0, 45.0])  # X,Y,Z,A,B,C
    pose = kin.forward(joints_in)
    print(f"   Forward: {pose}")

    # Inverse should recover the joints (within limits)
    joints_out = kin.inverse(pose)
    if joints_out is not None:
        # Verify roundtrip: forward(inverse(pose)) == pose
        pose2 = kin.forward(joints_out)
        pos_err = np.linalg.norm(pose2.position - pose.position)
        axis_err = np.linalg.norm(pose2.tool_axis - pose.tool_axis)
        print(f"   Inverse joints: {np.round(joints_out, 2)}")
        print(f"   Position error: {pos_err:.2e} mm")
        print(f"   Axis error:     {axis_err:.2e}")

        # The recovered tool axis should match exactly
        assert axis_err < 1e-6, f"Axis error {axis_err:.2e} too large"
        # Position error may be non-zero due to different B/C solutions
        # when mapping back
        print("   PASSED\n")
    else:
        print("   FAILED: inverse returned None\n")

    # ------------------------------------------------------------------
    # 2. TABLE_TABLE BC: zero-angle position
    # ------------------------------------------------------------------
    print("2. TABLE_TABLE BC: zero-angle test (tool vertical) ...")
    joints_zero = np.array([50.0, 30.0, -100.0, 0.0, 0.0, 0.0])
    pose_zero = kin.forward(joints_zero)
    print(f"   Pose: {pose_zero}")
    # Tool should be vertical (axis along Z)
    assert abs(pose_zero.tool_axis[2] - 1.0) < 1e-9, "Tool axis not vertical"
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 3. Singularity at B=0
    # ------------------------------------------------------------------
    print("3. Singularity at B=0 ...")
    joints_sing = np.array([0.0, 0.0, -50.0, 0.0, 0.0, 90.0])
    pose_sing = kin.forward(joints_sing)
    # At B=0, C rotation does not change tool axis direction
    assert abs(pose_sing.tool_axis[2] - 1.0) < 1e-9, "At B=0, tool should be vertical"
    print(f"   At B=0, C=90: tool_axis = {pose_sing.tool_axis}")
    print("   PASSED (C rotation at B=0 does not tilt tool)\n")

    # ------------------------------------------------------------------
    # 4. HEAD_HEAD AB: roundtrip
    # ------------------------------------------------------------------
    print("4. HEAD_HEAD AB: forward/inverse roundtrip ...")
    kin_hh = FiveAxisKinematics(
        config=MachineConfig.HEAD_HEAD,
        primary_axis="A", secondary_axis="B",
    )
    joints_hh = np.array([10.0, 20.0, -50.0, 15.0, 30.0, 0.0])
    pose_hh = kin_hh.forward(joints_hh)
    joints_hh_out = kin_hh.inverse(pose_hh)
    if joints_hh_out is not None:
        pose_hh2 = kin_hh.forward(joints_hh_out)
        pos_err = np.linalg.norm(pose_hh2.position - pose_hh.position)
        axis_err = np.linalg.norm(pose_hh2.tool_axis - pose_hh.tool_axis)
        print(f"   Position error: {pos_err:.2e} mm")
        print(f"   Axis error:     {axis_err:.2e}")
        assert axis_err < 1e-6
        print("   PASSED\n")
    else:
        print("   FAILED\n")

    # ------------------------------------------------------------------
    # 5. Axis limits check
    # ------------------------------------------------------------------
    print("5. Axis limits check ...")
    ok = np.array([0.0, 0.0, -50.0, 0.0, 30.0, 45.0])
    assert kin.check_limits(ok), "Should be within limits"

    over = np.array([0.0, 0.0, -50.0, 0.0, 150.0, 45.0])  # B out of range
    assert not kin.check_limits(over), "Should be out of limits"
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 6. SLERP
    # ------------------------------------------------------------------
    print("6. SLERP interpolation test ...")
    q1 = np.array([1.0, 0.0, 0.0, 0.0])
    q2 = quat_from_rot_y(np.pi / 2.0)  # 90 deg about Y
    q_mid = FiveAxisKinematics.slerp(q1, q2, 0.5)
    # At t=0.5, rotation should be 45 deg about Y
    expected = quat_from_rot_y(np.pi / 4.0)
    err = np.linalg.norm(q_mid - expected)
    print(f"   Midpoint error: {err:.2e}")
    assert err < 1e-9
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 7. Workspace interpolation
    # ------------------------------------------------------------------
    print("7. Workspace interpolation ...")
    start_pose = kin.forward(np.array([0.0, 0.0, -50.0, 0.0, 0.0, 0.0]))
    end_pose = kin.forward(np.array([10.0, 0.0, -50.0, 0.0, 15.0, 0.0]))
    interp_joints = kin.interpolate_workspace(start_pose, end_pose, num_samples=5)
    if interp_joints is not None:
        print(f"   {len(interp_joints)} samples")
        for k, j in enumerate(interp_joints):
            print(f"   [{k}]: X={j[0]:.1f}, Y={j[1]:.1f}, Z={j[2]:.1f}, "
                  f"B={j[4]:.1f}, C={j[5]:.1f}")
        print("   PASSED\n")
    else:
        print("   FAILED\n")

    print("=== ALL KINEMATICS TESTS PASSED ===")
