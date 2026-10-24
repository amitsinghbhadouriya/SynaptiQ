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

1. On the landing page click **Launch dashboard**.
2. Click **Load demo workspace**. SynaptiQ ingests the bundled *Lumen Labs Employee Handbook*
   (fictional, non-sensitive), loads its manually reviewed 14-question test set and runs a
   deliberately narrow **baseline** (chunk 280/0, top-k 1).
3. The baseline's failures are diagnosed and the top recommendation (for example
   *Increase top-k from 1 to 2*) is run automatically as a **candidate** on the same questions.
4. Explore **Overview → Evaluations** (click any question for its evidence) **→ Analytics → Reports**.

Every number is computed by the run you just started — nothing is precomputed. With the default
Sentence Transformers model the demo measured 71% → 86% pass rate (2 questions fixed, 0
regressed); exact values depend on the embedding backend.

---

## Running the app

| Command | What you get |
|---|---|
| `streamlit run app.py` | **Main app.** Landing page, dashboard and Workbench at <http://localhost:8501> |
| `uvicorn backend.api:app --reload` | REST API (<http://localhost:8000/docs>) **and** the same website at <http://localhost:8000> |
| `pytest` | Test suite (offline, ~1 minute) |

Streamlit and FastAPI use the same local storage folder, and ChromaDB's local store is not meant
to be shared by two processes. Run one of them at a time — or give the second its own storage, e.g.
`$env:CHROMA_PATH="./storage/api/chroma"; $env:DB_PATH="./storage/api/synaptiq.db"` before starting
uvicorn. SynaptiQ holds a lock on the folder, so a second process stops with a clear message.

### Pages

* **Home** — the 3D landing page.
* **Dashboard** — the evaluation dashboard (modeled on the reference video): pill navigation
  (Overview, Documents, Evaluations, Analytics, Reports), light/dark toggle with a circular reveal,
  count-up numbers, staggered card entrances and a Magic Bento overview grid.
* **Workbench** (user menu → Workbench) — native Streamlit tools: `st.file_uploader`, human review of
  generated questions in a pandas `st.data_editor`, runs with a live progress bar, raw results tables
  and Plotly charts, and run comparison.

---

## How the website is built

The landing page is built from self-contained sections (`frontend/src/landing/sections/`):
`Navbar → Hero → Problem → Loop → Showcase → Features → Diagnosis → Pipeline → TechStack → CallToAction`.

| React Bits component | Used for |
|---|---|
| **TechText** | The animated "SynaptiQ" wordmark in the hero (metrics intro, letter reveal, click-kick) |
| **ElectricLogo** | The glowing SynaptiQ logo mark above the wordmark (WebGL, interactive) |
| **ScrollFloat** | Every section heading floats in as you scroll |
| **ScrollReveal** | Section copy and the closing statement reveal word by word on scroll |
| **ScrollExpand** | A dashboard screenshot expands to full screen on scroll and reveals the three test modes |
| **TargetCursor** | The bracket cursor that locks onto cards and images across the landing page |
| **StarBorder** | Every button — landing CTAs and all dashboard buttons |
| **AccordionGallery** | Feature explanation cards (illustrated, no photos; extended with `media`/`content` slots) |
| **BounceCards** | The technology stack cards |
| **MagicBento** | The dashboard Overview grid (border glow, spotlight, click ripple) |

The 3D hero background is a custom three.js scene (`components/three/SynapseScene.jsx`): a rotating
synapse network with travelling signal pulses, pointer parallax and scroll fade.

**One UI, two hosts.** `frontend/src/bridge/transport.js` detects where it runs: inside Streamlit it
uses the component protocol (Python receives each UI action, runs it, and sends back new state); when
served by FastAPI it calls `/api/v1/ui/*`. Both paths use `backend/ui_bridge.py`.

Colours are deliberately restrained: near-black and neutral greys, one blue accent, green/red only
for pass/fail. Chart palettes were checked for colour-vision-deficiency separation and contrast.

### Rebuilding the front end (only if you change it)

Requires Node.js 18+.

```bash
npm --prefix frontend install
npm --prefix frontend run build    # writes frontend/dist, used by Streamlit and FastAPI
npm --prefix frontend run dev      # hot-reload at http://localhost:5173 (proxies /api to :8000)
```

---

## Evaluation method
