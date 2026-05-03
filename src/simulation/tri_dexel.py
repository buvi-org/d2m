"""Core tri-dexel data structures and interval arithmetic.

The tri-dexel model represents a 3D solid as three orthogonal 2D grids of dexel
(depth element) columns. Each column stores sorted intervals of where material
exists along a ray in the grid's axis direction.

Reference: "Tri-Dexel Model for Geometric Simulation of 5-Axis CNC Machining"
"""

from dataclasses import dataclass
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
        return bool(np.all(point >= self.min) and np.all(point <= self.max))

    def intersects(self, other: "AABB") -> bool:
        return bool(np.all(self.max >= other.min) and np.all(other.max >= self.min))

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
    3. Adjacent intervals with zero gap are merged.

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

    # -----------------------------------------------------------------
    #  SUBTRACTION -- The Hot Path
    # -----------------------------------------------------------------

    def subtract(self, sub_start: float, sub_end: float) -> None:
        """Remove material from [sub_start, sub_end] in-place.

        O(n) single pass over the sorted intervals.  Builds a new list of
        surviving interval slices (worst-case length = original + 1 when a
        single interval is split).

        Handles five overlap cases for each interval [a, b] vs. [s, e]:

        Case 1  s <= a  and  b <= e   interval fully inside sub   -> delete
        Case 2  a <  s  and  e <  b   sub fully inside interval   -> split [a,s],[e,b]
        Case 3  s <= a  and  a < e <= b   sub overlaps left edge  -> [e, b]
        Case 4  a <= s < b  and  b <= e   sub overlaps right edge -> [a, s]
        Case 5  b <= s  or  a >= e        disjoint                -> keep as-is
        """
        if sub_end <= sub_start:
            return  # degenerate / zero-length removal is a no-op

        new_intervals: list[DexelInterval] = []

        for iv in self._intervals:
            a, b = iv.start, iv.end

            # Case 5a: interval entirely before subtraction range
            if b <= sub_start:
                new_intervals.append(iv)
                continue

            # Case 5b: interval entirely after subtraction range
            if a >= sub_end:
                new_intervals.append(iv)
                continue

            # Case 1: interval completely covered by subtraction
            if sub_start <= a and b <= sub_end:
                continue

            # Case 2: subtraction range lies wholly inside interval -> split
            if a < sub_start and sub_end < b:
                new_intervals.append(DexelInterval(a, sub_start, iv.material_id))
                new_intervals.append(DexelInterval(sub_end, b, iv.material_id))
                continue

            # Case 3: subtraction overlaps left (early) portion
            if sub_start <= a and a < sub_end < b:
                new_intervals.append(DexelInterval(sub_end, b, iv.material_id))
                continue

            # Case 4: subtraction overlaps right (late) portion
            if a < sub_start < b and b <= sub_end:
                new_intervals.append(DexelInterval(a, sub_start, iv.material_id))
                continue

            # Fallback (should never reach here if cases are complete)
            new_intervals.append(iv)

        self._intervals = new_intervals

    # -----------------------------------------------------------------
    #  UNION
    # -----------------------------------------------------------------

    def union(self, other: "DexelColumn") -> "DexelColumn":
        """Merge two DexelColumns into one, combining overlapping intervals.

        Uses the classic merge-sort merge step over two sorted lists.
        Complexity: O(n + m) where n, m are the interval counts.

        Args:
            other: Another DexelColumn to merge with this one.

        Returns:
            New DexelColumn with merged, sorted, non-overlapping intervals.
        """
        if self.is_empty:
            return other.copy()
        if other.is_empty:
            return self.copy()

        # Merge-sort the two interval lists by start value, then compact
        merged: list[DexelInterval] = []
        i, j = 0, 0
        a = self._intervals
        b = other._intervals

        # Build sorted merged list of all intervals (may have overlaps)
        all_ivs: list[DexelInterval] = []
        while i < len(a) and j < len(b):
            if a[i].start <= b[j].start:
                all_ivs.append(DexelInterval(a[i].start, a[i].end, a[i].material_id))
                i += 1
            else:
                all_ivs.append(DexelInterval(b[j].start, b[j].end, b[j].material_id))
                j += 1
        while i < len(a):
            all_ivs.append(DexelInterval(a[i].start, a[i].end, a[i].material_id))
            i += 1
        while j < len(b):
            all_ivs.append(DexelInterval(b[j].start, b[j].end, b[j].material_id))
            j += 1

        # Compact: merge overlapping / adjacent intervals
        if not all_ivs:
            return DexelColumn()

        result: list[DexelInterval] = []
        current = DexelInterval(all_ivs[0].start, all_ivs[0].end, all_ivs[0].material_id)

        for iv in all_ivs[1:]:
            if iv.start <= current.end:
                # Overlap or adjacency -- extend current
                current.end = max(current.end, iv.end)
            else:
                result.append(current)
                current = DexelInterval(iv.start, iv.end, iv.material_id)
        result.append(current)

        return DexelColumn(result)

    # -----------------------------------------------------------------
    #  INTERSECTION
    # -----------------------------------------------------------------

    def intersect_range(self, start: float, end: float) -> "DexelColumn":
        """Extract intervals within [start, end], clipped to the range.

        Complexity: O(n) single pass.

        Args:
            start: Start of query range (mm).
            end: End of query range (mm).

        Returns:
            New DexelColumn with intervals clipped to [start, end].
        """
        if end <= start:
            return DexelColumn()

        result: list[DexelInterval] = []
        for iv in self._intervals:
            if iv.end <= start:
                continue  # before query range
            if iv.start >= end:
                break     # past query range (sorted, so we can exit)

            clipped_start = max(iv.start, start)
            clipped_end = min(iv.end, end)
            if clipped_start < clipped_end:
                result.append(DexelInterval(clipped_start, clipped_end, iv.material_id))

        return DexelColumn(result)

    # -----------------------------------------------------------------
    #  ADD / INSERT
    # -----------------------------------------------------------------

    def add_interval(self, start: float, end: float) -> None:
        """Add a material interval, merging with existing intervals if they overlap.

        This is equivalent to a self-union with a single-interval column.
        Complexity: O(n) -- finds insertion point, then merges forward.

        Args:
            start: Entry distance (mm).
            end: Exit distance (mm).
        """
        if end <= start:
            return

        # Build result list: copy intervals before insertion,
        # merge overlapping ones, copy intervals after
        result: list[DexelInterval] = []
        s, e = start, end
        inserted = False

        for iv in self._intervals:
            if iv.end < s:
                # Before the new interval
                result.append(iv)
            elif iv.start > e:
                # After the new interval, insert the merged one first
                if not inserted:
                    result.append(DexelInterval(s, e))
                    inserted = True
                result.append(iv)
            else:
                # Overlaps -- expand the new interval bounds
                s = min(s, iv.start)
                e = max(e, iv.end)

        if not inserted:
            result.append(DexelInterval(s, e))

        self._intervals = result

    # -----------------------------------------------------------------
    #  SERIALISATION
    # -----------------------------------------------------------------

    def to_flat(self) -> np.ndarray:
        """Return (N, 2) float64 array of [start, end] pairs for batch operations."""
        if not self._intervals:
            return np.empty((0, 2), dtype=np.float64)
        return np.array([[iv.start, iv.end] for iv in self._intervals], dtype=np.float64)

    @classmethod
    def from_flat(cls, arr: np.ndarray) -> "DexelColumn":
        """Create a DexelColumn from a (N, 2) array of [start, end] pairs.

        Assumes the array is already sorted and non-overlapping.
        """
        intervals = [DexelInterval(start=float(row[0]), end=float(row[1])) for row in arr]
        return cls(intervals)

    @classmethod
    def from_intervals_list(cls, pairs: list[Tuple[float, float]]) -> "DexelColumn":
        """Create a DexelColumn from a list of (start, end) tuples.

        Sorts and merges overlapping pairs to maintain invariants.
        """
        if not pairs:
            return cls()
        sorted_pairs = sorted(pairs, key=lambda p: p[0])
        result: list[DexelInterval] = []
        cur = DexelInterval(sorted_pairs[0][0], sorted_pairs[0][1])
        for s, e in sorted_pairs[1:]:
            if s <= cur.end:
                cur.end = max(cur.end, e)
            else:
                result.append(cur)
                cur = DexelInterval(s, e)
        result.append(cur)
        return cls(result)

    # -----------------------------------------------------------------
    #  UTILITIES
    # -----------------------------------------------------------------

    def copy(self) -> "DexelColumn":
        """Deep copy of this column."""
        return DexelColumn([DexelInterval(iv.start, iv.end, iv.material_id)
                            for iv in self._intervals])

    def first_entry(self) -> Optional[float]:
        """Return the start of the first (closest) material interval, or None."""
        if self._intervals:
            return self._intervals[0].start
        return None

    def last_exit(self) -> Optional[float]:
        """Return the end of the last (farthest) material interval, or None."""
        if self._intervals:
            return self._intervals[-1].end
        return None

    def __repr__(self) -> str:
        if not self._intervals:
            return "DexelColumn([])"
        ivals = ", ".join(f"[{iv.start:.3f}, {iv.end:.3f}]" for iv in self._intervals)
        return f"DexelColumn([{ivals}])"

    def __len__(self) -> int:
        return len(self._intervals)

    def __getitem__(self, idx: int) -> DexelInterval:
        return self._intervals[idx]


# =========================================================================
#  DexelGrid
# =========================================================================

class DexelGrid:
    """2D grid of DexelColumns representing rays along one axis direction.

    A DexelGrid with axis='z' represents rays cast along the +Z direction
    through a grid in the XY plane.  Each cell [i][j] corresponds to a ray
    at position (ox + i*res, oy + j*res, oz) going in +Z.

    Attributes:
        axis: 'x', 'y', or 'z' -- the direction dexel rays are cast.
        origin: (3,) numpy array (x, y, z) in workpiece coordinates.
        resolution: Grid spacing in mm.
        nu_cells: Number of cells in the first orthogonal axis.
        nv_cells: Number of cells in the second orthogonal axis.
    """

    __slots__ = ("axis", "origin", "resolution", "nu_cells", "nv_cells",
                 "_columns", "_ray_direction", "_nu_idx", "_nv_idx",
                 "_ray_axis_idx")

    # Mapping from axis to (nu_axis_idx, nv_axis_idx) -- indices into the
    # 3D origin vector for grid-plane coordinates.
    _AXIS_MAP = {
        "z": (0, 1, (0, 0, 1)),   # nu=X, nv=Y, ray_dir=(0,0,1)
        "x": (1, 2, (1, 0, 0)),   # nu=Y, nv=Z, ray_dir=(1,0,0)
        "y": (0, 2, (0, 1, 0)),   # nu=X, nv=Z, ray_dir=(0,1,0)
    }

    def __init__(self, axis: str, origin: Tuple[float, float, float],
                 resolution: float, nu_cells: int, nv_cells: int):
        axis_lower = axis.lower()
        if axis_lower not in self._AXIS_MAP:
            raise ValueError(f"Axis must be 'x', 'y', or 'z', got '{axis}'")

        self.axis = axis_lower
        self.origin = np.array(origin, dtype=np.float64)
        self.resolution = float(resolution)
        self.nu_cells = nu_cells
        self.nv_cells = nv_cells

        nu_idx, nv_idx, self._ray_direction = self._AXIS_MAP[axis_lower]
        self._nu_idx = nu_idx
        self._nv_idx = nv_idx
        self._ray_axis_idx = 3 - nu_idx - nv_idx  # the remaining axis

        # Initialize empty columns
        self._columns: list[list[DexelColumn]] = [
            [DexelColumn() for _ in range(nv_cells)]
            for _ in range(nu_cells)
        ]

    # -----------------------------------------------------------------
    #  Grid -> World coordinate helpers
    # -----------------------------------------------------------------

    def ray_origin(self, i: int, j: int) -> np.ndarray:
        """3D origin point of the ray for grid cell (i, j) in workpiece coords.

        For axis='z' (grid in XY):  ray_origin = (ox + i*res,  oy + j*res,  oz)
        For axis='x' (grid in YZ):  ray_origin = (ox,  oy + i*res,  oz + j*res)
        For axis='y' (grid in XZ):  ray_origin = (ox + i*res,  oy,  oz + j*res)
        """
        pt = self.origin.copy()
        pt[self._nu_idx] += (i + 0.5) * self.resolution
        pt[self._nv_idx] += (j + 0.5) * self.resolution
        return pt

    def ray_direction(self) -> np.ndarray:
        """Normalised ray direction vector for this grid.

        Returns (3,) float array: (0,0,1) for z-axis, etc.
        """
        return np.array(self._ray_direction, dtype=np.float64)

    def world_to_grid(self, point: np.ndarray) -> Tuple[int, int]:
        """Convert a 3D world point to (i, j) grid indices.

        Returns the nearest cell index, clamped to valid range.

        Args:
            point: (3,) float array in workpiece coordinates.

        Returns:
            (i, j) tuple of integer grid indices.
        """
        i = int((point[self._nu_idx] - self.origin[self._nu_idx]) / self.resolution)
        j = int((point[self._nv_idx] - self.origin[self._nv_idx]) / self.resolution)
        i = max(0, min(self.nu_cells - 1, i))
        j = max(0, min(self.nv_cells - 1, j))
        return i, j

    def grid_to_world(self, i: int, j: int, dist_along_ray: float) -> np.ndarray:
        """Convert a grid cell + distance along ray to a 3D world point.

        point = ray_origin(i, j) + dist_along_ray * ray_direction

        Args:
            i: nu-cell index.
            j: nv-cell index.
            dist_along_ray: Distance along the ray direction from the origin.

        Returns:
            (3,) float array, 3D world point.
        """
        return self.ray_origin(i, j) + dist_along_ray * self.ray_direction()

    # -----------------------------------------------------------------
    #  Access
    # -----------------------------------------------------------------

    def get_column(self, i: int, j: int) -> DexelColumn:
        """Get the DexelColumn at grid index (i, j)."""
        if not (0 <= i < self.nu_cells and 0 <= j < self.nv_cells):
            raise IndexError(
                f"Grid index ({i}, {j}) out of bounds "
                f"[0..{self.nu_cells - 1}, 0..{self.nv_cells - 1}]"
            )
        return self._columns[i][j]

    def set_column(self, i: int, j: int, col: DexelColumn) -> None:
        """Set the DexelColumn at grid index (i, j)."""
        if not (0 <= i < self.nu_cells and 0 <= j < self.nv_cells):
            raise IndexError(
                f"Grid index ({i}, {j}) out of bounds "
                f"[0..{self.nu_cells - 1}, 0..{self.nv_cells - 1}]"
            )
        self._columns[i][j] = col

    # -----------------------------------------------------------------
    #  Affected columns (bounding-box cull)
    # -----------------------------------------------------------------

    def affected_columns(self, bbox: AABB) -> list[Tuple[int, int]]:
        """Return (i, j) grid indices whose rays intersect a bounding box.

        Projects the bbox onto the grid plane and returns all cells
        within that projection.  This is the fast culling step before
        per-column ray-tool intersection.

        Args:
            bbox: Axis-aligned bounding box in workpiece coordinates.

        Returns:
            List of (i, j) tuples for columns potentially intersecting the bbox.
        """
        # Project bbox onto the grid plane
        imin_f = (bbox.min[self._nu_idx] - self.origin[self._nu_idx]) / self.resolution
        imax_f = (bbox.max[self._nu_idx] - self.origin[self._nu_idx]) / self.resolution
        jmin_f = (bbox.min[self._nv_idx] - self.origin[self._nv_idx]) / self.resolution
        jmax_f = (bbox.max[self._nv_idx] - self.origin[self._nv_idx]) / self.resolution

        imin = max(0, int(np.floor(imin_f)))
        imax = min(self.nu_cells - 1, int(np.ceil(imax_f)))
        jmin = max(0, int(np.floor(jmin_f)))
        jmax = min(self.nv_cells - 1, int(np.ceil(jmax_f)))

        if imin > imax or jmin > jmax:
            return []

        # Generate all pairs
        indices: list[Tuple[int, int]] = []
        for i in range(imin, imax + 1):
            for j in range(jmin, jmax + 1):
                indices.append((i, j))
        return indices

    # -----------------------------------------------------------------
    #  Initialisation from mesh (ray-casting)
    # -----------------------------------------------------------------

    def init_from_mesh(self, mesh: trimesh.Trimesh) -> None:
        """Initialise dexel columns by ray-casting through the mesh.

        Casts a ray for every cell in the grid.  Intersection points are
        paired into (entry, exit) intervals.  Only works correctly with
        watertight (closed, manifold) meshes.

        Uses trimesh.ray.intersects_location for per-ray intersection.
        For large grids this can be memory-intensive; batching is used
        to keep memory under control.

        Args:
            mesh: A watertight trimesh.Trimesh representing the workpiece.
        """
        # Compute an epsilon offset so rays start just outside the mesh
        bmin = mesh.bounds[0]
        bmax = mesh.bounds[1]
        axis_idx = self._ray_axis_idx
        eps = self.resolution * 2.0

        ray_dir = self.ray_direction()

        total_cells = self.nu_cells * self.nv_cells
        batch_size = 100_000  # cast up to 100k rays at a time
        flat_idx = 0

        # Pre-allocate origin array for batches
        while flat_idx < total_cells:
            batch_end = min(flat_idx + batch_size, total_cells)
            n_rays = batch_end - flat_idx

            origins = np.empty((n_rays, 3), dtype=np.float64)
            mapping = []  # (i, j) for each ray

            for idx in range(flat_idx, batch_end):
                i = idx // self.nv_cells
                j = idx % self.nv_cells
                origins[idx - flat_idx] = self.ray_origin(i, j)
                mapping.append((i, j))

            # Ray-cast from outside the bounds slightly
            # For z-axis: start below min z, look up
            # The ray origin is already computed at cell centres; we offset
            # along the negative direction to start before the mesh
            neg_dir = -ray_dir * (eps + self.resolution)
            origins_offset = origins + neg_dir

            # trimesh ray-cast: origins + directions
            directions = np.tile(ray_dir, (n_rays, 1))

            try:
                locations, index_ray, index_tri = mesh.ray.intersects_location(
                    ray_origins=origins_offset,
                    ray_directions=directions,
                    multiple_hits=True,
                )
            except Exception:
                # Fallback: try per-ray (slower but more robust)
                locations = np.empty((0, 3))
                index_ray = np.empty(0, dtype=np.int64)
                for r in range(n_rays):
                    try:
                        hits, _, _ = mesh.ray.intersects_location(
                            ray_origins=origins_offset[r:r+1],
                            ray_directions=directions[r:r+1],
                            multiple_hits=True,
                        )
                        if len(hits) > 0:
                            locations = np.vstack([locations, hits]) if len(locations) > 0 else hits
                            index_ray = np.append(index_ray, np.full(len(hits), r, dtype=np.int64))
                    except Exception:
                        pass

            # Group hits by ray index
            if len(locations) > 0:
                for r in range(n_rays):
                    mask = index_ray == r
                    hits_r = locations[mask]
                    if len(hits_r) == 0:
                        continue
                    # Project hits onto ray direction to get distances
                    dists = np.dot(hits_r - origins_offset[r], ray_dir)
                    dists.sort()
                    # Pair hits: even indices are entries, odd are exits
                    intervals: list[DexelInterval] = []
                    k = 0
                    while k + 1 < len(dists):
                        entry = dists[k]
                        exit_ = dists[k + 1]
                        if exit_ - entry > 1e-9:  # non-degenerate interval
                            intervals.append(DexelInterval(float(entry), float(exit_)))
                        k += 2
                    # Handle odd number of hits: last entry goes to the far bound
                    # (the mesh should be watertight, but be robust)
                    if k < len(dists):
                        intervals.append(DexelInterval(float(dists[k]), float(dists[k] + eps)))

                    i, j = mapping[r]
                    self._columns[i][j] = DexelColumn(intervals)

            flat_idx = batch_end

    # -----------------------------------------------------------------
    #  Statistics
    # -----------------------------------------------------------------

    @property
    def total_columns(self) -> int:
        return self.nu_cells * self.nv_cells

    @property
    def nonempty_columns(self) -> int:
        return sum(1 for row in self._columns for col in row if not col.is_empty)

    @property
    def size_bytes(self) -> int:
        """Estimated memory usage in bytes."""
        total = 0
        for row in self._columns:
            for col in row:
                # each interval = ~32 bytes (2 float64 + object overhead + list node)
                total += col.count * 32
        # Add the column object overhead: ~56 bytes per column
        total += self.total_columns * 56
        return total

    def material_volume_along_ray(self, i: int, j: int) -> float:
        """Material length along ray at (i, j) in mm."""
        return self._columns[i][j].material_volume()

    def total_volume(self) -> float:
        """Total material volume from this grid (mm^3).

        Sum of interval lengths * cell_area (resolution^2).
        """
        cell_area = self.resolution * self.resolution
        total = 0.0
        for row in self._columns:
            for col in row:
                total += col.material_volume() * cell_area
        return total


# =========================================================================
#  TriDexelModel
# =========================================================================

class TriDexelModel:
    """Three orthogonal DexelGrids representing a 3D workpiece.

    Uses three DexelGrids (along X, Y, and Z axes) to represent the workpiece
    from all three orthogonal directions.  This enables accurate material
    removal simulation for 5-axis machining where the tool can approach from
    any direction.

    Attributes:
        dexel_z: DexelGrid with rays along +Z (grid plane XY).
        dexel_x: DexelGrid with rays along +X (grid plane YZ).
        dexel_y: DexelGrid with rays along +Y (grid plane XZ).
        bounds:   AABB of the workpiece in mm.
        resolution: Grid spacing in mm (same for all grids).
    """

    __slots__ = ("dexel_z", "dexel_x", "dexel_y", "bounds", "resolution")

    def __init__(self, dexel_z: DexelGrid, dexel_x: DexelGrid,
                 dexel_y: DexelGrid, bounds: AABB, resolution: float):
        self.dexel_z = dexel_z
        self.dexel_x = dexel_x
        self.dexel_y = dexel_y
        self.bounds = bounds
        self.resolution = float(resolution)

    # -----------------------------------------------------------------
    #  Construction from mesh
    # -----------------------------------------------------------------

    @classmethod
    def from_mesh(cls, mesh: trimesh.Trimesh, resolution: float = 0.1) -> "TriDexelModel":
        """Create a TriDexelModel from a trimesh mesh.

        Voxelises the mesh into three orthogonal dexel grids at the specified
        resolution.  Each grid independently casts rays through the mesh.

        Args:
            mesh: A watertight trimesh.Trimesh representing the workpiece.
            resolution: Grid spacing in mm (default 0.1).

        Returns:
            Initialised TriDexelModel.
        """
        bmin = mesh.bounds[0]
        bmax = mesh.bounds[1]
        bounds = AABB(min=bmin.copy(), max=bmax.copy())

        # Number of cells in each direction:
        # For a Z-axis grid: nx = ceil((xmax - xmin) / res), ny = ceil((ymax - ymin) / res)
        ext = bmax - bmin
        nx = max(1, int(np.ceil(ext[0] / resolution)))
        ny = max(1, int(np.ceil(ext[1] / resolution)))
        nz_ = max(1, int(np.ceil(ext[2] / resolution)))

        origin = tuple(float(v) for v in bmin)

        # Create three grids -- each starts empty, populated afterward
        dexel_z = DexelGrid("z", origin, resolution, nx, ny)
        dexel_x = DexelGrid("x", origin, resolution, ny, nz_)  # YZ plane, nu=Y, nv=Z
        dexel_y = DexelGrid("y", origin, resolution, nx, nz_)  # XZ plane, nu=X, nv=Z

        # Populate from mesh
        dexel_z.init_from_mesh(mesh)
        dexel_x.init_from_mesh(mesh)
        dexel_y.init_from_mesh(mesh)

        return cls(dexel_z, dexel_x, dexel_y, bounds, resolution)

    # -----------------------------------------------------------------
    #  Material query
    # -----------------------------------------------------------------

    def get_material_at(self, point: np.ndarray) -> bool:
        """Test if a 3D point contains material (consensus: 2 out of 3 grids).

        Args:
            point: (3,) float array in workpiece coordinates.

        Returns:
            True if the point is inside the material.
        """
        # Quick reject: point outside the bounding box
        if not self.bounds.contains(point):
            return False

        votes = 0

        # Z-grid: XY -> Z
        if self.dexel_z.nu_cells > 0 and self.dexel_z.nv_cells > 0:
            i, j = self.dexel_z.world_to_grid(point)
            col = self.dexel_z.get_column(i, j)
            dist = point[2] - self.dexel_z.ray_origin(i, j)[2]
            for iv in col._intervals:
                if iv.start <= dist <= iv.end:
                    votes += 1
                    break

        # X-grid: YZ -> X
        if self.dexel_x.nu_cells > 0 and self.dexel_x.nv_cells > 0:
            i, j = self.dexel_x.world_to_grid(point)
            col = self.dexel_x.get_column(i, j)
            dist = point[0] - self.dexel_x.ray_origin(i, j)[0]
            for iv in col._intervals:
                if iv.start <= dist <= iv.end:
                    votes += 1
                    break

        # Y-grid: XZ -> Y
        if self.dexel_y.nu_cells > 0 and self.dexel_y.nv_cells > 0:
            i, j = self.dexel_y.world_to_grid(point)
            col = self.dexel_y.get_column(i, j)
            dist = point[1] - self.dexel_y.ray_origin(i, j)[1]
            for iv in col._intervals:
                if iv.start <= dist <= iv.end:
                    votes += 1
                    break

        return votes >= 2

    # -----------------------------------------------------------------
    #  Volume
    # -----------------------------------------------------------------

    def volume(self) -> float:
        """Total material volume from all three grids, averaged.

        Returns:
            Volume in mm^3.
        """
        v_z = self.dexel_z.total_volume()
        v_x = self.dexel_x.total_volume()
        v_y = self.dexel_y.total_volume()

        count = 0
        total = 0.0
        if v_z > 0:
            total += v_z
            count += 1
        if v_x > 0:
            total += v_x
            count += 1
        if v_y > 0:
            total += v_y
            count += 1
        return total / count if count > 0 else 0.0

    # -----------------------------------------------------------------
    #  Mesh extraction (stub -- full implementation in Phase 5)
    # -----------------------------------------------------------------

    def to_mesh(self) -> trimesh.Trimesh:
        """Extract a triangle mesh from the tri-dexel model.

        Uses modified marching cubes across all three dexel grids.
        Full implementation in Phase 5.

        Returns:
            A trimesh.Trimesh of the current material state.
        """
        # Stub -- implemented fully in Phase 5 (surface.py)
        # Returns a simple wireframe bbox for now
        corners = np.array([
            self.bounds.min,
            [self.bounds.max[0], self.bounds.min[1], self.bounds.min[2]],
            [self.bounds.max[0], self.bounds.max[1], self.bounds.min[2]],
            [self.bounds.min[0], self.bounds.max[1], self.bounds.min[2]],
            [self.bounds.min[0], self.bounds.min[1], self.bounds.max[2]],
            [self.bounds.max[0], self.bounds.min[1], self.bounds.max[2]],
            self.bounds.max,
            [self.bounds.min[0], self.bounds.max[1], self.bounds.max[2]],
        ])
        return trimesh.Trimesh(vertices=corners)

    # -----------------------------------------------------------------
    #  Statistics
    # -----------------------------------------------------------------

    @property
    def memory_bytes(self) -> int:
        """Estimated total memory usage in bytes."""
        return (self.dexel_z.size_bytes +
                self.dexel_x.size_bytes +
                self.dexel_y.size_bytes)

    @property
    def total_nonempty_columns(self) -> int:
        """Total number of columns with material across all three grids."""
        return (self.dexel_z.nonempty_columns +
                self.dexel_x.nonempty_columns +
                self.dexel_y.nonempty_columns)

    def __repr__(self) -> str:
        return (
            f"TriDexelModel(res={self.resolution:.3f}mm, "
            f"bounds=[{self.bounds.min}, {self.bounds.max}], "
            f"vol={self.volume():.1f}mm^3, "
            f"mem={self.memory_bytes / 1024 / 1024:.1f}MB)"
        )


# =========================================================================
#  Self-test (runs when file is executed directly)
# =========================================================================

if __name__ == "__main__":
    print("=== Tri-Dexel Core Data Structures Self-Test ===\n")

    # ------------------------------------------------------------------
    # 1. DexelColumn.subtract -- all 5 cases
    # ------------------------------------------------------------------
    print("1. DexelColumn subtract test...")
    # Build a column with material from 0 to 10
    col = DexelColumn([DexelInterval(0.0, 10.0)])

    # Case 1: sub completely covers -> empty
    c1 = col.copy()
    c1.subtract(-1.0, 11.0)
    assert c1.is_empty, f"Case 1 failed: {c1}"

    # Case 2: sub inside interval -> split
    c2 = col.copy()
    c2.subtract(3.0, 7.0)
    assert len(c2) == 2, f"Case 2 failed: {c2}"
    assert abs(c2[0].start - 0.0) < 1e-9 and abs(c2[0].end - 3.0) < 1e-9
    assert abs(c2[1].start - 7.0) < 1e-9 and abs(c2[1].end - 10.0) < 1e-9

    # Case 3: sub overlaps left -> trim
    c3 = col.copy()
    c3.subtract(-1.0, 4.0)
    assert len(c3) == 1, f"Case 3 failed: {c3}"
    assert abs(c3[0].start - 4.0) < 1e-9 and abs(c3[0].end - 10.0) < 1e-9

    # Case 4: sub overlaps right -> trim
    c4 = col.copy()
    c4.subtract(6.0, 12.0)
    assert len(c4) == 1, f"Case 4 failed: {c4}"
    assert abs(c4[0].start - 0.0) < 1e-9 and abs(c4[0].end - 6.0) < 1e-9

    # Case 5: disjoint
    c5 = col.copy()
    c5.subtract(12.0, 15.0)
    assert len(c5) == 1, f"Case 5 failed: {c5}"

    # Edge case: exact match
    c6 = col.copy()
    c6.subtract(0.0, 10.0)
    assert c6.is_empty, f"Exact match failed: {c6}"

    # Edge case: zero-length subtraction
    c7 = col.copy()
    c7.subtract(5.0, 5.0)
    assert len(c7) == 1, f"Zero-length sub failed: {c7}"

    # Multi-interval subtraction
    c8 = DexelColumn([
        DexelInterval(0.0, 2.0),
        DexelInterval(4.0, 6.0),
        DexelInterval(8.0, 10.0),
    ])
    c8.subtract(1.0, 9.0)
    assert len(c8) == 2, f"Multi-interval sub failed: {c8}"
    assert abs(c8[0].end - 1.0) < 1e-9
    assert abs(c8[1].start - 9.0) < 1e-9
    print("   PASSED: All 5 subtract cases + edge cases\n")

    # ------------------------------------------------------------------
    # 2. DexelColumn.union
    # ------------------------------------------------------------------
    print("2. DexelColumn union test...")
    # a: [0,2] and [5,7],  b: [1,6] and [8,10]
    # Merged: [0,7] (from [0,2]+[1,6]+[5,7]) and [8,10] (gap at 7-8)
    a = DexelColumn([DexelInterval(0.0, 2.0), DexelInterval(5.0, 7.0)])
    b = DexelColumn([DexelInterval(1.0, 6.0), DexelInterval(8.0, 10.0)])
    u = a.union(b)
    assert len(u) == 2, f"Union failed, expected 2 intervals: {u}"
    assert abs(u[0].start) < 1e-9 and abs(u[0].end - 7.0) < 1e-9, f"First interval: {u[0]}"
    assert abs(u[1].start - 8.0) < 1e-9 and abs(u[1].end - 10.0) < 1e-9, f"Second interval: {u[1]}"

    # Overlapping intervals that fully merge
    c = DexelColumn([DexelInterval(0.0, 4.0)])
    d = DexelColumn([DexelInterval(2.0, 6.0)])
    v = c.union(d)
    assert len(v) == 1, f"Merge should give 1 interval: {v}"
    assert abs(v[0].start) < 1e-9 and abs(v[0].end - 6.0) < 1e-9
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 3. DexelColumn.intersect_range
    # ------------------------------------------------------------------
    print("3. DexelColumn intersect_range test...")
    a = DexelColumn([DexelInterval(2.0, 5.0), DexelInterval(7.0, 9.0)])
    r = a.intersect_range(3.0, 8.0)
    assert len(r) == 2, f"Intersect failed: {r}"
    assert abs(r[0].start - 3.0) < 1e-9 and abs(r[0].end - 5.0) < 1e-9
    assert abs(r[1].start - 7.0) < 1e-9 and abs(r[1].end - 8.0) < 1e-9
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 4. DexelColumn.add_interval
    # ------------------------------------------------------------------
    print("4. DexelColumn add_interval test...")
    a = DexelColumn([DexelInterval(1.0, 3.0), DexelInterval(6.0, 8.0)])
    # Add bridging interval that connects the two
    a.add_interval(3.0, 6.0)
    assert len(a) == 1, f"Add bridging failed: {a}"
    assert abs(a[0].start - 1.0) < 1e-9 and abs(a[0].end - 8.0) < 1e-9
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 5. DexelGrid ray_origin / world_to_grid / grid_to_world
    # ------------------------------------------------------------------
    print("5. DexelGrid coordinate transforms...")
    grid = DexelGrid("z", (0.0, 0.0, 0.0), 0.1, 100, 100)

    # ray_origin for cell (50, 50) should be (5.05, 5.05, 0)
    ro = grid.ray_origin(50, 50)
    assert abs(ro[0] - 5.05) < 1e-9, f"ray_origin x: {ro[0]}"
    assert abs(ro[1] - 5.05) < 1e-9, f"ray_origin y: {ro[1]}"
    assert abs(ro[2] - 0.0) < 1e-9, f"ray_origin z: {ro[2]}"

    i, j = grid.world_to_grid(np.array([5.05, 5.05, 3.0]))
    assert i == 50 and j == 50, f"world_to_grid: {(i, j)}"

    pt = grid.grid_to_world(50, 50, 3.0)
    assert abs(pt[2] - 3.0) < 1e-9, f"grid_to_world z: {pt[2]}"
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 6. DexelGrid.affected_columns
    # ------------------------------------------------------------------
    print("6. DexelGrid affected_columns (culling test)...")
    grid = DexelGrid("z", (0.0, 0.0, 0.0), 1.0, 100, 100)
    bbox = AABB(min=np.array([20.0, 30.0, -1.0]), max=np.array([25.0, 35.0, 1.0]))
    affected = grid.affected_columns(bbox)
    # Should cover columns [20..25] x [30..35] = 6*6 = 36 columns
    assert len(affected) == 36, f"affected_columns count: {len(affected)}"
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 7. TriDexelModel.from_mesh (with a simple box mesh)
    # ------------------------------------------------------------------
    print("7. TriDexelModel.from_mesh test (box mesh)...")
    box = trimesh.creation.box(extents=[10.0, 10.0, 10.0])
    model = TriDexelModel.from_mesh(box, resolution=0.5)
    vol = model.volume()
    expected_vol = 1000.0  # 10x10x10
    error_pct = abs(vol - expected_vol) / expected_vol * 100
    print(f"   Mesh volume: {expected_vol:.1f} mm^3")
    print(f"   Dexel volume: {vol:.1f} mm^3")
    print(f"   Error: {error_pct:.2f}%")
    print(f"   Memory: {model.memory_bytes / 1024 / 1024:.2f} MB")
    assert error_pct < 10.0, f"Volume error {error_pct:.2f}% exceeds 10%"

    # Test material query
    pt_inside = np.array([5.0, 5.0, 5.0])
    result = model.get_material_at(pt_inside)
    print(f"   Material at center (5,5,5): {result}")
    assert result, "Center of box should have material"

    pt_outside = np.array([15.0, 5.0, 5.0])
    result2 = model.get_material_at(pt_outside)
    print(f"   Material outside (15,5,5): {result2}")
    assert not result2, "Outside box should have no material"

    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 8. TriDexelModel.from_mesh with sphere (test volume accuracy)
    # ------------------------------------------------------------------
    print("8. TriDexelModel sphere volume accuracy test...")
    sphere = trimesh.creation.icosphere(subdivisions=4, radius=5.0)
    model2 = TriDexelModel.from_mesh(sphere, resolution=0.2)
    vol2 = model2.volume()
    expected_sphere_vol = (4.0 / 3.0) * np.pi * (5.0 ** 3)  # ~523.6 mm^3
    error_pct2 = abs(vol2 - expected_sphere_vol) / expected_sphere_vol * 100
    print(f"   Sphere volume (analytic): {expected_sphere_vol:.2f} mm^3")
    print(f"   Dexel volume: {vol2:.2f} mm^3")
    print(f"   Error: {error_pct2:.2f}%")
    print(f"   Memory: {model2.memory_bytes / 1024 / 1024:.2f} MB")
    assert error_pct2 < 15.0, f"Sphere volume error {error_pct2:.2f}% exceeds 15%"
    print("   PASSED\n")

    print("=== ALL TESTS PASSED ===")
