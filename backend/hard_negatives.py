"""Hard-negative context miner identifying deceptively similar unsupportive passages."""

from __future__ import annotations

from typing import List, Dict


class HardNegativeMiner:
    @staticmethod
    def find_hard_negatives(target_chunk_id: str, candidates: List[Dict[str, str]]) -> List[str]:
        """Returns chunk IDs of top candidates that do not equal target_chunk_id."""
        return [c["id"] for c in candidates if c["id"] != target_chunk_id][:2]
