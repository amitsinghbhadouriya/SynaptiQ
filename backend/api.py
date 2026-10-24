"""FastAPI service: REST API for SynaptiQ plus the built website.

Run with:  uvicorn backend.api:app --reload
Docs:      http://localhost:8000/docs
Website:   http://localhost:8000/  (landing page + dashboard, served from frontend/dist)

Add authentication, HTTPS and rate limiting before exposing this beyond localhost.
"""

from __future__ import annotations

import logging
import threading
import time
import uuid
from contextlib import asynccontextmanager
from typing import Any, Literal

from fastapi import BackgroundTasks, FastAPI, File, HTTPException, Query, Request, UploadFile
from fastapi.responses import JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from . import __version__
from .config import PROJECT_ROOT
from .document_loader import DocumentLoadError
from .experiments import IncompatibleRuns
from .process_lock import StorageInUse
from .schemas import MODES, QUESTION_TYPES, EvaluationRun, new_id, to_jsonable
from .service import NotFound, Workspace
from .ui_bridge import build_state, handle_event

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
log = logging.getLogger("synaptiq.api")

_workspace: Workspace | None = None
_workspace_lock = threading.Lock()


def workspace() -> Workspace:
    global _workspace
    with _workspace_lock:
        if _workspace is None:
            try:
                _workspace = Workspace()
            except StorageInUse as exc:
                raise HTTPException(503, str(exc)) from exc
            _workspace.status()  # loads the embedding model once, up front
    return _workspace


def _warm_up() -> None:
    try:
        workspace()
    except HTTPException as exc:
        log.error("%s", exc.detail)


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Warm up in the background so the server accepts requests immediately.
    threading.Thread(target=_warm_up, name="synaptiq-warmup", daemon=True).start()
    yield


app = FastAPI(
    title="SynaptiQ API",
    version=__version__,
    description="RAG evaluation, root-cause intelligence and optimization.",
    lifespan=lifespan,
)


@app.middleware("http")
async def request_context(request: Request, call_next):
    request_id = request.headers.get("x-request-id") or uuid.uuid4().hex[:12]
    started = time.perf_counter()
    response = await call_next(request)
    response.headers["x-request-id"] = request_id
    if request.url.path.startswith("/api/"):
        log.info("request_id=%s method=%s path=%s status=%s ms=%d", request_id, request.method, request.url.path,
                 response.status_code, (time.perf_counter() - started) * 1000)
    return response


@app.exception_handler(NotFound)
async def not_found_handler(_: Request, exc: NotFound):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(IncompatibleRuns)
async def incompatible_handler(_: Request, exc: IncompatibleRuns):
    return JSONResponse(status_code=409, content={"detail": str(exc)})


# ------------------------------------------------------------------- models
class GenerateRequest(BaseModel):
    document_id: str
    count: int = Field(10, ge=1, le=500)
    question_types: list[Literal["factual", "numerical", "multi_hop", "unanswerable"]] = list(QUESTION_TYPES)


class ImportRequest(BaseModel):
    document_id: str
    questions: list[dict[str, Any]]


class ReviewRequest(BaseModel):
    review_status: Literal["pending", "approved", "rejected"] | None = None
    question: str | None = None
    reference_answer: str | None = None


class RunConfiguration(BaseModel):
    top_k: int | None = Field(None, ge=1, le=20)
    chunk_size: int | None = Field(None, ge=100, le=4000)
    chunk_overlap: int | None = Field(None, ge=0, le=1000)
    embedding_model: str | None = None
    embedding_backend: Literal["auto", "sentence-transformers", "hashing"] | None = None
    prompt_version: Literal["grounded-v1", "grounded-strict-v2"] | None = None
    max_answer_sentences: int | None = Field(None, ge=1, le=5)
    abstain_threshold: float | None = Field(None, ge=0, le=1)
    label: str | None = Field(None, max_length=80)


class RunRequest(BaseModel):
    dataset_id: str = Field(..., description="ds_<document_id>")
    modes: list[Literal["retriever", "generator", "end_to_end"]] = list(MODES)
    configuration: RunConfiguration = RunConfiguration()


class CompareRequest(BaseModel):
    baseline_run_id: str
    candidate_run_id: str
    strict: bool = True


def _run_payload(run: EvaluationRun, include_results: bool = False) -> dict[str, Any]:
    payload = run.to_dict()
    if include_results and run.status == "completed":
        payload["results"] = to_jsonable(workspace().storage.get_results(run.run_id))
    return payload


# ----------------------------------------------------------------- endpoints
@app.get("/api/v1/health")
def health() -> dict[str, Any]:
    return {"status": "ok", "version": __version__, "environment": workspace().status()}


@app.post("/api/v1/documents", status_code=201)
async def upload_document(file: UploadFile = File(...)) -> dict[str, Any]:
    ws = workspace()
    limit = ws.settings.max_upload_mb * 1024 * 1024
    data = await file.read(limit + 1)
    if len(data) > limit:
        raise HTTPException(413, f"The file is larger than the {ws.settings.max_upload_mb} MB limit.")
    try:
        document, created = ws.ingest(file.filename or "upload", data)
    except DocumentLoadError as exc:
        raise HTTPException(422, {"code": exc.code, "message": exc.message}) from exc
    return {"document_id": document.document_id, "filename": document.filename, "status": document.status,
            "chunk_count": document.metadata.get("chunk_count"), "created": created}


@app.get("/api/v1/documents")
def list_documents() -> list[dict[str, Any]]:
    return [d.summary() for d in workspace().storage.list_documents()]


@app.delete("/api/v1/documents/{document_id}", status_code=204)
def delete_document(document_id: str) -> Response:
    workspace().delete_document(document_id)
    return Response(status_code=204)


@app.post("/api/v1/evaluation/questions/generate")
def generate_questions(body: GenerateRequest) -> dict[str, Any]:
    questions = workspace().generate_test_set(body.document_id, body.count, list(body.question_types))
    return {"dataset_id": f"ds_{body.document_id}", "status": "review_required", "candidate_count": len(questions)}


@app.post("/api/v1/evaluation/questions/import")
def import_questions(body: ImportRequest) -> dict[str, Any]:
    try:
        questions = workspace().import_test_set(body.document_id, body.questions)
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc
    return {"dataset_id": f"ds_{body.document_id}", "status": "review_required", "imported": len(questions)}


@app.get("/api/v1/evaluation/datasets/{dataset_id}")
def get_dataset(dataset_id: str) -> dict[str, Any]:
    document_id = dataset_id.removeprefix("ds_")
    workspace().get_document(document_id)
    questions = workspace().storage.list_questions(document_id)
    return {"dataset_id": dataset_id, "document_id": document_id, "questions": [q.to_dict() for q in questions]}


@app.patch("/api/v1/evaluation/questions/{question_id}")
def review_question(question_id: str, body: ReviewRequest) -> dict[str, Any]:
    question = workspace().review_question(question_id, body.review_status, question=body.question,
                                           reference_answer=body.reference_answer)
    return question.to_dict()


@app.post("/api/v1/evaluation/runs", status_code=202)
def create_run(body: RunRequest, background: BackgroundTasks, wait: bool = Query(False)) -> dict[str, Any]:
    ws = workspace()
    document_id = body.dataset_id.removeprefix("ds_")
    ws.get_document(document_id)
    if not ws.dataset_questions(document_id):
        raise HTTPException(422, "This dataset has no questions. Generate or import a test set first.")
