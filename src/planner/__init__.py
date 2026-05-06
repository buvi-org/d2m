"""
d2m Planner Module - AI-Powered Computer-Aided Process Planning

Uses DeepSeek V4 Pro (OpenAI-compatible chat API) to generate manufacturing
process plans from part geometry features, material specifications, and
tolerance requirements.

Provides:
- Prompt templates for manufacturing process planning
- ProcessPlanner client with retry, JSON parsing, and validation
- Dataset conversion utilities for fine-tuning data preparation

Primary classes for external use:
    ProcessPlanner - DeepSeek API client for plan generation
"""

__version__ = "0.1.0"

from .prompts import (
    SYSTEM_PROMPT,
    PLAN_GENERATION_TEMPLATE,
    FEATURE_ANALYSIS_TEMPLATE,
    format_features_for_prompt,
    build_plan_prompt,
)
from .inference import ProcessPlanner
from .dataset import convert_to_instruction_format, batch_convert
