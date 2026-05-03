"""Core tri-dexel data structures and interval arithmetic.

The tri-dexel model represents a 3D solid as three orthogonal 2D grids of dexel
(depth element) columns. Each column stores sorted intervals of where material
exists along a ray in the grid's axis direction.

Reference: "Tri-Dexel Model for Geometric Simulation of 5-Axis CNC Machining"
"""

from dataclasses import dataclass, field
from typing import Optional, Tuple
import numpy as np
import trimesh


@dataclass(slots=True)
class DexelInterval:
    """A single [start, end] interval along a ray, representing material presence.

    Attributes:
        start: Distance from ray origin to material entry point (mm).
        end: Distance from ray origin to material exit point (mm).
        material_id: Reserved for multi-material support (default 0 = stock material).
    """
    start: float
    end: float
    material_id: int = 0

    @property
    def length(self) -> float:
        """Length of material along this interval in mm."""
        return self.end - self.start

    def contains(self, dist: float) -> bool:
        """Check if a distance along the ray falls within this interval."""
        return self.start <= dist <= self.end

    def overlaps(self, other_start: float, other_end: float) -> bool:
        """Check if this interval overlaps with [other_start, other_end]."""
        return self.start < other_end and other_start < self.end


@dataclass
class AABB:
    """Axis-Aligned Bounding Box."""
    min: np.ndarray  # (3,) float
    max: np.ndarray  # (3,) float

    @property
    def center(self) -> np.ndarray:
        return (self.min + self.max) / 2.0

    @property
    def extents(self) -> np.ndarray:
        return (self.max - self.min) / 2.0

    def contains(self, point: np.ndarray) -> bool:
        return np.all(point >= self.min) and np.all(point <= self.max)

    def intersects(self, other: "AABB") -> bool:
        return np.all(self.max >= other.min) and np.all(other.max >= self.min)

    def union(self, other: "AABB") -> "AABB":
        return AABB(
            min=np.minimum(self.min, other.min),
            max=np.maximum(self.max, other.max),
        )


class DexelColumn:
    """Sorted, non-overlapping list of DexelIntervals along a single ray.

    This is the core data structure. All interval operations maintain the invariants:
    1. Intervals are sorted by start value (ascending).
    2. Intervals do not overlap.
    3. Adjacent intervals are merged (no zero-gap pairs).

    The subtraction algorithm is the hot path -- O(n) single pass, minimal allocation.
    """

    __slots__ = ("_intervals",)

    def __init__(self, intervals: Optional[list[DexelInterval]] = None):
        self._intervals: list[DexelInterval] = intervals if intervals is not None else []

    @property
    def intervals(self) -> list[DexelInterval]:
        """Return a copy of the interval list (for external read access)."""
        return list(self._intervals)

    @property
    def is_empty(self) -> bool:
        return len(self._intervals) == 0

    @property
    def count(self) -> int:
        return len(self._intervals)

    def material_volume(self) -> float:
        """Total material length along this ray (sum of interval lengths)."""
        return sum(iv.length for iv in self._intervals)

    def subtract(self, sub_start: float, sub_end: float) -> None:
        """Remove material from [sub_start, sub_end] in-place.

        This is THE hot path. O(n) single pass with minimal allocation.
        Handles all 5 overlap cases:
        1. sub completely covers interval → remove interval
        2. sub completely inside interval → split into two
        3. sub overlaps left side → trim left
        4. sub overlaps right side → trim right
        5. disjoint → keep unchanged

        Args:
            sub_start: Start of removal range along the ray (mm).
            sub_end: End of removal range along the ray (mm).
        """
        # Placeholder -- will be fully implemented in Phase 2.
        pass

    def union(self, other: "DexelColumn") -> "DexelColumn":
        """Merge two DexelColumns into one, combining overlapping intervals.

        Complexity: O(n + m) where n, m are the interval counts.

        Args:
            other: Another DexelColumn to merge with this one.

        Returns:
            New DexelColumn with merged, sorted, non-overlapping intervals.
        """
        # Placeholder -- will be fully implemented in Phase 2.
        pass

    def intersect_range(self, start: float, end: float) -> "DexelColumn":
        """Extract intervals within [start, end], clipped to the range.

        Args:
            start: Start of query range (mm).
            end: End of query range (mm).

        Returns:
            New DexelColumn with intervals clipped to [start, end].
        """
        # Placeholder -- will be fully implemented in Phase 2.
        pass

    def add_interval(self, start: float, end: float) -> None:
        """Add a material interval, merging with existing intervals if they overlap.

        Args:
            start: Entry distance (mm).
            end: Exit distance (mm).
        """
        # Placeholder -- will be fully implemented in Phase 2.
        pass

    def to_flat(self) -> np.ndarray:
        """Return (N, 2) float64 array of [start, end] pairs for batch operations."""
        if not self._intervals:
            return np.empty((0, 2), dtype=np.float64)
        return np.array([[iv.start, iv.end] for iv in self._intervals], dtype=np.float64)

    @classmethod
    def from_flat(cls, arr: np.ndarray) -> "DexelColumn":
        """Create a DexelColumn from a (N, 2) array of [start, end] pairs."""
        intervals = [DexelInterval(start=row[0], end=row[1]) for row in arr]
        return cls(intervals)

    def copy(self) -> "DexelColumn":
        """Deep copy of this column."""
        return DexelColumn([DexelInterval(iv.start, iv.end, iv.material_id)
                            for iv in self._intervals])

    def __repr__(self) -> str:
        ivals = ", ".join(f"[{iv.start:.3f}, {iv.end:.3f}]" for iv in self._intervals)
        return f"DexelColumn([{ivals}])"

    def __len__(self) -> int:
        return len(self._intervals)

    def __getitem__(self, idx: int) -> DexelInterval:
        return self._intervals[idx]


class DexelGrid:
    """2D grid of DexelColumns representing rays along one axis direction.

    A DexelGrid with axis='Z' represents rays cast along the +Z direction
    through a grid in the XY plane. Each cell [i][j] corresponds to a ray
    at position (origin.x + i*res, origin.y + j*res, 0) going in +Z.

    Attributes:
        axis: 'x', 'y', or 'z' -- the direction dexe rays are cast.
        origin: (3,) tuple of (x, y, z) in workpiece coordinates.
        resolution: Grid spacing in mm.
        nu_cells: Number of cells in the first orthogonal axis.
        nv_cells: Number of cells in the second orthogonal axis.
    """

    __slots__ = ("axis", "origin", "resolution", "nu_cells", "nv_cells", "_columns")

    def __init__(self, axis: str, origin: Tuple[float, float, float],
                 resolution: float, nu_cells: int, nv_cells: int):
        self.axis = axis.lower()
        if self.axis not in ('x', 'y', 'z'):
            raise ValueError(f"Axis must be 'x', 'y', or 'z', got '{axis}'")

        self.origin = origin
        self.resolution = resolution
        self.nu_cells = nu_cells
        self.nv_cells = nv_cells
        self._columns: list[list[DexelColumn]] = []

    def get_column(self, i: int, j: int) -> DexelColumn:
        """Get the DexelColumn at grid index (i, j).

        Args:
            i: Index along the first orthogonal axis (nu).
            j: Index along the second orthogonal axis (nv).

        Returns:
            The DexelColumn at that cell.
        """
        if not (0 <= i < self.nu_cells and 0 <= j < self.nv_cells):
            raise IndexError(f"Grid index ({i}, {j}) out of bounds "
                             f"[0..{self.nu_cells-1}, 0..{self.nv_cells-1}]")
        return self._columns[i][j]

    def affected_columns(self, bbox: AABB) -> list[Tuple[int, int]]:
        """Return list of (i, j) grid indices whose rays intersect the bounding box.

        Uses bounding box projection onto the grid plane for fast culling.

        Args:
            bbox: Axis-aligned bounding box in workpiece coordinates.

        Returns:
            List of (i, j) tuples for columns potentially intersecting the bbox.
        """
        # Placeholder -- will be fully implemented in Phase 2.
        pass

    def init_from_mesh(self, mesh: trimesh.Trimesh) -> None:
        """Initialize dexel columns by ray-casting through the mesh.

        For each cell in the grid, casts a ray and computes the intersection
        intervals with the mesh, populating the corresponding DexelColumn.

        Args:
            mesh: A watertight trimesh representing the workpiece.
        """
        # Placeholder -- will be fully implemented in Phase 2.
        pass

    def ray_origin(self, i: int, j: int) -> np.ndarray:
        """Get the 3D origin point of the ray for grid cell (i, j).

        Args:
            i: Index along first orthogonal axis.
            j: Index along second orthogonal axis.

        Returns:
            (3,) numpy array of the ray origin in workpiece coordinates.
        """
        # Placeholder -- will be fully implemented in Phase 2.
        pass

    @property
    def size_bytes(self) -> int:
        """Estimated memory usage in bytes."""
        total = 0
        for row in self._columns:
            for col in row:
                total += col.count * 24  # approx per interval
        return total


class TriDexelModel:
    """Three orthogonal DexelGrids representing a 3D workpiece.

    Uses three DexelGrids (along X, Y, and Z axes) to represent the workpiece
    from all three orthogonal directions. This enables accurate material removal
    simulation for 5-axis machining where the tool can approach from any direction.

    Attributes:
        dexel_z: DexelGrid with rays along Z-axis (grid in XY plane).
        dexel_x: DexelGrid with rays along X-axis (grid in YZ plane).
        dexel_y: DexelGrid with rays along Y-axis (grid in XZ plane).
        bounds: AABB of the workpiece in mm.
        resolution: Grid spacing in mm (same for all grids).
    """

    __slots__ = ("dexel_z", "dexel_x", "dexel_y", "bounds", "resolution")

    def __init__(self, dexel_z: DexelGrid, dexel_x: DexelGrid,
                 dexel_y: DexelGrid, bounds: AABB, resolution: float):
        self.dexel_z = dexel_z
        self.dexel_x = dexel_x
        self.dexel_y = dexel_y
        self.bounds = bounds
        self.resolution = resolution

    @classmethod
    def from_mesh(cls, mesh: trimesh.Trimesh, resolution: float = 0.1) -> "TriDexelModel":
        """Create a TriDexelModel from a trimesh mesh.

        Voxelizes the mesh into three orthogonal dexel grids at the specified
        resolution. Each grid independently casts rays through the mesh.

        Args:
            mesh: A watertight trimesh representing the workpiece.
            resolution: Grid spacing in mm (default 0.1).

        Returns:
            Initialized TriDexelModel.
        """
        # Placeholder -- will be fully implemented in Phase 2.
        pass

    def to_mesh(self) -> trimesh.Trimesh:
        """Extract a triangle mesh from the tri-dexel model.

        Uses modified marching cubes across all three dexel grids.

        Returns:
            A trimesh.Trimesh of the current material state.
        """
        # Placeholder -- will be fully implemented in Phase 5.
        pass

    def get_material_at(self, point: np.ndarray) -> bool:
        """Test if a 3D point contains material (consensus: 2 out of 3 grids).

        Args:
            point: (3,) float array in workpiece coordinates.

        Returns:
            True if the point is inside the material.
        """
        # Placeholder -- will be fully implemented in Phase 2.
        pass

    def volume(self) -> float:
        """Total material volume from all three grids, averaged.

        Returns:
            Volume in mm^3.
        """
        # Placeholder -- will be fully implemented in Phase 2.
        pass

    @property
    def memory_bytes(self) -> int:
        """Estimated total memory usage."""
        return (self.dexel_z.size_bytes +
                self.dexel_x.size_bytes +
                self.dexel_y.size_bytes)
