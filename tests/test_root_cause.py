import pytest

from backend.root_cause import LABELS, NEXT_ACTIONS, diagnose


@pytest.mark.parametrize(
    "retrieval,generator,e2e,e2e_correct,expected",
    [
        (False, True, False, False, "LIKELY_RETRIEVAL_FAILURE"),
        (True, False, False, False, "LIKELY_GENERATION_FAILURE"),
        (False, False, False, False, "LIKELY_COMBINED_FAILURE"),
        (True, True, False, False, "PIPELINE_INTERACTION_FAILURE"),
        (True, True, True, True, "PASS"),
        (False, True, True, True, "CORRECT_BUT_UNGROUNDED"),
        (None, None, None, None, "UNCERTAIN_REQUIRES_REVIEW"),
        (True, None, None, None, "UNCERTAIN_REQUIRES_REVIEW"),
    ],
)
def test_answerable_rules(retrieval, generator, e2e, e2e_correct, expected):
    result = diagnose(retrieval, generator, e2e, end_to_end_correct=e2e_correct)
    assert result.code == expected
    assert result.reason and result.label == LABELS[expected] and result.next_action == NEXT_ACTIONS[expected]


def test_missing_measurements_are_not_failures():
    # Unknown retrieval must never be read as a retrieval failure.
    assert diagnose(None, True, True).code == "UNCERTAIN_REQUIRES_REVIEW"


def test_unanswerable_questions():
    assert diagnose(None, True, True, answerable=False).code == "PASS"
    hallucination = diagnose(None, False, False, answerable=False)
    assert hallucination.code == "LIKELY_GENERATION_FAILURE" and "unanswerable" in hallucination.reason
    assert diagnose(None, None, None, answerable=False).code == "UNCERTAIN_REQUIRES_REVIEW"


def test_notes_are_kept():
    assert diagnose(True, True, True, notes=["evidence at rank 1"]).evidence == ["evidence at rank 1"]
