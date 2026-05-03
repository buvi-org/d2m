"""Material removal engine -- the core simulation algorithm.

Subtracts tool volumes from the tri-dexel workpiece representation.
This is the hot path of the entire simulation system.

Algorithm per tool pose:
1. For each dexel grid (Z, X, Y):
   a. Transform tool bbox to world frame, get affected columns (bbox cull)
   b. For each affected column, transform ray to tool-local
   c. Compute ray-tool intersection intervals
   d. Subtract intervals from the column

For swept volumes (toolpaths between two poses):
- Sample intermediate poses, compute union of intersection intervals
  across all samples per column, then subtract once.
"""

from dataclasses import dataclass, field
from typing import Optional
import time
import numpy as np

from .tri_dexel import TriDexelModel, DexelColumn, DexelGrid, AABB
from .tools import Tool
from .kinematics import ToolPose
from .swept_volume import (
    SweptVolumeSampler, SweptIntervalResult,
    world_to_tool, direction_to_tool,
)


# =========================================================================
#  Result types
# =========================================================================

@dataclass
class RemovalResult:
    """Statistics from a material removal operation.

    Attributes:
        columns_modified: Number of dexel columns that were changed.
        volume_removed:   Total volume removed in mm^3.
        time_ms:          Time taken for the operation (ms).
        grid_results:     Per-grid detail dict.
    """
    columns_modified: int = 0
    volume_removed: float = 0.0
    time_ms: float = 0.0
    grid_results: dict = field(default_factory=dict)


@dataclass
class Gouge:
    """A detected gouge (material removed below target surface).

    Attributes:
        position: (3,) float gouge location (mm).
        depth:    Depth of gouge in mm (positive = below target).
        severity: 'minor' | 'moderate' | 'severe'.
    """
    position: np.ndarray
    depth: float
    severity: str = "minor"


@dataclass
class Collision:
    """A detected collision.

    Attributes:
        tool_position:  (3,) float, tool position at collision (mm).
        collision_type: e.g. 'holder_part', 'tool_fixture'.
        penetration:    Overlap depth in mm.
    """
    tool_position: np.ndarray
    collision_type: str
    penetration: float = 0.0


# =========================================================================
#  Material Removal Engine
# =========================================================================

class MaterialRemovalEngine:
    """Engine for subtracting tool volumes from a tri-dexel workpiece model.

    Performs material removal at single tool poses and along swept paths.
    Uses bounding-box culling to minimise the number of columns checked.

    Attributes:
        tri_dexel:      The TriDexelModel representing the workpiece.
        swept_sampler:  SweptVolumeSampler for toolpath discretisation.
    """

    def __init__(self, tri_dexel: TriDexelModel,
                 linear_resolution: float = 0.1,
                 angular_resolution_deg: float = 5.0):
        self.tri_dexel = tri_dexel
        self.swept_sampler = SweptVolumeSampler(
            linear_resolution=linear_resolution,
            angular_resolution_deg=angular_resolution_deg,
        )

    # -----------------------------------------------------------------
    #  Single-pose removal
    # -----------------------------------------------------------------

    def remove_tool_at_pose(self, tool: Tool, pose: ToolPose) -> RemovalResult:
        """Subtract tool volume at a single pose from all three dexel grids.

        Args:
            tool: Cutting tool.
            pose: ToolPose in workpiece coordinates.

        Returns:
            RemovalResult with aggregate statistics.
        """
        t_start = time.perf_counter()
        total_cols = 0
        total_vol = 0.0
        results: dict = {}

        grids = [
            ("z", self.tri_dexel.dexel_z),
            ("x", self.tri_dexel.dexel_x),
            ("y", self.tri_dexel.dexel_y),
        ]

        for axis, grid in grids:
            n_cols, vol = self._remove_at_pose_on_grid(tool, pose, grid)
            total_cols += n_cols
            total_vol += vol
            results[axis] = {"columns_modified": n_cols, "volume_removed": vol}

        t_elapsed = (time.perf_counter() - t_start) * 1000.0

        return RemovalResult(
            columns_modified=total_cols,
            volume_removed=total_vol,
            time_ms=t_elapsed,
            grid_results=results,
        )

    def _remove_at_pose_on_grid(
        self, tool: Tool, pose: ToolPose, grid: DexelGrid,
    ) -> tuple[int, float]:
        """Subtract tool at a single pose from one DexelGrid.

        Returns (columns_modified, volume_removed).
        """
        # Transform tool bbox to world frame
        world_bbox = self._tool_bbox_in_world(tool, pose)
        affected = grid.affected_columns(world_bbox)

        if not affected:
            return 0, 0.0

        cols_modified = 0
        vol_removed = 0.0
        ray_dir = grid.ray_direction()

        for i, j in affected:
            col = grid.get_column(i, j)
            vol_before = col.material_volume()

            ray_orig = grid.ray_origin(i, j)
            O_local = world_to_tool(ray_orig, pose)
            D_local = direction_to_tool(ray_dir, pose)

            intersection = tool.ray_intersection(O_local, D_local)
            if intersection.is_empty:
                continue

            for iv in intersection.intervals:
                col.subtract(iv.start, iv.end)

            vol_after = col.material_volume()
            vol_diff = vol_before - vol_after
            if vol_diff > 1e-12:
                cols_modified += 1
                vol_removed += vol_diff

        # Convert from linear distance to volume (multiply by cell area)
        cell_area = grid.resolution * grid.resolution
        vol_removed *= cell_area

        return cols_modified, vol_removed

    # -----------------------------------------------------------------
    #  Swept-volume removal
    # -----------------------------------------------------------------

    def remove_tool_swept(self, tool: Tool, start_pose: ToolPose,
                          end_pose: ToolPose) -> RemovalResult:
        """Subtract tool swept volume along a 5-axis move.

        Samples intermediate poses, computes the union of intersection
        intervals across all samples per column, subtracts once.

        Args:
            tool:        Cutting tool.
            start_pose:  Start tool pose.
            end_pose:    End tool pose.

        Returns:
            RemovalResult with aggregate statistics.
        """
        t_start = time.perf_counter()
        total_cols = 0
        total_vol = 0.0
        results: dict = {}

        grids = [
            ("z", self.tri_dexel.dexel_z),
            ("x", self.tri_dexel.dexel_x),
            ("y", self.tri_dexel.dexel_y),
        ]

        for axis, grid in grids:
            n_cols, vol = self._remove_swept_on_grid(
                tool, start_pose, end_pose, grid
            )
            total_cols += n_cols
            total_vol += vol
            results[axis] = {"columns_modified": n_cols, "volume_removed": vol}

        t_elapsed = (time.perf_counter() - t_start) * 1000.0

        return RemovalResult(
            columns_modified=total_cols,
            volume_removed=total_vol,
            time_ms=t_elapsed,
            grid_results=results,
        )

    def _remove_swept_on_grid(
        self, tool: Tool, start_pose: ToolPose, end_pose: ToolPose,
        grid: DexelGrid,
    ) -> tuple[int, float]:
        """Subtract swept volume on one DexelGrid.

        1. Sample poses between start and end.
        2. For each column, union intersection intervals across all poses.
        3. Subtract the union from the column.
        """
        # Use the SweptVolumeSampler to get per-column interval unions
        swept = self.swept_sampler.compute_swept_intervals(
            tool, start_pose, end_pose, grid
        )

        if not swept.intervals:
            return 0, 0.0

        cols_modified = 0
        vol_removed = 0.0

        for (i, j), to_remove in swept.intervals.items():
            col = grid.get_column(i, j)
            vol_before = col.material_volume()

            for iv in to_remove.intervals:
                col.subtract(iv.start, iv.end)

            vol_after = col.material_volume()
            vol_diff = vol_before - vol_after
            if vol_diff > 1e-12:
                cols_modified += 1
                vol_removed += vol_diff

        cell_area = grid.resolution * grid.resolution
        vol_removed *= cell_area

        return cols_modified, vol_removed

    # -----------------------------------------------------------------
    #  Helpers
    # -----------------------------------------------------------------

    def _tool_bbox_in_world(self, tool: Tool, pose: ToolPose) -> AABB:
        """Compute the tool's world-space AABB at a given pose."""
        from .swept_volume import quaternion_to_matrix

        local = tool.bbox_at_origin()
        R = quaternion_to_matrix(pose.orientation)

        corners = np.array([
            [local.min[0], local.min[1], local.min[2]],
            [local.max[0], local.min[1], local.min[2]],
            [local.min[0], local.max[1], local.min[2]],
            [local.min[0], local.min[1], local.max[2]],
            [local.max[0], local.max[1], local.min[2]],
            [local.max[0], local.min[1], local.max[2]],
            [local.min[0], local.max[1], local.max[2]],
            [local.max[0], local.max[1], local.max[2]],
        ])
        corners_world = (R @ corners.T).T + pose.position

        return AABB(
            min=corners_world.min(axis=0),
            max=corners_world.max(axis=0),
        )

    # -----------------------------------------------------------------
    #  Validation stubs (Phase 6)
    # -----------------------------------------------------------------

    def validate_no_gouge(self, target_vertices: np.ndarray,
                          target_faces: np.ndarray,
                          tolerance: float = 0.01) -> list[Gouge]:
        """Check for material removed below the target surface.

        Full implementation in Phase 6 (validator.py).
        """
        return []

    def compute_uncut_volume(self, target_vertices: np.ndarray,
                             target_faces: np.ndarray) -> float:
        """Volume of material remaining above the target surface.

        Full implementation in Phase 6.
        """
        return 0.0


# =========================================================================
#  Self-test
# =========================================================================

if __name__ == "__main__":
    print("=== Material Removal Engine Self-Test ===\n")

    import trimesh
    from .tools import BallEndmill, FlatEndmill
    from .swept_volume import quaternion_to_matrix

    # ------------------------------------------------------------------
    # 1. Single pose removal -- ball endmill into box
    # ------------------------------------------------------------------
    print("1. Single-pose removal: ball endmill plunging into box ...")

    stock = trimesh.creation.box(extents=[20.0, 20.0, 20.0])
    model = TriDexelModel.from_mesh(stock, resolution=0.5)
    engine = MaterialRemovalEngine(model, linear_resolution=0.5)

    vol_before = model.volume()
    print(f"   Stock volume before: {vol_before:.2f} mm^3")

    tool = BallEndmill(diameter=6.0, flute_length=30.0)
    # Plunge 5mm deep at the center of the top face
    # Box origin is at (-10,-10,-10) (trimesh centers at origin for 20x20x20)
    # Top face at z=0. Tool tip starts at z=0 and plunges to z=-5.
    # Wait -- tool tip at origin. We want the tool at the center.
    pose = ToolPose(
        position=np.array([0.0, 0.0, 0.0]),
        orientation=np.array([1.0, 0.0, 0.0, 0.0]),
    )

    result = engine.remove_tool_at_pose(tool, pose)
    vol_after = model.volume()
    vol_removed = vol_before - vol_after

    print(f"   Stock volume after:  {vol_after:.2f} mm^3")
    print(f"   Volume removed:      {vol_removed:.2f} mm^3")
    print(f"   Columns modified:    {result.columns_modified}")
    print(f"   Time:                {result.time_ms:.3f} ms")

    # A 6mm diameter ball endmill at the center of the top face:
    # Should remove roughly a hemispherical volume = 2/3 * pi * (3)^3 ≈ 56.5 mm^3
    expected_min = 30.0  # conservative
    assert vol_removed > expected_min, (
        f"Volume removed {vol_removed:.1f} < expected minimum {expected_min:.1f}"
    )
    assert result.columns_modified > 0, "No columns were modified"
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 2. Swept volume -- horizontal slot cut
    # ------------------------------------------------------------------
    print("2. Swept volume: ball endmill cutting a horizontal slot ...")

    model2 = TriDexelModel.from_mesh(stock, resolution=0.5)
    engine2 = MaterialRemovalEngine(model2, linear_resolution=0.5)

    vol_before2 = model2.volume()

    # Move from (-5, 0, 0) to (5, 0, 0) -- 10mm slot across the center
    start = ToolPose(
        position=np.array([-5.0, 0.0, 0.0]),
        orientation=np.array([1.0, 0.0, 0.0, 0.0]),
    )
    end = ToolPose(
        position=np.array([5.0, 0.0, 0.0]),
        orientation=np.array([1.0, 0.0, 0.0, 0.0]),
    )

    result2 = engine2.remove_tool_swept(tool, start, end)
    vol_after2 = model2.volume()
    vol_removed2 = vol_before2 - vol_after2

    print(f"   Volume removed:      {vol_removed2:.2f} mm^3")
    print(f"   Columns modified:    {result2.columns_modified}")
    print(f"   Time:                {result2.time_ms:.3f} ms")

    # Slot of length ~10mm with 6mm ball endmill at z=0:
    # Rough volume = 10 * (pi * 3^2 / 2) ≈ 141.4 mm^3 (half cylinder sweep)
    assert vol_removed2 > 50.0, (
        f"Swept volume removed {vol_removed2:.1f} < expected minimum 50.0"
    )
    assert result2.columns_modified > 0, "No columns modified in swept removal"
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 3. 5-axis tilted tool removal
    # ------------------------------------------------------------------
    print("3. 5-axis tilted tool: ball endmill at 45 degrees ...")

    model3 = TriDexelModel.from_mesh(stock, resolution=0.5)
    engine3 = MaterialRemovalEngine(model3, linear_resolution=0.5)

    vol_before3 = model3.volume()

    # Tool tilted 45 degrees about Y axis
    angle = np.radians(45.0)
    half = angle / 2.0
    q_tilted = np.array([np.cos(half), 0.0, np.sin(half), 0.0])

    pose3 = ToolPose(
        position=np.array([0.0, 0.0, 0.0]),
        orientation=q_tilted,
    )

    result3 = engine3.remove_tool_at_pose(tool, pose3)
    vol_after3 = model3.volume()
    vol_removed3 = vol_before3 - vol_after3

    print(f"   Volume removed:      {vol_removed3:.2f} mm^3")
    print(f"   Columns modified:    {result3.columns_modified}")
    print(f"   Time:                {result3.time_ms:.3f} ms")

    assert vol_removed3 > 20.0, (
        f"Tilted volume removed {vol_removed3:.1f} < expected minimum 20.0"
    )
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 4. Material-at-point check after removal
    # ------------------------------------------------------------------
    print("4. Material-at-point after removal ...")

    # After the tilted tool removal, the area near the top should have less material
    has_mat = model3.get_material_at(np.array([0.0, 0.0, -0.5]))
    print(f"   Material at (0, 0, -0.5): {has_mat}")

    # Deep inside the box (near bottom), material should still be intact
    # Box is 20x20x20 centered at origin, so bottom at z=-10
    deep_mat = model3.get_material_at(np.array([0.0, 0.0, -8.0]))
    print(f"   Material at (0, 0, -8.0): {deep_mat}")
    assert deep_mat, "Deep inside box should still have material"

    # Point outside the box should return False
    outside_mat = model3.get_material_at(np.array([0.0, 0.0, -18.0]))
    print(f"   Material at (0, 0, -18) [outside]: {outside_mat}")
    assert not outside_mat, "Point outside box should return False"
    print("   PASSED\n")

    print("=== ALL MATERIAL REMOVAL TESTS PASSED ===")
