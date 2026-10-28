"""Unit tests for HyDE expansion strategy."""

from backend.hyde import HyDEExpander


def test_hyde_prompt_and_terms():
    hyde = HyDEExpander()
    prompt = hyde.build_hypothetical_prompt("How does backpropagation work?")
    assert "Question: How does backpropagation work?" in prompt

    terms = hyde.extract_search_terms("Neural networks optimize weights through gradient descent")
    assert "neural" in terms
    assert "gradient" in terms
