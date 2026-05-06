"""Utilities for converting manufacturing process plan data into
instruction-following training format for fine-tuning.

Supports the standard conversational format used by OpenAI fine-tuning,
DeepSeek fine-tuning, Llama chat templates, and similar instruction-tuned
models:

    {
        "messages": [
            {"role": "system", "content": "<system prompt>"},
            {"role": "user", "content": "<features + specs>"},
            {"role": "assistant", "content": "<JSON process plan>"}
        ]
    }

Also provides batch conversion from directories of feature/plan JSON pairs.
"""

from __future__ import annotations

import os
import json
import logging
from pathlib import Path
from typing import Optional

from .prompts import SYSTEM_PROMPT, PLAN_GENERATION_TEMPLATE, format_features_for_prompt

logger = logging.getLogger(__name__)


# =========================================================================
#   Single-sample conversion
# =========================================================================

def convert_to_instruction_format(
    features_json: str,
    plan_json: str,
    include_system: bool = True,
    custom_system_prompt: Optional[str] = None,
) -> dict:
    """Convert a feature specification and its corresponding process plan
    into the instruction-following format for fine-tuning.

    The feature specification should be a JSON string describing the part:
        {
            "material": "Aluminum 6061-T6",
            "volume": 500,
            "dimensions": {"x": 150, "y": 100, "z": 50},
            "tolerances": "+/-0.05mm",
            "features": [
                {
                    "feature_id": "F001",
                    "type": "pocket",
                    "dimensions": {"width": 50, "depth": 15},
                    ...
                }
            ]
        }

    The plan should be a JSON string with the process plan (as produced by
    ProcessPlanner.generate_plan or authored by an expert).

    Args:
        features_json:      JSON string of feature specification.
        plan_json:          JSON string of the corresponding process plan.
        include_system:     Include the system prompt message (default True).
        custom_system_prompt: Override the default system prompt if provided.

    Returns:
        Dict with 'messages' key containing the conversation in
        instruction-following format. Suitable for JSONL output.

    Raises:
        json.JSONDecodeError: If either input string is not valid JSON.
        ValueError:           If the features JSON is missing required fields.
    """
    # Parse inputs
    try:
        features_data = json.loads(features_json)
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"features_json is not valid JSON: {e}", features_json, 0,
        ) from e

    try:
        plan_data = json.loads(plan_json)
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"plan_json is not valid JSON: {e}", plan_json, 0,
        ) from e

    # Validate features data
    required = {"material", "features"}
    missing = required - set(features_data.keys())
    if missing:
        raise ValueError(
            f"features_json missing required fields: {missing}. "
            f"Required: material, features"
        )

    # Extract fields
    material = features_data["material"]
    volume = features_data.get("volume", 100)
    dimensions = features_data.get("dimensions", {"x": 100, "y": 100, "z": 50})
    tolerances = features_data.get("tolerances", "\u00b10.1mm")
    features = features_data["features"]

    # Build the user prompt
    user_prompt = _build_user_prompt_from_spec(
        features=features,
        material=material,
        volume=volume,
        dimensions=dimensions,
        tolerances=tolerances,
    )

    # Build the message list
    messages: list[dict] = []

    if include_system:
        system_text = custom_system_prompt if custom_system_prompt else SYSTEM_PROMPT
        messages.append({"role": "system", "content": system_text})

    messages.append({"role": "user", "content": user_prompt})

    # Re-serialize the plan to ensure consistent formatting
    assistant_content = json.dumps(plan_data, indent=2, ensure_ascii=False)
    messages.append({"role": "assistant", "content": assistant_content})

    return {"messages": messages}


def _build_user_prompt_from_spec(
    features: list[dict],
    material: str,
    volume: int = 100,
    dimensions: Optional[dict] = None,
    tolerances: str = "\u00b10.1mm",
) -> str:
    """Build the user-facing prompt from a structured feature specification.

    Internal helper used by convert_to_instruction_format.

    Args:
        features:   List of feature dictionaries.
        material:   Material name.
        volume:     Production volume.
        dimensions: Part dimensions dict.
        tolerances: Tolerance string.

    Returns:
        Formatted prompt string.
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
#   Batch conversion
# =========================================================================

def batch_convert(
    input_dir: str,
    output_file: str,
    include_system: bool = True,
    overwrite: bool = False,
) -> int:
    """Process a directory of feature/plan JSON pairs and convert them
    to a JSONL file in instruction-following format.

    The input directory should contain files organized as follows:

        input_dir/
            part_001/
                features.json   # Feature specification
                plan.json       # Expert plan (or model-generated)
            part_002/
                features.json
                plan.json
            ...

    Or as flat files with naming convention:

        input_dir/
            part_001_features.json
            part_001_plan.json
            part_002_features.json
            part_002_plan.json
            ...

    Each pair is converted to a single JSONL line.

    Args:
        input_dir:      Directory containing feature/plan pairs.
        output_file:    Path to output JSONL file.
        include_system: Include the system prompt message in each sample.
        overwrite:      If True, overwrite the output file if it exists.

    Returns:
        Number of samples written.

    Raises:
        FileExistsError: If output_file exists and overwrite is False.
        FileNotFoundError: If input_dir does not exist.
    """
    input_path = Path(input_dir)
    if not input_path.exists():
        raise FileNotFoundError(f"Input directory not found: {input_dir}")
    if not input_path.is_dir():
        raise NotADirectoryError(f"Not a directory: {input_dir}")

    output_path = Path(output_file)
    if output_path.exists() and not overwrite:
        raise FileExistsError(
            f"Output file exists: {output_file}. Use overwrite=True to replace."
        )

    # Discover feature/plan pairs
    pairs = _discover_pairs(input_path)
    logger.info("Found %d feature/plan pair(s) in %s", len(pairs), input_dir)

    if not pairs:
        logger.warning("No feature/plan pairs found in %s", input_dir)
        return 0

    # Convert each pair and write JSONL
    output_path.parent.mkdir(parents=True, exist_ok=True)
    samples_written = 0
    errors: list[tuple[str, str]] = []

    with open(output_path, "w", encoding="utf-8") as f:
        for name, (features_path, plan_path) in sorted(pairs.items()):
            try:
                features_text = features_path.read_text(encoding="utf-8")
                plan_text = plan_path.read_text(encoding="utf-8")

                sample = convert_to_instruction_format(
                    features_json=features_text,
                    plan_json=plan_text,
                    include_system=include_system,
                )

                f.write(json.dumps(sample, ensure_ascii=False) + "\n")
                samples_written += 1
                logger.debug("  Converted: %s", name)

            except (json.JSONDecodeError, ValueError, OSError) as e:
                logger.error("  Failed: %s — %s", name, e)
                errors.append((name, str(e)))
                continue

    if errors:
        logger.warning(
            "%d/%d pair(s) failed conversion: %s",
            len(errors), len(pairs),
            ", ".join(name for name, _ in errors),
        )

    logger.info(
        "Wrote %d samples to %s", samples_written, output_file,
    )
    return samples_written


def _discover_pairs(input_path: Path) -> dict[str, tuple[Path, Path]]:
    """Discover feature/plan JSON file pairs in a directory.

    Supports two layouts:
      1. Subdirectories: part_XXX/features.json + plan.json
      2. Flat files:     part_XXX_features.json + part_XXX_plan.json

    Args:
        input_path: Path to the input directory.

    Returns:
        Dict mapping a logical pair name to (features_path, plan_path).
    """
    pairs: dict[str, tuple[Path, Path]] = {}

    # Layout 1: Subdirectories with features.json and plan.json
    for subdir in sorted(input_path.iterdir()):
        if not subdir.is_dir():
            continue

        features_file = subdir / "features.json"
        plan_file = subdir / "plan.json"

        if features_file.exists() and plan_file.exists():
            pairs[subdir.name] = (features_file, plan_file)

    # Layout 2: Flat files with naming convention
    features_files: dict[str, Path] = {}
    plan_files: dict[str, Path] = {}

    for file in sorted(input_path.iterdir()):
        if not file.is_file() or not file.suffix == ".json":
            continue

        stem = file.stem  # filename without .json
        if stem.endswith("_features"):
            base = stem[:-len("_features")]
            features_files[base] = file
        elif stem.endswith("_plan"):
            base = stem[:-len("_plan")]
            plan_files[base] = file

    # Match flat-file pairs
    for base, f_path in features_files.items():
        if base in plan_files and base not in pairs:
            pairs[base] = (f_path, plan_files[base])

    return pairs


# =========================================================================
#   Self-test
# =========================================================================

if __name__ == "__main__":
    print("=== Dataset Conversion Self-Test ===\n")

    import tempfile

    # ------------------------------------------------------------------
    # 1. convert_to_instruction_format: basic roundtrip
    # ------------------------------------------------------------------
    print("1. convert_to_instruction_format: basic ...")
    features_obj = {
        "material": "Aluminum 6061-T6",
        "volume": 500,
        "dimensions": {"x": 150, "y": 100, "z": 50},
        "tolerances": "+/-0.05mm critical, +/-0.1mm general",
        "features": [
            {
                "feature_id": "F001",
                "type": "pocket",
                "dimensions": {"width": 80, "depth": 12},
                "location": "top face, centered",
                "tolerance": "+/-0.05mm",
            },
            {
                "feature_id": "F002",
                "type": "hole",
                "dimensions": "dia 8 x 20 deep",
                "location": "top face, at (30, 30)",
                "tolerance": "H7",
            },
        ],
    }
    plan_obj = {
        "part_summary": {
            "material": "Aluminum 6061-T6",
            "overall_size_mm": [150, 100, 50],
            "feature_count": 2,
            "complexity_level": "simple",
            "estimated_setups": 1,
        },
        "operations": [
            {
                "step_number": 1,
                "operation_name": "Rough Pocket F001",
                "tool": {"type": "flat_endmill", "diameter_mm": 12.0},
                "cutting_parameters": {
                    "rpm": 10000,
                    "feed_rate_mm_per_min": 1500.0,
                    "depth_of_cut_mm": 3.0,
                    "stepover_mm": 4.0,
                },
                "strategy": "adaptive",
            },
            {
                "step_number": 2,
                "operation_name": "Drill F002",
                "tool": {"type": "drill", "diameter_mm": 8.0},
                "cutting_parameters": {
                    "rpm": 3000,
                    "feed_rate_mm_per_min": 200.0,
                    "depth_of_cut_mm": 4.0,
                },
                "strategy": "peck_drill",
            },
        ],
        "total_estimated_time_minutes": 12.5,
        "dfm_notes": [],
        "alternative_approaches": [],
    }

    sample = convert_to_instruction_format(
        features_json=json.dumps(features_obj),
        plan_json=json.dumps(plan_obj),
    )

    assert "messages" in sample
    assert len(sample["messages"]) == 3  # system, user, assistant
    assert sample["messages"][0]["role"] == "system"
    assert sample["messages"][1]["role"] == "user"
    assert sample["messages"][2]["role"] == "assistant"

    # Assistant message should contain the plan
    assistant_content = json.loads(sample["messages"][2]["content"])
    assert "operations" in assistant_content
    print(f"   Messages: {len(sample['messages'])} (system, user, assistant)")
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 2. convert_to_instruction_format: without system prompt
    # ------------------------------------------------------------------
    print("2. convert_to_instruction_format: no system prompt ...")
    sample_no_sys = convert_to_instruction_format(
        features_json=json.dumps(features_obj),
        plan_json=json.dumps(plan_obj),
        include_system=False,
    )
    assert len(sample_no_sys["messages"]) == 2  # user, assistant
    assert sample_no_sys["messages"][0]["role"] == "user"
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 3. convert_to_instruction_format: custom system prompt
    # ------------------------------------------------------------------
    print("3. convert_to_instruction_format: custom system prompt ...")
    custom_sys = "You are an expert CNC programmer."
    sample_custom = convert_to_instruction_format(
        features_json=json.dumps(features_obj),
        plan_json=json.dumps(plan_obj),
        custom_system_prompt=custom_sys,
    )
    assert sample_custom["messages"][0]["content"] == custom_sys
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 4. convert_to_instruction_format: invalid JSON
    # ------------------------------------------------------------------
    print("4. convert_to_instruction_format: invalid features JSON ...")
    try:
        convert_to_instruction_format(
            features_json="not json",
            plan_json=json.dumps(plan_obj),
        )
        assert False, "Should have raised JSONDecodeError"
    except json.JSONDecodeError:
        print("   Caught expected JSONDecodeError")
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 5. convert_to_instruction_format: missing required fields
    # ------------------------------------------------------------------
    print("5. convert_to_instruction_format: missing fields ...")
    bad_features = json.dumps({"volume": 100})  # missing material, features
    try:
        convert_to_instruction_format(
            features_json=bad_features,
            plan_json=json.dumps(plan_obj),
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "material" in str(e), f"Wrong message: {e}"
        print(f"   Caught expected ValueError: {e}")
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 6. batch_convert: subdirectory layout
    # ------------------------------------------------------------------
    print("6. batch_convert: subdirectory layout ...")
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create subdirectory structure
        for i in range(1, 4):
            part_dir = Path(tmpdir) / f"part_{i:03d}"
            part_dir.mkdir(parents=True)

            feat = {
                "material": "Aluminum 6061-T6",
                "volume": 100 * i,
                "dimensions": {"x": 100, "y": 80, "z": 40},
                "tolerances": "+/-0.1mm",
                "features": [
                    {
                        "feature_id": f"F{i}",
                        "type": "pocket",
                        "dimensions": f"width {10*i} x depth {5*i}",
                    }
                ],
            }
            plan = {
                "operations": [
                    {
                        "step_number": 1,
                        "operation_name": f"Rough Part {i}",
                        "tool": {"type": "flat_endmill", "diameter_mm": 10.0},
                        "cutting_parameters": {
                            "rpm": 8000,
                            "feed_rate_mm_per_min": 1000.0,
                            "depth_of_cut_mm": 2.0,
                        },
                        "strategy": "adaptive",
                    }
                ],
                "total_estimated_time_minutes": 5.0 * i,
            }

            (part_dir / "features.json").write_text(json.dumps(feat, indent=2))
            (part_dir / "plan.json").write_text(json.dumps(plan, indent=2))

        output_file = Path(tmpdir) / "output.jsonl"
        count = batch_convert(
            input_dir=tmpdir,
            output_file=str(output_file),
            overwrite=False,
        )
        assert count == 3, f"Expected 3 samples, got {count}"
        assert output_file.exists()

        # Verify the JSONL format: each line is valid JSON with "messages" key
        lines = output_file.read_text(encoding="utf-8").strip().split("\n")
        assert len(lines) == 3
        for i, line in enumerate(lines):
            parsed = json.loads(line)
            assert "messages" in parsed
            assert len(parsed["messages"]) == 3
            assert parsed["messages"][0]["role"] == "system"
            assert parsed["messages"][1]["role"] == "user"
            assert parsed["messages"][2]["role"] == "assistant"

        print(f"   Converted {count} samples to {output_file}")
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 7. batch_convert: flat file layout
    # ------------------------------------------------------------------
    print("7. batch_convert: flat file layout ...")
    with tempfile.TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)
        for i in range(1, 3):
            feat = {
                "material": "Titanium Ti-6Al-4V",
                "volume": 50,
                "dimensions": {"x": 60, "y": 40, "z": 20},
                "tolerances": "+/-0.02mm",
                "features": [
                    {"feature_id": f"F{i}", "type": "slot", "dimensions": "width 6 x depth 3"}
                ],
            }
            plan = {
                "operations": [],
                "total_estimated_time_minutes": 3.0,
            }

            (base / f"bracket_{i}_features.json").write_text(json.dumps(feat))
            (base / f"bracket_{i}_plan.json").write_text(json.dumps(plan))

        output_file = str(base / "flat_output.jsonl")
        count = batch_convert(
            input_dir=tmpdir,
            output_file=output_file,
            overwrite=False,
        )
        assert count == 2, f"Expected 2 samples, got {count}"
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 8. batch_convert: empty directory
    # ------------------------------------------------------------------
    print("8. batch_convert: empty directory ...")
    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = str(Path(tmpdir) / "empty.jsonl")
        count = batch_convert(
            input_dir=tmpdir,
            output_file=output_file,
            overwrite=False,
        )
        assert count == 0, f"Expected 0, got {count}"
        assert not Path(output_file).exists()  # No file written
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 9. batch_convert: overwrite protection
    # ------------------------------------------------------------------
    print("9. batch_convert: overwrite protection ...")
    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = Path(tmpdir) / "existing.jsonl"
        output_file.write_text("existing content")

        try:
            batch_convert(
                input_dir=tmpdir,
                output_file=str(output_file),
                overwrite=False,
            )
            assert False, "Should have raised FileExistsError"
        except FileExistsError as e:
            assert "exist" in str(e).lower()
            print(f"   Caught expected FileExistsError: {e}")
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 10. batch_convert: non-existent input directory
    # ------------------------------------------------------------------
    print("10. batch_convert: non-existent input directory ...")
    try:
        batch_convert(
            input_dir="/nonexistent/path/12345",
            output_file="/tmp/output.jsonl",
        )
        assert False, "Should have raised FileNotFoundError"
    except FileNotFoundError as e:
        print(f"   Caught expected FileNotFoundError: {e}")
    print("   PASSED\n")

    # ------------------------------------------------------------------
    # 11. Roundtrip: JSON with Unicode
    # ------------------------------------------------------------------
    print("11. convert_to_instruction_format: Unicode roundtrip ...")
    features_unicode = {
        "material": "Stainless Steel 316L",
        "volume": 200,
        "features": [
            {
                "feature_id": "F\xfc1",
                "type": "chamfer",
                "dimensions": "1mm \u00d7 45\u00b0",
                "tolerance": "\u00b10.01mm",
            }
        ],
    }
    plan_unicode = {
        "operations": [
            {
                "step_number": 1,
                "operation_name": "Finish Chamfer \u00d8",
                "tool": {"type": "chamfer_tool", "diameter_mm": 6.0},
                "cutting_parameters": {
                    "rpm": 5000,
                    "feed_rate_mm_per_min": 300.0,
                    "depth_of_cut_mm": 1.0,
                },
                "strategy": "chamfer",
            }
        ],
        "total_estimated_time_minutes": 2.0,
    }
    sample_uni = convert_to_instruction_format(
        features_json=json.dumps(features_unicode, ensure_ascii=False),
        plan_json=json.dumps(plan_unicode, ensure_ascii=False),
    )
    # Re-serialize to verify no data loss
    reserialized = json.dumps(sample_uni, ensure_ascii=False)
    assert "\u00b1" in reserialized or "\u00b0" in reserialized
    print("   PASSED\n")

    print("=== ALL DATASET TESTS PASSED ===")
