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
        if any(chunk.start_char < e.end and e.start < chunk.end_char for e in evidence):
            ids.append(chunk.chunk_id)
    return ids


# ------------------------------------------------------------------ offline
def _candidates(document: Document) -> list[Sentence]:
    out = []
    for section in document.sections:
        for s in split_sentences(document.text[section.start : section.end], offset=section.start):
            if not 50 <= len(s.text) <= 280 or "?" in s.text or not s.text.endswith((".", "!", ")")):
                continue
            if len(content_tokens(s.text)) < 5:
                continue
            out.append(s)
    return out


_VERB_HINTS = re.compile(
    r"\b(is|are|was|were|must|can|may|will|should|shall|has|have|had|does|do|run|runs|take|takes|cover|covers|"
    r"receive|receives|apply|applies|include|includes|require|requires|offer|offers|allow|allows|describe|describes|"
    r"complete|completes|return|returns|match|matches|renew|renews|need|needs|get|gets|provide|provides)\b",
    re.IGNORECASE,
)
_BAD_SUBJECT_START = ("this ", "these ", "those ", "it ", "they ", "there ", "each ", "every ", "any ", "all ", "the ")


def _subject(sentence: str) -> str | None:
    """Words before the first verb-like token, e.g. 'Hotel stays within the country are …' -> 'hotel stays within the country'."""
    match = _VERB_HINTS.search(sentence)
    if not match:
        return None
    subject = sentence[: match.start()].strip(" ,;:")
    words = subject.split()
    if not 1 <= len(words) <= 7 or any(c in subject for c in "()\"'"):
        return None
    if words[0].lower() in {"if", "when", "for", "during", "outside", "within", "up", "after", "before", "while"}:
        return None
    proper = any(w[:1].isupper() for w in words[1:]) or subject[:2].isupper()
    lowered = subject if proper else subject[0].lower() + subject[1:]
    for prefix in _BAD_SUBJECT_START:
        if lowered.lower().startswith(prefix):
            lowered = lowered[len(prefix):] if prefix in ("the ", "every ", "each ", "all ", "any ") else ""
    return lowered.strip() or None


def _keyphrase(sentence: str, idf: dict[str, float], limit: int = 4) -> str:
    words = [w for w in tokenize(sentence) if w not in STOPWORDS and len(w) > 2 and not any(c.isdigit() for c in w)]
    if not words:
        return "this topic"
    ranked = sorted(set(words), key=lambda w: idf.get(w, 0.0), reverse=True)[:limit]
    ordered, seen = [], set()
    for w in words:
        if w in ranked and w not in seen:
            ordered.append(w)
            seen.add(w)
    return " ".join(ordered)


def generate_offline(document: Document, count: int = 10, seed: int = 7, types: list[str] | None = None) -> list[EvalQuestion]:
    types = types or ["factual", "numerical", "multi_hop", "unanswerable"]
    rng = random.Random(seed)
    candidates = _candidates(document)
    if not candidates:
        return []
    doc_tokens = [set(tokenize(s.text)) for s in candidates]
    df: dict[str, int] = {}
    for tokens in doc_tokens:
        for t in tokens:
            df[t] = df.get(t, 0) + 1
    idf = {t: math.log(len(candidates) / d) for t, d in df.items()}
    vocabulary = set(content_tokens(document.text))

    numeric = [s for s in candidates if numbers_in(s.text)]
    plain = [s for s in candidates if not numbers_in(s.text)] or candidates
    quotas = {
