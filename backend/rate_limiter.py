"""Sliding-window rate limiter protecting SynaptiQ endpoints against abuse."""

from __future__ import annotations

import time
import threading
from collections import deque
from typing import Dict, Tuple


class SlidingWindowRateLimiter:
    """Tracks client request timestamps within a rolling window."""

    def __init__(self, limit: int = 30, window_seconds: float = 60.0):
        self.limit = limit
        self.window = window_seconds
        self._clients: Dict[str, deque[float]] = {}
        self._lock = threading.Lock()

    def is_allowed(self, client_id: str) -> Tuple[bool, int, float]:
        """Returns (is_allowed, remaining_requests, retry_after_seconds)."""
        now = time.time()
        window_start = now - self.window

        with self._lock:
            if client_id not in self._clients:
                self._clients[client_id] = deque()

            q = self._clients[client_id]
            while q and q[0] <= window_start:
                q.popleft()

            if len(q) < self.limit:
                q.append(now)
                remaining = self.limit - len(q)
                return True, remaining, 0.0

            oldest = q[0]
            retry_after = max(0.1, (oldest + self.window) - now)
            return False, 0, retry_after

    def reset(self, client_id: str | None = None) -> None:
        """Reset counters for a single client or all clients."""
        with self._lock:
            if client_id:
                self._clients.pop(client_id, None)
            else:
                self._clients.clear()


default_rate_limiter = SlidingWindowRateLimiter(limit=30, window_seconds=60.0)
