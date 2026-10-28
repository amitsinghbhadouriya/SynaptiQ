"""Hybrid Retriever orchestrating dense embeddings and BM25 lexical search."""

from __future__ import annotations

from typing import List, Dict, Any
from .retrieval_schemas import HybridSearchConfig, ScoredPassage
from .rrf import reciprocal_rank_fusion


class HybridRetriever:
    """Combines dense vector retrieval with BM25 sparse keyword search."""

    def __init__(self, config: HybridSearchConfig | None = None):
        self.config = config or HybridSearchConfig()

    def fuse(
        self,
        dense_results: List[Dict[str, Any]],
        sparse_results: List[Dict[str, Any]]
    ) -> List[ScoredPassage]:
        """Fuses dense and sparse candidate passages using Reciprocal Rank Fusion."""
        dense_ids = [r["id"] for r in dense_results]
        sparse_ids = [r["id"] for r in sparse_results]

        passage_lookup = {}
        for r in dense_results:
            passage_lookup[r["id"]] = r
        for r in sparse_results:
            if r["id"] not in passage_lookup:
                passage_lookup[r["id"]] = r

        fused = reciprocal_rank_fusion(
            dense_ids,
            sparse_ids,
            k=self.config.rrf_k,
            dense_weight=self.config.dense_weight,
            sparse_weight=self.config.sparse_weight
        )

        out: List[ScoredPassage] = []
        for chunk_id, score in fused[:self.config.top_k]:
            data = passage_lookup[chunk_id]
            out.append(ScoredPassage(
                chunk_id=chunk_id,
                text=data.get("text", ""),
                metadata=data.get("metadata", {}),
                fused_score=score
            ))
        return out
