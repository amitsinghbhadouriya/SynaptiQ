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
    if not sections:
        from .schemas import SectionSpan

        sections = [SectionSpan(0, len(text))]

    for section in sections:
        sentences: list[Sentence] = []
        for sentence in split_sentences(text[section.start : section.end], offset=section.start):
            sentences.extend(_hard_split(sentence, chunk_size) if len(sentence.text) > chunk_size else [sentence])

        window: list[Sentence] = []
        for sentence in sentences:
            if window and sentence.end - window[0].start > chunk_size:
                chunks.append(_make_chunk(document, text, window, len(chunks), index_key, section))
                # Carry trailing sentences forward as overlap.
                carry: list[Sentence] = []
                for previous in reversed(window):
                    if window[-1].end - previous.start > chunk_overlap:
                        break
                    carry.insert(0, previous)
                window = carry if carry and sentence.end - carry[0].start <= chunk_size else []
            window.append(sentence)
        if window:
            chunks.append(_make_chunk(document, text, window, len(chunks), index_key, section))
    return chunks


def _make_chunk(document: Document, text: str, window: list[Sentence], index: int, index_key: str, section) -> Chunk:
    start, end = window[0].start, window[-1].end
    return Chunk(
        chunk_id=f"{document.document_id}-{index_key}-{index:04d}",
        document_id=document.document_id,
        chunk_index=index,
        text=text[start:end],
        start_char=start,
        end_char=end,
        index_key=index_key,
        page_number=section.page_number,
        metadata={"section": section.label or "", "filename": document.filename},
    )
