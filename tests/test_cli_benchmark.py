"""Unit tests for retrieval benchmark CLI."""

from scripts.benchmark_retrieval import run_benchmark


def test_run_benchmark():
    metrics = run_benchmark(num_queries=5)
    assert "avg_latency_ms" in metrics
    assert metrics["avg_latency_ms"] >= 0.0
