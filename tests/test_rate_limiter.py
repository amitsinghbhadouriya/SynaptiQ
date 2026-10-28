"""Unit tests for sliding-window rate limiter."""

import time
from backend.rate_limiter import SlidingWindowRateLimiter


def test_rate_limiter_allows_up_to_limit():
    limiter = SlidingWindowRateLimiter(limit=5, window_seconds=1.0)
    for _ in range(5):
        allowed, rem, _ = limiter.is_allowed("client_a")
        assert allowed is True

    # 6th request rejected
    allowed, rem, retry_after = limiter.is_allowed("client_a")
    assert allowed is False
    assert rem == 0
    assert retry_after > 0


def test_rate_limiter_distinct_clients():
    limiter = SlidingWindowRateLimiter(limit=2, window_seconds=1.0)
    assert limiter.is_allowed("c1")[0] is True
    assert limiter.is_allowed("c1")[0] is True
    assert limiter.is_allowed("c1")[0] is False

    # c2 still allowed
    assert limiter.is_allowed("c2")[0] is True
