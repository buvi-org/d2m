"""
d2m Knowledge Graph Module -- Phase 0 Manufacturing Rule Engine

Provides pure-Python manufacturing domain knowledge for DfM validation.
All rules are hardcoded with traceable references (Machinery's Handbook,
ASM Metals Handbook, ISO standards).  No external graph database is
required.

Primary functions for external use:
    get_material_properties    -- Look up physical/mechanical material data.
    get_compatible_processes   -- List viable manufacturing processes per material.
    get_feeds_speeds           -- Look up recommended cutting parameters.
    check_hole_process         -- Determine required hole-making operations.
    check_pocket_process       -- Determine required pocket-machining operations.
    check_wall_thickness       -- DFM wall-thickness risk assessment.
    validate_tool_selection    -- Verify tool appropriateness for a feature.
    run_all_rules              -- Aggregate all checks across a feature set.
"""

__version__ = "0.1.0"

from .rules import (
    # Return dataclasses
    RuleMessage,
    OperationStep,
    RuleResult,

    # Data access functions
    get_material_properties,
    list_materials,
    list_tool_types,
    get_compatible_processes,
    get_feeds_speeds,

    # Rule-check functions
    check_hole_process,
    check_pocket_process,
    check_wall_thickness,
    validate_tool_selection,

    # Aggregate runner
    run_all_rules,
)
