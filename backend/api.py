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
