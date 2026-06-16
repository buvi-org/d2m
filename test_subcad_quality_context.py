"""Tests for SubCAD quality, inspection, and collision policy context."""

import json
import sys
import tempfile
from pathlib import Path

from src.subcad.quality_context import (
    QualityContext,
    clearance_limits,
    collision_required,
    load_quality_context,
    needs_probe,
    required_inspection_methods,
    tolerance_bands,
)


passed = 0
failed = 0


def check(label, condition, detail=""):
    global passed, failed
    if condition:
        passed += 1
        print(f"  PASS  {label}")
    else:
        failed += 1
        print(f"  FAIL  {label}  -- {detail}")


quality_data = {
    "schema_version": "subcad.quality_context.v1",
    "tolerances": {
        "default": {"linear_mm": 0.10, "methods": ["caliper"]},
        "features": {
            "bearing_bore": {
                "nominal_mm": 20.0,
                "tolerance_mm": 0.01,
                "methods": ["bore_gage"],
                "requires_probe": True,
                "critical": True,
            }
        },
    },
    "inspection": {
        "required": True,
        "methods": ["caliper"],
        "requirements": [
            {
                "target": "datum_a",
                "methods": ["on_machine_probe"],
                "required": True,
                "requires_probe": True,
            }
        ],
    },
    "surface_finish": {
        "features": {
            "seal_face": {
                "ra_um": 0.8,
                "methods": ["profilometer"],
                "required": True,
            }
        }
    },
    "critical_dimensions": [
        {
            "name": "bolt_circle",
            "feature": "hole_pattern",
            "nominal_mm": 50.0,
            "plus_mm": 0.02,
            "minus_mm": 0.03,
            "methods": ["cmm"],
        }
    ],
    "critical_features": {
        "thin_wall": {"methods": ["visual", "ultrasonic"], "required": True}
    },
    "collision_policy": {
        "enabled": True,
        "required": True,
        "clearance_mm": 2.0,
        "holder_check": True,
        "fixture_check": True,
        "holder_clearance_mm": 4.0,
        "fixture_clearance_mm": 6.0,
        "rapid_clearance_mm": 10.0,
    },
}


print("=" * 60)
print("SubCAD Quality Context Test")
print("=" * 60)

print("\n1. Dict loading and tolerance bands ...")
context = load_quality_context(quality_data)
bands = context.tolerance_bands("bearing_bore")
check("quality context loads schema", context.schema_version == "subcad.quality_context.v1")
check("default tolerance band is included", "default" in bands, bands)
check("feature tolerance band is included", "bearing_bore" in bands, bands)
check(
    "nominal tolerance expands to lower limit",
    abs(bands["bearing_bore"]["lower_mm"] - 19.99) < 0.000001,
    bands["bearing_bore"],
)
check(
    "nominal tolerance expands to upper limit",
    abs(bands["bearing_bore"]["upper_mm"] - 20.01) < 0.000001,
    bands["bearing_bore"],
)
normalized_default = load_quality_context({
    "tolerances": {"default": {"nominal_mm": 10.0, "tolerance_mm": 0.05}}
})
default_dict = normalized_default.to_dict()["tolerances"]["default"]
check("default tolerance serializes lower limit", abs(default_dict["lower_mm"] - 9.95) < 0.000001, default_dict)
check("default tolerance serializes upper limit", abs(default_dict["upper_mm"] - 10.05) < 0.000001, default_dict)

print("\n2. Inspection method helpers ...")
bore_methods = context.required_inspection_methods("bearing_bore")
datum_methods = context.required_inspection_methods("datum_a")
finish_methods = context.required_inspection_methods("seal_face")
check("global inspection method applies to feature", "caliper" in bore_methods, bore_methods)
check("feature tolerance method is required", "bore_gage" in bore_methods, bore_methods)
check("datum probing method is required", "on_machine_probe" in datum_methods, datum_methods)
check("surface finish inspection method is required", "profilometer" in finish_methods, finish_methods)

print("\n3. Probe detection ...")
check("probe is required by explicit feature tolerance", context.needs_probe("bearing_bore"))
check("probe is required by CMM critical dimension", context.needs_probe("hole_pattern"))
check("plain finish inspection does not require probe", not context.needs_probe("seal_face"))

print("\n4. Collision policy helpers ...")
limits = context.clearance_limits()
check("collision gate is required", context.collision_required())
check("holder clearance is normalized", limits["holder_clearance_mm"] == 4.0, limits)
check("fixture clearance is normalized", limits["fixture_clearance_mm"] == 6.0, limits)
check("rapid clearance is normalized", limits["rapid_clearance_mm"] == 10.0, limits)

print("\n5. Module-level convenience helpers ...")
check("module tolerance helper works", "bearing_bore" in tolerance_bands(quality_data, "bearing_bore"))
check("module inspection helper works", "bore_gage" in required_inspection_methods(quality_data, "bearing_bore"))
check("module probe helper works", needs_probe(quality_data, "datum_a"))
check("module collision helper works", collision_required(quality_data))
check("module clearance helper works", clearance_limits(quality_data)["fixture_clearance_mm"] == 6.0)

print("\n6. JSON loading and plan-style nesting ...")
with tempfile.TemporaryDirectory() as tmpdir:
    path = Path(tmpdir) / "quality.json"
    path.write_text(json.dumps(quality_data), encoding="utf-8")
    from_json = QualityContext.from_json(path)
check("quality context loads from JSON", from_json.collision_required())

nested = load_quality_context({"schema_version": "subcad.shop_floor.v1", "quality": quality_data})
check("quality context unwraps process-plan quality field", nested.needs_probe("bearing_bore"))

print("\n7. Optional collision policy behavior ...")
optional = load_quality_context({
    "collision_policy": {"enabled": True, "required": False, "clearance_mm": 1.5}
})
check("optional policy is not required globally", not optional.collision_required())
check(
    "operation can require optional collision policy",
    optional.collision_required({"requires_collision_check": True}),
)

print("\n" + "=" * 60)
print(f"Passed: {passed}")
print(f"Failed: {failed}")
print("=" * 60)

if failed:
    sys.exit(1)
