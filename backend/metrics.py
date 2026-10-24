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
        chunk.supports = best >= HIT_COVERAGE


def retrieval_metrics(evidence: list[EvidenceSpan], retrieved: list[RetrievedChunk], k: int) -> dict[str, float | None]:
    """hit@k, context recall/precision (rank-aware) and MRR from span overlap.

    `retrieved` may hold more than k candidates; only the first k count for scoring,
    the rest are used to report where the first supporting chunk was found.
    """
    if not evidence:
        return {"hit_at_k": None, "context_recall": None, "context_precision": None, "mrr": None,
                "first_relevant_rank": None}
    annotate_retrieved(retrieved, evidence)
    top = retrieved[:k]
    ranges = [(c.start_char, c.end_char) for c in top]
    coverages = [span_coverage(span, ranges) for span in evidence]
    recall = sum(coverages) / len(coverages)
    hit = all(c >= HIT_COVERAGE for c in coverages)

    relevant_seen, precision_sum = 0, 0.0
    for i, chunk in enumerate(top, start=1):
        if chunk.coverage > 0:
            relevant_seen += 1
            precision_sum += relevant_seen / i
    precision = precision_sum / relevant_seen if relevant_seen else 0.0
    first = next((c.rank for c in retrieved if c.coverage > 0), None)
    first_in_top = next((c.rank for c in top if c.coverage > 0), None)
    # Smallest k (within the candidate list) at which every evidence span would be covered.
    full_rank = None
    for n in range(1, len(retrieved) + 1):
        window = [(c.start_char, c.end_char) for c in retrieved[:n]]
        if all(span_coverage(span, window) >= HIT_COVERAGE for span in evidence):
            full_rank = n
            break
    return {
        "hit_at_k": 1.0 if hit else 0.0,
        "context_recall": round(recall, 4),
        "context_precision": round(precision, 4),
        "mrr": round(1.0 / first_in_top, 4) if first_in_top else 0.0,
        "first_relevant_rank": float(first) if first else None,
        "full_coverage_rank": float(full_rank) if full_rank else None,
    }


def semantic_similarity(embedder: Embedder | None, a: str, b: str) -> float | None:
    if embedder is None or not a or not b:
        return None
    va, vb = embedder.embed([a, b])
    return max(0.0, min(1.0, cosine(va, vb)))


def answer_correctness(answer: str, reference: str, embedder: Embedder | None) -> float | None:
    if not answer or not reference:
        return None
    if is_abstention(answer):
        return 0.0
    ref_tokens = content_tokens(reference)
    recall = overlap_ratio(ref_tokens, content_tokens(answer)) if ref_tokens else 0.0
    sim = semantic_similarity(embedder, answer, reference)
    score = 0.65 * recall + 0.35 * (sim if sim is not None else recall)
