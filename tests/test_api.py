import base64

import pytest
from fastapi.testclient import TestClient

from backend import api
from tests.conftest import SAMPLE


@pytest.fixture
def client(workspace, monkeypatch):
    monkeypatch.setattr(api, "_workspace", workspace)
    with TestClient(api.app) as test_client:
        yield test_client


def test_health(client):
    body = client.get("/api/v1/health").json()
    assert body["status"] == "ok" and body["environment"]["embedding"]["backend"] == "hashing"


def test_upload_generate_run_export(client):
    upload = client.post("/api/v1/documents", files={"file": ("handbook.txt", SAMPLE.read_bytes(), "text/plain")})
    assert upload.status_code == 201
    document_id = upload.json()["document_id"]
    assert upload.json()["chunk_count"] > 0

    generated = client.post("/api/v1/evaluation/questions/generate", json={"document_id": document_id, "count": 6})
    assert generated.json()["status"] == "review_required" and generated.json()["candidate_count"] > 0

    dataset = client.get(f"/api/v1/evaluation/datasets/ds_{document_id}").json()
    question_id = dataset["questions"][0]["question_id"]
    reviewed = client.patch(f"/api/v1/evaluation/questions/{question_id}", json={"review_status": "approved"})
    assert reviewed.json()["review_status"] == "approved"

    run = client.post(
        "/api/v1/evaluation/runs?wait=true",
        json={"dataset_id": f"ds_{document_id}", "modes": ["retriever", "generator", "end_to_end"],
              "configuration": {"top_k": 3, "chunk_size": 500, "chunk_overlap": 80}},
    )
    assert run.status_code == 202 and run.json()["status"] == "completed"
    run_id = run.json()["run_id"]

    detail = client.get(f"/api/v1/evaluation/runs/{run_id}").json()
    assert detail["configuration"]["top_k"] == 3 and detail["results"]

    csv = client.get(f"/api/v1/evaluation/runs/{run_id}/export?format=csv")
    assert csv.status_code == 200 and csv.text.startswith("question_id,")
    assert client.get(f"/api/v1/evaluation/runs/{run_id}/export?format=xml").status_code == 422


def test_async_run_returns_pollable_id(client):
    document_id = client.post("/api/v1/documents", files={"file": ("h.txt", SAMPLE.read_bytes(), "text/plain")}).json()["document_id"]
    client.post("/api/v1/evaluation/questions/generate", json={"document_id": document_id, "count": 4})
    queued = client.post("/api/v1/evaluation/runs", json={"dataset_id": f"ds_{document_id}"}).json()
    assert queued["status"] == "queued" and queued["run_id"]
    # TestClient runs background tasks before returning, so the run is finished here.
    assert client.get(f"/api/v1/evaluation/runs/{queued['run_id']}").json()["status"] == "completed"


def test_errors_are_clear(client):
    bad = client.post("/api/v1/documents", files={"file": ("x.exe", b"MZ...", "application/octet-stream")})
    assert bad.status_code == 422 and bad.json()["detail"]["code"] == "unsupported_type"
    assert client.get("/api/v1/evaluation/runs/run_missing").status_code == 404
    assert client.post("/api/v1/evaluation/runs", json={"dataset_id": "ds_missing"}).status_code == 404


def test_demo_compare_and_ui_bridge(client):
    demo = client.post("/api/v1/demo").json()
    if demo["candidate_run_id"]:
        comparison = client.post("/api/v1/evaluation/compare", json={
            "baseline_run_id": demo["baseline_run_id"], "candidate_run_id": demo["candidate_run_id"]}).json()
        assert comparison["sample_size"] == 14

    state = client.get("/api/v1/ui/state").json()
    assert state["runs"] and state["results"] and state["charts"]["trend"]["pass_rate"]["data"]

    uploaded = client.post("/api/v1/ui/action", json={
        "type": "upload", "nonce": "n1",
        "files": [{"name": "again.txt", "data": base64.b64encode(SAMPLE.read_bytes()).decode()}],
    }).json()
    assert uploaded["notice"]["nonce"] == "n1" and "Already indexed" in uploaded["notice"]["message"]

    exported = client.post("/api/v1/ui/action", json={"type": "export", "run_id": demo["baseline_run_id"],
                                                      "format": "json", "nonce": "n2"}).json()
    assert exported["download"]["filename"].endswith(".json")

    unknown = client.post("/api/v1/ui/action", json={"type": "nope", "nonce": "n3"}).json()
    assert unknown["notice"]["level"] == "error"
