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
