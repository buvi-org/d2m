"""Tests for setup intent context helpers."""
import sys
from dataclasses import dataclass

from src.subcad.setup_context import (
    SETUP_CONTEXT_SCHEMA_VERSION,
    SetupContext,
    coerce_setup_context,
    load_setup_context,
    normalize_face_selector,
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


@dataclass
class FixtureObject:
    name: str
    fixture_type: str
    description: str = ""


@dataclass
class IntentObject:
    workholding: FixtureObject
    part_orientation: dict
    accessible_faces: list
    operation_side: str
    setup_count: int
    work_offset: str
    work_offset_values: tuple
    stock_allowance: float
    notes: str


print("=" * 60)
print("SubCAD Setup Context Test")
print("=" * 60)

print("\n1. Face selector aliases normalize ...")
check("top maps to >Z", normalize_face_selector("top") == ">Z")
check("+x maps to >X", normalize_face_selector("+x") == ">X")
check("front maps to <Y", normalize_face_selector("front") == "<Y")

print("\n2. Dict setup intent is coerced ...")
ctx = load_setup_context({
    "workholding": {"name": "kurt_dx6_vise", "fixture_type": "vise"},
    "part_orientation": {"primary_face": "top"},
    "datum": {"work_offset": "g55", "work_offset_values": [10, 20, 30]},
    "accessible_faces": ["top", "+X"],
    "operation_side": "top",
    "setup_count": 2,
    "stock_allowance": 1.5,
    "notes": "flip after top features",
})
check("schema version is explicit", ctx.schema_version == SETUP_CONTEXT_SCHEMA_VERSION, ctx.schema_version)
check("fixture alias accepted", ctx.fixture["name"] == "kurt_dx6_vise", ctx.fixture)
check("workholding alias property", ctx.workholding == ctx.fixture, ctx.workholding)
check("work offset uppercased", ctx.work_offset == "G55", ctx.work_offset)
check("offset values padded", ctx.work_offset_values == (10.0, 20.0, 30.0, 0.0, 0.0, 0.0), ctx.work_offset_values)
check("accessible faces normalized", ctx.accessible_faces == [">Z", ">X"], ctx.accessible_faces)
check("primary face follows operation side", ctx.primary_face == ">Z", ctx.primary_face)
check("can access declared side", ctx.can_access_face("+x"))
check("bottom requires reorientation", ctx.requires_reorientation("<Z"))
check("stock allowance normalized", ctx.stock_allowance == {"uniform_mm": 1.5}, ctx.stock_allowance)

print("\n3. Object setup intent is coerced ...")
obj = IntentObject(
    workholding=FixtureObject("soft_jaws", "soft_jaws"),
    part_orientation={"primary_face": "+Z"},
    accessible_faces=["+Z", "-Z"],
    operation_side="-Z",
    setup_count=2,
    work_offset="G56",
    work_offset_values=(1, 2, 3, 0, 0, 90),
    stock_allowance=0.25,
    notes="second-op cleanup",
)
ctx = coerce_setup_context(obj)
check("object fixture converted", ctx.fixture["name"] == "soft_jaws", ctx.fixture)
check("object side normalized", ctx.operation_side == "<Z", ctx.operation_side)
check("operation side is included first", ctx.accessible_faces[0] == "<Z", ctx.accessible_faces)
check("top remains accessible", ctx.can_access_face(">Z"), ctx.accessible_faces)

print("\n4. Plan metadata bridge is validation-friendly ...")
metadata = ctx.to_plan_metadata(setup_name="op2_bottom")
setup = metadata["setups"]["op2_bottom"]
check("plan metadata has fixture", metadata["fixture"]["name"] == "soft_jaws", metadata)
check("plan setup face selector", setup["face_selector"] == "<Z", setup)
check("plan setup work offset", setup["work_offset"] == "G56", setup)
check("work offset map emitted", metadata["work_offsets"]["G56"] == [1.0, 2.0, 3.0, 0.0, 0.0, 90.0], metadata)
check("setup carries accessible faces", setup["accessible_faces"] == ["<Z", ">Z"], setup)

print("\n5. Validation rejects invalid setup intent ...")
try:
    load_setup_context({"operation_side": "diagonal"})
    invalid_face_rejected = False
except ValueError:
    invalid_face_rejected = True
check("invalid face is rejected", invalid_face_rejected)

try:
    load_setup_context({"setup_count": 0})
    invalid_count_rejected = False
except ValueError:
    invalid_count_rejected = True
check("invalid setup count is rejected", invalid_count_rejected)

print("\n" + "=" * 60)
print(f"Passed: {passed}")
print(f"Failed: {failed}")
print("=" * 60)

if failed:
    sys.exit(1)
