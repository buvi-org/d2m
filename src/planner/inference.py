"""DeepSeek V4 Pro API client for manufacturing process planning.

Provides the ProcessPlanner class which wraps the OpenAI-compatible
DeepSeek chat completions API with:
- Structured plan generation from part features
- Feature-level analysis and tooling recommendations
- Retry with exponential backoff for transient failures
- JSON parsing with markdown-fence handling
- Response validation
- Token usage logging
"""

from __future__ import annotations

import os
import json
import re
import time
import logging
from typing import Optional, Any

from openai import OpenAI

from .prompts import (
    SYSTEM_PROMPT,
    PLAN_GENERATION_TEMPLATE,
    FEATURE_ANALYSIS_TEMPLATE,
    format_features_for_prompt,
    build_plan_prompt,
)

logger = logging.getLogger(__name__)


# =========================================================================
#   JSON extraction helpers
# =========================================================================

def _extract_json(text: str) -> str:
    """Extract a JSON object from text that may contain markdown fences,
    explanatory prefixes, or trailing commentary.

    Attempts in order:
      1. Strip ```json ... ``` fences.
      2. Strip ``` ... ``` fences.
      3. Find the first '{' and last '}' and return the substring.
      4. Return the original text unchanged.

    Args:
        text: Raw API response text.

    Returns:
        String that should parse as JSON.
    """
    text = text.strip()

    # Pattern 1: ```json ... ```
    fence_pattern = re.compile(r"```json\s*(.*?)\s*```", re.DOTALL)
    match = fence_pattern.search(text)
    if match:
        return match.group(1).strip()

    # Pattern 2: ``` ... ```
    fence_pattern_any = re.compile(r"```\s*(.*?)\s*```", re.DOTALL)
    match = fence_pattern_any.search(text)
    if match:
        return match.group(1).strip()

    # Pattern 3: Find first { to last }
    start = text.find("{")
    end = text.rfind("}")
    if start >= 0 and end > start:
        return text[start:end + 1]

    return text


def _parse_json_safe(text: str) -> dict:
    """Parse extracted JSON text safely.

    Tries the standard json.loads first, then falls back to stripping
    problematic characters (BOM, trailing commas, etc.).

    Args:
        text: Extracted JSON string.

    Returns:
        Parsed dict.

    Raises:
        json.JSONDecodeError: If parsing fails after all attempts.
    """
    errors: list[str] = []
    text = text.strip()

    # Attempt 1: Direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        errors.append(f"direct: {e}")

    # Attempt 2: Remove BOM and common issues
    text_clean = text.lstrip("\ufeff").strip()
    if text_clean != text:
        try:
            return json.loads(text_clean)
        except json.JSONDecodeError as e:
            errors.append(f"cleaned: {e}")

    # Attempt 3: Handle trailing commas before } or ]
    text_no_trailing = re.sub(r",\s*([}\]])", r"\1", text)
    if text_no_trailing != text:
        try:
            return json.loads(text_no_trailing)
        except json.JSONDecodeError as e:
            errors.append(f"no_trailing_commas: {e}")

    raise json.JSONDecodeError(
        f"All JSON parsing attempts failed: {'; '.join(errors)}",
        text, 0,
    )


# =========================================================================
#   Plan structure validation
# =========================================================================

def _validate_plan_structure(plan: dict) -> list[str]:
    """Validate that a parsed plan dict has the expected structure.

    Checks for required top-level keys and validates the operations list.
    Missing or malformed fields are logged as warnings but do not raise
    exceptions — the caller decides how to handle them.

    Args:
        plan: Parsed plan dictionary.

    Returns:
        List of validation warnings (empty if fully valid).
    """
    warnings: list[str] = []

    # Required top-level keys
    required_keys = {"operations", "total_estimated_time_minutes"}
    missing_keys = required_keys - set(plan.keys())
    if missing_keys:
        warnings.append(f"Missing top-level keys: {missing_keys}")

    # Operations must be a list
    ops = plan.get("operations")
    if not isinstance(ops, list):
        warnings.append(f"'operations' must be a list, got {type(ops).__name__}")
        return warnings

    if len(ops) == 0:
        warnings.append("Operations list is empty")

    # Validate each operation
    op_required = {"step_number", "operation_name", "tool", "strategy"}
    for i, op in enumerate(ops):
        if not isinstance(op, dict):
            warnings.append(f"Operation {i} is not a dict (got {type(op).__name__})")
            continue

        op_missing = op_required - set(op.keys())
        if op_missing:
            warnings.append(f"Operation {i} ('{op.get('operation_name', '?')}'): "
                            f"missing keys: {op_missing}")

        # Validate tool sub-dict
        tool = op.get("tool", {})
        if isinstance(tool, dict):
            if "type" not in tool:
                warnings.append(f"Operation {i}: tool missing 'type'")
            if "diameter_mm" not in tool and "diameter" not in tool:
                warnings.append(f"Operation {i}: tool missing 'diameter_mm'")

        # Check cutting_parameters
        cp = op.get("cutting_parameters")
        if isinstance(cp, dict):
            for p in ("rpm", "feed_rate_mm_per_min", "depth_of_cut_mm"):
                if p not in cp:
                    warnings.append(f"Operation {i}: cutting_parameters missing '{p}'")

    # Check dfm_notes if present
    dfm = plan.get("dfm_notes")
    if dfm is not None and not isinstance(dfm, list):
        warnings.append(f"'dfm_notes' must be a list, got {type(dfm).__name__}")

    return warnings


# =========================================================================
#   ProcessPlanner
# =========================================================================

class ProcessPlanner:
    """Client for generating manufacturing process plans via DeepSeek V4 Pro.

    Uses the OpenAI-compatible chat completions API. The base URL defaults
    to https://api.deepseek.com and the API key is read from the
    DEEPSEEK_API_KEY environment variable.

    Usage::

        planner = ProcessPlanner()
        plan = planner.generate_plan(
            features=[{"feature_id": "F1", "type": "pocket", ...}],
            material="Aluminum 6061-T6",
            volume=500,
            dimensions={"x": 150, "y": 100, "z": 50},
        )
        print(plan["operations"][0]["operation_name"])

    Attributes:
        client:   OpenAI client instance pointed at the DeepSeek API.
        model:    Model identifier string (default: "deepseek-chat").
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "deepseek-chat",
        base_url: str = "https://api.deepseek.com",
    ):
        """Initialize the planner client.

        Args:
            api_key: DeepSeek API key. Reads DEEPSEEK_API_KEY env var if None.
            model:   Model identifier (e.g., "deepseek-chat", "deepseek-reasoner").
            base_url: API base URL. Defaults to DeepSeek's endpoint.

        Raises:
            ValueError: If no API key is provided or found in the environment.
        """
        resolved_key = api_key or os.environ.get("DEEPSEEK_API_KEY")
        if not resolved_key:
            raise ValueError(
                "DeepSeek API key not found. Provide api_key argument or set "
                "the DEEPSEEK_API_KEY environment variable."
            )

        self.client = OpenAI(
            api_key=resolved_key,
            base_url=base_url,
            timeout=60.0,
            max_retries=0,  # We handle retries ourselves
        )
        self.model = model
        self._last_usage: Optional[dict] = None

    # -----------------------------------------------------------------
    #   Properties
    # -----------------------------------------------------------------

    @property
    def last_usage(self) -> Optional[dict]:
        """Token usage from the most recent API call.

        Returns:
            Dict with 'prompt_tokens', 'completion_tokens', 'total_tokens',
            or None if no call has been made yet.
        """
        return self._last_usage

    # -----------------------------------------------------------------
    #   Core chat method
    # -----------------------------------------------------------------

    def chat(
        self,
        messages: list[dict],
        temperature: float = 0.3,
        max_tokens: int = 4096,
        max_retries: int = 3,
    ) -> str:
        """Send a chat completion request with retry logic.

        Uses exponential backoff starting at 1 second, doubling each retry.
        Handles rate limiting (429), server errors (5xx), and connection
        errors. Logs token usage on success.

        Args:
            messages:    List of message dicts with 'role' and 'content' keys.
            temperature: Sampling temperature (0.0 to 2.0). Default 0.3 for
                         consistent, reproducible plans.
            max_tokens:  Maximum completion tokens.
            max_retries: Maximum retry attempts for transient failures.

        Returns:
            The assistant's response text.

        Raises:
            RuntimeError: If all retries are exhausted.
            ValueError:   If messages format is invalid.
        """
        if not messages:
            raise ValueError("messages list cannot be empty")

        last_error: Optional[Exception] = None
        backoff = 1.0  # seconds

        for attempt in range(max_retries + 1):
            try:
                logger.debug(
                    "Chat attempt %d/%d: model=%s temp=%.2f max_tokens=%d",
                    attempt + 1, max_retries + 1, self.model, temperature, max_tokens,
                )

                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )

                # Log token usage
                usage = response.usage
                if usage:
                    self._last_usage = {
                        "prompt_tokens": usage.prompt_tokens,
                        "completion_tokens": usage.completion_tokens,
                        "total_tokens": usage.total_tokens,
                    }
                    logger.info(
                        "Tokens: prompt=%d completion=%d total=%d",
                        usage.prompt_tokens,
                        usage.completion_tokens,
                        usage.total_tokens,
                    )

                # Extract content
                choices = response.choices
                if not choices or not choices[0].message.content:
                    raise RuntimeError("API returned empty response")

                return choices[0].message.content

            except Exception as e:
                last_error = e
                error_type = type(e).__name__
                error_str = str(e)

                # Determine if retryable
                is_retryable = (
                    "rate" in error_str.lower()
                    or "429" in error_str
                    or "500" in error_str
                    or "502" in error_str
                    or "503" in error_str
                    or "timeout" in error_str.lower()
                    or "connection" in error_str.lower()
                )

                if attempt < max_retries and is_retryable:
                    logger.warning(
                        "Retryable error on attempt %d/%d (%s): %s. "
                        "Backing off %.1fs",
                        attempt + 1, max_retries + 1, error_type, error_str, backoff,
                    )
                    time.sleep(backoff)
                    backoff *= 2.0
                    continue

                # Non-retryable or exhausted
                if attempt == max_retries:
                    logger.error(
                        "All %d retries exhausted. Last error: %s: %s",
                        max_retries + 1, error_type, error_str,
                    )
                else:
                    logger.error(
                        "Non-retryable error: %s: %s", error_type, error_str,
                    )
                raise

        raise RuntimeError(
            f"Chat failed after {max_retries + 1} attempts. "
            f"Last error: {type(last_error).__name__}: {last_error}"
        )

    # -----------------------------------------------------------------
    #   Plan generation
    # -----------------------------------------------------------------

    def generate_plan(
        self,
        features: list[dict],
        material: str,
        volume: int = 100,
        dimensions: Optional[dict] = None,
        tolerances: str = "\u00b10.1mm",
        temperature: float = 0.3,
        max_tokens: int = 4096,
    ) -> dict:
        """Generate a complete manufacturing process plan from part features
        and material specifications.

        Args:
            features:    List of feature dictionaries with feature_id, type,
                         dimensions, location, tolerance, etc.
            material:    Material name (e.g., "Aluminum 6061-T6").
            volume:      Production volume in units.
            dimensions:  Dict with 'x', 'y', 'z' or 'length', 'width', 'height'
                         keys in mm. Defaults to 100x100x50.
            tolerances:  Tolerance specification string.
            temperature: LLM sampling temperature.
            max_tokens:  Maximum completion tokens.

        Returns:
            Parsed process plan dict with keys: operations,
            total_estimated_time_minutes, dfm_notes, alternative_approaches.

        Raises:
            json.JSONDecodeError: If the API response cannot be parsed as JSON.
            RuntimeError:         If the API call fails after retries.
            ValueError:           If the plan fails structural validation (logged).
        """
        if dimensions is None:
            dimensions = {"x": 100, "y": 100, "z": 50}

        # Build the complete prompt
        prompt = build_plan_prompt(
            features=features,
            material=material,
            volume=volume,
            dimensions=dimensions,
            tolerances=tolerances,
        )

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ]

        logger.info(
            "Generating plan: material=%s features=%d volume=%d",
            material, len(features), volume,
        )

        # Call the API
        response_text = self.chat(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        # Extract and parse JSON
        json_text = _extract_json(response_text)
        try:
            plan = _parse_json_safe(json_text)
        except json.JSONDecodeError as e:
            logger.error("Failed to parse plan JSON: %s", e)
            # Log a snippet of the response for debugging
            snippet = response_text[:500] + "..." if len(response_text) > 500 else response_text
            logger.error("Raw response (truncated): %s", snippet)
            raise

        # Validate structure
        warnings = _validate_plan_structure(plan)
        for w in warnings:
            logger.warning("Plan validation: %s", w)

        # Attach metadata
        plan.setdefault("_metadata", {})
        plan["_metadata"].update({
            "model": self.model,
            "material": material,
            "volume": volume,
            "token_usage": self._last_usage,
        })

        return plan

    # -----------------------------------------------------------------
    #   Feature analysis
    # -----------------------------------------------------------------

    def analyze_features(
        self,
        features: list[dict],
        material: str,
        temperature: float = 0.3,
        max_tokens: int = 3072,
    ) -> dict:
        """Analyze part features and recommend tooling and machining strategies
        without generating a full process plan.

        Useful as a preliminary step to understand feature machinability
        before committing to a full plan generation.

        Args:
            features:    List of feature dictionaries.
            material:    Material name.
            temperature: LLM sampling temperature.
            max_tokens:  Maximum completion tokens.

        Returns:
            Parsed dict with keys: feature_analyses, tool_list,
            sequencing_recommendations, critical_path_features.

        Raises:
            json.JSONDecodeError: If the API response cannot be parsed.
            RuntimeError:         If the API call fails.
        """
        features_text = format_features_for_prompt(features)
        prompt = FEATURE_ANALYSIS_TEMPLATE.format(
            material=material,
            features_text=features_text,
        )

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ]

        logger.info(
            "Analyzing features: material=%s features=%d",
            material, len(features),
        )

        response_text = self.chat(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        json_text = _extract_json(response_text)
        try:
            result = _parse_json_safe(json_text)
        except json.JSONDecodeError as e:
            logger.error("Failed to parse feature analysis JSON: %s", e)
            raise

        result.setdefault("_metadata", {})
        result["_metadata"].update({
            "model": self.model,
            "material": material,
            "token_usage": self._last_usage,
        })

        return result


# =========================================================================
#   Self-test
# =========================================================================

if __name__ == "__main__":
    print("=== ProcessPlanner Self-Test ===\n")

    # Configure logging for tests
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    # ------------------------------------------------------------------
    # 1. JSON extraction: clean JSON
    # ------------------------------------------------------------------
    print("1. _extract_json: clean JSON ...")
    clean = '{"key": "value", "nested": {"a": 1}}'
    result = _extract_json(clean)
    assert result == clean, f"Expected unchanged, got: {result}"
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 2. JSON extraction: markdown-fenced JSON
    # ------------------------------------------------------------------
    print("2. _extract_json: markdown-fenced JSON ...")
    md_fenced = '```json\n{"ops": [1, 2, 3]}\n```'
    result = _extract_json(md_fenced)
    assert result == '{"ops": [1, 2, 3]}', f"Got: {result}"
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 3. JSON extraction: JSON with prefix text
    # ------------------------------------------------------------------
    print("3. _extract_json: text prefix + JSON ...")
    prefixed = 'Here is your plan:\n{"operations": [{"step": 1}]}\nLet me know if you need changes.'
    result = _extract_json(prefixed)
    assert "operations" in result
    assert result.startswith("{") and result.endswith("}")
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 4. JSON extraction: plain markdown fence (no language)
    # ------------------------------------------------------------------
    print("4. _extract_json: plain markdown fence ...")
    plain_fence = '```\n{"x": 1}\n```'
    result = _extract_json(plain_fence)
    assert result == '{"x": 1}', f"Got: {result}"
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 5. _parse_json_safe: valid JSON
    # ------------------------------------------------------------------
    print("5. _parse_json_safe: valid JSON ...")
    parsed = _parse_json_safe('{"a": 1, "b": [2, 3]}')
    assert parsed == {"a": 1, "b": [2, 3]}, f"Got: {parsed}"
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 6. _parse_json_safe: JSON with trailing comma
    # ------------------------------------------------------------------
    print("6. _parse_json_safe: trailing comma ...")
    parsed = _parse_json_safe('{"a": 1, "b": [2, 3,],}')
    assert parsed == {"a": 1, "b": [2, 3]}, f"Got: {parsed}"
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 7. _validate_plan_structure: valid plan
    # ------------------------------------------------------------------
    print("7. _validate_plan_structure: valid plan ...")
    valid_plan = {
        "operations": [
            {
                "step_number": 1,
                "operation_name": "Face Mill Top",
                "tool": {"type": "flat_endmill", "diameter_mm": 50.0},
                "cutting_parameters": {
                    "rpm": 8000,
                    "feed_rate_mm_per_min": 2000.0,
                    "depth_of_cut_mm": 2.0,
                },
                "strategy": "face_mill",
            },
            {
                "step_number": 2,
                "operation_name": "Rough Pocket",
                "tool": {"type": "flat_endmill", "diameter_mm": 12.0},
                "cutting_parameters": {
                    "rpm": 10000,
                    "feed_rate_mm_per_min": 1500.0,
                    "depth_of_cut_mm": 3.0,
                    "stepover_mm": 4.0,
                },
                "strategy": "adaptive",
            },
        ],
        "total_estimated_time_minutes": 45.5,
        "dfm_notes": ["Thin wall section may need support"],
        "alternative_approaches": [],
    }
    warnings = _validate_plan_structure(valid_plan)
    assert len(warnings) == 0, f"Unexpected warnings: {warnings}"
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 8. _validate_plan_structure: invalid (missing fields)
    # ------------------------------------------------------------------
    print("8. _validate_plan_structure: invalid plan ...")
    invalid_plan = {
        "operations": [
            {
                "step_number": 1,
                # missing operation_name, tool, strategy
            },
        ],
        # missing total_estimated_time_minutes
    }
    warnings = _validate_plan_structure(invalid_plan)
    assert len(warnings) > 0, "Expected warnings for invalid plan"
    print(f"   Warnings: {warnings}")
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 9. _validate_plan_structure: empty operations
    # ------------------------------------------------------------------
    print("9. _validate_plan_structure: empty operations ...")
    empty_plan = {
        "operations": [],
        "total_estimated_time_minutes": 0,
    }
    warnings = _validate_plan_structure(empty_plan)
    assert any("empty" in w.lower() for w in warnings), f"Expected empty warning, got: {warnings}"
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 10. ProcessPlanner init error (no API key)
    # ------------------------------------------------------------------
    print("10. ProcessPlanner init error (no API key) ...")
    old_key = os.environ.pop("DEEPSEEK_API_KEY", None)
    try:
        ProcessPlanner()
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "API key" in str(e), f"Wrong error: {e}"
        print(f"   Caught expected error: {e}")
    finally:
        if old_key is not None:
            os.environ["DEEPSEEK_API_KEY"] = old_key
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 11. ProcessPlanner init with explicit key
    # ------------------------------------------------------------------
    print("11. ProcessPlanner init with explicit key ...")
    planner = ProcessPlanner(api_key="sk-test-dummy-key")
    assert planner.model == "deepseek-chat"
    assert planner._last_usage is None
    print(f"   Model: {planner.model}")
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 12. ProcessPlanner init with custom model
    # ------------------------------------------------------------------
    print("12. ProcessPlanner init with custom model ...")
    planner2 = ProcessPlanner(
        api_key="sk-test-custom",
        model="deepseek-reasoner",
    )
    assert planner2.model == "deepseek-reasoner"
    print(f"   Model: {planner2.model}")
    print("   PASSED\n")

    print("=== ALL PROCESS PLANNER TESTS PASSED ===")
