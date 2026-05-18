"""SubCAD -- Subtractive CAD library.

Start with a stock block and cut material away using machining operations.
Each operation is simultaneously a geometry modifier AND a manufacturing
instruction recorded in a JSON-serializable process plan.

Usage::

    from src.subcad import Stock

    part = (Stock.rectangular(100, 50, 20, material="aluminum_6061")
        .face_mill(depth=1.0)
        .pocket(width=30, length=20, depth=5, corner_radius=2)
        .drill(diameter=6, cx=25, cy=10, depth=15)
        .chamfer(width=0.5)
    )
    part.to_step("output.step")
    print(part.process_plan())
"""

from .stock import Stock
from .process_plan import ProcessPlan, OperationStep
from .tool_library import ToolSpec, ToolCatalog, to_sim_tool
from .operations import (
    MachiningOperation,
    FaceMillOp,
    PocketOp,
    CircularPocketOp,
    SpotDrillOp,
    DrillOp,
    TapOp,
    ChamferOp,
    ContourOp,
    SlotOp,
    create_operation,
    threaded_hole_ops,
)
from .material import (
    get_material_props,
    list_materials,
    get_feeds_speeds,
    get_compatible_processes,
    is_plastic,
    is_metal,
    get_melting_point,
    get_machinability,
)

__all__ = [
    # Core classes
    "Stock",
    "ProcessPlan",
    "OperationStep",
    "ToolSpec",
    "ToolCatalog",
    # Operation classes
    "MachiningOperation",
    "FaceMillOp",
    "PocketOp",
    "CircularPocketOp",
    "SpotDrillOp",
    "DrillOp",
    "TapOp",
    "ChamferOp",
    "ContourOp",
    "SlotOp",
    # Factory & helpers
    "create_operation",
    "threaded_hole_ops",
    "to_sim_tool",
    # Material API
    "get_material_props",
    "list_materials",
    "get_feeds_speeds",
    "get_compatible_processes",
    "is_plastic",
    "is_metal",
    "get_melting_point",
    "get_machinability",
]
