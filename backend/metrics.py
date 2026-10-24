"""Evaluation metrics.

Retrieval metrics compare character spans: a question's reference evidence is stored
as (start, end) offsets in the document, and every chunk knows its own offsets. This
keeps retrieval scoring exact and comparable across different chunking settings.

Answer metrics are transparent, documented heuristics (not universal probabilities):

* answer_correctness = 0.65 * reference-token recall + 0.35 * semantic similarity,
  capped at 0.4 when a number from the reference answer is missing from the answer.
* faithfulness = share of answer sentences whose content words are >= 80% present
  in the supplied context (or semantically >= 0.8 similar to a context sentence).
* answer_relevancy = semantic similarity between question and answer.

Missing or not-applicable values are None, never 0.
"""

from __future__ import annotations

from .embeddings import Embedder, cosine
from .schemas import EvidenceSpan, RetrievedChunk
from .text_utils import content_tokens, is_abstention, numbers_in, overlap_ratio, split_sentences

HIT_COVERAGE = 0.5
CORRECTNESS_PASS = 0.6
FAITHFULNESS_PASS = 0.6
SUPPORT_TOKEN_PRECISION = 0.8
SUPPORT_SEMANTIC = 0.8

THRESHOLDS = {
    "hit_coverage": HIT_COVERAGE,
    "correctness_pass": CORRECTNESS_PASS,
    "faithfulness_pass": FAITHFULNESS_PASS,
}


def _covered(start: int, end: int, ranges: list[tuple[int, int]]) -> int:
    """Number of characters in [start, end) covered by the union of ranges."""
    clipped = sorted((max(start, a), min(end, b)) for a, b in ranges if b > start and a < end)
    covered, cursor = 0, start
    for a, b in clipped:
        a = max(a, cursor)
        if b > a:
            covered += b - a
            cursor = b
    return covered


def span_coverage(span: EvidenceSpan, ranges: list[tuple[int, int]]) -> float:
    length = span.end - span.start
    return _covered(span.start, span.end, ranges) / length if length > 0 else 0.0


def annotate_retrieved(retrieved: list[RetrievedChunk], evidence: list[EvidenceSpan]) -> None:
    """Mark each retrieved chunk with how much reference evidence it contains."""
    for chunk in retrieved:
        best = 0.0
        for span in evidence:
            best = max(best, span_coverage(span, [(chunk.start_char, chunk.end_char)]))
        chunk.coverage = round(best, 4)
