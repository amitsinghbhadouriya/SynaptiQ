"""Unit tests for latency timer."""

import time
from backend.latency_timer import LatencyTracker


def test_latency_tracker_timing():
    tracker = LatencyTracker()
    with tracker.track("retrieval"):
        time.sleep(0.01)

    assert "retrieval" in tracker.phases
    assert tracker.phases["retrieval"] >= 5.0
