"""Prompt templates for manufacturing process planning.

Provides the system persona, structured generation templates, and helper
functions to convert feature data into prompt-ready text.

The prompts are engineered for DeepSeek V4 Pro (and compatible models) to
produce detailed, rule-compliant JSON process plans with cutting parameters,
DFM notes, and alternative approaches.
"""

from __future__ import annotations

from typing import Optional

# =========================================================================
#   System prompt: manufacturing engineer persona
# =========================================================================

SYSTEM_PROMPT = """You are a senior manufacturing engineer with 20 years of experience in CNC machining and injection molding. You generate detailed, rule-compliant manufacturing process plans from part specifications.

**Your expertise includes:**
- 3-axis and 5-axis CNC machining strategies
- Tool selection based on feature geometry, material, and tolerances
- Calculation of cutting parameters (RPM, feed rates, depth of cut) from first principles
- Design for Manufacturability (DFM) analysis
- Process sequencing to minimize setups and tool changes
- Knowledge of ISO tolerance grades and surface finish requirements

**Rules you must follow:**
1. Roughing always precedes finishing; no finishing pass on unmachined stock.
2. Drill before ream before tap for threaded holes.
3. Cut internal features before external features when possible to maintain rigidity.
4. Deep pockets require progressive depth steps (no single-pass full-depth cuts).
5. Thin walls (< 3mm) need reduced depths of cut and climb milling.
6. Hard materials (Ti, Inconel, tool steels) need conservative parameters.
7. Always specify coolant: flood for steels/aluminum, mist for titanium, air blast for plastics.
8. 5-axis operations are preferred for complex contours; justify when used.
9. Each operation must specify a valid tool size + type combination.
10. Tolerance requirements dictate the number of finishing passes.

**Cutting parameter guidelines:**
- Aluminum: 8000-15000 RPM, 1000-3000 mm/min, 2-5mm DOC roughing
- Mild steel: 2000-4000 RPM, 300-800 mm/min, 1-3mm DOC roughing
- Stainless steel: 1500-3000 RPM, 150-400 mm/min, 0.5-2mm DOC roughing
- Titanium: 800-1500 RPM, 50-150 mm/min, 0.3-1mm DOC roughing
- Tool steel (annealed): 1500-3000 RPM, 200-500 mm/min, 0.5-2mm DOC roughing
- Plastics (ABS, Nylon): 10000-20000 RPM, 2000-4000 mm/min, 2-5mm DOC

Always return JSON. Never include markdown code fences or explanatory text outside the JSON object."""


# =========================================================================
#   Plan generation template
# =========================================================================

PLAN_GENERATION_TEMPLATE = """Given the following part specification, generate a complete manufacturing process plan.

**Material**: {material}
**Production Volume**: {volume} units
**Overall Dimensions**: {dimensions_x}mm x {dimensions_y}mm x {dimensions_z}mm

**Features**:
{features_text}

**Tolerances**: {tolerances}

**Part Origin**: Bottom-center of stock (X = length/2, Y = width/2, Z = 0 at bottom face)

Generate a JSON process plan with the following structure:

{{
  "part_summary": {{
    "material": "string",
    "overall_size_mm": [x, y, z],
    "feature_count": integer,
    "complexity_level": "simple | moderate | complex",
    "estimated_setups": integer
  }},
  "operations": [
    {{
      "step_number": integer,
      "operation_name": "string (e.g., Face Mill Top, Rough Pocket, Finish Contour, Drill Holes)",
      "tool": {{
        "type": "flat_endmill | ball_endmill | bull_nose_endmill | drill | chamfer_tool | thread_mill | tap | reamer",
        "diameter_mm": float,
        "corner_radius_mm": float,
        "flute_length_mm": float,
        "material": "carbide | HSS | CBN | PCD"
      }},
      "machine_type": "3_axis_cnc | 5_axis_cnc | mill_turn | drill_tap",
      "cutting_parameters": {{
        "rpm": integer,
        "feed_rate_mm_per_min": float,
        "depth_of_cut_mm": float,
        "stepover_mm": float
      }},
      "strategy": "adaptive | parallel | contour | pocket | drill | peck_drill | ream | tap | face_mill | chamfer | thread_mill | slot | plunge",
      "features_referenced": ["feature_id_1", "feature_id_2"],
      "coolant": "flood | mist | air_blast | none",
      "estimated_time_minutes": float,
      "notes": "Engineering rationale for this operation"
    }}
  ],
  "total_estimated_time_minutes": float,
  "dfm_notes": [
    "string: design-for-manufacturability observation or suggestion"
  ],
  "alternative_approaches": [
    {{
      "description": "string describing alternative strategy",
      "tradeoffs": "pros and cons vs the primary plan",
      "estimated_time_minutes": float
    }}
  ]
}}

**Important:**
- Sequence operations logically: roughing -> semi-finishing -> finishing
- Minimize tool changes by grouping operations that use the same tool
- Operations list should cover ALL features in the part specification
- Cutting parameters must respect the material guidelines from the system prompt
- Include specific tool diameters (not ranges) based on feature sizes
- DFM notes should be actionable observations for the part designer

Return ONLY valid JSON. No markdown fences, no commentary."""


# =========================================================================
#   Feature analysis template
# =========================================================================

FEATURE_ANALYSIS_TEMPLATE = """Analyze the following part features and suggest appropriate tooling and machining strategies.

**Material**: {material}
**Features**:
{features_text}

For each feature, provide:

{{
  "feature_analyses": [
    {{
      "feature_id": "string",
      "feature_type": "string",
      "geometry_description": "brief description of shape and dimensions",
      "accessible_from": ["top", "front", "bottom", "left", "right", "back", "3+2_angle"],
      "recommended_tools": [
        {{
          "tool_type": "flat_endmill | ball_endmill | drill | etc.",
          "diameter_mm": float,
          "rationale": "why this tool is suitable"
        }}
      ],
      "primary_strategy": "adaptive | pocket | contour | drill | etc.",
      "estimated_operations": integer,
      "difficulty": "easy | moderate | challenging",
      "requires_5axis": boolean,
      "special_considerations": ["list of concerns (undercuts, deep pockets, thin walls, etc.)"]
    }}
  ],
  "tool_list": [
    {{
      "type": "string",
      "diameters_needed": [float, ...],
      "total_operations": integer
    }}
  ],
  "sequencing_recommendations": [
    "string: high-level ordering suggestion"
  ],
  "critical_path_features": ["feature_id for features that drive the process sequence"]
}}

Return ONLY valid JSON. No markdown fences, no commentary."""


# =========================================================================
#   Helper functions
# =========================================================================

def format_features_for_prompt(features: list[dict]) -> str:
    """Convert a list of structured feature dictionaries into readable text
    suitable for inclusion in a prompt.

    Each feature dict should have at minimum:
        - feature_id: str
        - type: str (e.g., pocket, hole, boss, slot, contour, chamfer, thread)
        - dimensions: dict or str (e.g., {"width": 20, "depth": 10} or "dia 6 x 20 deep")

    Optional keys:
        - location: str (e.g., "top face, centered")
        - surface_finish: str (e.g., "Ra 3.2")
        - tolerance: str (e.g., "H7", "+/-0.05mm")
        - notes: str

    Args:
        features: List of feature dictionaries.

    Returns:
        Multi-line string describing each feature, numbered and formatted.
    """
    if not features:
        return "(No features specified)"

    lines: list[str] = []
    for i, feat in enumerate(features, start=1):
        fid = feat.get("feature_id", f"feature_{i}")
        ftype = feat.get("type", "unknown")
        dims = feat.get("dimensions", "")
        location = feat.get("location", "")
        surface = feat.get("surface_finish", "")
        tolerance = feat.get("tolerance", "")
        notes = feat.get("notes", "")

        # Build a compact dimension string
        if isinstance(dims, dict):
            dims_str = ", ".join(f"{k}={v}" for k, v in dims.items())
        else:
            dims_str = str(dims)

        # Build the line
        parts = [f"  {fid}. [{ftype.upper()}]"]
        if dims_str:
            parts.append(dims_str)
        if location:
            parts.append(f"@ {location}")
        extras = []
        if tolerance:
            extras.append(f"tolerance: {tolerance}")
        if surface:
            extras.append(f"surface: {surface}")
        if notes:
            extras.append(f"note: {notes}")
        if extras:
            parts.append("(" + "; ".join(extras) + ")")

        lines.append(" ".join(parts))

    return "\n".join(lines)


def build_plan_prompt(
    features: list[dict],
    material: str,
    volume: int = 100,
    dimensions: Optional[dict] = None,
    tolerances: str = "\u00b10.1mm",
) -> str:
    """Build a complete plan generation prompt by filling the template
    with structured feature data and part specifications.

    Args:
        features: List of feature dictionaries (see format_features_for_prompt).
        material: Material name (e.g., "Aluminum 6061-T6", "Titanium Ti-6Al-4V").
        volume: Production volume in units.
        dimensions: Dict with 'x', 'y', 'z' keys in mm.
                    Defaults to 100x100x50 if not provided.
        tolerances: Tolerance specification string (e.g., "+/-0.05mm", "ISO 2768-m").

    Returns:
        Complete prompt string ready for the chat completion API.
    """
    if dimensions is None:
        dimensions = {"x": 100, "y": 100, "z": 50}

    dim_x = dimensions.get("x", dimensions.get("length", 100))
    dim_y = dimensions.get("y", dimensions.get("width", 100))
    dim_z = dimensions.get("z", dimensions.get("height", 50))

    features_text = format_features_for_prompt(features)

    prompt = PLAN_GENERATION_TEMPLATE.format(
        material=material,
        volume=volume,
        dimensions_x=dim_x,
        dimensions_y=dim_y,
        dimensions_z=dim_z,
        features_text=features_text,
        tolerances=tolerances,
    )
    return prompt


# =========================================================================
#   Self-test
# =========================================================================

if __name__ == "__main__":
    print("=== Prompt Templates Self-Test ===\n")

    # ------------------------------------------------------------------
    # 1. System prompt is non-empty
    # ------------------------------------------------------------------
    print("1. System prompt loaded ...")
    assert len(SYSTEM_PROMPT) > 500, f"System prompt too short: {len(SYSTEM_PROMPT)} chars"
    print(f"   Length: {len(SYSTEM_PROMPT)} chars")
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 2. format_features_for_prompt with sample data
    # ------------------------------------------------------------------
    print("2. format_features_for_prompt ...")
    sample_features = [
        {
            "feature_id": "F001",
            "type": "pocket",
            "dimensions": {"width": 50, "depth": 15, "corner_radius": 5},
            "location": "top face, centered",
            "tolerance": "+/-0.05mm",
            "surface_finish": "Ra 3.2",
        },
        {
            "feature_id": "F002",
            "type": "hole",
            "dimensions": "dia 8 x 30 deep",
            "location": "top face, at (25, 25)",
            "tolerance": "H7",
        },
        {
            "feature_id": "F003",
            "type": "contour",
            "dimensions": {"outer_profile": True},
            "location": "perimeter",
            "notes": "full depth profile cut",
        },
        {
            "feature_id": "F004",
            "type": "thread",
            "dimensions": "M6 x 1.0 x 20 deep",
            "location": "side face, centered",
        },
    ]
    text = format_features_for_prompt(sample_features)
    print(text)
    assert "F001" in text
    assert "POCKET" in text
    assert "H7" in text
    assert "F004" in text
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 3. format_features_for_prompt with empty list
    # ------------------------------------------------------------------
    print("3. format_features_for_prompt (empty) ...")
    empty_text = format_features_for_prompt([])
    print(f"   Output: {empty_text}")
    assert "No features" in empty_text
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 4. format_features_for_prompt with no IDs
    # ------------------------------------------------------------------
    print("4. format_features_for_prompt (auto-generated IDs) ...")
    no_id_features = [
        {"type": "slot", "dimensions": "width 10 x depth 5 x length 40"},
        {"type": "chamfer", "dimensions": "1mm x 45deg", "location": "all edges"},
    ]
    text = format_features_for_prompt(no_id_features)
    print(text)
    assert "feature_1" in text
    assert "feature_2" in text
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 5. build_plan_prompt
    # ------------------------------------------------------------------
    print("5. build_plan_prompt ...")
    prompt = build_plan_prompt(
        features=sample_features,
        material="Aluminum 6061-T6",
        volume=500,
        dimensions={"x": 150, "y": 100, "z": 50},
        tolerances="+/-0.05mm on critical features, +/-0.1mm general",
    )
    assert "Aluminum 6061-T6" in prompt
    assert "150mm x 100mm x 50mm" in prompt
    assert "F001" in prompt
    assert "F004" in prompt
    assert "500 units" in prompt
    print(f"   Prompt length: {len(prompt)} chars")
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 6. build_plan_prompt with default dimensions
    # ------------------------------------------------------------------
    print("6. build_plan_prompt (default dimensions) ...")
    prompt_default = build_plan_prompt(
        features=[{"feature_id": "F1", "type": "pocket", "dimensions": "10x10x5"}],
        material="Mild Steel",
        volume=10,
    )
    assert "100mm x 100mm x 50mm" in prompt_default
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 7. build_plan_prompt with alternate dimension keys
    # ------------------------------------------------------------------
    print("7. build_plan_prompt (alternate dimension keys) ...")
    prompt_alt = build_plan_prompt(
        features=[{"feature_id": "F1", "type": "hole", "dimensions": "dia 5"}],
        material="ABS",
        volume=1000,
        dimensions={"length": 200, "width": 80, "height": 40},
    )
    assert "200mm x 80mm x 40mm" in prompt_alt
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 8. Feature analysis template
    # ------------------------------------------------------------------
    print("8. FEATURE_ANALYSIS_TEMPLATE ...")
    analysis_text = FEATURE_ANALYSIS_TEMPLATE.format(
        material="Stainless Steel 316",
        features_text=text,
    )
    assert "Stainless Steel 316" in analysis_text
    assert "feature_analyses" in analysis_text
    print(f"   Length: {len(analysis_text)} chars")
    print("   PASSED\n")

    print("=== ALL PROMPT TESTS PASSED ===")
