"""LLM token pricing estimator for evaluation runs."""

from __future__ import annotations

from typing import Dict

# Pricing per 1,000 tokens (input, output) in USD
PRICING_TABLE = {
    "gpt-4o-mini": (0.00015, 0.00060),
    "gemini-1.5-flash": (0.000075, 0.00030),
    "claude-3-haiku": (0.00025, 0.00125),
}


def estimate_run_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    rates = PRICING_TABLE.get(model, (0.0002, 0.0008))
    cost = (input_tokens / 1000.0) * rates[0] + (output_tokens / 1000.0) * rates[1]
    return round(cost, 6)
