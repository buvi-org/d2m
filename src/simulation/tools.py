"""APT standard tool definitions with ray-tool intersection formulas.

Supports the APT 7-parameter tool model with analytic ray-intersection
for each tool type. All tools are defined in their local coordinate frame:
tip at origin, tool axis along +Z.

Reference: ANSI/ISO 4343, APT Programmer's Reference Manual
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
import numpy as np

from .tri_dexel import DexelColumn


@dataclass
class ToolParameters:
    """APT 7-parameter tool geometry definition.

    Attributes:
        diameter: Cutting diameter D (mm).
        corner_radius: Corner radius R (mm). 0 for sharp corner.
        length: Total tool length L (mm).
        flute_length: Length of cutting flutes FL (mm).
        taper_angle: Side taper angle A (degrees). 0 = straight.
        tip_angle: Bottom angle B (degrees). 0 = flat, 90 = ball (full radius).
        tip_diameter: Diameter at tip d (mm). For drills, chamfer tools.
    """
    diameter: float
    corner_radius: float = 0.0
    length: float = 100.0
    flute_length: float = 50.0
    taper_angle: float = 0.0
    tip_angle: float = 0.0
    tip_diameter: float = 0.0


class Tool(ABC):
    """Abstract base class for all cutting tools.

    All tools are parameterized by their APT 7-parameter geometry.
    Subclasses implement analytic ray-tool intersection for their
    specific geometry.

    The tool coordinate system:
    - Tip at origin (0, 0, 0)
    - Tool axis along +Z
    - The cutting portion extends from z=0 to z=flute_length
    """

    def __init__(self, params: ToolParameters):
        self.params = params

    @property
    def diameter(self) -> float:
        return self.params.diameter

    @property
    def radius(self) -> float:
        return self.params.diameter / 2.0

    @property
    def length(self) -> float:
        return self.params.length

    @property
    def flute_length(self) -> float:
        return self.params.flute_length

    @abstractmethod
    def ray_intersection(self, ray_origin: np.ndarray, ray_direction: np.ndarray) -> DexelColumn:
        """Compute intersection intervals of this tool with a ray.

        The ray is given in the tool's local coordinate system:
        - origin: (3,) float, starting point of ray
        - direction: (3,) float, normalized ray direction

        Returns a DexelColumn with sorted entry/exit intervals where
        the ray passes through the tool volume.

        Args:
            ray_origin: (3,) float array, ray start in tool-local coords.
            ray_direction: (3,) float array, normalized ray direction.

        Returns:
            DexelColumn of intersection intervals (may be empty).
        """
        ...

    @abstractmethod
    def swept_volume_bbox(self, start_pose, end_pose) -> "AABB":
        """Compute the bounding box of the swept volume between two tool poses.

        Args:
            start_pose: ToolPose at the start of the move.
            end_pose: ToolPose at the end of the move.

        Returns:
            AABB enclosing the entire swept volume.
        """
        ...

    def bbox_at_origin(self) -> "AABB":
        """Axis-aligned bounding box of the tool in its local frame.

        Returns:
            AABB with min/max corners.
        """
        # Placeholder -- implement in Phase 2
        from .tri_dexel import AABB
        r = self.radius
        h = self.flute_length
        return AABB(
            min=np.array([-r, -r, 0.0]),
            max=np.array([r, r, h]),
        )


class FlatEndmill(Tool):
    """Flat endmill: cylinder + flat bottom disc.

    APT params: D > 0, R = 0, A = 0, B = 0.

    Geometry: Cylinder of radius D/2 from z=0 to z=FL,
    capped with a flat disc at z=0.
    """

    def ray_intersection(self, ray_origin: np.ndarray, ray_direction: np.ndarray) -> DexelColumn:
        # Placeholder -- implement in Phase 2
        return DexelColumn()

    def swept_volume_bbox(self, start_pose, end_pose) -> "AABB":
        # Placeholder -- implement in Phase 3
        from .tri_dexel import AABB
        return AABB(min=np.zeros(3), max=np.zeros(3))


class BallEndmill(Tool):
    """Ball endmill: cylinder + hemisphere at tip.

    APT params: D > 0, R = D/2, A = 0, B = 90.

    Geometry: Cylinder of radius D/2 from z=R to z=FL,
    hemisphere of radius D/2 centered at (0, 0, D/2).
    This is the most common tool for 5-axis machining.
    """

    def __init__(self, diameter: float, flute_length: float = 50.0, length: float = 100.0):
        params = ToolParameters(
            diameter=diameter,
            corner_radius=diameter / 2.0,
            length=length,
            flute_length=flute_length,
            tip_angle=90.0,
        )
        super().__init__(params)

    def ray_intersection(self, ray_origin: np.ndarray, ray_direction: np.ndarray) -> DexelColumn:
        """Ray-ball-endmill intersection.

        Two components:
        1. Cylinder of radius D/2 from z=D/2 to z=FL
        2. Sphere of radius D/2 centered at (0,0,D/2), capped at z <= D/2

        Returns the union of both intersection intervals.
        """
        # Placeholder -- implement in Phase 2
        return DexelColumn()

    def swept_volume_bbox(self, start_pose, end_pose) -> "AABB":
        # Placeholder -- implement in Phase 3
        from .tri_dexel import AABB
        return AABB(min=np.zeros(3), max=np.zeros(3))


class BullNoseEndmill(Tool):
    """Bull nose endmill: cylinder + toroidal corner + flat bottom.

    APT params: D > 0, 0 < R < D/2, A = 0, B = 0.

    Geometry: Cylinder of radius D/2, flat bottom of radius (D/2-R),
    torus corner of major radius R.
    """

    def ray_intersection(self, ray_origin: np.ndarray, ray_direction: np.ndarray) -> DexelColumn:
        # Placeholder -- implement in Phase 2
        return DexelColumn()

    def swept_volume_bbox(self, start_pose, end_pose) -> "AABB":
        from .tri_dexel import AABB
        return AABB(min=np.zeros(3), max=np.zeros(3))


class Drill(Tool):
    """Drill: cone tip + cylinder body.

    APT params: D > 0, B = tip angle (typically 118 deg), d = 0.

    Geometry: Cone from tip to where cone diameter = D,
    cylinder from that height to FL.
    """

    def ray_intersection(self, ray_origin: np.ndarray, ray_direction: np.ndarray) -> DexelColumn:
        # Placeholder -- implement in Phase 2
        return DexelColumn()

    def swept_volume_bbox(self, start_pose, end_pose) -> "AABB":
        from .tri_dexel import AABB
        return AABB(min=np.zeros(3), max=np.zeros(3))


class ChamferTool(Tool):
    """Chamfer tool: truncated cone.

    APT params: D > 0, d > 0, A = chamfer angle.

    Geometry: Truncated cone from tip diameter d at z=0
    to full diameter D at z=h.
    """

    def ray_intersection(self, ray_origin: np.ndarray, ray_direction: np.ndarray) -> DexelColumn:
        # Placeholder -- implement in Phase 2
        return DexelColumn()

    def swept_volume_bbox(self, start_pose, end_pose) -> "AABB":
        from .tri_dexel import AABB
        return AABB(min=np.zeros(3), max=np.zeros(3))


class ThreadMill(Tool):
    """Thread mill: approximated as cylinder for material removal.

    Thread form is too fine for dexel resolution, so we approximate
    as a cylinder. Thread validation is handled by Tier 1 rules.
    """

    def ray_intersection(self, ray_origin: np.ndarray, ray_direction: np.ndarray) -> DexelColumn:
        # Placeholder -- implement in Phase 2
        return DexelColumn()

    def swept_volume_bbox(self, start_pose, end_pose) -> "AABB":
        from .tri_dexel import AABB
        return AABB(min=np.zeros(3), max=np.zeros(3))


class DovetailCutter(Tool):
    """Dovetail cutter: reverse taper cone.

    APT params: D > 0, A = negative taper (dovetail angle).

    Geometry: Reverse cone -- radius increases with depth.
    """

    def ray_intersection(self, ray_origin: np.ndarray, ray_direction: np.ndarray) -> DexelColumn:
        # Placeholder -- implement in Phase 2
        return DexelColumn()

    def swept_volume_bbox(self, start_pose, end_pose) -> "AABB":
        from .tri_dexel import AABB
        return AABB(min=np.zeros(3), max=np.zeros(3))


def create_tool(tool_type: str, **kwargs) -> Tool:
    """Factory function to create a tool by name.

    Args:
        tool_type: One of 'flat_endmill', 'ball_endmill', 'bull_nose',
                   'drill', 'chamfer', 'thread_mill', 'dovetail'.
        **kwargs: Tool-specific parameters (diameter, flute_length, etc.).

    Returns:
        A Tool subclass instance.
    """
    tool_map = {
        "flat_endmill": FlatEndmill,
        "ball_endmill": BallEndmill,
        "bull_nose": BullNoseEndmill,
        "drill": Drill,
        "chamfer": ChamferTool,
        "thread_mill": ThreadMill,
        "dovetail": DovetailCutter,
    }
    if tool_type not in tool_map:
        raise ValueError(f"Unknown tool type: {tool_type}. "
                         f"Available: {list(tool_map.keys())}")

    if tool_type == "ball_endmill":
        return BallEndmill(**kwargs)

    params = ToolParameters(**kwargs)
    return tool_map[tool_type](params)
