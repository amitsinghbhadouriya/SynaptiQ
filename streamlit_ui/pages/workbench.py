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
