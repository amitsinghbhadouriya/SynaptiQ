# SynaptiQ

**RAG evaluation, root-cause intelligence and optimization.**
*Evaluate with Evidence. Diagnose with Intelligence. Improve with Confidence.*

SynaptiQ tests the **retriever**, the **generator** and the **end-to-end pipeline** of a RAG system
separately, explains why an answer failed using the source evidence, recommends one targeted
configuration change, and measures whether that change actually helped — on the same test set.

| Landing page (3D) | Dashboard (light) |
|---|---|
| ![Landing page](docs/screenshots/landing-hero.png) | ![Dashboard overview](docs/screenshots/dashboard-overview-light.png) |
| **Dashboard (dark)** | **Analytics** |
| ![Dashboard dark](docs/screenshots/dashboard-overview-dark.png) | ![Analytics](docs/screenshots/dashboard-analytics-dark.png) |

---

## What's inside

| Layer | Technology | Where |
|---|---|---|
| Core logic & pipeline | Python 3.12 | `backend/` |
| Web UI | **Streamlit** (hosts the React UI as a custom component + native Workbench page) | `app.py`, `streamlit_ui/` |
| REST API + standalone website | **FastAPI** | `backend/api.py` |
| PDF extraction | **PyMuPDF** | `backend/document_loader.py` |
| DOCX extraction | **python-docx** | `backend/document_loader.py` |
| TXT handling & cleaning | standard Python | `backend/document_loader.py`, `backend/text_utils.py` |
| Embeddings | **Sentence Transformers** (`all-MiniLM-L6-v2`) | `backend/embeddings.py` |
| Vector index & metadata | **ChromaDB** (persistent, local) | `backend/vector_store.py` |
| RAG evaluation metrics | **Ragas** (non-LLM metrics) + transparent custom metrics | `backend/ragas_adapter.py`, `backend/metrics.py` |
| Results tables & exports | **pandas** | `backend/reports.py` |
| Charts | **Plotly** (built in Python, rendered by plotly.js in the dashboard and by Streamlit in the Workbench) | `backend/charts.py` |
| Run history | **SQLite** | `backend/storage.py` |
| Automated tests | **pytest** (61 tests) | `tests/` |
| Optional live LLM | Claude via the official `anthropic` SDK | `backend/generator.py` |
| Front end | React 19 + Vite, three.js, GSAP, ogl, React Bits components | `frontend/` (pre-built in `frontend/dist`) |

The app runs **fully offline by default**: an extractive generator answers from the evidence, and
if the embedding model cannot be downloaded the app falls back to deterministic hashing embeddings.
Every run records which backend was actually used, so results are never silently mixed.

---

## Quick start

> **Use Python 3.11 or 3.12.** Brand-new interpreters (3.13+/3.15) may not have wheels for
> `torch` and `chromadb` yet. Check with `python --version`.

### Windows (PowerShell)

```powershell
cd synaptiq
py -3.12 -m venv .venv            # or: uv venv --python 3.12 .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env            # optional — defaults work offline
streamlit run app.py
```

If PowerShell blocks activation, run `.venv\Scripts\activate.bat` from Command Prompt instead.
No Python 3.12? Install it from python.org or with `uv python install 3.12`.

### macOS / Linux

```bash
cd synaptiq
python3.12 -m venv .venv && source .venv/bin/activate
pip install --upgrade pip && pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

Open <http://localhost:8501>. The first start downloads the small embedding model (~90 MB) and
loads it; later starts are faster. To save disk space you can install the CPU-only PyTorch wheel
first: `pip install torch --index-url https://download.pytorch.org/whl/cpu`.

### Try the demo (about 10 seconds)

