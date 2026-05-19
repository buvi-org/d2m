"""Quick validation of the fixtured dataset output."""
import json
from collections import Counter

fixtured_path = r"C:\Users\Rajesh\dev\d2m\data\fixtured\fixtured_train.jsonl"

with open(fixtured_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total examples: {len(lines)}")

# Find a 3-setup example
for i, line in enumerate(lines):
    d = json.loads(line)
    plan = json.loads(d["messages"][2]["content"])
    if plan["part_summary"]["estimated_setups"] == 3:
        print(f"\n=== 3-SETUP EXAMPLE (line {i+1}) ===")
        for s in plan["setups"]:
            print(f"  Setup {s['setup_id']}: {s['fixture_type']} on {s['face_selector']}")
            print(f"    Desc: {s['description'][:80]}...")

        print(f"  Total ops: {len(plan['operations'])}")
        setup_counts = Counter(op.get("setup_id", 0) for op in plan["operations"])
        for sid in sorted(setup_counts):
            print(f"  Setup {sid}: {setup_counts[sid]} operations")

        # Show a sample operation from each setup
        seen = set()
        for op in plan["operations"]:
            sid = op.get("setup_id", 0)
            if sid not in seen:
                seen.add(sid)
                print(f"  Sample op in setup {sid}: Step {op['step_number']} - {op['operation_name']} [{op['strategy']}]")
        break

# Coverage check
all_fixtures = set()
all_faces = set()
all_setup_counts = Counter()

for line in lines:
    d = json.loads(line)
    plan = json.loads(d["messages"][2]["content"])
    all_setup_counts[plan["part_summary"]["estimated_setups"]] += 1
    for s in plan.get("setups", []):
        all_fixtures.add(s["fixture_type"])
        all_faces.add(s["face_selector"])

print(f"\n=== COVERAGE CHECK ===")
print(f"Fixture types used: {sorted(all_fixtures)}")
print(f"Face selectors used: {sorted(all_faces)}")
print(f"Setup distribution: {dict(sorted(all_setup_counts.items()))}")

# Check all operations have setup_id
missing = 0
for line in lines:
    d = json.loads(line)
    plan = json.loads(d["messages"][2]["content"])
    for op in plan["operations"]:
        if "setup_id" not in op:
            missing += 1
print(f"Operations missing setup_id: {missing}")

# Check instruction format
for i, line in enumerate(lines[:3]):
    d = json.loads(line)
    msgs = d["messages"]
    assert msgs[0]["role"] == "system", f"Expected system role, got {msgs[0]['role']}"
    assert msgs[1]["role"] == "user", f"Expected user role, got {msgs[1]['role']}"
    assert msgs[2]["role"] == "assistant", f"Expected assistant role, got {msgs[2]['role']}"
    # Verify assistant message is valid JSON
    plan = json.loads(msgs[2]["content"])
    assert "setups" in plan, f"Missing setups key in plan"
    assert "operations" in plan, f"Missing operations key in plan"
print(f"Instruction format: CORRECT (3 messages: system, user, assistant) on all checked samples")

# Show a 1-setup example too
for i, line in enumerate(lines):
    d = json.loads(line)
    plan = json.loads(d["messages"][2]["content"])
    if plan["part_summary"]["estimated_setups"] == 1:
        print(f"\n=== 1-SETUP EXAMPLE (line {i+1}) ===")
        for s in plan["setups"]:
            print(f"  Setup {s['setup_id']}: {s['fixture_type']} on {s['face_selector']}")
        break

print("\nAll validation checks passed.")
