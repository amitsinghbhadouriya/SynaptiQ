"""Preloads deterministic response fixtures for offline evaluation."""

from __future__ import annotations

from .cli_utils import print_header, print_success

FIXTURES = {
    "What is SynaptiQ?": "SynaptiQ is an advanced RAG and hallucination diagnostic suite.",
    "What is BM25?": "BM25 is a probabilistic lexical ranking algorithm.",
}


def preload():
    print_header("Preloading LLM Evaluation Fixtures")
    print_success(f"Cached {len(FIXTURES)} offline mock responses.")
    return len(FIXTURES)


if __name__ == "__main__":
    preload()
