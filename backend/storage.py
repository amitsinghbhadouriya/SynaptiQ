"""SQLite persistence for documents, chunks, test questions, runs and results.

Vectors live in ChromaDB; this database holds the relational side so runs can be
reproduced and compared. A new connection is opened per call, which keeps it safe
to use from Streamlit's script threads and FastAPI workers alike.
"""

from __future__ import annotations

import json
import sqlite3
import threading
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

from .schemas import (
    Chunk,
    Document,
    EvalQuestion,
    EvaluationRun,
    ModeResult,
    QuestionResult,
    RetrievedChunk,
    RunConfig,
)

SCHEMA_VERSION = 1

SCHEMA = """
CREATE TABLE IF NOT EXISTS schema_version (version INTEGER NOT NULL);

CREATE TABLE IF NOT EXISTS documents (
    document_id   TEXT PRIMARY KEY,
    filename      TEXT NOT NULL,
    content_hash  TEXT NOT NULL,
    file_type     TEXT NOT NULL,
    created_at    TEXT NOT NULL,
    status        TEXT NOT NULL,
    text          TEXT NOT NULL,
    metadata_json TEXT NOT NULL DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS chunks (
    chunk_id      TEXT PRIMARY KEY,
    document_id   TEXT NOT NULL REFERENCES documents(document_id) ON DELETE CASCADE,
    index_key     TEXT NOT NULL,
    chunk_index   INTEGER NOT NULL,
    text          TEXT NOT NULL,
    start_char    INTEGER NOT NULL,
    end_char      INTEGER NOT NULL,
    page_number   INTEGER,
    metadata_json TEXT NOT NULL DEFAULT '{}'
);
CREATE INDEX IF NOT EXISTS idx_chunks_doc_key ON chunks(document_id, index_key);

CREATE TABLE IF NOT EXISTS evaluation_questions (
    question_id          TEXT PRIMARY KEY,
    document_id          TEXT NOT NULL REFERENCES documents(document_id) ON DELETE CASCADE,
    question             TEXT NOT NULL,
    reference_answer     TEXT NOT NULL,
    supporting_chunk_ids TEXT NOT NULL DEFAULT '[]',
    evidence_json        TEXT NOT NULL DEFAULT '[]',
    question_type        TEXT NOT NULL,
    review_status        TEXT NOT NULL,
    source               TEXT NOT NULL,
    created_at           TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS evaluation_runs (
    run_id             TEXT PRIMARY KEY,
    document_id        TEXT NOT NULL REFERENCES documents(document_id) ON DELETE CASCADE,
    dataset_id         TEXT NOT NULL,
    created_at         TEXT NOT NULL,
    configuration_json TEXT NOT NULL,
    modes_json         TEXT NOT NULL,
    status             TEXT NOT NULL,
    duration_ms        INTEGER,
    summary_json       TEXT NOT NULL DEFAULT '{}',
    label              TEXT NOT NULL DEFAULT '',
    parent_run_id      TEXT,
    error              TEXT
);

CREATE TABLE IF NOT EXISTS evaluation_results (
    result_id           TEXT PRIMARY KEY,
    run_id              TEXT NOT NULL REFERENCES evaluation_runs(run_id) ON DELETE CASCADE,
