"""Unit tests for retrieval LRU cache."""

from backend.retrieval_cache import RetrievalLRUCache


def test_cache_hits_and_eviction():
    cache = RetrievalLRUCache(capacity=2)
    cache.put("k1", "val1")
    cache.put("k2", "val2")

    assert cache.get("k1") == "val1"
    assert cache.hits == 1

    cache.put("k3", "val3")  # Evicts k2 because k1 was accessed
    assert cache.get("k2") is None
    assert cache.misses == 1
