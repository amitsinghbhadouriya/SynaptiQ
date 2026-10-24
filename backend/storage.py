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
    question_id         TEXT NOT NULL,
    mode                TEXT NOT NULL,
    passed              INTEGER,
    retrieved_json      TEXT NOT NULL DEFAULT '[]',
    generated_answer    TEXT,
    contexts_json       TEXT NOT NULL DEFAULT '[]',
    metrics_json        TEXT NOT NULL DEFAULT '{}',
    diagnosis           TEXT NOT NULL,
    diagnosis_label     TEXT NOT NULL,
    diagnosis_reason    TEXT NOT NULL,
    evidence_notes_json TEXT NOT NULL DEFAULT '[]',
    recommendation_json TEXT,
    latency_ms          INTEGER,
    estimated_cost      REAL,
    error               TEXT
);
CREATE INDEX IF NOT EXISTS idx_results_run ON evaluation_results(run_id);
"""


def _dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, default=lambda o: o.__dict__)


class Storage:
    def __init__(self, db_path: Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._write_lock = threading.Lock()
        with self._connect() as conn:
            conn.executescript(SCHEMA)
            if conn.execute("SELECT COUNT(*) FROM schema_version").fetchone()[0] == 0:
                conn.execute("INSERT INTO schema_version(version) VALUES (?)", (SCHEMA_VERSION,))

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self.db_path, timeout=30)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA journal_mode = WAL")
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    # ---------------------------------------------------------------- documents
    def save_document(self, doc: Document) -> None:
        with self._write_lock, self._connect() as conn:
            # Upsert (not INSERT OR REPLACE): REPLACE deletes the row first, which would cascade to chunks.
            conn.execute(
                "INSERT INTO documents VALUES (?,?,?,?,?,?,?,?) ON CONFLICT(document_id) DO UPDATE SET "
                "filename=excluded.filename, status=excluded.status, metadata_json=excluded.metadata_json",
                (doc.document_id, doc.filename, doc.content_hash, doc.file_type, doc.created_at, doc.status,
                 doc.text, _dumps(doc.metadata)),
            )

    @staticmethod
    def _row_to_document(row: sqlite3.Row) -> Document:
        return Document(
            document_id=row["document_id"], filename=row["filename"], file_type=row["file_type"],
            content_hash=row["content_hash"], text=row["text"], status=row["status"],
            created_at=row["created_at"], metadata=json.loads(row["metadata_json"] or "{}"),
        )

    def get_document(self, document_id: str) -> Document | None:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM documents WHERE document_id = ?", (document_id,)).fetchone()
        return self._row_to_document(row) if row else None

    def find_document_by_hash(self, content_hash: str) -> Document | None:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM documents WHERE content_hash = ?", (content_hash,)).fetchone()
        return self._row_to_document(row) if row else None

    def list_documents(self) -> list[Document]:
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM documents ORDER BY created_at DESC").fetchall()
        return [self._row_to_document(r) for r in rows]

    def delete_document(self, document_id: str) -> bool:
        with self._write_lock, self._connect() as conn:
            run_ids = [r[0] for r in conn.execute("SELECT run_id FROM evaluation_runs WHERE document_id = ?", (document_id,))]
            for run_id in run_ids:
                conn.execute("DELETE FROM evaluation_results WHERE run_id = ?", (run_id,))
            conn.execute("DELETE FROM evaluation_runs WHERE document_id = ?", (document_id,))
            conn.execute("DELETE FROM evaluation_questions WHERE document_id = ?", (document_id,))
