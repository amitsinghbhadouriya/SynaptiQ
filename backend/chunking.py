"""Sentence-aware chunking with configurable size/overlap and stable IDs.

Chunks never cross a section boundary (a PDF page or a document heading), carry their
absolute character offsets in the document, and get IDs derived from the document,
the index settings and their position — so the same settings always yield the same IDs.
"""

from __future__ import annotations

from .schemas import Chunk, Document
from .text_utils import Sentence, split_sentences


def _hard_split(sentence: Sentence, size: int) -> list[Sentence]:
    """Break an over-long sentence at whitespace so no chunk exceeds the size limit."""
    pieces: list[Sentence] = []
    text, start = sentence.text, sentence.start
    while len(text) > size:
        cut = text.rfind(" ", 0, size)
        cut = cut if cut > size // 2 else size
        pieces.append(Sentence(text[:cut].strip(), start, start + cut))
        rest = text[cut:]
        lead = len(rest) - len(rest.lstrip())
        start += cut + lead
        text = rest.lstrip()
    if text:
        pieces.append(Sentence(text, start, start + len(text)))
    return pieces


def chunk_document(document: Document, chunk_size: int, chunk_overlap: int, index_key: str) -> list[Chunk]:
    if chunk_size < 50:
        raise ValueError("chunk_size must be at least 50 characters")
    if not 0 <= chunk_overlap < chunk_size:
        raise ValueError("chunk_overlap must be between 0 and chunk_size - 1")

    text = document.text
    chunks: list[Chunk] = []
    sections = document.sections or []
