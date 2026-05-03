"""Gouge, collision, and constraint validation for simulated plans.

Validates simulation results against manufacturing constraints:
- Gouge detection: tool removed material below the target surface
- Collision detection: tool holder hit part, fixture, or machine
- Tolerance checking: remaining stock is within specified tolerance
- Tool constraint checking: tool is appropriate for the feature
"""

from dataclasses import dataclass, field
from typing import Optional
import numpy as np
import trimesh

from .tri_dexel import TriDexelModel
from .kinematics import ToolPose, FiveAxisKinematics
from .tools import Tool
from .material_removal import Gouge, Collision


@dataclass
class ValidationReport:
    """Complete validation report for a simulation.

    Attributes:
        passed: True if all checks passed.
        gouges: List of detected gouges.
        collisions: List of detected collisions.
        tolerance_violations: Points exceeding tolerance bounds.
        warnings: Non-fatal issues.
        score: 0-100 quality score (100 = perfect).
    """
    passed: bool = True
    gouges: list[Gouge] = field(default_factory=list)
    collisions: list[Collision] = field(default_factory=list)
    tolerance_violations: list = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    score: float = 100.0
    details: dict = field(default_factory=dict)


class SimulationValidator:
    """Validates simulation results for manufacturing correctness.

    Checks:
    1. Gouging: Tool removed material below the desired surface
    2. Collision: Tool holder hit the part, fixture, or clamps
    3. Tolerances: Remaining uncut material is within spec
    4. Axis limits: Machine axes are within travel limits
    5. Tool constraints: Tool is compatible with feature geometry
    """

    def __init__(self, tri_dexel: TriDexelModel,
                 target_mesh: trimesh.Trimesh,
                 kinematics: Optional[FiveAxisKinematics] = None,
                 gouge_tolerance: float = 0.01,
                 uncut_tolerance: float = 0.1):
        self.tri_dexel = tri_dexel
        self.target_mesh = target_mesh
        self.kinematics = kinematics
        self.gouge_tolerance = gouge_tolerance
        self.uncut_tolerance = uncut_tolerance

    def validate(self) -> ValidationReport:
        """Run all validation checks and return a report.

        Returns:
            ValidationReport with pass/fail and details.
        """
        # Placeholder -- implement in Phase 6
        return ValidationReport()

    def check_gouges(self) -> list[Gouge]:
        """Check for gouges where material was removed below target surface.

        Samples the target surface at dexel resolution and checks whether
        material exists at the expected positions.

        Returns:
            List of Gouge objects.
        """
        # Placeholder -- implement in Phase 6
        return []

    def check_collisions(self, tool_poses: list[ToolPose],
                         tool: Tool,
                         fixture_mesh: Optional[trimesh.Trimesh] = None) -> list[Collision]:
        """Check for tool/holder collisions along a toolpath.

        Uses the tool's swept bounding box to detect potential collisions
        with the part (non-cutting contact), fixture, and clamp bodies.

        Args:
            tool_poses: List of tool poses along the path.
            tool: The tool used.
            fixture_mesh: Optional fixture mesh for collision checking.

        Returns:
            List of Collision objects.
        """
        # Placeholder -- implement in Phase 6
        return []

    def check_tolerances(self) -> list:
        """Check remaining stock against specified tolerances.

        Computes signed deviation everywhere and flags regions where
        uncut material exceeds the allowed tolerance.

        Returns:
            List of tolerance violations.
        """
        # Placeholder -- implement in Phase 6
        return []

    def check_axis_limits(self, joints: np.ndarray) -> list[str]:
        """Check if all machine axes are within travel limits.

        Args:
            joints: (6,) float array of joint positions.

        Returns:
            List of warning strings for axis limit violations.
        """
        if self.kinematics is None:
            return []
        warnings = []
        axis_names = ["X", "Y", "Z", "A", "B", "C"]
        for i, name in enumerate(axis_names):
            if name in self.kinematics.axis_limits:
                lo, hi = self.kinematics.axis_limits[name]
                if joints[i] < lo:
                    warnings.append(f"{name} axis at {joints[i]:.1f} below limit {lo}")
                elif joints[i] > hi:
                    warnings.append(f"{name} axis at {joints[i]:.1f} above limit {hi}")
        return warnings

    def compute_quality_score(self, gouges: list[Gouge],
                              collisions: list[Collision],
                              tolerance_violations: list) -> float:
        """Compute a 0-100 quality score from validation results.

        100 = perfect (zero gouges, zero collisions, within tolerance).
        Penalties:
        - Each gouge: -10 to -30 depending on severity
        - Each collision: -20
        - Each tolerance violation: -5

        Returns:
            Score from 0 to 100.
        """
        score = 100.0
        for g in gouges:
            if g.severity == "severe":
                score -= 30
            elif g.severity == "moderate":
                score -= 15
            else:
                score -= 10
        for _ in collisions:
            score -= 20
        for _ in tolerance_violations:
            score -= 5
        return max(0.0, score)
