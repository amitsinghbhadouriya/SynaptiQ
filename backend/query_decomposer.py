"""Query decomposition engine splitting complex multi-hop queries into sub-questions."""

from __future__ import annotations

import re
from typing import List


class QueryDecomposer:
    """Splits multi-faceted questions into atomic sub-queries for focused retrieval."""

    def decompose(self, query: str) -> List[str]:
        q = query.strip()
        if not q:
            return []

        # Split on coordinating conjunctions and transition words
        sub_queries = re.split(r"\s+(?:and also|as well as|compared to|versus|vs\.?)\s+", q, flags=re.IGNORECASE)
        cleaned = [s.strip(" ?,.;") for s in sub_queries if len(s.strip()) > 5]

        return cleaned if len(cleaned) > 1 else [q]
