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

### Three independent modes

| Mode | Input | Scored on |
|---|---|---|
| **Retriever-only** | question → retriever | Does the top-k contain the labelled evidence? |
| **Generator-only** | question + known-correct evidence (retriever bypassed) | Is the answer correct and supported? |
| **End-to-end** | question → retriever → generator | Is the final answer correct and supported by what was retrieved? |

Reference evidence is stored as **character spans** in the source document, and every chunk knows
its own offsets, so retrieval is scored exactly and stays comparable across chunking settings.

### Metrics (documented heuristics, not universal probabilities)

| Metric | Definition | Pass threshold |
|---|---|---|
| Hit@k | every evidence span ≥ 50% covered by the top-k chunks | 1.0 |
| Context recall | mean share of evidence characters covered by the top-k | — |
| Context precision | rank-aware precision of chunks that contain evidence | — |
| MRR / first evidence rank | where the first supporting chunk appears | — |
| Answer correctness | 0.65 × reference-token recall + 0.35 × semantic similarity; capped at 0.4 if a reference number is missing | ≥ 0.60 |
| Faithfulness | share of answer sentences supported by the supplied context | ≥ 0.60 |
| Answer relevancy | semantic similarity of question and answer | — |
| Abstention correctness | declines unanswerable questions, answers answerable ones | — |
| Ragas context recall | Ragas non-LLM context recall (sentence level) | — |
| Ragas string similarity | Ragas `NonLLMStringSimilarity` (answer vs reference) | — |
| Latency / cost | measured per mode; cost only when the provider reports token usage | — |

Missing or not-applicable values are stored as `null`, never as zero. Means ignore unmeasured values.
LLM-judged Ragas metrics are not wired in this build.

### Root-cause diagnosis (`backend/root_cause.py`)

| Observed evidence | Diagnosis | Next action |
|---|---|---|
| Evidence missing from top-k, generator passes with evidence | Retrieval failure | Inspect chunking, embeddings, top-k, ranking |
| Evidence retrieved, generator fails even with evidence | Generation failure | Inspect prompt, model, context handling |
| Evidence missing and end-to-end fails | Combined failure | Fix retrieval first |
| Both parts pass alone, pipeline fails | Pipeline interaction | Inspect prompt assembly and context ordering |
| Correct answer, evidence not retrieved | Correct but ungrounded | Do not treat as grounded |
| Conflicting or missing measurements | Needs review | Inspect the source and question |

Inputs are three-state (pass / fail / not measured). Unanswerable questions pass when the system
declines and are flagged as a generation failure when it answers anyway.

### Recommendations and verification

Each failure yields one concrete change, derived from its evidence: the exact rank of missing
evidence gives a top-k, partial coverage suggests larger overlapping chunks, over- or under-abstention
moves the abstention threshold, unsupported answers suggest the strict prompt. Retrieval fixes are
prioritised. **Test it** runs the change on the same question set; **Reports** compares raw metrics,
fixed and regressed questions, latency and cost, and warns about small samples or multiple changes.

---

## Using Claude (optional)

```dotenv
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=your-key
LLM_MODEL=claude-opus-5-5
LLM_EFFORT=low
```

Answers are then generated by Claude with a grounded prompt that treats document text as untrusted
data, and **Generate test set** asks Claude for questions with verbatim evidence quotes (quotes that
cannot be located in the document are discarded). The server-side refusal fallback
(`LLM_REFUSAL_FALLBACK=true`) re-runs a declined request on Anthropic's recommended model; set it to
`false` to turn it off. Cost estimates use published per-token prices or your overrides. Only send
documents you are allowed to share with a third-party API.

---

## REST API

Interactive docs at `/docs` when uvicorn is running.

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/v1/health` | Status and active backends |
| POST | `/api/v1/documents` | Upload (multipart `file`) → `document_id`, `chunk_count` |
| GET / DELETE | `/api/v1/documents[/{id}]` | List / delete (removes chunks, vectors, questions, runs) |
| POST | `/api/v1/evaluation/questions/generate` | Candidate questions (`review_required`) |
| POST | `/api/v1/evaluation/questions/import` | Import reviewed questions with evidence quotes |
| GET | `/api/v1/evaluation/datasets/{dataset_id}` | Questions, references, evidence, review status |
| PATCH | `/api/v1/evaluation/questions/{id}` | Approve / reject / edit |
| POST | `/api/v1/evaluation/runs` | Queue a run (`?wait=true` to run synchronously) |
| GET | `/api/v1/evaluation/runs[/{id}]` | Run status, aggregate metrics, per-question results |
| POST | `/api/v1/evaluation/runs/{id}/recommendation` | Run the top recommendation as a candidate |
| POST | `/api/v1/evaluation/compare` | Compare two runs (409 if question sets differ, unless `strict=false`) |
| GET | `/api/v1/evaluation/runs/{id}/export?format=csv\|json` | Export |
| POST | `/api/v1/demo` | Load the demo workspace |

Responses carry an `x-request-id`; requests are logged without document text. Add authentication,
HTTPS and rate limiting before exposing the API beyond localhost.

---

## Project structure

```text
synaptiq/
├── app.py                      # Streamlit entry point (Home, Dashboard, Workbench)
├── streamlit_ui/               # component wrapper, shared helpers, pages
├── backend/
│   ├── config.py               # settings from .env
│   ├── document_loader.py      # PDF / DOCX / TXT
│   ├── chunking.py             # sentence-aware chunks with stable IDs and offsets
│   ├── embeddings.py           # Sentence Transformers + hashing fallback
│   ├── vector_store.py         # ChromaDB + in-memory fallback
│   ├── retriever.py, generator.py, synthetic_qa.py
│   ├── metrics.py, ragas_adapter.py, evaluator.py
│   ├── root_cause.py, recommendations.py, experiments.py
│   ├── storage.py              # SQLite run history
│   ├── charts.py, reports.py   # Plotly figures, pandas tables, exports
│   ├── service.py, ui_bridge.py, process_lock.py
│   └── api.py                  # FastAPI app
├── frontend/                   # React source + pre-built dist/
├── data/sample_docs/           # sample handbook (TXT, PDF, DOCX)
├── data/evaluation_sets/       # manually reviewed test set for the demo
├── scripts/make_sample_docs.py
├── tests/                      # pytest suite
├── docs/screenshots/
├── storage/                    # created at runtime (ChromaDB, SQLite, uploads) — not committed
└── reports/                    # exports — check privacy before sharing
```

---

## Testing

```bash
pytest
```

The suite runs offline (hashing embeddings, in-memory vectors) and covers parsing of all three file
types and their error cases, chunking, retrieval scoring, the offline and Claude generator adapters
(with a fake client), metrics, every diagnosis rule, recommendations, comparisons, storage integrity,
the cross-process storage lock and the REST API end to end.

---

## Limitations

* Metrics are transparent heuristics; validate a sample of judgements manually.
* Offline test-set generation produces template questions — review them, or use Claude for better ones.
* Root-cause diagnosis is evidence-backed inference, not proof of causality.
* Small test sets give preliminary results; the comparison view says so.
* Scanned PDFs need OCR, which is out of scope.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `pip install` fails on torch/chromadb | Use Python 3.11 or 3.12 |
| Dashboard shows "Starting SynaptiQ — loading the embedding model…" for long | First run downloads the model; needs internet once |
| "Another SynaptiQ process is already using …" | Stop the other server or set separate `CHROMA_PATH` / `DB_PATH` |
| "The web UI build is missing" | `npm --prefix frontend install && npm --prefix frontend run build` |
| Embeddings show *hashing* in Environment | The model could not load (offline); results are still valid but lexical |
| Ragas shows unavailable | `pip install -r requirements.txt` (keeps the langchain-community pin) |
