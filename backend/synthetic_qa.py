"""Synthetic test-set generation, import and evidence location.

Every generated question carries its reference answer and the exact evidence span(s)
in the source document. Generated questions start as "pending" so a human reviews
them before they are trusted as ground truth.

* Offline (default): template questions built from informative sentences, plus
  unanswerable questions about topics the document never mentions.
* Claude (LLM_PROVIDER=anthropic): questions written by the model with a verbatim
  evidence quote, which is then located in the document. Quotes that cannot be found
  are discarded rather than trusted.
"""

from __future__ import annotations

import difflib
import json
import math
import random
import re
from pathlib import Path
from typing import Any

from .chunking import chunk_document
from .schemas import Document, EvalQuestion, EvidenceSpan, new_id
from .text_utils import STOPWORDS, Sentence, content_tokens, numbers_in, split_sentences, tokenize

UNANSWERABLE_TOPICS = [
    "the cryptocurrency investment policy",
    "on-site helicopter landing rules",
    "the budget of the Mars research station",
    "pet insurance for aquarium fish",
    "sponsorship of the 2031 sailing regatta",
    "the procedure for adopting office llamas",
    "underwater welding certification",
    "the company vineyard harvest schedule",
]


def locate_quote(text: str, quote: str) -> tuple[int, int] | None:
    """Find a quote in the document: exact, then whitespace-insensitive, then fuzzy sentence match."""
    quote = (quote or "").strip().strip('"').strip()
    if len(quote) < 8:
        return None
    index = text.find(quote)
    if index >= 0:
        return index, index + len(quote)
    pattern = r"\s+".join(re.escape(part) for part in quote.split())
    match = re.search(pattern, text, flags=re.IGNORECASE)
    if match:
        return match.start(), match.end()
    best, best_ratio = None, 0.0
    for sentence in split_sentences(text):
        ratio = difflib.SequenceMatcher(None, sentence.text.lower(), quote.lower()).ratio()
        if ratio > best_ratio:
            best, best_ratio = sentence, ratio
    if best is not None and best_ratio >= 0.82:
        return best.start, best.end
    return None


def _evidence(document: Document, quotes: list[str]) -> list[EvidenceSpan] | None:
    spans = []
    for quote in quotes:
        located = locate_quote(document.text, quote)
        if located is None:
            return None
        spans.append(EvidenceSpan(located[0], located[1], document.text[located[0] : located[1]]))
    return spans


def supporting_chunk_ids(document: Document, evidence: list[EvidenceSpan], chunk_size: int, overlap: int, index_key: str) -> list[str]:
    """Chunk IDs (for the given settings) that overlap the evidence spans."""
    ids = []
    for chunk in chunk_document(document, chunk_size, overlap, index_key):
