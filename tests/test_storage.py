import subprocess
import sys
import textwrap

from backend import process_lock
from backend.schemas import EvaluationRun, ModeResult, QuestionResult, RunConfig


def test_resaving_parents_keeps_children(workspace, sample_bytes):
    """Regression: INSERT OR REPLACE would cascade-delete chunks and results."""
    document, _ = workspace.ingest("handbook.txt", sample_bytes)
    key = document.metadata["index_key"]
    before = len(workspace.storage.get_chunks(document.document_id, key))
    workspace.storage.save_document(document)
    assert len(workspace.storage.get_chunks(document.document_id, key)) == before > 0

    run = EvaluationRun("run_x", document.document_id, "ds", RunConfig(), ["retriever"], status="running")
    workspace.storage.save_run(run)
    workspace.storage.save_results("run_x", [QuestionResult("q1", {"retriever": ModeResult("retriever", True)}, "PASS", "Pass", "")])
    run.status = "completed"
    workspace.storage.save_run(run)
    assert len(workspace.storage.get_results("run_x")) == 1
    assert workspace.storage.get_run("run_x").status == "completed"


def test_delete_document_removes_everything(workspace, demo):
    document_id = demo["document_id"]
    workspace.delete_document(document_id)
    assert workspace.storage.get_document(document_id) is None
