"""Unit tests for token cost estimation."""

from backend.cost_estimator import estimate_run_cost


def test_estimate_run_cost():
    cost = estimate_run_cost("gpt-4o-mini", 1000, 500)
    assert cost > 0.0001
