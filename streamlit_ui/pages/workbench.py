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

    runs = [r for r in workspace.storage.list_runs() if r.status == "completed"]
    if not runs:
        st.info("No completed runs yet.")
    else:
        st.subheader("Run history")
        st.dataframe(runs_frame(runs), width="stretch", hide_index=True)
        run_ids = [r.run_id for r in runs]
        default = run_ids.index(st.session_state["selected_run_id"]) if st.session_state.get("selected_run_id") in run_ids else 0
        run_id = st.selectbox("Inspect run", run_ids, index=default,
                              format_func=lambda rid: next(f"{r.label or r.configuration.short()} — {doc_names.get(r.document_id, '')}" for r in runs if r.run_id == rid))
        run = workspace.get_run(run_id)
        results = workspace.storage.get_results(run_id)
        questions = workspace.storage.list_questions(run.document_id)
        s = run.summary
        m = st.columns(5)
        m[0].metric("Pass rate", f"{s['pass_rate']:.0%}")
        m[1].metric("Hit@k", f"{(s['headline'].get('hit_at_k') or 0):.0%}")
        m[2].metric("Context recall", f"{(s['headline'].get('context_recall') or 0):.2f}")
        m[3].metric("Faithfulness", "—" if s['headline'].get('faithfulness') is None else f"{s['headline']['faithfulness']:.2f}")
        m[4].metric("Correctness", "—" if s['headline'].get('answer_correctness') is None else f"{s['headline']['answer_correctness']:.2f}")

        doc_runs = [r for r in runs if r.document_id == run.document_id]
        c1, c2 = st.columns(2)
        c1.plotly_chart(go_fig.Figure(charts.trend_figures(doc_runs)["pass_rate"]), width="stretch")
        donut = charts.failure_donut(s, LABELS)
        if donut:
            c2.plotly_chart(go_fig.Figure(donut), width="stretch")
        else:
            c2.success("No failing questions in this run.")

        st.subheader("Per-question results")
        frame = results_frame(results, questions)
        st.dataframe(frame, width="stretch", hide_index=True)
        d1, d2 = st.columns(2)
        d1.download_button("Download CSV", frame.to_csv(index=False), f"synaptiq_{run_id}.csv", "text/csv")
        d2.download_button("Download JSON", workspace.export(run_id, "json")[2], f"synaptiq_{run_id}.json", "application/json")
        with st.expander("Run configuration"):
            st.code(json.dumps(run.configuration.to_dict(), indent=2), language="json")

# ----------------------------------------------------------------- compare
with tab_compare:
    runs = [r for r in workspace.storage.list_runs() if r.status == "completed"]
    if len(runs) < 2:
        st.info("Two completed runs are needed for a comparison.")
    else:
        label_of = {r.run_id: f"{r.label or r.configuration.short()} · {r.created_at[:16]}" for r in runs}
        c1, c2 = st.columns(2)
        base = c1.selectbox("Baseline", list(label_of), index=1, format_func=label_of.get)
        cand = c2.selectbox("Candidate", list(label_of), index=0, format_func=label_of.get)
        if base == cand:
            st.warning("Pick two different runs.")
        else:
            try:
                comparison = workspace.compare(base, cand, strict=True)
            except IncompatibleRuns as exc:
                st.error(str(exc))
            else:
                for warning in comparison["warnings"]:
                    st.warning(warning)
                st.write("Changed settings:", comparison["config_changes"] or "none")
                st.dataframe(pd.DataFrame(comparison["metrics"]), width="stretch", hide_index=True)
                st.plotly_chart(go_fig.Figure(charts.comparison_figure(comparison)), width="stretch")
                q = comparison["questions"]
                st.write(f"Fixed: {len(q['fixed'])} · Regressed: {len(q['regressed'])} · "
                         f"Still failing: {len(q['still_failing'])} · Still passing: {q['still_passing']}")

