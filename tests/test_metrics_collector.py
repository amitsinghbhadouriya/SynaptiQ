"""Unit tests for in-memory metrics collector."""

from backend.metrics_collector import MetricsCollector


def test_metrics_collector_operations():
    col = MetricsCollector()
    col.increment("requests_total")
    col.record_latency("retrieval_ms", 12.5)

    summary = col.get_summary()
    assert summary["counters"]["requests_total"] == 1
    assert summary["latencies"]["retrieval_ms"]["count"] == 1
