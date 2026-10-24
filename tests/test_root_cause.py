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
