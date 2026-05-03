"""
d2m Simulation Module - 5-Axis Tri-Dexel CNC Simulation Core

Provides multi-fidelity manufacturing simulation:
- Tri-dexel material removal engine (Tier 2: seconds)
- 5-axis machine kinematics (table-table, head-head, head-table)
- APT standard tool definitions with ray-tool intersection
- Surface extraction via modified marching cubes
- Gouge, collision, and constraint validation

Primary classes for external use:
    FiveAxisSimulator - Main orchestrator
    TriDexelModel - Three-orthogonal-dexel workpiece representation
    FiveAxisKinematics - Machine kinematics chain
    Tool - APT standard tool base class (subclass for specific geometry)
"""

__version__ = "0.1.0"

from .tri_dexel import DexelInterval, DexelColumn, DexelGrid, TriDexelModel
from .tools import Tool, FlatEndmill, BallEndmill, BullNoseEndmill, Drill, ChamferTool
from .kinematics import FiveAxisKinematics, MachineConfig, ToolPose
from .simulator import FiveAxisSimulator, SimulationResult, MoveResult
