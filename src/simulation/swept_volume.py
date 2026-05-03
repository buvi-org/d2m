"""Tool swept volume computation for 5-axis CNC moves.

Computes the volume of space swept by a tool as it moves between two
poses.  Uses sampled intermediate poses (SLERP for rotation, linear for
translation) and computes the union of tool intersections at each pose.

The sampling error is bounded by the grid resolution.
"""

from dataclasses import dataclass
from typing import Dict, Tuple
import numpy as np

from .tri_dexel import AABB, DexelColumn, DexelGrid, TriDexelModel
from .tools import Tool
from .kinematics import ToolPose, FiveAxisKinematics


@dataclass
class SweptIntervalResult:
    """Result of computing swept intervals for a single grid.

    Attributes:
        grid_axis: 'x', 'y', or 'z' identifying which grid was processed.
        intervals: Dict mapping (i, j) -> DexelColumn of intervals to subtract.
        affected_count: Number of columns that had non-empty intersection.
    """
    grid_axis: str
    intervals: Dict[Tuple[int, int], DexelColumn]
    affected_count: int = 0


def quaternion_to_matrix(q: np.ndarray) -> np.ndarray:
    """Convert a unit quaternion [w, x, y, z] to a 3x3 rotation matrix.

    The matrix rotates vectors from the local frame to the world frame:
        v_world = R * v_local

    Args:
        q: (4,) quaternion [w, x, y, z], scalar-first.

    Returns:
        (3, 3) rotation matrix.
    """
    w, x, y, z = q[0], q[1], q[2], q[3]
    return np.array([
        [1 - 2*y*y - 2*z*z,     2*x*y - 2*w*z,     2*x*z + 2*w*y],
        [    2*x*y + 2*w*z, 1 - 2*x*x - 2*z*z,     2*y*z - 2*w*x],
        [    2*x*z - 2*w*y,     2*y*z + 2*w*x, 1 - 2*x*x - 2*y*y],
    ], dtype=np.float64)


def world_to_tool(point: np.ndarray, pose: ToolPose) -> np.ndarray:
    """Transform a point from workpiece frame to tool-local frame.

    Tool-local: tip at origin, tool axis along +Z.

    Args:
        point: (3,) float in workpiece coordinates.
        pose: ToolPose giving tool position and orientation in workpiece frame.

    Returns:
        (3,) float in tool-local coordinates.
    """
    R = quaternion_to_matrix(pose.orientation)
    # Inverse rotation: R.T = R^-1 (since R is orthonormal)
    return R.T @ (point - pose.position)


def direction_to_tool(direction: np.ndarray, pose: ToolPose) -> np.ndarray:
    """Transform a direction vector from workpiece to tool-local frame.

    Only applies rotation (no translation for directions).

    Args:
        direction: (3,) normalized direction in workpiece frame.
        pose: ToolPose.

    Returns:
        (3,) normalized direction in tool-local frame.
    """
    R = quaternion_to_matrix(pose.orientation)
    return R.T @ direction


class SweptVolumeSampler:
    """Samples tool poses along a 5-axis move and computes swept volume geometry.

    For each sampled pose, computes the tool's intersection with affected
    dexel columns.  Returns the union of all intersection intervals for
    material removal.

    Attributes:
        linear_resolution:   Maximum distance between pose samples (mm).
        angular_resolution:  Maximum angular change between samples (radians).
    """

    def __init__(self, linear_resolution: float = 0.1,
                 angular_resolution_deg: float = 5.0):
        self.linear_resolution = linear_resolution
        self.angular_resolution = np.radians(angular_resolution_deg)

    # -----------------------------------------------------------------
    #  Pose interpolation
    # -----------------------------------------------------------------

    def sample_poses(self, start_pose: ToolPose,
                     end_pose: ToolPose) -> list[ToolPose]:
        """Generate interpolated tool poses between start and end.

        Number of samples n is:
            n = max( 2,  ceil(translational_dist / linear_resolution) + 1,
                          ceil(angular_dist / angular_resolution) + 1  )

        Translation:  linear interpolation.
        Rotation:     SLERP (spherical linear interpolation).

        Args:
            start_pose: ToolPose at the start.
            end_pose:   ToolPose at the end.

        Returns:
            List of ToolPose from start to end, inclusive.
        """
        trans_dist = float(np.linalg.norm(end_pose.position - start_pose.position))
        ang_dist = FiveAxisKinematics.quaternion_angular_distance(
            start_pose.orientation, end_pose.orientation
        )

        n_trans = max(2, int(np.ceil(trans_dist / self.linear_resolution)) + 1)
        n_ang = max(2, int(np.ceil(ang_dist / self.angular_resolution)) + 1)
        n = max(n_trans, n_ang)

        result: list[ToolPose] = []
        for k in range(n):
            t = k / (n - 1) if n > 1 else 0.0
            pos = start_pose.position + t * (end_pose.position - start_pose.position)
            q = FiveAxisKinematics.slerp(
                start_pose.orientation, end_pose.orientation, t
            )
            result.append(ToolPose(position=pos.copy(), orientation=q.copy()))
        return result

    # -----------------------------------------------------------------
    #  Swept bounding box
    # -----------------------------------------------------------------

    def swept_bbox(self, tool: Tool, start_pose: ToolPose,
                   end_pose: ToolPose) -> AABB:
        """Bounding box of the entire swept volume.

        Expands the tool's local bbox to world frame at start and end,
        then takes the union.  This is a conservative (possibly loose)
        bound.

        Args:
            tool: The cutting tool.
            start_pose: Start tool pose.
            end_pose:   End tool pose.

        Returns:
            AABB containing the entire swept volume.
        """
        local_bbox = tool.bbox_at_origin()

        def bbox_in_world(pose: ToolPose) -> AABB:
            R = quaternion_to_matrix(pose.orientation)
            # Transform the 8 corners of the local bbox to world frame
            corners_local = np.array([
                [local_bbox.min[0], local_bbox.min[1], local_bbox.min[2]],
                [local_bbox.max[0], local_bbox.min[1], local_bbox.min[2]],
                [local_bbox.min[0], local_bbox.max[1], local_bbox.min[2]],
                [local_bbox.min[0], local_bbox.min[1], local_bbox.max[2]],
                [local_bbox.max[0], local_bbox.max[1], local_bbox.min[2]],
                [local_bbox.max[0], local_bbox.min[1], local_bbox.max[2]],
                [local_bbox.min[0], local_bbox.max[1], local_bbox.max[2]],
                [local_bbox.max[0], local_bbox.max[1], local_bbox.max[2]],
            ])
            corners_world = (R @ corners_local.T).T + pose.position
            return AABB(
                min=corners_world.min(axis=0),
                max=corners_world.max(axis=0),
            )

        bbox_start = bbox_in_world(start_pose)
        bbox_end = bbox_in_world(end_pose)

        # Also add intermediate samples for safety
        poses = self.sample_poses(start_pose, end_pose)
        bbox = bbox_start.union(bbox_end)
        for p in poses[1:-1]:
            bbox = bbox.union(bbox_in_world(p))

        return bbox

    # -----------------------------------------------------------------
    #  Compute swept intervals for one grid
    # -----------------------------------------------------------------

    def compute_swept_intervals(
        self, tool: Tool, start_pose: ToolPose, end_pose: ToolPose,
        grid: DexelGrid,
    ) -> SweptIntervalResult:
        """Compute ray-tool intersection intervals for all affected columns.

        For each column in the swept volume's projected bounding box,
        compute the union of tool intersection intervals across all
        sampled poses.

        Args:
            tool:        The cutting tool.
            start_pose:  Start tool pose.
            end_pose:    End tool pose.
            grid:        DexelGrid to compute for.

        Returns:
            SweptIntervalResult with a dict of (i,j) -> DexelColumn.
        """
        # 1. Compute swept bbox and affected columns
        bbox = self.swept_bbox(tool, start_pose, end_pose)
        affected = grid.affected_columns(bbox)

        if not affected:
            return SweptIntervalResult(
                grid_axis=grid.axis, intervals={}, affected_count=0
            )

        # 2. Sample poses
        poses = self.sample_poses(start_pose, end_pose)

        # 3. For each column, union intervals across all poses
        result: Dict[Tuple[int, int], DexelColumn] = {}
        affected_count = 0

        ray_dir_world = grid.ray_direction()

        for i, j in affected:
            ray_orig_world = grid.ray_origin(i, j)

            # Accumulate intervals from every pose
            merged = DexelColumn()
            for pose in poses:
                # Transform ray to tool-local
                O_local = world_to_tool(ray_orig_world, pose)
                D_local = direction_to_tool(ray_dir_world, pose)

                # Compute intersection in tool-local space
                col_local = tool.ray_intersection(O_local, D_local)
                if col_local.is_empty:
                    continue

                # Transform interval distances back to world-frame distances
                # The tool-local t values are along D_local.
                # D_local's magnitude is 1 (rotation preserves length), so
                # t_local == t_world  -- distances are invariant under rotation.
                # BUT the tool-local origin is different from the grid ray
                # origin, so t_local measures from the tool-local origin,
                # NOT from the grid ray origin.  We need to convert.
                #
                # In tool-local: point = O_local + t_local * D_local
                # In world:      point = ray_orig_world + t_world * ray_dir_world
                #
                # world_to_tool(ray_orig_world + t_world * D_world)
                #   = R.T * (ray_orig_world + t_world*D_world - pose.position)
                #   = R.T * (ray_orig_world - pose.position) + t_world * R.T * D_world
                #   = O_local + t_world * D_local
                #
                # So t_local = t_world + (O_local - world_to_tool(ray_orig, pose))
                # Actually, t_local = t_world, because:
                #   point_world = ray_orig_world + t_world * D_world
                #   point_local = R.T*(P_world - pose.position) = R.T*(P_world)
                #   O_local = R.T*(ray_orig_world - pose.position)
                #   D_local = R.T*D_world
                #   P_local = O_local + t_world * D_local
                # So t_world == t_local because the same t is used for both.
                #
                # The distance from the ray origin to the intersection point
                # is exactly t_local.  So we can use t_local directly.

                for iv in col_local.intervals:
                    # t_local values are our grid distances
                    merged.add_interval(iv.start, iv.end)

            if not merged.is_empty:
                result[(i, j)] = merged
                affected_count += 1

        return SweptIntervalResult(
            grid_axis=grid.axis, intervals=result, affected_count=affected_count,
        )
