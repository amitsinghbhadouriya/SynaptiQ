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
        modes["generator"] = ModeResult("generator", False, metrics=gen_metrics)
    return QuestionResult("q", modes, code, code, "")


def test_recommends_exact_top_k_from_evidence_rank():
    config = RunConfig(top_k=2)
    rec = for_question(_result("LIKELY_RETRIEVAL_FAILURE", {"first_relevant_rank": 4.0, "full_coverage_rank": 4.0}), config)
    assert rec["change"] == {"key": "top_k", "from": 2, "to": 4}
    assert apply_change(config, rec["change"]).top_k == 4


def test_recommends_threshold_changes_for_abstention_problems():
    config = RunConfig(abstain_threshold=0.3)
    over = for_question(_result("LIKELY_GENERATION_FAILURE", gen_metrics={"abstained": 1.0, "answer_correctness": 0.0}), config)
    assert over["change"]["key"] == "abstain_threshold" and over["change"]["to"] < 0.3
    hallucinated = for_question(
        _result("LIKELY_GENERATION_FAILURE", gen_metrics={"abstained": 0.0, "abstention_correct": 0.0, "answer_correctness": None}),
        config,
    )
    assert hallucinated["change"]["key"] == "abstain_threshold" and hallucinated["change"]["to"] > 0.3


def test_top_recommendation_prefers_retrieval_fixes():
    config = RunConfig(top_k=1)
    results = []
    for rank in (2.0, 3.0):
        r = _result("LIKELY_RETRIEVAL_FAILURE", {"first_relevant_rank": rank, "full_coverage_rank": rank})
        r.recommendation = for_question(r, config)
        results.append(r)
    g = _result("LIKELY_GENERATION_FAILURE", gen_metrics={"abstained": 1.0, "answer_correctness": 0.0})
    g.recommendation = for_question(g, config)
    results.append(g)
    top = top_recommendation(results, config)
    assert top["change"]["key"] == "top_k" and top["change"]["to"] == 3  # the larger k covers both questions
    assert top["votes"] == 2 and top["candidate_config"]["top_k"] == 3
