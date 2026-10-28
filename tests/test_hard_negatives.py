"""Unit tests for hard-negative mining."""

from backend.hard_negatives import HardNegativeMiner


def test_find_hard_negatives():
    cands = [{"id": "c1"}, {"id": "c2"}, {"id": "c3"}]
    negs = HardNegativeMiner.find_hard_negatives("c1", cands)
    assert "c1" not in negs
    assert "c2" in negs
