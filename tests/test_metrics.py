import pytest

from backend import ragas_adapter
from backend.embeddings import HashingEmbedder
from backend.metrics import answer_correctness, faithfulness, generation_metrics, mean, span_coverage
from backend.schemas import EvidenceSpan
from backend.text_utils import ABSTAIN_ANSWER, is_abstention, token_f1

EMB = HashingEmbedder()
REFERENCE = "Full-time employees receive 24 days of paid annual leave per calendar year."
CONTEXT = [REFERENCE + " Remaining days expire on 31 March."]


def test_span_coverage_union():
    span = EvidenceSpan(100, 200, "x")
    assert span_coverage(span, [(100, 150), (140, 200)]) == pytest.approx(1.0)
    assert span_coverage(span, [(0, 50)]) == 0.0
    assert span_coverage(span, [(150, 400)]) == pytest.approx(0.5)


def test_correctness_rewards_reference_facts():
    good = answer_correctness("Full-time staff get 24 days of paid annual leave each year.", REFERENCE, EMB)
    wrong_number = answer_correctness("Full-time staff get 20 days of paid annual leave each year.", REFERENCE, EMB)
    assert good >= 0.6
    assert wrong_number <= 0.4  # a missing reference number caps the score


def test_abstention_scores_zero_correctness():
    assert answer_correctness(ABSTAIN_ANSWER, REFERENCE, EMB) == 0.0
    assert is_abstention("The document does not mention this.")
    assert not is_abstention("Employees receive 24 days.")


def test_faithfulness_detects_unsupported_claims():
    assert faithfulness(REFERENCE, CONTEXT, EMB) == 1.0
    mixed = faithfulness(REFERENCE + " Interns also receive a free company car and gym membership.", CONTEXT, EMB)
    assert mixed == 0.5
    assert faithfulness(ABSTAIN_ANSWER, CONTEXT, EMB) is None  # not applicable, not zero


def test_generation_metrics_for_unanswerable_question():
    metrics, passed = generation_metrics("Crypto salaries?", ABSTAIN_ANSWER, "n/a", CONTEXT, answerable=False, embedder=EMB)
    assert passed is True and metrics["abstention_correct"] == 1.0 and metrics["answer_correctness"] is None
    metrics, passed = generation_metrics("Crypto salaries?", REFERENCE, "n/a", CONTEXT, answerable=False, embedder=EMB)
    assert passed is False and metrics["abstention_correct"] == 0.0


def test_mean_ignores_missing_values():
    assert mean([1.0, None, 0.0]) == 0.5
    assert mean([None, None]) is None


def test_token_f1():
    assert token_f1("24 days of leave", "24 days of leave") == 1.0
    assert token_f1("bananas", "24 days of leave") == 0.0


def test_ragas_metrics_when_installed():
    if not ragas_adapter.status()["available"]:
        pytest.skip("ragas not installed")
    assert 0.9 <= ragas_adapter.string_similarity(REFERENCE, REFERENCE) <= 1.0
    assert ragas_adapter.context_recall(CONTEXT, [REFERENCE]) == pytest.approx(1.0)
    assert ragas_adapter.context_recall(["Unrelated text about parking."], [REFERENCE]) == pytest.approx(0.0)
