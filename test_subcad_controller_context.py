"""Tests for controller/post context loading and helper queries."""

import sys

from src.subcad.controller_context import ControllerContext, load_controller_context


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


print("=" * 60)
print("SubCAD Controller Context Test")
print("=" * 60)

print("\n1. Controller JSON can be loaded by id ...")
generic = load_controller_context("generic_3axis_debug")
check("generic controller id", generic.controller_id == "generic_3axis_debug", generic.controller_id)
check("generic source is captured", generic.source.endswith("generic_3axis_debug.json"), generic.source)
check("generic supports G81", generic.supports_cycle("g81"), generic.supported_cycles)
check("generic rejects unsupported cycle", not generic.supports_cycle("G234"), generic.supported_cycles)
check("generic flood coolant supported", generic.supports_coolant("flood"), generic.coolant_codes)
check("generic M08 coolant code supported", generic.supports_coolant("M08"), generic.coolant_codes)
check("generic flood coolant code", generic.coolant_code("FLOOD") == "M08", generic.coolant_code("FLOOD"))
check("generic probing disabled", not generic.supports_probing(), generic.probing)
check("generic post dialect", generic.post_dialect == "generic_3axis_debug", generic.post_dialect)

print("\n2. Rich controller JSON exposes rotary, probing, macros, and offsets ...")
haas = load_controller_context("controllers/haas_ngc_mill.json")
check("haas supports through-spindle coolant", haas.supports_coolant("through spindle"), haas.coolant_codes)
check("haas coolant code lookup", haas.coolant_code("through_spindle") == "M88", haas.coolant_codes)
check("haas supports indexed 5-axis mode", haas.supports_rotary_mode("indexed-5axis"), haas.rotary_modes)
check("haas supports probing", haas.supports_probing(), haas.probing)
check("haas supports rigid tapping", haas.supports_rigid_tapping(), haas.rigid_tapping)
check("haas supports macros", haas.supports_macros(), haas.macro_support)
check("haas supports G110 coordinate system", haas.supports_coordinate_system("g110"), haas.coordinate_systems)
check("haas rejects unknown rotary mode", not haas.supports_rotary_mode("polar_interpolation"), haas.rotary_modes)

print("\n3. Dictionary input accepts validation-friendly aliases ...")
alias_context = load_controller_context({
    "controller_id": "alias_control",
    "name": "Alias Control",
    "capabilities": {
        "controller_cycles": ["g81", "G81", "g83"],
        "coolant": ["flood", "through-spindle"],
        "probing": "true",
        "rigid_tapping": {"supported": True},
        "macro_support": {"supported": False},
        "coordinate_systems": ["g54", "G55"],
    },
})
alias_dict = alias_context.to_dict()
check("cycles are normalized and unique", alias_context.supported_cycles == ["G81", "G83"], alias_context.supported_cycles)
check("coolant aliases are normalized", alias_context.coolant_modes == ["flood", "through_spindle"], alias_context.coolant_modes)
check("probing string coerces to bool", alias_context.supports_probing(), alias_context.probing)
check("macro support dict coerces to bool", not alias_context.supports_macros(), alias_context.macro_support)
check("to_dict exposes controller_cycles", alias_dict["capabilities"]["controller_cycles"] == ["G81", "G83"], alias_dict)
check("to_dict exposes coolant list", alias_dict["capabilities"]["coolant"] == ["flood", "through_spindle"], alias_dict)

print("\n4. Existing context objects pass through the loader ...")
manual = ControllerContext.from_dict({
    "controller_id": "manual",
    "name": "Manual",
    "supported_cycles": ["G81"],
})
check("loader returns same instance", load_controller_context(manual) is manual)

print("\n" + "=" * 60)
print(f"Passed: {passed}")
print(f"Failed: {failed}")
print("=" * 60)

if failed:
    sys.exit(1)
