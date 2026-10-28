"""Hypothetical Document Embeddings (HyDE) zero-shot document expansion."""

from __future__ import annotations

import re


class HyDEExpander:
    """Constructs hypothetical ideal documents to bridge the query-document vocabulary gap."""

    def build_hypothetical_prompt(self, question: str) -> str:
        return (
            "Please write a short, informative passage that thoroughly answers the following question:\n"
            f"Question: {question}\n\n"
            "Passage:"
        )

    def extract_search_terms(self, hypothetical_doc: str) -> list[str]:
        tokens = re.findall(r"[A-Za-z0-9_-]{4,}", hypothetical_doc.lower())
        return list(dict.fromkeys(tokens))[:20]
