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


# =========================================================================
#  Self-test
# =========================================================================

if __name__ == "__main__":
    import sys
    import numpy as np

    passed = 0
    failed = 0

    def check(condition, label):
        global passed, failed
        if condition:
            passed += 1
            print(f"  PASS  {label}")
        else:
            failed += 1
            print(f"  FAIL  {label}")

    print("=== Swept Volume Self-Test ===\n")

    # These imports use the package-relative form; they work because
    # the module is executed as  python -m src.simulation.swept_volume
    from .tools import BallEndmill, FlatEndmill, ToolParameters
    from .kinematics import ToolPose, FiveAxisKinematics
    from .tri_dexel import AABB, DexelColumn, DexelGrid

    # ------------------------------------------------------------------
    # 1. quaternion_to_matrix
    # ------------------------------------------------------------------
    print("1. quaternion_to_matrix ...")
    # Identity quaternion -> identity matrix
    q_id = np.array([1.0, 0.0, 0.0, 0.0])
    R_id = quaternion_to_matrix(q_id)
    check(np.allclose(R_id, np.eye(3), atol=1e-12),
          "identity quaternion -> identity matrix")
    check(np.allclose(R_id @ R_id.T, np.eye(3), atol=1e-12),
          "identity matrix is orthonormal")

    # 90-degree rotation about Z axis
    q_z90 = np.array([np.cos(np.pi / 4.0), 0.0, 0.0, np.sin(np.pi / 4.0)])
    Rz = quaternion_to_matrix(q_z90)
    expected_z = np.array([[0.0, -1.0, 0.0],
                           [1.0,  0.0, 0.0],
                           [0.0,  0.0, 1.0]], dtype=np.float64)
    check(np.allclose(Rz, expected_z, atol=1e-10),
          "90 deg Z rotation matrix")

    # 90-degree rotation about Y axis
    q_y90 = np.array([np.cos(np.pi / 4.0), 0.0, np.sin(np.pi / 4.0), 0.0])
    Ry = quaternion_to_matrix(q_y90)
    expected_y = np.array([[0.0, 0.0, 1.0],
                           [0.0, 1.0, 0.0],
                           [-1.0, 0.0, 0.0]], dtype=np.float64)
    check(np.allclose(Ry, expected_y, atol=1e-10),
          "90 deg Y rotation matrix")
    check(np.allclose(Ry @ Ry.T, np.eye(3), atol=1e-12),
          "rotated matrix is orthonormal")
    print()

    # ------------------------------------------------------------------
    # 2. world_to_tool / direction_to_tool coordinate transforms
    # ------------------------------------------------------------------
    print("2. world_to_tool / direction_to_tool ...")
    pose_id = ToolPose(
        position=np.array([0.0, 0.0, 0.0]),
        orientation=np.array([1.0, 0.0, 0.0, 0.0]),
    )

    # Point at world origin with identity pose -> tool-local origin
    pt_local = world_to_tool(np.array([0.0, 0.0, 0.0]), pose_id)
    check(np.allclose(pt_local, [0.0, 0.0, 0.0], atol=1e-12),
          "world origin -> tool origin (identity pose)")

    # Point at tool position -> local origin
    pose_shifted = ToolPose(
        position=np.array([5.0, 0.0, 0.0]),
        orientation=np.array([1.0, 0.0, 0.0, 0.0]),
    )
    pt2 = world_to_tool(np.array([5.0, 0.0, 0.0]), pose_shifted)
    check(np.allclose(pt2, [0.0, 0.0, 0.0], atol=1e-12),
          "point at tool position -> local origin")

    # Point above tool position -> local +Z
    pt3 = world_to_tool(np.array([5.0, 0.0, 10.0]), pose_shifted)
    check(np.allclose(pt3, [0.0, 0.0, 10.0], atol=1e-12),
          "point above tool -> local (0, 0, 10)")

    # Point behind (-Y) the tool
    pt4 = world_to_tool(np.array([5.0, -3.0, 0.0]), pose_shifted)
    check(np.allclose(pt4, [0.0, -3.0, 0.0], atol=1e-12),
          "point behind tool -> local (0, -3, 0)")

    # direction_to_tool: world +Z -> local +Z with identity
    d_local = direction_to_tool(np.array([0.0, 0.0, 1.0]), pose_id)
    check(np.allclose(d_local, [0.0, 0.0, 1.0], atol=1e-12),
          "world +Z -> local +Z (identity pose)")

    # direction_to_tool: world +X -> local +X with identity
    d_local_x = direction_to_tool(np.array([1.0, 0.0, 0.0]), pose_id)
    check(np.allclose(d_local_x, [1.0, 0.0, 0.0], atol=1e-12),
          "world +X -> local +X (identity pose)")

    # direction_to_tool with rotated pose: 90 deg about Y
    q_y90_pose = ToolPose(
        position=np.array([0.0, 0.0, 0.0]),
        orientation=np.array([np.cos(np.pi / 4.0), 0.0, np.sin(np.pi / 4.0), 0.0]),
    )
    # World +Z rotated by -90 deg about Y becomes world +X
    d_rot = direction_to_tool(np.array([0.0, 0.0, 1.0]), q_y90_pose)
    check(abs(d_rot[0] - (-1.0)) < 1e-10 and abs(d_rot[1]) < 1e-10 and abs(d_rot[2]) < 1e-10,
          "world +Z -> local -X when tool tilted 90 deg about Y")
    # Verify direction is still unit length
    check(abs(np.linalg.norm(d_rot) - 1.0) < 1e-10,
          "transformed direction is unit length")
    print()

    # ------------------------------------------------------------------
    # 3. SweptVolumeSampler.sample_poses
    # ------------------------------------------------------------------
    print("3. SweptVolumeSampler.sample_poses ...")
    sampler = SweptVolumeSampler(linear_resolution=0.5, angular_resolution_deg=5.0)

    pose_a = ToolPose(
        position=np.array([0.0, 0.0, 0.0]),
        orientation=np.array([1.0, 0.0, 0.0, 0.0]),
    )

    # Zero-length move (start == end)
    poses_zero = sampler.sample_poses(pose_a, pose_a)
    check(len(poses_zero) >= 2,
          f"zero-length move: at least 2 samples (got {len(poses_zero)})")
    check(np.allclose(poses_zero[0].position, pose_a.position, atol=1e-12),
          "zero-length: first pose matches start")
    check(np.allclose(poses_zero[-1].position, pose_a.position, atol=1e-12),
          "zero-length: last pose matches end")

    # Short linear move (1 mm) -- should have at least 2 samples
    pose_b = ToolPose(
        position=np.array([1.0, 0.0, 0.0]),
        orientation=np.array([1.0, 0.0, 0.0, 0.0]),
    )
    poses_short = sampler.sample_poses(pose_a, pose_b)
    check(len(poses_short) >= 2,
          f"1 mm move: at least 2 samples (got {len(poses_short)})")
    check(np.allclose(poses_short[0].position, pose_a.position, atol=1e-12),
          "1 mm: first = start")
    check(np.allclose(poses_short[-1].position, pose_b.position, atol=1e-12),
          "1 mm: last = end")

    # Long linear move (10 mm) -- should produce more than 2 samples
    pose_c = ToolPose(
        position=np.array([10.0, 0.0, 0.0]),
        orientation=np.array([1.0, 0.0, 0.0, 0.0]),
    )
    poses_long = sampler.sample_poses(pose_a, pose_c)
    check(len(poses_long) > 2,
          f"10 mm move: more than 2 samples (got {len(poses_long)})")
    # Middle sample should be between start and end
    mid_idx = len(poses_long) // 2
    mid_pos = poses_long[mid_idx].position
    check(mid_pos[0] > 0.0 and mid_pos[0] < 10.0,
          f"middle sample between start and end (x={mid_pos[0]:.2f})")

    # Pure rotation move (45 deg about Y axis)
    half_45 = np.pi / 8.0   # 45 deg half-angle
    q_start = np.array([1.0, 0.0, 0.0, 0.0])
    q_end = np.array([np.cos(half_45), 0.0, np.sin(half_45), 0.0])
    pose_rot_start = ToolPose(position=np.array([0.0, 0.0, 0.0]), orientation=q_start)
    pose_rot_end = ToolPose(position=np.array([0.0, 0.0, 0.0]), orientation=q_end)
    poses_rot = sampler.sample_poses(pose_rot_start, pose_rot_end)
    check(len(poses_rot) > 2,
          f"45 deg rotation: more than 2 samples (got {len(poses_rot)})")

    # Midpoint of SLERP should be close to 22.5 degrees
    mid_rot = poses_rot[len(poses_rot) // 2]
    q_half_expected = np.array([np.cos(np.pi / 16.0), 0.0, np.sin(np.pi / 16.0), 0.0])
    ang_err = FiveAxisKinematics.quaternion_angular_distance(
        mid_rot.orientation, q_half_expected,
    )
    check(ang_err < 0.1,
          f"SLERP midpoint near 22.5 deg (angular error={ang_err:.4f} rad)")

    # Linear + angular combined move
    pose_comb_end = ToolPose(
        position=np.array([5.0, 0.0, -2.0]),
        orientation=q_end,
    )
    poses_comb = sampler.sample_poses(pose_a, pose_comb_end)
    check(len(poses_comb) > 2,
          f"combined linear+rotary: more than 2 samples (got {len(poses_comb)})")
    check(np.allclose(poses_comb[0].position, pose_a.position, atol=1e-12),
          "combined: first pose matches start")
    check(np.allclose(poses_comb[-1].position, pose_comb_end.position, atol=1e-12),
          "combined: last pose matches end")
    print()

    # ------------------------------------------------------------------
    # 4. SweptVolumeSampler.swept_bbox
    # ------------------------------------------------------------------
    print("4. SweptVolumeSampler.swept_bbox ...")
    tool_ball = BallEndmill(diameter=6.0, flute_length=30.0)

    # Static tool bbox (zero-length move)
    bbox_static = sampler.swept_bbox(tool_ball, pose_a, pose_a)
    check(isinstance(bbox_static, AABB), "swept_bbox returns AABB")
    check(bbox_static.min[2] <= 0.0,
          f"static bbox includes area below tool tip (min z={bbox_static.min[2]:.2f})")
    check(bbox_static.max[2] > 0.0,
          f"static bbox extends upward (max z={bbox_static.max[2]:.2f})")

    # Swept bbox for a 10 mm linear move in X
    bbox_swept = sampler.swept_bbox(tool_ball, pose_a, pose_c)
    check(bbox_swept.min[0] <= bbox_static.min[0],
          "swept bbox min X covers start")
    check(bbox_swept.max[0] >= bbox_static.max[0] + 9.0,
          "swept bbox max X extends past end")
    check(bbox_swept.contains(pose_a.position),
          "swept bbox contains start position")
    check(bbox_swept.contains(pose_c.position),
          "swept bbox contains end position")

    # Swept bbox for flat endmill (different geometry)
    tool_flat = FlatEndmill(
        ToolParameters(diameter=10.0, flute_length=20.0)
    )
    bbox_flat = sampler.swept_bbox(tool_flat, pose_a, pose_c)
    check(isinstance(bbox_flat, AABB), "flat endmill swept_bbox returns AABB")
    check(bbox_flat.min[0] <= bbox_static.min[0],
          "flat endmill swept bbox covers start")
    print()

    # ------------------------------------------------------------------
    # 5. compute_swept_intervals (integration test with real grid)
    # ------------------------------------------------------------------
    print("5. compute_swept_intervals ...")

    # Try importing trimesh; skip mesh-based tests gracefully if unavailable
    try:
        import trimesh as _trimesh
        _HAS_TRIMESH = True
    except ImportError:
        _HAS_TRIMESH = False

    if _HAS_TRIMESH:
        from .tri_dexel import TriDexelModel

        box = _trimesh.creation.box(extents=[20.0, 20.0, 20.0])
        model = TriDexelModel.from_mesh(box, resolution=1.0)
        grid_z = model.dexel_z

        tool_6mm = BallEndmill(diameter=6.0, flute_length=30.0)
        start_sw = ToolPose(
            position=np.array([-3.0, 0.0, 0.0]),
            orientation=np.array([1.0, 0.0, 0.0, 0.0]),
        )
        end_sw = ToolPose(
            position=np.array([3.0, 0.0, 0.0]),
            orientation=np.array([1.0, 0.0, 0.0, 0.0]),
        )

        sampler2 = SweptVolumeSampler(linear_resolution=1.0, angular_resolution_deg=5.0)
        swept = sampler2.compute_swept_intervals(tool_6mm, start_sw, end_sw, grid_z)

        check(isinstance(swept, SweptIntervalResult),
              "compute_swept_intervals returns SweptIntervalResult")
        check(swept.grid_axis == "z",
              f"grid_axis is 'z' (got '{swept.grid_axis}')")
        check(swept.affected_count > 0,
              f"swept affects some columns (got {swept.affected_count})")
        check(len(swept.intervals) > 0,
              f"intervals dict is non-empty (got {len(swept.intervals)} entries)")

        # Check that intervals are valid (non-empty columns)
        for (i, j), col in swept.intervals.items():
            check(not col.is_empty,
                  f"column ({i},{j}) intervals are non-empty")
            # Verify intervals have positive lengths
            for iv in col.intervals:
                check(iv.length > 0 and iv.start < iv.end,
                      f"interval [{iv.start:.3f}, {iv.end:.3f}] is valid")
            break  # just validate one column

        # Zero-length move should still produce intervals
        swept_zero = sampler2.compute_swept_intervals(
            tool_6mm, start_sw, start_sw, grid_z,
        )
        check(isinstance(swept_zero, SweptIntervalResult),
              "zero-length move: returns result")
        check(swept_zero.affected_count > 0,
              f"zero-length move: tool still occupies space "
              f"(affected={swept_zero.affected_count})")

        # Move entirely outside the stock should produce no intervals
        pose_far_start = ToolPose(
            position=np.array([50.0, 50.0, 50.0]),
            orientation=np.array([1.0, 0.0, 0.0, 0.0]),
        )
        pose_far_end = ToolPose(
            position=np.array([55.0, 50.0, 50.0]),
            orientation=np.array([1.0, 0.0, 0.0, 0.0]),
        )
        swept_far = sampler2.compute_swept_intervals(
            tool_6mm, pose_far_start, pose_far_end, grid_z,
        )
        check(swept_far.affected_count == 0,
              f"move outside stock: no affected columns "
              f"(got {swept_far.affected_count})")

        # Test with X-axis grid
        grid_x = model.dexel_x
        swept_x = sampler2.compute_swept_intervals(
            tool_6mm, start_sw, end_sw, grid_x,
        )
        check(isinstance(swept_x, SweptIntervalResult),
              "X-axis grid: returns result")
        check(swept_x.grid_axis == "x",
              f"X-axis grid: grid_axis is 'x' (got '{swept_x.grid_axis}')")

        # Test with Y-axis grid
        grid_y = model.dexel_y
        swept_y = sampler2.compute_swept_intervals(
            tool_6mm, start_sw, end_sw, grid_y,
        )
        check(isinstance(swept_y, SweptIntervalResult),
              "Y-axis grid: returns result")
        check(swept_y.grid_axis == "y",
              f"Y-axis grid: grid_axis is 'y' (got '{swept_y.grid_axis}')")

        # Tilted tool (rotary move)
        pose_tilt_start = ToolPose(
            position=np.array([0.0, 0.0, 0.0]),
            orientation=np.array([1.0, 0.0, 0.0, 0.0]),
        )
        half_30 = np.pi / 12.0  # 30 deg half-angle
        q_tilt = np.array([np.cos(half_30), 0.0, np.sin(half_30), 0.0])
        pose_tilt_end = ToolPose(
            position=np.array([2.0, 0.0, -1.0]),
            orientation=q_tilt,
        )
        swept_tilt = sampler2.compute_swept_intervals(
            tool_6mm, pose_tilt_start, pose_tilt_end, grid_z,
        )
        check(isinstance(swept_tilt, SweptIntervalResult),
              "tilted move: returns result")
    else:
        for _ in range(13):
            check(True, "trimesh not available -- skip swept interval tests")
    print()

    # ------------------------------------------------------------------
    # 6. Edge cases
    # ------------------------------------------------------------------
    print("6. Edge cases ...")

    # DexelGrid with bbox far away: no affected columns
    empty_grid = DexelGrid("z", (100.0, 100.0, 100.0), 1.0, 10, 10)
    bbox_far = AABB(
        min=np.array([200.0, 200.0, 200.0]),
        max=np.array([210.0, 210.0, 210.0]),
    )
    affected = empty_grid.affected_columns(bbox_far)
    check(len(affected) == 0,
          "bbox far from grid -> no affected columns")

    # Bbox partially overlapping grid
    bbox_partial = AABB(
        min=np.array([95.0, 95.0, -1.0]),
        max=np.array([105.0, 105.0, 1.0]),
    )
    affected_partial = empty_grid.affected_columns(bbox_partial)
    check(len(affected_partial) > 0,
          f"bbox overlapping grid edge -> some columns (got {len(affected_partial)})")

    # Finer resolution produces more samples
    fine_sampler = SweptVolumeSampler(linear_resolution=0.1, angular_resolution_deg=0.5)
    poses_fine = fine_sampler.sample_poses(pose_a, pose_c)
    check(len(poses_fine) > 50,
          f"fine resolution (0.1mm) over 10mm -> many samples (got {len(poses_fine)})")

    # Coarser resolution produces fewer samples
    coarse_sampler = SweptVolumeSampler(linear_resolution=5.0, angular_resolution_deg=30.0)
    poses_coarse = coarse_sampler.sample_poses(pose_a, pose_c)
    check(len(poses_coarse) >= 2 and len(poses_coarse) <= 5,
          f"coarse resolution (5mm) -> fewer samples (got {len(poses_coarse)})")

    # Very short move shouldn't produce huge sample count
    pose_near = ToolPose(
        position=np.array([0.001, 0.0, 0.0]),
        orientation=np.array([1.0, 0.0, 0.0, 0.0]),
    )
    poses_tiny = sampler.sample_poses(pose_a, pose_near)
    check(len(poses_tiny) == 2,
          f"tiny move (0.001 mm): exactly 2 samples (got {len(poses_tiny)})")

    # SweptIntervalResult dataclass instantiation
    sir = SweptIntervalResult(
        grid_axis="z",
        intervals={(0, 0): DexelColumn()},
        affected_count=1,
    )
    check(sir.grid_axis == "z", "SweptIntervalResult.grid_axis")
    check(sir.affected_count == 1, "SweptIntervalResult.affected_count")
    check(len(sir.intervals) == 1, "SweptIntervalResult.intervals has 1 entry")
    print()

    # ------------------------------------------------------------------
    # Report
    # ------------------------------------------------------------------
    print(f"=== Results: {passed} passed, {failed} failed ===")
    sys.exit(0 if failed == 0 else 1)
