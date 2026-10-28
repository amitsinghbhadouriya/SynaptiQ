"""In-memory metrics collector tracking request counters and latency histograms."""

from __future__ import annotations

import threading
from typing import Dict, List, Any


class MetricsCollector:
    def __init__(self):
        self._counters: Dict[str, int] = {}
        self._latencies: Dict[str, List[float]] = {}
        self._lock = threading.Lock()

    def increment(self, name: str, amount: int = 1) -> None:
        with self._lock:
            self._counters[name] = self._counters.get(name, 0) + amount

    def record_latency(self, name: str, duration_ms: float) -> None:
        with self._lock:
            if name not in self._latencies:
                self._latencies[name] = []
            self._latencies[name].append(duration_ms)

    def get_summary(self) -> Dict[str, Any]:
        with self._lock:
            summary = {"counters": dict(self._counters), "latencies": {}}
            for k, v in self._latencies.items():
                if v:
                    summary["latencies"][k] = {
                        "count": len(v),
                        "avg_ms": round(sum(v) / len(v), 2),
                        "p95_ms": round(sorted(v)[int(len(v) * 0.95)], 2)
                    }
            return summary


metrics_collector = MetricsCollector()
