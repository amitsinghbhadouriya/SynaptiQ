"""Unit tests for multi-hop query decomposition."""

from backend.query_decomposer import QueryDecomposer


def test_query_decomposer_splitting():
    decomposer = QueryDecomposer()
    subs = decomposer.decompose("What is FastAPI and also how does Uvicorn work?")
    assert len(subs) == 2
    assert "FastAPI" in subs[0]
    assert "Uvicorn" in subs[1]


def test_query_decomposer_single_question():
    decomposer = QueryDecomposer()
    subs = decomposer.decompose("What is RAG?")
    assert len(subs) == 1
