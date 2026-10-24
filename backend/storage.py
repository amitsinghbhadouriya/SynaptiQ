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
            conn.execute("DELETE FROM chunks WHERE document_id = ?", (document_id,))
            return conn.execute("DELETE FROM documents WHERE document_id = ?", (document_id,)).rowcount > 0

    # ------------------------------------------------------------------- chunks
    def save_chunks(self, chunks: list[Chunk]) -> None:
        if not chunks:
            return
        with self._write_lock, self._connect() as conn:
            conn.execute(
                "DELETE FROM chunks WHERE document_id = ? AND index_key = ?", (chunks[0].document_id, chunks[0].index_key)
            )
            conn.executemany(
                "INSERT INTO chunks VALUES (?,?,?,?,?,?,?,?,?)",
                [(c.chunk_id, c.document_id, c.index_key, c.chunk_index, c.text, c.start_char, c.end_char,
                  c.page_number, _dumps(c.metadata)) for c in chunks],
            )

    def get_chunks(self, document_id: str, index_key: str) -> list[Chunk]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM chunks WHERE document_id = ? AND index_key = ? ORDER BY chunk_index", (document_id, index_key)
            ).fetchall()
        return [
            Chunk(chunk_id=r["chunk_id"], document_id=r["document_id"], chunk_index=r["chunk_index"], text=r["text"],
                  start_char=r["start_char"], end_char=r["end_char"], index_key=r["index_key"],
                  page_number=r["page_number"], metadata=json.loads(r["metadata_json"] or "{}"))
            for r in rows
        ]

    def chunk_counts(self) -> dict[str, int]:
        """Chunk count per document for its most recently built index."""
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT document_id, index_key, COUNT(*) AS n FROM chunks GROUP BY document_id, index_key"
            ).fetchall()
        counts: dict[str, int] = {}
        for row in rows:
            counts[row["document_id"]] = max(counts.get(row["document_id"], 0), row["n"])
        return counts

    # ---------------------------------------------------------------- questions
    def save_questions(self, questions: list[EvalQuestion]) -> None:
        with self._write_lock, self._connect() as conn:
            conn.executemany(
                "INSERT OR REPLACE INTO evaluation_questions VALUES (?,?,?,?,?,?,?,?,?,?)",
                [(q.question_id, q.document_id, q.question, q.reference_answer, _dumps(q.supporting_chunk_ids),
                  _dumps([e.__dict__ for e in q.evidence]), q.question_type, q.review_status, q.source, q.created_at)
                 for q in questions],
            )

    def list_questions(self, document_id: str | None = None, include_rejected: bool = True) -> list[EvalQuestion]:
        sql = "SELECT * FROM evaluation_questions"
        params: tuple = ()
        if document_id:
            sql += " WHERE document_id = ?"
            params = (document_id,)
        sql += " ORDER BY created_at, question_id"
        with self._connect() as conn:
            rows = conn.execute(sql, params).fetchall()
        questions = [
            EvalQuestion.from_dict({
                "question_id": r["question_id"], "document_id": r["document_id"], "question": r["question"],
                "reference_answer": r["reference_answer"], "question_type": r["question_type"],
                "evidence": json.loads(r["evidence_json"] or "[]"),
                "supporting_chunk_ids": json.loads(r["supporting_chunk_ids"] or "[]"),
                "review_status": r["review_status"], "source": r["source"], "created_at": r["created_at"],
            })
            for r in rows
        ]
        return questions if include_rejected else [q for q in questions if q.review_status != "rejected"]

    def get_question(self, question_id: str) -> EvalQuestion | None:
        return next((q for q in self.list_questions() if q.question_id == question_id), None)

    def update_question(self, question_id: str, **fields: Any) -> bool:
        allowed = {"question", "reference_answer", "review_status", "question_type"}
        updates = {k: v for k, v in fields.items() if k in allowed and v is not None}
        if not updates:
            return False
        assignments = ", ".join(f"{k} = ?" for k in updates)
        with self._write_lock, self._connect() as conn:
            cur = conn.execute(
                f"UPDATE evaluation_questions SET {assignments} WHERE question_id = ?", (*updates.values(), question_id)
            )
            return cur.rowcount > 0

    def delete_questions(self, document_id: str, source: str | None = None) -> None:
        with self._write_lock, self._connect() as conn:
            if source:
                conn.execute("DELETE FROM evaluation_questions WHERE document_id = ? AND source = ?", (document_id, source))
            else:
                conn.execute("DELETE FROM evaluation_questions WHERE document_id = ?", (document_id,))

    # --------------------------------------------------------------------- runs
    def save_run(self, run: EvaluationRun) -> None:
        with self._write_lock, self._connect() as conn:
            conn.execute(
                "INSERT INTO evaluation_runs VALUES (?,?,?,?,?,?,?,?,?,?,?,?) ON CONFLICT(run_id) DO UPDATE SET "
                "configuration_json=excluded.configuration_json, modes_json=excluded.modes_json, "
                "status=excluded.status, duration_ms=excluded.duration_ms, summary_json=excluded.summary_json, "
                "label=excluded.label, parent_run_id=excluded.parent_run_id, error=excluded.error",
                (run.run_id, run.document_id, run.dataset_id, run.created_at, _dumps(run.configuration.to_dict()),
                 _dumps(run.modes), run.status, run.duration_ms, _dumps(run.summary), run.label, run.parent_run_id,
                 run.error),
            )

    @staticmethod
    def _row_to_run(row: sqlite3.Row) -> EvaluationRun:
        return EvaluationRun(
            run_id=row["run_id"], document_id=row["document_id"], dataset_id=row["dataset_id"],
            configuration=RunConfig.from_dict(json.loads(row["configuration_json"])),
            modes=json.loads(row["modes_json"]), status=row["status"], created_at=row["created_at"],
            duration_ms=row["duration_ms"], summary=json.loads(row["summary_json"] or "{}"), label=row["label"],
            parent_run_id=row["parent_run_id"], error=row["error"],
        )

    def get_run(self, run_id: str) -> EvaluationRun | None:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM evaluation_runs WHERE run_id = ?", (run_id,)).fetchone()
        return self._row_to_run(row) if row else None

    def list_runs(self, document_id: str | None = None) -> list[EvaluationRun]:
        sql, params = "SELECT * FROM evaluation_runs", ()
        if document_id:
            sql, params = sql + " WHERE document_id = ?", (document_id,)
        with self._connect() as conn:
            rows = conn.execute(sql + " ORDER BY created_at DESC, rowid DESC", params).fetchall()
        return [self._row_to_run(r) for r in rows]

    def delete_run(self, run_id: str) -> None:
        with self._write_lock, self._connect() as conn:
            conn.execute("DELETE FROM evaluation_results WHERE run_id = ?", (run_id,))
            conn.execute("DELETE FROM evaluation_runs WHERE run_id = ?", (run_id,))

    # ------------------------------------------------------------------ results
    def save_results(self, run_id: str, results: list[QuestionResult]) -> None:
        rows = []
        for result in results:
            for mode, mode_result in result.modes.items():
                rows.append((
                    f"{run_id}:{result.question_id}:{mode}", run_id, result.question_id, mode,
                    None if mode_result.passed is None else int(mode_result.passed),
                    _dumps([r.__dict__ for r in mode_result.retrieved]), mode_result.answer,
                    _dumps(mode_result.contexts), _dumps(mode_result.metrics), result.diagnosis,
                    result.diagnosis_label, result.diagnosis_reason, _dumps(result.evidence_notes),
                    _dumps(result.recommendation) if result.recommendation else None, mode_result.latency_ms,
                    mode_result.estimated_cost, mode_result.error,
                ))
        with self._write_lock, self._connect() as conn:
            conn.execute("DELETE FROM evaluation_results WHERE run_id = ?", (run_id,))
            conn.executemany("INSERT INTO evaluation_results VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", rows)

    def get_results(self, run_id: str) -> list[QuestionResult]:
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM evaluation_results WHERE run_id = ? ORDER BY rowid", (run_id,)).fetchall()
        grouped: dict[str, QuestionResult] = {}
        for r in rows:
            mode_result = ModeResult(
                mode=r["mode"], passed=None if r["passed"] is None else bool(r["passed"]),
                metrics=json.loads(r["metrics_json"] or "{}"),
                retrieved=[RetrievedChunk(**x) for x in json.loads(r["retrieved_json"] or "[]")],
                answer=r["generated_answer"], contexts=json.loads(r["contexts_json"] or "[]"),
                latency_ms=r["latency_ms"], estimated_cost=r["estimated_cost"], error=r["error"],
            )
            entry = grouped.get(r["question_id"])
            if entry is None:
                entry = QuestionResult(
                    question_id=r["question_id"], modes={}, diagnosis=r["diagnosis"],
                    diagnosis_label=r["diagnosis_label"], diagnosis_reason=r["diagnosis_reason"],
                    evidence_notes=json.loads(r["evidence_notes_json"] or "[]"),
                    recommendation=json.loads(r["recommendation_json"]) if r["recommendation_json"] else None,
                )
                grouped[r["question_id"]] = entry
            entry.modes[r["mode"]] = mode_result
        return list(grouped.values())
