import pytest

from backend.experiments import IncompatibleRuns, compare_runs
from backend.recommendations import apply_change, for_question, top_recommendation
from backend.schemas import ModeResult, QuestionResult, RunConfig


def test_demo_runs_baseline_and_candidate(workspace, demo):
    baseline = workspace.get_run(demo["baseline_run_id"])
    assert baseline.status == "completed"
    assert baseline.summary["questions"] == 14  # the reviewed sample test set
    assert set(baseline.summary["modes"]) == {"retriever", "generator", "end_to_end"}
    assert baseline.summary["environment"]["embedding_backend"] == "hashing"
    if demo["candidate_run_id"]:
        candidate = workspace.get_run(demo["candidate_run_id"])
        assert candidate.parent_run_id == baseline.run_id
        comparison = workspace.compare(baseline.run_id, candidate.run_id)
        assert comparison["sample_size"] == 14
        assert comparison["config_changes"]  # exactly what the recommendation changed
        assert any("preliminary" in w for w in comparison["warnings"])


def test_compare_rejects_different_question_sets(workspace, demo):
    run_id = demo["baseline_run_id"]
    run = workspace.get_run(run_id)
    results = workspace.storage.get_results(run_id)
    with pytest.raises(IncompatibleRuns):
        compare_runs(run, run, results, results[:-1], strict=True)
    relaxed = compare_runs(run, run, results, results[:-1], strict=False)
    assert relaxed["sample_size"] == len(results) - 1 and relaxed["warnings"]


def _result(code, metrics=None, gen_metrics=None):
    modes = {"retriever": ModeResult("retriever", False, metrics=metrics or {})}
    if gen_metrics is not None:
