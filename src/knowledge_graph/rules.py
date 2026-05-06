"""Manufacturing rule engine for DfM (Design for Manufacturing) validation.

Enforces hard manufacturing constraints before the LLM generates CAPP
process plans.  All rules are pure Python -- no external graph database
required for Phase 0.

All recommendations cite their source for traceability.

Reference sources:
  - Machinery's Handbook, 31st Edition (Erik Oberg et al.)
  - ASM Metals Handbook, Vol. 16 (Machining)
  - ISO 286 (Geometrical product specifications -- tolerances)
  - ISO 13399 (Cutting tool data representation and exchange)
  - Sandvik Coromant Metal Cutting Technical Guide
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional
import math


# =========================================================================
#   Return-type dataclasses
# =========================================================================


@dataclass
class RuleMessage:
    """A single rule evaluation result (warning, error, or suggestion).

    Attributes:
        severity:   "error" (hard block) or "warn" (advisory).
        message:    Human-readable description of the issue.
        source:     Reference authority (e.g. "Machinery's Handbook").
        suggestion: Actionable recommendation to resolve the issue.
    """
    severity: str          # "error" | "warn"
    message: str
    source: str
    suggestion: str

    def to_dict(self) -> dict:
        return {
            "severity": self.severity,
            "message": self.message,
            "source": self.source,
            "suggestion": self.suggestion,
        }


@dataclass
class OperationStep:
    """A suggested manufacturing operation step.

    Attributes:
        operation:    Operation name (e.g. "spot_drill", "rough_pocket").
        tool_type:    Recommended tool type.
        tool_diameter_mm: Recommended tool diameter in mm.
        depth_mm:     Depth of cut for this operation.
        notes:        Free-form notes for the planner.
        feeds_speeds: Optional feeds/speeds dict for this step.
    """
    operation: str
    tool_type: str
    tool_diameter_mm: float
    depth_mm: float = 0.0
    notes: str = ""
    feeds_speeds: Optional[dict] = None

    def to_dict(self) -> dict:
        d = {
            "operation": self.operation,
            "tool_type": self.tool_type,
            "tool_diameter_mm": self.tool_diameter_mm,
            "depth_mm": self.depth_mm,
            "notes": self.notes,
        }
        if self.feeds_speeds is not None:
            d["feeds_speeds"] = self.feeds_speeds
        return d


@dataclass
class RuleResult:
    """Aggregate result from running all rules against a feature set.

    Attributes:
        warnings:            Non-blocking advisory messages.
        errors:              Hard blocking issues (must be resolved).
        suggested_operations: Ordered list of recommended operations.
    """
    warnings: list[dict] = field(default_factory=list)
    errors: list[dict] = field(default_factory=list)
    suggested_operations: list[dict] = field(default_factory=list)


# =========================================================================
#   Material Properties Database
# =========================================================================
#   Reference: ASM Metals Handbook Vol. 16, MatWeb, manufacturer datasheets.
# =========================================================================

_MATERIAL_PROPERTIES: dict[str, dict] = {
    # ---- Metals -----------------------------------------------------------
    "aluminum_6061": {
        "material_type": "metal",
        "family": "aluminum",
        "density_gcm3": 2.70,
        "tensile_strength_mpa": 310,
        "yield_strength_mpa": 276,
        "hardness_hb": 95,
        "thermal_conductivity_wmk": 167,
        "melting_point_c": 585,
        "youngs_modulus_gpa": 68.9,
        "machinability_pct": 270,       # Relative to B1112 = 100%
        "elongation_pct": 12,
        "warp_risk_min_wall_mm": 0.5,
        "description": "General-purpose wrought aluminium alloy. Excellent machinability, good corrosion resistance.",
    },
    "aluminum_7075": {
        "material_type": "metal",
        "family": "aluminum",
        "density_gcm3": 2.81,
        "tensile_strength_mpa": 572,
        "yield_strength_mpa": 503,
        "hardness_hb": 150,
        "thermal_conductivity_wmk": 130,
        "melting_point_c": 477,
        "youngs_modulus_gpa": 71.7,
        "machinability_pct": 190,
        "elongation_pct": 7,
        "warp_risk_min_wall_mm": 0.5,
        "description": "High-strength aerospace aluminium. Zinc-bearing alloy, harder to machine than 6061.",
    },
    "steel_4140": {
        "material_type": "metal",
        "family": "steel",
        "density_gcm3": 7.85,
        "tensile_strength_mpa": 655,
        "yield_strength_mpa": 415,
        "hardness_hb": 197,
        "thermal_conductivity_wmk": 42.6,
        "melting_point_c": 1416,
        "youngs_modulus_gpa": 205,
        "machinability_pct": 65,
        "elongation_pct": 25,
        "warp_risk_min_wall_mm": 0.5,
        "description": "Chromium-molybdenum alloy steel. Good strength and toughness, commonly heat-treated.",
    },
    "steel_304": {
        "material_type": "metal",
        "family": "stainless_steel",
        "density_gcm3": 8.00,
        "tensile_strength_mpa": 505,
        "yield_strength_mpa": 215,
        "hardness_hb": 170,
        "thermal_conductivity_wmk": 16.2,
        "melting_point_c": 1400,
        "youngs_modulus_gpa": 193,
        "machinability_pct": 45,         # Work-hardens severely
        "elongation_pct": 70,
        "warp_risk_min_wall_mm": 0.5,
        "description": "Austenitic stainless steel. High corrosion resistance, work-hardens rapidly during machining.",
    },
    "stainless_316": {
        "material_type": "metal",
        "family": "stainless_steel",
        "density_gcm3": 8.00,
        "tensile_strength_mpa": 580,
        "yield_strength_mpa": 290,
        "hardness_hb": 217,
        "thermal_conductivity_wmk": 16.3,
        "melting_point_c": 1375,
        "youngs_modulus_gpa": 193,
        "machinability_pct": 36,         # Worse than 304 due to molybdenum
        "elongation_pct": 50,
        "warp_risk_min_wall_mm": 0.5,
        "description": "Molybdenum-bearing austenitic stainless. Superior corrosion resistance, gummy in machining.",
    },
    "titanium_6al4v": {
        "material_type": "metal",
        "family": "titanium",
        "density_gcm3": 4.43,
        "tensile_strength_mpa": 950,
        "yield_strength_mpa": 880,
        "hardness_hb": 334,
        "thermal_conductivity_wmk": 6.7,
        "melting_point_c": 1660,
        "youngs_modulus_gpa": 113.8,
        "machinability_pct": 22,         # Very poor -- low thermal conductivity
        "elongation_pct": 14,
        "warp_risk_min_wall_mm": 0.5,
        "description": "Alpha-beta titanium alloy. Extremely high strength-to-weight ratio, very difficult to machine.",
    },
    "brass_c360": {
        "material_type": "metal",
        "family": "copper_alloy",
        "density_gcm3": 8.50,
        "tensile_strength_mpa": 345,
        "yield_strength_mpa": 124,
        "hardness_hb": 80,
        "thermal_conductivity_wmk": 115,
        "melting_point_c": 885,
        "youngs_modulus_gpa": 97,
        "machinability_pct": 100,        # The baseline for machinability ratings
        "elongation_pct": 53,
        "warp_risk_min_wall_mm": 0.5,
        "description": "Free-cutting brass with lead addition. Best machinability, used as the 100% reference.",
    },

    # ---- Plastics ---------------------------------------------------------
    "abs": {
        "material_type": "plastic",
        "family": "thermoplastic",
        "density_gcm3": 1.05,
        "tensile_strength_mpa": 46,
        "yield_strength_mpa": 46,
        "hardness_hb": None,             # Not applicable (Shore D ~85)
        "thermal_conductivity_wmk": 0.17,
        "melting_point_c": 200,          # Glass transition ~105 C
        "youngs_modulus_gpa": 2.3,
        "machinability_pct": None,
        "elongation_pct": 20,
        "warp_risk_min_wall_mm": 1.0,    # Plastics warp more easily
        "description": "Acrylonitrile butadiene styrene. Common 3D-printing and injection-moulding plastic.",
    },
    "polycarbonate": {
        "material_type": "plastic",
        "family": "thermoplastic",
        "density_gcm3": 1.20,
        "tensile_strength_mpa": 65,
        "yield_strength_mpa": 62,
        "hardness_hb": None,
        "thermal_conductivity_wmk": 0.20,
        "melting_point_c": 267,
        "youngs_modulus_gpa": 2.4,
        "machinability_pct": None,
        "elongation_pct": 110,
        "warp_risk_min_wall_mm": 1.0,
        "description": "High-impact transparent thermoplastic. Machines well but melts at high speeds.",
    },
    "nylon_pa6": {
        "material_type": "plastic",
        "family": "thermoplastic",
        "density_gcm3": 1.14,
        "tensile_strength_mpa": 76,
        "yield_strength_mpa": 45,
        "hardness_hb": None,
        "thermal_conductivity_wmk": 0.23,
        "melting_point_c": 220,
        "youngs_modulus_gpa": 2.8,
        "machinability_pct": None,
        "elongation_pct": 200,
        "warp_risk_min_wall_mm": 1.0,
        "description": "Polyamide with good wear resistance. Absorbs moisture -- dimensional stability concerns.",
    },
    "polypropylene": {
        "material_type": "plastic",
        "family": "thermoplastic",
        "density_gcm3": 0.90,
        "tensile_strength_mpa": 33,
        "yield_strength_mpa": 33,
        "hardness_hb": None,
        "thermal_conductivity_wmk": 0.12,
        "melting_point_c": 165,
        "youngs_modulus_gpa": 1.5,
        "machinability_pct": None,
        "elongation_pct": 300,
        "warp_risk_min_wall_mm": 1.0,
        "description": "Low-cost commodity plastic. Flexible, excellent chemical resistance, melts easily during machining.",
    },
    "peek": {
        "material_type": "plastic",
        "family": "thermoplastic",
        "density_gcm3": 1.31,
        "tensile_strength_mpa": 100,
        "yield_strength_mpa": 97,
        "hardness_hb": None,
        "thermal_conductivity_wmk": 0.25,
        "melting_point_c": 343,
        "youngs_modulus_gpa": 3.7,
        "machinability_pct": None,
        "elongation_pct": 30,
        "warp_risk_min_wall_mm": 1.0,
        "description": "High-performance engineering thermoplastic. Excellent machinability, withstands high temperatures.",
    },
}

# =========================================================================
#   Material -> Process Compatibility Matrix
# =========================================================================
#   Which manufacturing processes are viable for each material.
#   Based on: ASM Handbook Vol. 16, industry practice.
# =========================================================================

_MATERIAL_PROCESSES: dict[str, list[str]] = {
    # Metals -- subtractive + EDM
    "aluminum_6061":    ["milling", "drilling", "turning", "grinding", "edm", "cnc_machining", "sawing"],
    "aluminum_7075":    ["milling", "drilling", "turning", "grinding", "edm", "cnc_machining", "sawing"],
    "steel_4140":       ["milling", "drilling", "turning", "grinding", "edm", "cnc_machining", "sawing", "heat_treating"],
    "steel_304":        ["milling", "drilling", "turning", "grinding", "edm", "cnc_machining", "sawing", "welding"],
    "stainless_316":    ["milling", "drilling", "turning", "grinding", "edm", "cnc_machining", "sawing", "welding"],
    "titanium_6al4v":   ["milling", "drilling", "turning", "grinding", "edm", "cnc_machining", "sawing", "3d_printing_dmls"],
    "brass_c360":       ["milling", "drilling", "turning", "grinding", "edm", "cnc_machining", "sawing"],

    # Plastics -- primarily additive / forming, but also machinable
    "abs":              ["injection_molding", "3d_printing_fdm", "cnc_machining", "milling", "drilling", "sawing", "thermoforming"],
    "polycarbonate":    ["injection_molding", "3d_printing_fdm", "cnc_machining", "milling", "drilling", "sawing", "thermoforming"],
    "nylon_pa6":        ["injection_molding", "3d_printing_sls", "cnc_machining", "milling", "drilling", "sawing"],
    "polypropylene":    ["injection_molding", "3d_printing_fdm", "cnc_machining", "milling", "drilling", "sawing", "thermoforming"],
    "peek":             ["injection_molding", "3d_printing_fdm", "3d_printing_sls", "cnc_machining", "milling", "drilling", "sawing"],
}

# =========================================================================
#   Feeds & Speeds Database
# =========================================================================
#   SFM = surface feet per minute (imperial, per Machinery's Handbook).
#   FPT = feed per tooth (mm/tooth) for a ~10 mm diameter tool.
#   All values assume carbide tooling, unless noted.
#
#   Sources: Machinery's Handbook 31st Ed., Sandvik Coromant, Kennametal.
# =========================================================================

_FEEDS_SPEEDS: dict[str, dict[str, dict[str, float]]] = {
    # =====================================================================
    #  Aluminum 6061  (high machinability, easy cutting)
    # =====================================================================
    "aluminum_6061": {
        "end_mill":       {"sfm": 800,  "fpt": 0.15, "num_flutes": 2},
        "ball_endmill":   {"sfm": 600,  "fpt": 0.10, "num_flutes": 2},
        "drill":          {"sfm": 400,  "fpt": 0.12, "num_flutes": 2},
        "spot_drill":     {"sfm": 300,  "fpt": 0.05, "num_flutes": 2},
        "reamer":         {"sfm": 200,  "fpt": 0.08, "num_flutes": 6},
        "tap":            {"sfm": 100,  "fpt": 0.05, "num_flutes": 4},
        "chamfer_tool":   {"sfm": 500,  "fpt": 0.10, "num_flutes": 4},
        "roughing_endmill": {"sfm": 900, "fpt": 0.20, "num_flutes": 3},
        "finish_endmill": {"sfm": 600,  "fpt": 0.08, "num_flutes": 4},
    },
    # =====================================================================
    #  Aluminum 7075  (stronger, slightly harder to cut than 6061)
    # =====================================================================
    "aluminum_7075": {
        "end_mill":       {"sfm": 700,  "fpt": 0.13, "num_flutes": 2},
        "ball_endmill":   {"sfm": 500,  "fpt": 0.09, "num_flutes": 2},
        "drill":          {"sfm": 350,  "fpt": 0.10, "num_flutes": 2},
        "spot_drill":     {"sfm": 250,  "fpt": 0.05, "num_flutes": 2},
        "reamer":         {"sfm": 180,  "fpt": 0.07, "num_flutes": 6},
        "tap":            {"sfm": 80,   "fpt": 0.04, "num_flutes": 4},
        "chamfer_tool":   {"sfm": 450,  "fpt": 0.09, "num_flutes": 4},
        "roughing_endmill": {"sfm": 800, "fpt": 0.18, "num_flutes": 3},
        "finish_endmill": {"sfm": 550,  "fpt": 0.07, "num_flutes": 4},
    },
    # =====================================================================
    #  Steel 4140  (alloy steel, medium machinability)
    # =====================================================================
    "steel_4140": {
        "end_mill":       {"sfm": 300,  "fpt": 0.10, "num_flutes": 4},
        "ball_endmill":   {"sfm": 250,  "fpt": 0.07, "num_flutes": 4},
        "drill":          {"sfm": 150,  "fpt": 0.08, "num_flutes": 2},
        "spot_drill":     {"sfm": 120,  "fpt": 0.04, "num_flutes": 2},
        "reamer":         {"sfm": 80,   "fpt": 0.05, "num_flutes": 6},
        "tap":            {"sfm": 40,   "fpt": 0.03, "num_flutes": 4},
        "chamfer_tool":   {"sfm": 200,  "fpt": 0.07, "num_flutes": 4},
        "roughing_endmill": {"sfm": 350, "fpt": 0.14, "num_flutes": 4},
        "finish_endmill": {"sfm": 220,  "fpt": 0.05, "num_flutes": 6},
    },
    # =====================================================================
    #  Steel 304  (austenitic stainless, poor machinability, work-hardens)
    # =====================================================================
    "steel_304": {
        "end_mill":       {"sfm": 180,  "fpt": 0.07, "num_flutes": 4},
        "ball_endmill":   {"sfm": 150,  "fpt": 0.05, "num_flutes": 4},
        "drill":          {"sfm": 90,   "fpt": 0.06, "num_flutes": 2},
        "spot_drill":     {"sfm": 80,   "fpt": 0.03, "num_flutes": 2},
        "reamer":         {"sfm": 50,   "fpt": 0.04, "num_flutes": 6},
        "tap":            {"sfm": 25,   "fpt": 0.02, "num_flutes": 4},
        "chamfer_tool":   {"sfm": 130,  "fpt": 0.05, "num_flutes": 4},
        "roughing_endmill": {"sfm": 200, "fpt": 0.10, "num_flutes": 4},
        "finish_endmill": {"sfm": 140,  "fpt": 0.04, "num_flutes": 6},
    },
    # =====================================================================
    #  Stainless 316  (even harder to machine than 304)
    # =====================================================================
    "stainless_316": {
        "end_mill":       {"sfm": 150,  "fpt": 0.06, "num_flutes": 4},
        "ball_endmill":   {"sfm": 120,  "fpt": 0.04, "num_flutes": 4},
        "drill":          {"sfm": 70,   "fpt": 0.05, "num_flutes": 2},
        "spot_drill":     {"sfm": 60,   "fpt": 0.03, "num_flutes": 2},
        "reamer":         {"sfm": 40,   "fpt": 0.03, "num_flutes": 6},
        "tap":            {"sfm": 20,   "fpt": 0.02, "num_flutes": 4},
        "chamfer_tool":   {"sfm": 100,  "fpt": 0.04, "num_flutes": 4},
        "roughing_endmill": {"sfm": 170, "fpt": 0.08, "num_flutes": 4},
        "finish_endmill": {"sfm": 110,  "fpt": 0.03, "num_flutes": 6},
    },
    # =====================================================================
    #  Titanium 6Al-4V  (very poor machinability -- low thermal conduct.)
    # =====================================================================
    "titanium_6al4v": {
        "end_mill":       {"sfm": 120,  "fpt": 0.05, "num_flutes": 4},
        "ball_endmill":   {"sfm": 100,  "fpt": 0.04, "num_flutes": 4},
        "drill":          {"sfm": 60,   "fpt": 0.04, "num_flutes": 2},
        "spot_drill":     {"sfm": 50,   "fpt": 0.02, "num_flutes": 2},
        "reamer":         {"sfm": 30,   "fpt": 0.03, "num_flutes": 6},
        "tap":            {"sfm": 15,   "fpt": 0.015, "num_flutes": 4},
        "chamfer_tool":   {"sfm": 80,   "fpt": 0.04, "num_flutes": 4},
        "roughing_endmill": {"sfm": 140, "fpt": 0.07, "num_flutes": 4},
        "finish_endmill": {"sfm": 90,   "fpt": 0.03, "num_flutes": 6},
    },
    # =====================================================================
    #  Brass C360  (best machinability for metals)
    # =====================================================================
    "brass_c360": {
        "end_mill":       {"sfm": 600,  "fpt": 0.12, "num_flutes": 2},
        "ball_endmill":   {"sfm": 450,  "fpt": 0.08, "num_flutes": 2},
        "drill":          {"sfm": 350,  "fpt": 0.10, "num_flutes": 2},
        "spot_drill":     {"sfm": 250,  "fpt": 0.04, "num_flutes": 2},
        "reamer":         {"sfm": 180,  "fpt": 0.06, "num_flutes": 6},
        "tap":            {"sfm": 80,   "fpt": 0.04, "num_flutes": 4},
        "chamfer_tool":   {"sfm": 400,  "fpt": 0.08, "num_flutes": 4},
        "roughing_endmill": {"sfm": 700, "fpt": 0.16, "num_flutes": 3},
        "finish_endmill": {"sfm": 450,  "fpt": 0.06, "num_flutes": 4},
    },
    # =====================================================================
    #  ABS  (thermoplastic -- watch for melting at high speed)
    # =====================================================================
    "abs": {
        "end_mill":       {"sfm": 500,  "fpt": 0.15, "num_flutes": 2},
        "ball_endmill":   {"sfm": 400,  "fpt": 0.10, "num_flutes": 2},
        "drill":          {"sfm": 250,  "fpt": 0.12, "num_flutes": 2},
        "spot_drill":     {"sfm": 200,  "fpt": 0.05, "num_flutes": 2},
        "reamer":         {"sfm": 120,  "fpt": 0.08, "num_flutes": 6},
        "tap":            {"sfm": 60,   "fpt": 0.04, "num_flutes": 4},
        "chamfer_tool":   {"sfm": 350,  "fpt": 0.10, "num_flutes": 4},
        "roughing_endmill": {"sfm": 550, "fpt": 0.20, "num_flutes": 2},
        "finish_endmill": {"sfm": 400,  "fpt": 0.08, "num_flutes": 4},
    },
    # =====================================================================
    #  Polycarbonate  (high impact, melts if too fast)
    # =====================================================================
    "polycarbonate": {
        "end_mill":       {"sfm": 400,  "fpt": 0.12, "num_flutes": 2},
        "ball_endmill":   {"sfm": 350,  "fpt": 0.08, "num_flutes": 2},
        "drill":          {"sfm": 200,  "fpt": 0.10, "num_flutes": 2},
        "spot_drill":     {"sfm": 150,  "fpt": 0.04, "num_flutes": 2},
        "reamer":         {"sfm": 100,  "fpt": 0.06, "num_flutes": 6},
        "tap":            {"sfm": 50,   "fpt": 0.03, "num_flutes": 4},
        "chamfer_tool":   {"sfm": 300,  "fpt": 0.08, "num_flutes": 4},
        "roughing_endmill": {"sfm": 450, "fpt": 0.18, "num_flutes": 2},
        "finish_endmill": {"sfm": 350,  "fpt": 0.06, "num_flutes": 4},
    },
    # =====================================================================
    #  Nylon PA6  (tough, absorbs moisture, gummy cutting)
    # =====================================================================
    "nylon_pa6": {
        "end_mill":       {"sfm": 450,  "fpt": 0.14, "num_flutes": 2},
        "ball_endmill":   {"sfm": 380,  "fpt": 0.09, "num_flutes": 2},
        "drill":          {"sfm": 220,  "fpt": 0.11, "num_flutes": 2},
        "spot_drill":     {"sfm": 180,  "fpt": 0.05, "num_flutes": 2},
        "reamer":         {"sfm": 110,  "fpt": 0.07, "num_flutes": 6},
        "tap":            {"sfm": 55,   "fpt": 0.04, "num_flutes": 4},
        "chamfer_tool":   {"sfm": 320,  "fpt": 0.09, "num_flutes": 4},
        "roughing_endmill": {"sfm": 500, "fpt": 0.19, "num_flutes": 2},
        "finish_endmill": {"sfm": 380,  "fpt": 0.07, "num_flutes": 4},
    },
    # =====================================================================
    #  Polypropylene  (soft, lowest melting point -- very easy to melt)
    # =====================================================================
    "polypropylene": {
        "end_mill":       {"sfm": 550,  "fpt": 0.16, "num_flutes": 2},
        "ball_endmill":   {"sfm": 450,  "fpt": 0.11, "num_flutes": 2},
        "drill":          {"sfm": 280,  "fpt": 0.13, "num_flutes": 2},
        "spot_drill":     {"sfm": 220,  "fpt": 0.05, "num_flutes": 2},
        "reamer":         {"sfm": 130,  "fpt": 0.08, "num_flutes": 6},
        "tap":            {"sfm": 65,   "fpt": 0.04, "num_flutes": 4},
        "chamfer_tool":   {"sfm": 380,  "fpt": 0.10, "num_flutes": 4},
        "roughing_endmill": {"sfm": 600, "fpt": 0.22, "num_flutes": 2},
        "finish_endmill": {"sfm": 450,  "fpt": 0.08, "num_flutes": 4},
    },
    # =====================================================================
    #  PEEK  (high-performance plastic, similar to brass in behaviour)
    # =====================================================================
    "peek": {
        "end_mill":       {"sfm": 350,  "fpt": 0.12, "num_flutes": 2},
        "ball_endmill":   {"sfm": 300,  "fpt": 0.08, "num_flutes": 2},
        "drill":          {"sfm": 180,  "fpt": 0.09, "num_flutes": 2},
        "spot_drill":     {"sfm": 140,  "fpt": 0.04, "num_flutes": 2},
        "reamer":         {"sfm": 90,   "fpt": 0.06, "num_flutes": 6},
        "tap":            {"sfm": 45,   "fpt": 0.03, "num_flutes": 4},
        "chamfer_tool":   {"sfm": 280,  "fpt": 0.08, "num_flutes": 4},
        "roughing_endmill": {"sfm": 400, "fpt": 0.16, "num_flutes": 2},
        "finish_endmill": {"sfm": 300,  "fpt": 0.06, "num_flutes": 4},
    },
}

# =========================================================================
#   Constant: SFM to m/min conversion
# =========================================================================
_FT_PER_M = 3.28084


def _sfm_to_m_per_min(sfm: float) -> float:
    """Convert surface feet per minute to metres per minute."""
    return sfm / _FT_PER_M


def _rpm_from_sfm(sfm: float, diameter_mm: float) -> float:
    """Compute spindle RPM given SFM and tool diameter in mm.

    RPM = SFM * 12 / (pi * D_inch)  where D_inch = D_mm / 25.4
        = SFM * 304.8 / (pi * D_mm)
    """
    if diameter_mm <= 0:
        return 0.0
    return (sfm * 304.8) / (math.pi * diameter_mm)


# =========================================================================
#   Public API
# =========================================================================


def get_material_properties(material: str) -> dict:
    """Return all known properties for a material.

    Args:
        material: Material key string, e.g. "aluminum_6061", "peek".

    Returns:
        dict of material properties.  Contains keys like density_gcm3,
        tensile_strength_mpa, hardness_hb, machinability_pct, etc.
        If the material is unknown, returns an empty dict.
    """
    return _MATERIAL_PROPERTIES.get(material, {}).copy()


def list_materials() -> list[str]:
    """Return all known material keys."""
    return sorted(_MATERIAL_PROPERTIES.keys())


def list_tool_types() -> list[str]:
    """Return all tool types that have feeds/speeds data."""
    # Collect unique tool types across all materials
    seen: set[str] = set()
    for speeds in _FEEDS_SPEEDS.values():
        seen.update(speeds.keys())
    return sorted(seen)


def get_compatible_processes(material: str) -> list[str]:
    """Return manufacturing processes compatible with the given material.

    Args:
        material: Material key string.

    Returns:
        List of process name strings.  Empty list if material unknown.
    """
    return list(_MATERIAL_PROCESSES.get(material, []))


def get_feeds_speeds(
    tool_type: str,
    tool_diameter_mm: float,
    material: str,
) -> dict:
    """Look up recommended feeds and speeds for a (tool, material) combination.

    Args:
        tool_type:          e.g. "end_mill", "drill", "ball_endmill", "reamer", ...
        tool_diameter_mm:   Tool cutting diameter in mm.
        material:           Material key string.

    Returns:
        dict with keys:
          - tool_type:            as passed in
          - material:             as passed in
          - tool_diameter_mm:     as passed in
          - sfm:                  recommended surface feet/min
          - surface_speed_m_min:  same, converted to m/min
          - fpt_mm:               feed per tooth (mm)
          - num_flutes:           recommended number of flutes
          - rpm:                  computed spindle RPM
          - feed_rate_mm_min:     computed linear feed rate (mm/min)
        If material or tool_type is unknown, returns a dict with an "error" key.
    """
    mat_speeds = _FEEDS_SPEEDS.get(material)
    if mat_speeds is None:
        return {
            "error": f"Unknown material '{material}'. Known: {list(_MATERIAL_PROPERTIES.keys())}",
        }

    tool_data = mat_speeds.get(tool_type)
    if tool_data is None:
        return {
            "error": f"Unknown tool type '{tool_type}' for material '{material}'. "
                     f"Known for {material}: {list(mat_speeds.keys())}",
        }

    sfm = tool_data["sfm"]
    fpt = tool_data["fpt"]
    num_flutes = tool_data["num_flutes"]

    rpm = _rpm_from_sfm(sfm, tool_diameter_mm)
    feed_rate = rpm * num_flutes * fpt

    return {
        "tool_type": tool_type,
        "material": material,
        "tool_diameter_mm": tool_diameter_mm,
        "sfm": sfm,
        "surface_speed_m_min": round(_sfm_to_m_per_min(sfm), 2),
        "fpt_mm": fpt,
        "num_flutes": num_flutes,
        "rpm": round(rpm, 0),
        "feed_rate_mm_min": round(feed_rate, 1),
    }


# =========================================================================
#   Feature-process checks
# =========================================================================


def check_hole_process(
    hole_diameter_mm: float,
    hole_depth_mm: float,
    tolerance_mm: float,
    has_thread: bool,
    material: str = "aluminum_6061",
) -> list[dict]:
    """Determine required hole-making operations given hole specifications.

    Follows the standard hole-making sequence:
      1. Spot drill (always, for positional accuracy)
      2. Drill to diameter
      3. Ream if tolerance < 0.05 mm
      4. Tap if threaded
      Additionally, peck drilling is required for deep holes (depth > 4 * dia).

    Args:
        hole_diameter_mm:  Finished hole diameter in mm.
        hole_depth_mm:     Depth of hole from entry surface in mm.
        tolerance_mm:      Bilateral tolerance band in mm (e.g. 0.05 for H7).
        has_thread:        True if the hole requires an internal thread.
        material:          Workpiece material key.

    Returns:
        list[dict] -- each dict is an OperationStep serialised.
    """
    steps: list[dict] = []

    # --- 1. Spot drill ---
    spot_dia = hole_diameter_mm * 1.0  # spot drill diameter roughly equals
    if spot_dia < 3.0:
        spot_dia = 3.0  # minimum practical spot drill
    fs = get_feeds_speeds("spot_drill", spot_dia, material)
    steps.append(OperationStep(
        operation="spot_drill",
        tool_type="spot_drill",
        tool_diameter_mm=round(spot_dia, 1),
        depth_mm=round(spot_dia * 0.5, 2),  # spot depth ~ half diameter
        notes="Spot drill for positional accuracy before full-depth drilling.",
        feeds_speeds=fs if "error" not in fs else None,
    ).to_dict())

    # --- 2. Drill ---
    depth_ratio = hole_depth_mm / hole_diameter_mm if hole_diameter_mm > 0 else 0
    peck = depth_ratio > 4.0
    drill_fs = get_feeds_speeds("drill", hole_diameter_mm, material)

    drill_notes = (
        f"Drill to depth {hole_depth_mm:.1f} mm. "
        f"Depth/diameter ratio = {depth_ratio:.1f}."
    )
    if peck:
        drill_notes += (
            f" DEEP HOLE: ratio {depth_ratio:.1f}x > 4x. "
            "Peck drilling REQUIRED -- retract every "
            f"{hole_diameter_mm * 2:.1f} mm to clear chips and prevent drill "
            "breakage. Use coolant through if available."
        )
    steps.append(OperationStep(
        operation="peck_drill" if peck else "drill",
        tool_type="drill",
        tool_diameter_mm=hole_diameter_mm,
        depth_mm=hole_depth_mm,
        notes=drill_notes,
        feeds_speeds=drill_fs if "error" not in drill_fs else None,
    ).to_dict())

    # --- 3. Ream (if tight tolerance) ---
    if tolerance_mm < 0.05:
        # Reamer is slightly larger than drill -- drill undersize for ream stock
        ream_stock = 0.25  # mm on diameter, split as 0.125 per side
        drill_dia_for_ream = hole_diameter_mm - ream_stock
        if drill_dia_for_ream < 0.5:
            drill_dia_for_ream = hole_diameter_mm * 0.96  # fallback: 4% undersize

        ream_fs = get_feeds_speeds("reamer", hole_diameter_mm, material)
        steps.append(OperationStep(
            operation="ream",
            tool_type="reamer",
            tool_diameter_mm=hole_diameter_mm,
            depth_mm=hole_depth_mm,
            notes=(
                f"Ream to final tolerance ±{tolerance_mm:.3f} mm. "
                f"Prior drill should be ~{drill_dia_for_ream:.2f} mm "
                f"(leaving {ream_stock:.2f} mm ream stock). "
                "Reaming should follow ISO 286 H7 practices."
            ),
            feeds_speeds=ream_fs if "error" not in ream_fs else None,
        ).to_dict())

    # --- 4. Tap (if threaded) ---
    if has_thread:
        # Tap drill size: approx nominal - pitch.  For metric coarse:
        # pitch ~ 0.15 * diameter for M3-M24 range.  This is a rough heuristic.
        tap_fs = get_feeds_speeds("tap", hole_diameter_mm, material)
        steps.append(OperationStep(
            operation="tap",
            tool_type="tap",
            tool_diameter_mm=hole_diameter_mm,
            depth_mm=hole_depth_mm,
            notes=(
                f"Tap internal thread.  Use appropriate tap drill size per "
                f"standard thread chart.  For metric coarse, tap drill ≈ "
                f"nominal diameter - pitch.  Ensure rigid tapping or "
                f"tension/compression holder.  Cutting oil recommended."
            ),
            feeds_speeds=tap_fs if "error" not in tap_fs else None,
        ).to_dict())

    return steps


def check_pocket_process(
    pocket_width_mm: float,
    pocket_depth_mm: float,
    min_corner_radius_mm: float,
    material: str = "aluminum_6061",
) -> list[dict]:
    """Determine required pocket-machining operations.

    Standard pocket strategy:
      1. Roughing endmill at ~80% of pocket width (maximise MRR).
      2. Finish endmill if min_corner_radius < roughing_tool_radius.
         (The roughing tool cannot reach tight internal corners.)

    Args:
        pocket_width_mm:       Narrowest width of the pocket in mm.
        pocket_depth_mm:       Total pocket depth from entry surface in mm.
        min_corner_radius_mm:  Smallest internal corner radius in the pocket.
        material:              Workpiece material key.

    Returns:
        list[dict] -- one or more OperationStep dicts.
    """
    steps: list[dict] = []
    material_props = _MATERIAL_PROPERTIES.get(material, {})
    is_plastic = material_props.get("material_type") == "plastic"

    # --- 1. Roughing ---
    rough_dia = pocket_width_mm * 0.80
    # Clamp rough_dia to a reasonable range
    if rough_dia < 1.0:
        rough_dia = 1.0
    if rough_dia > pocket_width_mm:
        rough_dia = pocket_width_mm

    # For deep pockets, may need multiple depth passes
    depth_ratio = pocket_depth_mm / rough_dia if rough_dia > 0 else 0
    axial_doc = rough_dia * 0.5 if is_plastic else rough_dia * 0.3
    # For metals axial DOC ~ 0.3D, for plastics ~ 0.5D (gentler on plastics
    # to avoid melting)

    rough_fs = get_feeds_speeds("roughing_endmill", rough_dia, material)
    rough_notes = (
        f"Rough pocket at {rough_dia:.1f} mm diameter (~{rough_dia/pocket_width_mm*100:.0f}% "
        f"of pocket width). Axial DOC: {axial_doc:.1f} mm per pass."
    )
    if depth_ratio > 3.0:
        rough_notes += (
            f" Deep pocket ({depth_ratio:.1f}x D). Consider trochoidal or adaptive "
            "clearing path for the first passes."
        )

    steps.append(OperationStep(
        operation="rough_pocket",
        tool_type="roughing_endmill",
        tool_diameter_mm=round(rough_dia, 1),
        depth_mm=pocket_depth_mm,
        notes=rough_notes,
        feeds_speeds=rough_fs if "error" not in rough_fs else None,
    ).to_dict())

    # --- 2. Finishing (if tight corners remain) ---
    rough_radius = rough_dia / 2.0
    needs_finish = (min_corner_radius_mm > 0 and
                    min_corner_radius_mm < rough_radius * 0.95)

    if needs_finish:
        # Finish tool must satisfy: tool_radius <= corner_radius
        finish_dia = min_corner_radius_mm * 2.0
        if finish_dia < 0.5:
            finish_dia = 0.5  # minimum practical

        finish_fs = get_feeds_speeds("finish_endmill", finish_dia, material)
        steps.append(OperationStep(
            operation="finish_pocket",
            tool_type="finish_endmill",
            tool_diameter_mm=round(finish_dia, 1),
            depth_mm=pocket_depth_mm,
            notes=(
                f"Finish pass to clean up internal corners (min radius "
                f"{min_corner_radius_mm:.2f} mm).  Roughing tool radius "
                f"({rough_radius:.2f} mm) cannot reach these corners.  "
                f"Use light radial engagement (~5-10% of tool dia)."
            ),
            feeds_speeds=finish_fs if "error" not in finish_fs else None,
        ).to_dict())

    return steps


def check_wall_thickness(
    min_thickness_mm: float,
    material: str = "aluminum_6061",
) -> list[dict]:
    """Check wall thickness against DFM minimums for the material.

    Thin walls are at risk of:
      - Warping during machining (residual stress release)
      - Vibration/chatter (low stiffness)
      - Break-through or distortion under clamping forces
      - In plastics: melting or deflection from cutting forces

    Args:
        min_thickness_mm:  Smallest wall thickness found in the part (mm).
        material:          Workpiece material key.

    Returns:
        list[dict] of RuleMessage dicts (warnings or errors).
    """
    messages: list[dict] = []
    material_props = _MATERIAL_PROPERTIES.get(material, {})
    mat_type = material_props.get("material_type", "metal")
    warp_limit = material_props.get("warp_risk_min_wall_mm", 0.5)

    if min_thickness_mm <= 0:
        messages.append(RuleMessage(
            severity="error",
            message=(
                f"Zero or negative wall thickness detected ({min_thickness_mm:.3f} mm). "
                "This is a geometry error -- the feature is self-intersecting or not closed."
            ),
            source="ISO 286 / GD&T fundamentals",
            suggestion="Verify the part geometry for valid solids. Check for overlapping features.",
        ).to_dict())
        return messages

    if min_thickness_mm < warp_limit:
        messages.append(RuleMessage(
            severity="warn",
            message=(
                f"Wall thickness ({min_thickness_mm:.2f} mm) is below the "
                f"recommended minimum of {warp_limit:.2f} mm for {material} "
                f"({mat_type})."
            ),
            source="ASM Metals Handbook Vol. 16 / Plastics Design Guide",
            suggestion=(
                f"Increase wall thickness to at least {warp_limit:.2f} mm. "
                "If geometry cannot change, consider using a sacrificial support, "
                "reducing cutting forces (smaller stepover, lower feed), or "
                "post-machining stress relief."
            ),
        ).to_dict())

    # Extra checks for very thin walls
    if min_thickness_mm < warp_limit * 0.5:
        messages.append(RuleMessage(
            severity="error",
            message=(
                f"Wall thickness ({min_thickness_mm:.2f} mm) is less than 50% "
                f"of the {mat_type} minimum ({warp_limit:.2f} mm). "
                "Part likely to fail during machining."
            ),
            source="Machinery's Handbook, 31st Ed. (DFM section)",
            suggestion=(
                "Redesign the part.  This wall thickness is below practical "
                "machining limits.  Consider additive manufacturing (DMLS/SLS) "
                "if the wall cannot be thickened."
            ),
        ).to_dict())

    if mat_type == "plastic" and min_thickness_mm < 2.0:
        # Plastics are especially vulnerable
        if min_thickness_mm < 1.0:
            messages.append(RuleMessage(
                severity="warn",
                message=(
                    f"Plastic wall thickness ({min_thickness_mm:.2f} mm) may "
                    "cause melting or deflection under cutting forces.  Plastics "
                    "have low thermal conductivity and stiffness."
                ),
                source="GE Plastics Design Guide / Machining Plastics (DuPont)",
                suggestion=(
                    "Use sharp, high-rake tooling.  Reduce spindle speed and "
                    "increase feed to minimise heat build-up.  Air blast cooling "
                    "may be sufficient; avoid water-based coolant if the plastic "
                    "is hygroscopic."
                ),
            ).to_dict())

    return messages


def validate_tool_selection(
    tool_type: str,
    tool_diameter_mm: float,
    feature_type: str,
    feature_dimensions: dict,
    material: str = "aluminum_6061",
) -> list[dict]:
    """Validate that a chosen tool is appropriate for the target feature.

    Checks performed:
      - Tool diameter vs feature width (tool must fit)
      - Tool diameter vs internal corner radius (tool must reach the corner)
      - Depth/diameter ratio (peck drilling if depth > 4x dia)
      - Material compatibility (is this tool type viable for the material)

    Args:
        tool_type:         e.g. "end_mill", "drill", "ball_endmill", ...
        tool_diameter_mm:  Tool cutting diameter in mm.
        feature_type:      "hole", "pocket", "slot", "face", "contour", "chamfer".
        feature_dimensions: dict with relevant dims:
            width_mm, depth_mm, corner_radius_mm, diameter_mm, length_mm, ...
        material:          Workpiece material key.

    Returns:
        list[dict] of RuleMessage dicts.
    """
    messages: list[dict] = []

    # --- Material compatibility ---
    processes = _MATERIAL_PROCESSES.get(material, [])
    tool_to_process: dict[str, str] = {
        "end_mill": "milling",
        "ball_endmill": "milling",
        "roughing_endmill": "milling",
        "finish_endmill": "milling",
        "drill": "drilling",
        "spot_drill": "drilling",
        "reamer": "drilling",
        "tap": "drilling",
        "chamfer_tool": "milling",
    }
    expected_process = tool_to_process.get(tool_type, "milling")
    if expected_process not in processes:
        messages.append(RuleMessage(
            severity="error",
            message=(
                f"Tool type '{tool_type}' requires '{expected_process}', which "
                f"is not listed as compatible with material '{material}'. "
                f"Compatible processes: {processes}"
            ),
            source="ASM Metals Handbook Vol. 16 / Material datasheets",
            suggestion=f"Select a material that supports {expected_process}, or use a different manufacturing method.",
        ).to_dict())

    # --- Feature-type specific checks ---
    width = feature_dimensions.get("width_mm", 0)
    depth = feature_dimensions.get("depth_mm", 0)
    corner_radius = feature_dimensions.get("corner_radius_mm", 0)
    diameter = feature_dimensions.get("diameter_mm", 0)

    if feature_type == "hole":
        # For holes, check tool fits in the hole
        hole_dia = diameter if diameter > 0 else width
        if hole_dia > 0 and tool_diameter_mm > hole_dia:
            messages.append(RuleMessage(
                severity="error",
                message=(
                    f"Tool diameter ({tool_diameter_mm:.2f} mm) exceeds hole "
                    f"diameter ({hole_dia:.2f} mm).  The tool will not fit."
                ),
                source="ISO 13399 / Tool selection best practice",
                suggestion=f"Select a tool with diameter <= {hole_dia:.2f} mm.",
            ).to_dict())

        if depth > 0 and tool_diameter_mm > 0:
            d_ratio = depth / tool_diameter_mm
            if d_ratio > 4.0:
                messages.append(RuleMessage(
                    severity="warn",
                    message=(
                        f"Hole depth ({depth:.1f} mm) is {d_ratio:.1f}x the tool "
                        f"diameter ({tool_diameter_mm:.1f} mm).  "
                        "Deep hole drilling risk."
                    ),
                    source="Machinery's Handbook, 31st Ed. (Drilling section)",
                    suggestion=(
                        "Use peck drilling cycle (G83).  Retract every "
                        f"{tool_diameter_mm * 2:.1f} mm.  Consider gun-drilling "
                        "for ratios > 10x."
                    ),
                ).to_dict())

    elif feature_type in ("pocket", "slot"):
        if width > 0 and tool_diameter_mm > width:
            messages.append(RuleMessage(
                severity="error",
                message=(
                    f"Tool diameter ({tool_diameter_mm:.2f} mm) exceeds "
                    f"{feature_type} width ({width:.2f} mm)."
                ),
                source="ISO 13399",
                suggestion=(
                    f"Select a tool with diameter <= {width:.2f} mm. "
                    f"For high-MRR roughing, use ~80% of width ({width * 0.8:.1f} mm)."
                ),
            ).to_dict())

        if corner_radius > 0 and tool_diameter_mm > 2 * corner_radius:
            messages.append(RuleMessage(
                severity="warn",
                message=(
                    f"Tool radius ({tool_diameter_mm / 2:.2f} mm) is larger than "
                    f"the minimum internal corner radius ({corner_radius:.2f} mm). "
                    "The tool cannot reach the corner -- leaving uncut material."
                ),
                source="Machinery's Handbook, 31st Ed.",
                suggestion=(
                    f"Either increase the corner radius to >= "
                    f"{tool_diameter_mm / 2:.2f} mm, or add a finish pass "
                    f"with a smaller tool (diameter <= {2 * corner_radius:.2f} mm)."
                ),
            ).to_dict())

        # Depth check
        if depth > 0 and tool_diameter_mm > 0:
            d_ratio = depth / tool_diameter_mm
            if d_ratio > 5.0:
                messages.append(RuleMessage(
                    severity="warn",
                    message=(
                        f"{feature_type.capitalize()} depth ({depth:.1f} mm) is "
                        f"{d_ratio:.1f}x the tool diameter.  Risk of tool "
                        "deflection, chatter, and poor surface finish."
                    ),
                    source="Sandvik Coromant Technical Guide",
                    suggestion=(
                        f"Use a larger-diameter tool if possible.  If not, "
                        f"reduce axial depth of cut to <= {tool_diameter_mm * 0.3:.1f} mm "
                        f"per pass and consider a relieved-shank (necked) tool."
                    ),
                ).to_dict())

    elif feature_type == "chamfer":
        chamfer_width = feature_dimensions.get("chamfer_width_mm", 0)
        if chamfer_width > 0 and tool_diameter_mm < chamfer_width * 2:
            messages.append(RuleMessage(
                severity="warn",
                message=(
                    f"Tool diameter ({tool_diameter_mm:.2f} mm) may be "
                    "insufficient for the specified chamfer width "
                    f"({chamfer_width:.2f} mm)."
                ),
                source="ISO 13399",
                suggestion=(
                    "Ensure the chamfer tool's cutting length covers the "
                    "chamfer width, or use multiple passes."
                ),
            ).to_dict())

    # --- Generic depth/diameter ratio for any feature on metals ---
    material_props = _MATERIAL_PROPERTIES.get(material, {})
    mat_type = material_props.get("material_type", "metal")
    if mat_type == "metal" and tool_diameter_mm > 0 and depth > 0:
        if tool_type == "drill" and depth > 10 * tool_diameter_mm:
            messages.append(RuleMessage(
                severity="error",
                message=(
                    f"Depth ({depth:.1f} mm) exceeds 10x drill diameter "
                    f"({tool_diameter_mm:.1f} mm).  Gun-drilling or EDM "
                    "required for this depth ratio."
                ),
                source="Machinery's Handbook, 31st Ed.",
                suggestion="Use gun-drilling, EDM drilling, or split the feature across two sides.",
            ).to_dict())

    # --- Plastic-specific: check for melting risk ---
    if mat_type == "plastic":
        plastic_speeds = _FEEDS_SPEEDS.get(material, {}).get(tool_type)
        if plastic_speeds:
            sfm = plastic_speeds["sfm"]
            if sfm > 500:
                messages.append(RuleMessage(
                    severity="warn",
                    message=(
                        f"Recommended SFM ({sfm}) for {material} with "
                        f"{tool_type} is high.  Risk of melting the plastic "
                        f"(melting point ~{material_props.get('melting_point_c', '?')} C)."
                    ),
                    source="DuPont Machining Plastics Guide",
                    suggestion=(
                        "Reduce spindle speed by 20-30%.  Use compressed air "
                        "cooling.  Ensure sharp tooling with high rake angle.  "
                        "Do NOT use coolant on hygroscopic plastics."
                    ),
                ).to_dict())

    return messages


# =========================================================================
#   Aggregate rule runner
# =========================================================================


def run_all_rules(
    features: list[dict],
    material: str = "aluminum_6061",
) -> dict:
    """Run all manufacturing rule checks against a set of features.

    This is the main entry point for Phase 0 CAPP rule evaluation.
    It aggregates hole-process rules, pocket-process rules, wall-thickness
    rules, and tool-validation rules across all features.

    Each feature dict must have:
      - type: str         "hole", "pocket", "slot", "face", "contour", "chamfer"
      - dimensions: dict  Feature-specific dimensions.
      - tool (optional):  dict with tool_type, tool_diameter_mm keys for
                          validation.

    Args:
        features:  List of feature descriptors (see above).
        material:  Workpiece material key.

    Returns:
        dict with keys:
          - warnings:            list[dict]  non-fatal advisory messages
          - errors:              list[dict]  hard manufacturing blockers
          - suggested_operations: list[dict] ordered operation steps
    """
    all_warnings: list[dict] = []
    all_errors: list[dict] = []
    all_ops: list[dict] = []

    # Validate material
    if material not in _MATERIAL_PROPERTIES:
        all_errors.append(RuleMessage(
            severity="error",
            message=f"Unknown material '{material}'. Known: {list(_MATERIAL_PROPERTIES.keys())}",
            source="Internal material database",
            suggestion="Specify a known material from the supported list.",
        ).to_dict())
        return {
            "warnings": all_warnings,
            "errors": all_errors,
            "suggested_operations": all_ops,
        }

    material_props = _MATERIAL_PROPERTIES[material]

    for i, feat in enumerate(features):
        feat_type = feat.get("type", "")
        dims = feat.get("dimensions", {})
        tool = feat.get("tool")

        if feat_type == "hole":
            dia = dims.get("diameter_mm", dims.get("width_mm", 0))
            depth = dims.get("depth_mm", 0)
            tol = dims.get("tolerance_mm", 0.10)  # default loose tolerance
            thread = dims.get("has_thread", False)

            if dia <= 0:
                all_errors.append(RuleMessage(
                    severity="error",
                    message=f"Feature[{i}]: Hole has invalid diameter ({dia}).",
                    source="Feature specification",
                    suggestion="Specify a valid hole diameter > 0.",
                ).to_dict())
                continue

            hole_ops = check_hole_process(dia, depth, tol, thread, material)
            for op in hole_ops:
                op["feature_index"] = i
            all_ops.extend(hole_ops)

            # Wall thickness check around the hole (if specified)
            min_wall = dims.get("min_wall_thickness_mm")
            if min_wall is not None:
                wall_msgs = check_wall_thickness(min_wall, material)
                for m in wall_msgs:
                    m["feature_index"] = i
                    if m["severity"] == "error":
                        all_errors.append(m)
                    else:
                        all_warnings.append(m)

        elif feat_type in ("pocket", "slot"):
            width = dims.get("width_mm", 0)
            depth = dims.get("depth_mm", 0)
            corner_r = dims.get("corner_radius_mm", 0)

            if width <= 0:
                all_errors.append(RuleMessage(
                    severity="error",
                    message=f"Feature[{i}]: {feat_type} has invalid width ({width}).",
                    source="Feature specification",
                    suggestion="Specify a valid width > 0.",
                ).to_dict())
                continue

            pocket_ops = check_pocket_process(width, depth, corner_r, material)
            for op in pocket_ops:
                op["feature_index"] = i
            all_ops.extend(pocket_ops)

            # Wall thickness check
            min_wall = dims.get("min_wall_thickness_mm")
            if min_wall is not None:
                wall_msgs = check_wall_thickness(min_wall, material)
                for m in wall_msgs:
                    m["feature_index"] = i
                    if m["severity"] == "error":
                        all_errors.append(m)
                    else:
                        all_warnings.append(m)

        elif feat_type == "chamfer":
            chamfer_w = dims.get("chamfer_width_mm", 0)
            depth = dims.get("depth_mm", 0)
            chamfer_op = OperationStep(
                operation="chamfer",
                tool_type="chamfer_tool",
                tool_diameter_mm=chamfer_w * 2.5 if chamfer_w > 0 else 6.0,
                depth_mm=depth,
                notes=(
                    f"Chamfer edge with {chamfer_w:.2f} mm width.  "
                    "Use a 90-degree chamfer tool (or angle matching the spec)."
                ),
                feeds_speeds=get_feeds_speeds("chamfer_tool",
                                              chamfer_w * 2.5 if chamfer_w > 0 else 6.0,
                                              material),
            ).to_dict()
            chamfer_op["feature_index"] = i
            all_ops.append(chamfer_op)

        elif feat_type == "face":
            width = dims.get("width_mm", 100)
            face_op = OperationStep(
                operation="face_mill",
                tool_type="end_mill",
                tool_diameter_mm=min(width, 50.0),
                depth_mm=dims.get("depth_mm", 1.0),
                notes=(
                    f"Face milling with {min(width, 50):.0f} mm tool.  "
                    "Use a face mill or large end mill for flatness."
                ),
                feeds_speeds=get_feeds_speeds("end_mill", min(width, 50.0), material),
            ).to_dict()
            face_op["feature_index"] = i
            all_ops.append(face_op)

        elif feat_type == "contour":
            depth = dims.get("depth_mm", 0)
            contour_op = OperationStep(
                operation="contour",
                tool_type="end_mill",
                tool_diameter_mm=dims.get("tool_diameter_mm", 10.0),
                depth_mm=depth,
                notes=(
                    "Profile/contour operation.  Ensure the tool has sufficient "
                    "flute length to reach the full depth.  Use multiple "
                    "Z-level passes if depth > 2x tool diameter."
                ),
                feeds_speeds=get_feeds_speeds(
                    "end_mill", dims.get("tool_diameter_mm", 10.0), material,
                ),
            ).to_dict()
            contour_op["feature_index"] = i
            all_ops.append(contour_op)

        else:
            all_warnings.append(RuleMessage(
                severity="warn",
                message=f"Feature[{i}]: Unknown feature type '{feat_type}'. No rules applied.",
                source="Rule engine",
                suggestion=f"Supported feature types: hole, pocket, slot, face, contour, chamfer.",
            ).to_dict())

        # --- Tool validation (if tool is specified) ---
        if tool is not None:
            tool_type = tool.get("tool_type", "")
            tool_dia = tool.get("tool_diameter_mm", 0)
            if tool_type and tool_dia > 0:
                tool_msgs = validate_tool_selection(
                    tool_type, tool_dia, feat_type, dims, material,
                )
                for m in tool_msgs:
                    m["feature_index"] = i
                    if m["severity"] == "error":
                        all_errors.append(m)
                    else:
                        all_warnings.append(m)

    # --- Global material checks ---
    # Check if the material itself imposes constraints
    if material_props.get("machinability_pct", 100) is not None:
        mach_pct = material_props["machinability_pct"]
        if mach_pct < 30:
            all_warnings.append(RuleMessage(
                severity="warn",
                message=(
                    f"Material '{material}' has very low machinability "
                    f"({mach_pct}%).  Expect high tool wear, low productivity, "
                    "and possible surface-integrity issues."
                ),
                source="ASM Metals Handbook Vol. 16",
                suggestion=(
                    "Use premium carbide or coated tooling.  Reduce cutting "
                    "speeds by 20-30% from baseline.  Ensure rigid workholding "
                    "and short tool overhang.  Consider PCD tooling for "
                    "non-ferrous materials."
                ),
            ).to_dict())

    # Check if the material is plastic and we have drilling -- coolant advice
    if material_props.get("material_type") == "plastic" and any(
        op.get("operation") in ("drill", "peck_drill", "ream", "tap")
        for op in all_ops
    ):
        all_warnings.append(RuleMessage(
            severity="warn",
            message=(
                f"Plastic material '{material}' with hole-making operations.  "
                "Many plastics absorb coolant and swell, affecting tolerances."
            ),
            source="DuPont Machining Plastics Guide",
            suggestion=(
                "Use compressed air or mist cooling instead of flood coolant.  "
                "If coolant is required, verify the plastic grade is compatible."
            ),
        ).to_dict())

    return {
        "warnings": all_warnings,
        "errors": all_errors,
        "suggested_operations": all_ops,
    }


# =========================================================================
#  Self-test
# =========================================================================

if __name__ == "__main__":
    print("=== Manufacturing Rule Engine Self-Test ===\n")

    passed = 0
    failed = 0

    def _check(label: str, condition: bool, detail: str = ""):
        global passed, failed
        if condition:
            passed += 1
            print(f"  PASS  {label}")
        else:
            failed += 1
            print(f"  FAIL  {label}  -- {detail}")

    # ------------------------------------------------------------------
    # 1. get_material_properties
    # ------------------------------------------------------------------
    print("1. get_material_properties ...")
    props = get_material_properties("aluminum_6061")
    _check("aluminum_6061 exists", len(props) > 0)
    _check("density correct", abs(props["density_gcm3"] - 2.70) < 0.01)
    _check("material_type is metal", props["material_type"] == "metal")
    _check("unknown material returns empty", get_material_properties("unobtanium") == {})

    props_abs = get_material_properties("abs")
    _check("ABS exists", len(props_abs) > 0)
    _check("ABS is plastic", props_abs["material_type"] == "plastic")
    _check("ABS hardness is None (not applicable)", props_abs["hardness_hb"] is None)

    # ------------------------------------------------------------------
    # 2. list_materials / list_tool_types
    # ------------------------------------------------------------------
    print("\n2. list_materials / list_tool_types ...")
    mats = list_materials()
    _check("12 materials", len(mats) == 12)
    _check("aluminum_6061 present", "aluminum_6061" in mats)
    _check("peek present", "peek" in mats)

    tools = list_tool_types()
    _check("at least 6 tool types", len(tools) >= 6)
    _check("end_mill present", "end_mill" in tools)
    _check("drill present", "drill" in tools)

    # ------------------------------------------------------------------
    # 3. get_compatible_processes
    # ------------------------------------------------------------------
    print("\n3. get_compatible_processes ...")
    al_procs = get_compatible_processes("aluminum_6061")
    _check("aluminum has milling", "milling" in al_procs)
    _check("aluminum has drilling", "drilling" in al_procs)
    _check("aluminum has edm", "edm" in al_procs)

    abs_procs = get_compatible_processes("abs")
    _check("ABS has injection_molding", "injection_molding" in abs_procs)
    _check("ABS has 3d_printing_fdm", "3d_printing_fdm" in abs_procs)
    _check("ABS does NOT have edm", "edm" not in abs_procs)

    _check("unknown material returns empty", get_compatible_processes("xyz") == [])

    # ------------------------------------------------------------------
    # 4. get_feeds_speeds
    # ------------------------------------------------------------------
    print("\n4. get_feeds_speeds ...")
    fs = get_feeds_speeds("end_mill", 10.0, "aluminum_6061")
    _check("no error", "error" not in fs)
    _check("sfm = 800", fs["sfm"] == 800)
    _check("fpt = 0.15", abs(fs["fpt_mm"] - 0.15) < 0.001)
    _check("rpm > 0", fs["rpm"] > 0)
    _check("feed_rate > 0", fs["feed_rate_mm_min"] > 0)
    # RPM at D=10mm, SFM=800: 800*304.8/(pi*10) = 7760 approx
    expected_rpm = 800 * 304.8 / (math.pi * 10.0)
    _check("rpm matches formula", abs(fs["rpm"] - expected_rpm) < 1.0,
           f"got {fs['rpm']:.0f}, expected ~{expected_rpm:.0f}")

    fs_ti = get_feeds_speeds("end_mill", 10.0, "titanium_6al4v")
    _check("titanium sfm much lower", fs_ti["sfm"] < 200)
    _check("titanium fpt lower", fs_ti["fpt_mm"] < 0.10)

    fs_err1 = get_feeds_speeds("end_mill", 10.0, "nonsense")
    _check("unknown material returns error", "error" in fs_err1)

    fs_err2 = get_feeds_speeds("laser_cutter", 10.0, "aluminum_6061")
    _check("unknown tool returns error", "error" in fs_err2)

    # ------------------------------------------------------------------
    # 5. check_hole_process
    # ------------------------------------------------------------------
    print("\n5. check_hole_process ...")
    # Standard hole: no thread, loose tolerance -> spot + drill
    hole_ops = check_hole_process(10.0, 20.0, 0.1, False,
                                  material="aluminum_6061")
    _check("2 operations (spot + drill)", len(hole_ops) == 2,
           f"got {len(hole_ops)}: {[o['operation'] for o in hole_ops]}")
    _check("first is spot_drill", hole_ops[0]["operation"] == "spot_drill")
    _check("second is drill", hole_ops[1]["operation"] == "drill")

    # Tight tolerance -> spot + drill + ream
    hole_ops_tight = check_hole_process(8.0, 16.0, 0.02, False,
                                        material="steel_4140")
    _check("tight tolerance adds ream", len(hole_ops_tight) == 3,
           f"got {len(hole_ops_tight)}")
    _check("ream present", any(o["operation"] == "ream" for o in hole_ops_tight))

    # Threaded -> spot + drill + tap
    hole_ops_thread = check_hole_process(6.0, 12.0, 0.1, True,
                                         material="aluminum_6061")
    _check("threaded adds tap", len(hole_ops_thread) == 3,
           f"got {len(hole_ops_thread)}")
    _check("tap present", any(o["operation"] == "tap" for o in hole_ops_thread))

    # Deep hole -> peck drilling
    hole_ops_deep = check_hole_process(4.0, 25.0, 0.1, False,
                                       material="aluminum_6061")
    _check("deep hole uses peck_drill",
           any(o["operation"] == "peck_drill" for o in hole_ops_deep))

    # Tight + threaded -> spot + drill + ream + tap (4 ops)
    hole_ops_full = check_hole_process(5.0, 10.0, 0.01, True,
                                       material="steel_4140")
    _check("full sequence = 4 ops", len(hole_ops_full) == 4,
           f"got {len(hole_ops_full)}: {[o['operation'] for o in hole_ops_full]}")

    # ------------------------------------------------------------------
    # 6. check_pocket_process
    # ------------------------------------------------------------------
    print("\n6. check_pocket_process ...")
    # Wide pocket, large corners -> rough only (rough radius=20, corner=25 > 20)
    pkt_ops = check_pocket_process(50.0, 10.0, 25.0, material="aluminum_6061")
    _check("wide loose-corners -> 1 op (rough only)", len(pkt_ops) == 1,
           f"got {len(pkt_ops)}")
    _check("operation is rough_pocket", pkt_ops[0]["operation"] == "rough_pocket")
    _check("rough tool ~80% of width",
           abs(pkt_ops[0]["tool_diameter_mm"] - 40.0) < 5.0)

    # Tight corners -> rough + finish
    pkt_ops_tight = check_pocket_process(20.0, 5.0, 1.0, material="steel_304")
    _check("tight corners -> 2 ops", len(pkt_ops_tight) == 2,
           f"got {len(pkt_ops_tight)}")
    _check("finish op present",
           any(o["operation"] == "finish_pocket" for o in pkt_ops_tight))

    # Small pocket with tiny tool
    pkt_ops_small = check_pocket_process(3.0, 2.0, 0.5, material="peek")
    _check("small pocket works", len(pkt_ops_small) >= 1)

    # ------------------------------------------------------------------
    # 7. check_wall_thickness
    # ------------------------------------------------------------------
    print("\n7. check_wall_thickness ...")
    wt_ok = check_wall_thickness(5.0, "aluminum_6061")
    _check("thick wall OK (metal)", len(wt_ok) == 0,
           f"got {len(wt_ok)} messages")

    wt_thin_metal = check_wall_thickness(0.3, "aluminum_6061")
    _check("thin metal warns", len(wt_thin_metal) >= 1)
    _check("thin metal has warn severity",
           any(m["severity"] == "warn" for m in wt_thin_metal))

    wt_very_thin_metal = check_wall_thickness(0.1, "titanium_6al4v")
    _check("very thin metal errors",
           any(m["severity"] == "error" for m in wt_very_thin_metal))

    wt_plastic_ok = check_wall_thickness(2.0, "abs")
    _check("thick plastic OK", len(wt_plastic_ok) == 0)

    wt_plastic_thin = check_wall_thickness(0.6, "nylon_pa6")
    _check("thin plastic (0.6mm) warns", len(wt_plastic_thin) >= 1)

    wt_plastic_very_thin = check_wall_thickness(0.4, "polypropylene")
    _check("very thin plastic errors",
           any(m["severity"] == "error" for m in wt_plastic_very_thin))

    # ------------------------------------------------------------------
    # 8. validate_tool_selection
    # ------------------------------------------------------------------
    print("\n8. validate_tool_selection ...")
    # Tool too big for hole
    msgs = validate_tool_selection("drill", 10.0, "hole",
                                   {"diameter_mm": 8.0, "depth_mm": 20.0},
                                   "aluminum_6061")
    _check("tool > hole is error", any(m["severity"] == "error" for m in msgs))

    # Tool OK for hole
    msgs_ok = validate_tool_selection("drill", 8.0, "hole",
                                      {"diameter_mm": 8.0, "depth_mm": 20.0},
                                      "aluminum_6061")
    _check("tool = hole is OK", len(msgs_ok) == 0,
           f"got {len(msgs_ok)}: {[m['message'] for m in msgs_ok]}")

    # Tool too big for pocket
    msgs_pkt = validate_tool_selection("end_mill", 20.0, "pocket",
                                       {"width_mm": 15.0, "depth_mm": 5.0},
                                       "aluminum_6061")
    _check("tool > pocket width is error",
           any(m["severity"] == "error" for m in msgs_pkt))

    # Corner radius violation
    msgs_corner = validate_tool_selection("end_mill", 10.0, "pocket",
                                          {"width_mm": 30.0, "depth_mm": 10.0,
                                           "corner_radius_mm": 2.0},
                                          "steel_4140")
    _check("corner radius warning",
           any(m["severity"] == "warn" for m in msgs_corner))

    # Deep hole
    msgs_deep = validate_tool_selection("drill", 4.0, "hole",
                                        {"diameter_mm": 4.0, "depth_mm": 25.0},
                                        "steel_304")
    _check("deep drill warns (6.25x)",
           any(m["severity"] == "warn" for m in msgs_deep))

    # Plastic material with high SFM tool -> melting risk
    msgs_plastic = validate_tool_selection("end_mill", 10.0, "pocket",
                                           {"width_mm": 30.0, "depth_mm": 5.0},
                                           "polypropylene")
    # PP end_mill SFM=550 which is >500, should trigger melting warning
    _check("plastic melting warning",
           any("melting" in m["message"].lower() for m in msgs_plastic),
           f"msgs: {[m['message'][:80] for m in msgs_plastic]}")

    # ------------------------------------------------------------------
    # 9. run_all_rules
    # ------------------------------------------------------------------
    print("\n9. run_all_rules (aggregate runner) ...")
    features = [
        {
            "type": "hole",
            "dimensions": {
                "diameter_mm": 8.0,
                "depth_mm": 20.0,
                "tolerance_mm": 0.02,
                "has_thread": True,
                "min_wall_thickness_mm": 0.3,  # thin wall -> should warn
            },
            "tool": {"tool_type": "drill", "tool_diameter_mm": 8.0},
        },
        {
            "type": "pocket",
            "dimensions": {
                "width_mm": 30.0,
                "depth_mm": 15.0,
                "corner_radius_mm": 2.0,
            },
        },
        {
            "type": "chamfer",
            "dimensions": {
                "chamfer_width_mm": 1.5,
                "depth_mm": 1.5,
            },
        },
        {
            "type": "face",
            "dimensions": {
                "width_mm": 100.0,
                "depth_mm": 1.0,
            },
        },
        {
            "type": "contour",
            "dimensions": {
                "depth_mm": 20.0,
                "tool_diameter_mm": 12.0,
            },
        },
    ]

    result = run_all_rules(features, "aluminum_6061")
    _check("result has warnings key", "warnings" in result)
    _check("result has errors key", "errors" in result)
    _check("result has suggested_operations", "suggested_operations" in result)
    _check("no hard errors", len(result["errors"]) == 0,
           f"errors: {[e['message'][:80] for e in result['errors']]}")
    _check("has warnings (thin wall)", len(result["warnings"]) >= 1,
           f"warnings: {[w['message'][:80] for w in result['warnings']]}")
    _check("has operations", len(result["suggested_operations"]) >= 5,
           f"got {len(result['suggested_operations'])} ops")

    # Check all operations have feature_index
    _check("all ops have feature_index",
           all("feature_index" in op for op in result["suggested_operations"]))

    # Test with bad tool selection
    features_bad = [
        {
            "type": "hole",
            "dimensions": {"diameter_mm": 5.0, "depth_mm": 10.0},
            "tool": {"tool_type": "drill", "tool_diameter_mm": 10.0},  # too big
        },
    ]
    result_bad = run_all_rules(features_bad, "aluminum_6061")
    _check("oversize tool produces error", len(result_bad["errors"]) >= 1)

    # Test with unknown material
    result_unknown = run_all_rules(features, "unobtanium")
    _check("unknown material produces error", len(result_unknown["errors"]) >= 1)

    # Test with titanium (low machinability)
    result_ti = run_all_rules(features[:1], "titanium_6al4v")
    _check("titanium has machinability warning",
           any("machinability" in w["message"].lower()
               for w in result_ti["warnings"]))

    # Test plastics drilling
    features_plastic = [
        {
            "type": "hole",
            "dimensions": {
                "diameter_mm": 6.0,
                "depth_mm": 12.0,
                "has_thread": False,
            },
        },
    ]
    result_plastic = run_all_rules(features_plastic, "abs")
    _check("plastic drilling has coolant warning",
           any("coolant" in w["message"].lower() or "plastic" in w["message"].lower()
               for w in result_plastic["warnings"]))

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    total = passed + failed
    print(f"\n=== {'ALL TESTS PASSED' if failed == 0 else 'SOME TESTS FAILED'} "
          f"({passed}/{total} passed) ===")
    if failed > 0:
        exit(1)
