"""Precise latency phase context manager for multi-stage execution."""

from __future__ import annotations

import time
from typing import Dict


class LatencyTracker:
    def __init__(self):
        self.phases: Dict[str, float] = {}

    def track(self, phase_name: str):
        class _PhaseContext:
            def __init__(self, tracker, name):
                self.tracker = tracker
                self.name = name

            def __enter__(self):
                self.start = time.perf_counter()
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                duration_ms = (time.perf_counter() - self.start) * 1000.0
                self.tracker.phases[self.name] = round(duration_ms, 2)

        return _PhaseContext(self, phase_name)
