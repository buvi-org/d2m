"""Self-tests for agentic_translator.py — tests all non-LLM components.

Run:  python test_agentic_translator.py

To test with a real LLM, set DEEPSEEK_API_KEY and run:
  python test_agentic_translator.py --live
"""

import json
import os
import sys
import tempfile

# --- Test helpers ---

passed = 0
failed = 0

def check(cond, label):
    global passed, failed
    if cond:
        passed += 1
        print(f"  PASS  {label}")
    else:
        failed += 1
        print(f"  FAIL  {label}")


# =========================================================================
#  Test 1: Imports
# =========================================================================

print("1. Module imports ...")
from src.data.agentic_translator import (
    AgenticTranslator,
    LLMClient,
    extract_code,
    build_system_prompt,
    build_user_prompt,
    build_iteration_prompt,
    translate_exploration_sample,
    translate_batch,
    SUBCAD_API_REFERENCE,
)

from src.data.subcad_repl import run_subcad, compare_to_reference, format_feedback
from src.data.cadquery_to_subcad import reconstruct_chains, classify_chain, _extract_measures

check(True, "all imports successful")


# =========================================================================
#  Test 2: System prompt
# =========================================================================

print("\n2. System prompt ...")
sys_prompt = build_system_prompt()
check("Stock.rectangular" in sys_prompt, "system prompt mentions Stock.rectangular")
check(".face_mill" in sys_prompt, "system prompt mentions face_mill")
check(".pocket" in sys_prompt, "system prompt mentions pocket")
check(".drill" in sys_prompt, "system prompt mentions drill")
check(".chamfer" in sys_prompt, "system prompt mentions chamfer")
check("part" in sys_prompt, "system prompt mentions 'part' variable")
check(len(sys_prompt) > 500, f"system prompt is substantial ({len(sys_prompt)} chars)")


# =========================================================================
#  Test 3: Code extraction
# =========================================================================

print("\n3. Code extraction ...")

# Fenced code block
response1 = """Here's the subCAD code:

```python
from src.subcad import Stock
part = Stock.rectangular(100, 50, 20).face_mill(1.0)
```
"""
code1 = extract_code(response1)
check(code1 is not None, "extracts fenced python code")
check("Stock.rectangular" in code1, "extracted code has Stock.rectangular")
check("```" not in code1, "extracted code has no fence markers")

# Fenced without language
response2 = """```
from src.subcad import Stock
part = Stock.rectangular(80, 40, 15)
```"""
code2 = extract_code(response2)
check(code2 is not None, "extracts fenced code without language tag")
check("Stock.rectangular" in code2, "extracted code has content")

# Bare code
response3 = """Here is the code:

from src.subcad import Stock
part = Stock.rectangular(100, 50, 20).face_mill(1.0)
)"""
code3 = extract_code(response3)
check(code3 is not None, "extracts bare code")
check("Stock.rectangular" in str(code3), "bare code has Stock.rectangular")

# No code
response4 = "I cannot translate this because..."
code4 = extract_code(response4)
check(code4 is None, "returns None when no code present")


# =========================================================================
#  Test 4: User prompt building
# =========================================================================

print("\n4. User prompt building ...")

# Load sample 1
with open("data/zero_to_cad_exploration/sample_1/ops_trace.json") as f:
    ops_trace = json.load(f)
with open("data/zero_to_cad_exploration/sample_1/cadquery_code.py", "r", encoding="utf-8") as f:
    cq_code = f.read()
step_path = "data/zero_to_cad_exploration/sample_1/model.step"

stock_dims = {"length": 90.0, "width": 40.0, "height": 25.0}
prompt = build_user_prompt(cq_code, ops_trace, step_path, stock_dims)

check("CadQuery" in prompt, "user prompt mentions CadQuery")
check(cq_code[:40] in prompt, "user prompt contains CadQuery code snippet")
check("90" in prompt or "90.0" in prompt, "user prompt includes stock length")
check("part" in prompt, "user prompt mentions 'part' variable")


# =========================================================================
#  Test 5: Iteration prompt building
# =========================================================================

print("\n5. Iteration prompt ...")

prev_code = "from src.subcad import Stock\npart = Stock.rectangular(100,50,20).face_mill(2.0)"
exec_result = {
    "success": True,
    "volume": 12000.0,
    "bbox": {"length": 100, "width": 50, "height": 18},
    "faces": 12,
    "plan": {"operations": [{"operation": "face_mill", "tool_type": "flat_endmill"}]},
}
comparison = {
    "match": False,
    "volume_ratio": 0.75,
    "iou_estimate": 0.75,
}

iter_prompt = build_iteration_prompt(prev_code, exec_result, comparison, 16000.0)
check("Previous Attempt" in iter_prompt, "iteration prompt references previous attempt")
check("too small" in iter_prompt or "0.75" in iter_prompt, "iteration prompt shows mismatch")
check("Stock.rectangular" in iter_prompt, "iteration prompt has API reference")
check(prev_code in iter_prompt, "iteration prompt includes previous code")


# Check if CadQuery is available for REPL-dependent tests
try:
    from src.subcad.geometry import create_rectangular_stock
    _test_shape = create_rectangular_stock(10, 10, 10)
    _HAS_CADQUERY_REPL = True
except Exception:
    _HAS_CADQUERY_REPL = False

# =========================================================================
#  Test 6: REPL integration (run_subcad with valid code)
# =========================================================================

print("\n6. REPL integration ...")

valid_code = """from src.subcad import Stock
part = (Stock.rectangular(100, 50, 20, material="aluminum_6061")
    .face_mill(depth=2.0)
    .drill(diameter=8, cx=30, cy=0, depth=15)
)"""

if _HAS_CADQUERY_REPL:
    result = run_subcad(valid_code)
    check(result["success"], "valid subcad code executes successfully")
    check(result.get("volume", 0) > 0, f"volume > 0 ({result.get('volume', 0):.1f})")
    check(result.get("faces", 0) > 0, f"faces > 0 ({result.get('faces', 0)})")
    check(result.get("step_path") is not None, "STEP file exported")
    check(result.get("stl_path") is not None, "STL file exported")
    check(result.get("process_plan", {}).get("operations"), "process plan has operations")

    _repl_result = result
    _repl_code = valid_code
    # NOTE: do NOT clean up temp files here — test 8 needs them
else:
    print("  SKIP  CadQuery not available — skipping REPL integration tests")
    _repl_result = None
    _repl_code = None


# =========================================================================
#  Test 7: REPL with invalid code (does not need Stock to succeed)
# =========================================================================

print("\n7. REPL error handling ...")

# Missing 'part' variable — code that creates nothing should fail
bad_code = """x = 42\ny = "hello\""""  # no Stock or Workplane at all
result = run_subcad(bad_code)
check(not result["success"], "fails when no 'part' variable")
check(result.get("error") is not None, "error message present")

# Syntax error — always detectable regardless of CadQuery
bad_code2 = """from src.subcad import Stock
part = Stock.rectangular(100, 50, 20
    .face_mill(1.0)"""
result = run_subcad(bad_code2)
check(not result["success"], "fails on syntax error")
check("Syntax" in result.get("error", ""), "error message says Syntax")


# =========================================================================
#  Test 8: compare_to_reference with real files
# =========================================================================

print("\n8. Geometry comparison ...")

if _HAS_CADQUERY_REPL and _repl_result is not None and _repl_result.get("success"):
    subcad_step = _repl_result["step_path"]
    if subcad_step and os.path.exists(subcad_step):
        # Compare to itself — should match (ratio = 1.0)
        comp = compare_to_reference(subcad_step, subcad_step)
        check(comp.get("match"), "self-comparison matches")
        check(abs(comp.get("volume_ratio", 0) - 1.0) < 0.001,
              f"self-comparison volume ratio is ~1.0 (got {comp.get('volume_ratio', 0)})")

        # Compare to a different part (sample_1 STEP)
        sample1_step = "data/zero_to_cad_exploration/sample_1/model.step"
        if os.path.exists(sample1_step):
            comp2 = compare_to_reference(subcad_step, sample1_step)
            # Different parts, so may or may not match — just check no error
            check("error" not in comp2 or comp2.get("error") is None,
                  "cross-part comparison has no error")
            check(isinstance(comp2.get("volume_ratio"), (int, float)),
                  "volume_ratio is numeric")

    # Clean up temp files (deferred from test 6)
    for k in ("step_path", "stl_path"):
        if _repl_result.get(k) and os.path.exists(_repl_result[k]):
            os.unlink(_repl_result[k])
else:
    print("  SKIP  CadQuery not available — skipping geometry comparison")

# =========================================================================
#  Test 9: format_feedback
# =========================================================================

print("\n9. Feedback formatting ...")

# format_feedback takes (code, exec_result, comparison)
comparison = {"match": False, "volume_ratio": 0.85, "target_volume": 5000.0,
              "candidate_volume": 4250.0, "volume_diff": 750.0}
exec_result = {"success": True, "volume": 4250.0, "faces": 42,
               "step_path": "/tmp/test.step", "stl_path": "/tmp/test.stl",
               "process_plan": {"operations": ["face_mill", "pocket", "drill"]}}
feedback = format_feedback(valid_code, exec_result, comparison)
check(len(feedback) > 0, "format_feedback returns non-empty string")
check("[OK]" in feedback or "[FAIL]" in feedback or "MATCH" in feedback or "MISMATCH" in feedback,
      "feedback has status marker (OK/FAIL/MATCH/MISMATCH)")


# =========================================================================
#  Test 10: translate_exploration_sample (import only — requires API key)
# =========================================================================

print("\n10. translate_exploration_sample ...")
check(callable(translate_exploration_sample), "translate_exploration_sample is callable")
check(callable(translate_batch), "translate_batch is callable")


# =========================================================================
#  Summary
# =========================================================================

total = passed + failed
print(f"\n{'='*60}")
print(f"  {'ALL PASSED' if failed == 0 else 'FAILURES PRESENT'}")
print(f"  {passed}/{total} tests passed")
print(f"{'='*60}")

if failed > 0:
    sys.exit(1)
