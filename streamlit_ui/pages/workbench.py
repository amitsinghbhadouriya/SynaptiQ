"""Workbench: native Streamlit tools — uploads, human review of test sets (pandas data editor),
runs with a live progress bar, results tables and Plotly charts, and run comparisons."""

import json

import pandas as pd
import plotly.graph_objects as go_fig
import streamlit as st

from backend import charts
from backend.document_loader import DocumentLoadError
from backend.experiments import IncompatibleRuns
from backend.reports import results_frame, runs_frame
from backend.root_cause import LABELS
from backend.schemas import MODES
from streamlit_ui.shared import DASHBOARD, HOME, get_workspace

workspace = get_workspace()

top = st.columns([6, 1.3, 1.3])
top[0].title("Workbench")
top[0].caption("Native Streamlit tools for reviewing test sets and inspecting raw results. Everything here is also in the dashboard.")
if top[1].button("← Dashboard", width="stretch"):
    st.switch_page(DASHBOARD)
if top[2].button("Landing page", width="stretch"):
    st.switch_page(HOME)

documents = workspace.storage.list_documents()
doc_names = {d.document_id: d.filename for d in documents}

tab_upload, tab_review, tab_runs, tab_compare = st.tabs(["Upload", "Test set review", "Runs & results", "Compare runs"])

# ------------------------------------------------------------------ upload
with tab_upload:
    files = st.file_uploader(
        "Upload PDF, DOCX or TXT", type=["pdf", "docx", "txt"], accept_multiple_files=True,
        help=f"Up to {workspace.settings.max_upload_mb} MB per file. Scanned PDFs need OCR (out of scope).",
    )
    if files and st.button("Ingest and index", type="primary"):
        for uploaded in files:
            try:
                with st.spinner(f"Indexing {uploaded.name}…"):
                    document, created = workspace.ingest(uploaded.name, uploaded.getvalue())
                st.success(f"{document.filename}: {'indexed' if created else 'already indexed'} "
                           f"({document.metadata.get('chunk_count', '?')} chunks).")
            except DocumentLoadError as exc:
                st.error(f"{uploaded.name}: {exc.message}")
    st.divider()
    if st.button("Load demo workspace"):
        with st.spinner("Running the demo baseline and the recommended candidate…"):
            info = workspace.load_demo()
        st.session_state["selected_run_id"] = info["candidate_run_id"] or info["baseline_run_id"]
        st.success("Demo workspace ready.")
    if documents:
        st.dataframe(
            pd.DataFrame([d.summary() for d in documents])[["filename", "file_type", "status", "created_at", "char_count"]],
            width="stretch", hide_index=True,
        )

# ------------------------------------------------------------------ review
with tab_review:
    if not documents:
        st.info("Upload a document first.")
    else:
        doc_id = st.selectbox("Document", list(doc_names), format_func=doc_names.get, key="review_doc")
        cols = st.columns([1, 1, 3])
        count = cols[0].number_input("Questions", 1, workspace.settings.max_questions, 10)
        if cols[1].button("Generate test set"):
            with st.spinner("Generating candidate questions…"):
                generated = workspace.generate_test_set(doc_id, int(count))
            st.success(f"Generated {len(generated)} pending questions.")
        questions = workspace.storage.list_questions(doc_id)
        if questions:
            frame = pd.DataFrame([{
                "question_id": q.question_id, "review_status": q.review_status, "type": q.question_type,
                "question": q.question, "reference_answer": q.reference_answer,
                "evidence": " | ".join(e.text for e in q.evidence), "source": q.source,
            } for q in questions])
            edited = st.data_editor(
                frame, hide_index=True, width="stretch", key=f"editor_{doc_id}",
                disabled=["question_id", "type", "evidence", "source"],
                column_config={
                    "review_status": st.column_config.SelectboxColumn("Review", options=["pending", "approved", "rejected"]),
                    "question": st.column_config.TextColumn("Question", width="large"),
                    "reference_answer": st.column_config.TextColumn("Reference answer", width="large"),
                    "question_id": None,
                },
            )
            if st.button("Save review changes", type="primary"):
                changed = 0
                for original, row in zip(frame.to_dict("records"), edited.to_dict("records")):
                    edits = {k: row[k] for k in ("review_status", "question", "reference_answer") if row[k] != original[k]}
                    if edits:
                        workspace.review_question(row["question_id"], edits.pop("review_status", None), **edits)
                        changed += 1
                st.success(f"Saved {changed} changed question(s).")
        else:
            st.caption("No questions yet for this document.")

# -------------------------------------------------------------------- runs
with tab_runs:
    if documents:
        with st.expander("Start a new run", expanded=False):
            with st.form("run_form"):
                doc_id = st.selectbox("Document", list(doc_names), format_func=doc_names.get)
                c1, c2, c3 = st.columns(3)
                defaults = workspace.default_config()
                chunk_size = c1.number_input("Chunk size", 100, 4000, defaults.chunk_size, step=20)
                overlap = c2.number_input("Chunk overlap", 0, 1000, defaults.chunk_overlap, step=10)
                top_k = c3.number_input("Top-k", 1, 20, defaults.top_k)
                modes = st.multiselect("Modes", list(MODES), default=list(MODES))
                label = st.text_input("Label", "")
                submitted = st.form_submit_button("Run evaluation", type="primary")
            if submitted:
                bar = st.progress(0.0, text="Starting…")

                def report(done, total, text):
                    bar.progress(done / max(1, total), text=f"{done}/{total} · {text[:80]}")

                config = workspace.default_config(chunk_size=int(chunk_size), chunk_overlap=int(overlap), top_k=int(top_k))
                try:
                    run = workspace.run_evaluation(doc_id, config, modes, label=label, progress=report)
                except ValueError as exc:
                    st.error(str(exc))
                else:
                    st.session_state["selected_run_id"] = run.run_id
                    (st.success if run.status == "completed" else st.error)(
                        f"Run {run.status}: {run.summary.get('passed', 0)}/{run.summary.get('questions', 0)} passed."
                        if run.status == "completed" else f"Run failed: {run.error}"
                    )
