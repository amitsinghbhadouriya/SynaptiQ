# System Architecture

This document explains the overall architecture of **SynaptiQ** in simple, plain English. You will learn how the frontend and backend talk to each other, how data flows through the application, and how each component is organized.

---

## 1. High-Level Overview

SynaptiQ is built around a **dual-host, decoupled architecture**:
- **Frontend**: A modern Single Page Application (SPA) built with **React 19** and **Vite**, featuring rich 3D graphics, smooth scroll animations, and an interactive evaluation dashboard.
- **Backend**: A robust **Python 3.11/3.12** engine that loads documents, creates vector embeddings, tests retrieval and generation, scores metrics, and diagnoses failures.
- **Dual-Host Support**: The exact same React frontend can be served in two ways:
  1. **Streamlit mode** (`streamlit run app.py`): Streamlit hosts the React app inside an embedded iframe component, and provides a native Python Workbench page.
  2. **FastAPI mode** (`uvicorn backend.api:app`): FastAPI serves the React app as static files from `frontend/dist` and provides a production-grade REST API at `/api/v1/*`.

```
                    +-----------------------------+
                    |        Web Browser          |
                    |   (React 19 Landing/UI)     |
                    +--------------+--------------+
                                   |
         +-------------------------+-------------------------+
         |                                                   |
 (Inside Streamlit)                                  (Inside FastAPI)
         |                                                   |
         v                                                   v
+-------------------------+                         +-------------------------+
|     Streamlit Host      |                         |      FastAPI Host       |
|  (streamlit_ui/comp.py) |                         |    (backend/api.py)     |
+------------+------------+                         +------------+------------+
             |                                                   |
             +-------------------------+-------------------------+
                                       |
                                       v
                        +-----------------------------+
                        |      Backend Service        |
                        |    (backend/service.py)     |
                        +--------------+--------------+
                                       |
        +------------------------------+------------------------------+
        |                              |                              |
        v                              v                              v
+---------------+              +---------------+              +---------------+
| ChromaDB      |              | SQLite        |              | Local Files   |
| (Vector Store)|              | (Run History) |              | (PDF/DOCX/TXT)|
+---------------+              +---------------+              +---------------+
```

---

## 2. Frontend Layer (`frontend/`)

The frontend is clean, modular, and fast:

### Technologies Used
- **React 19**: Modern UI rendering with React hooks.
- **Vite**: Ultra-fast build tool and bundler.
- **Three.js**: Interactive 3D synapse network background in the hero section.
- **GSAP**: Smooth timeline-based animations for cards and transitions.
- **Lucide Icons**: Crisp, lightweight vector iconography.

### Major Sections & Pages
1. **Landing Page (`frontend/src/landing/`)**:
   - `Navbar`: Floating glassmorphism navbar with brand mark and section shortcuts.
   - `Hero`: 3D interactive Three.js synapse scene, glowing brand logo, dynamic wordmark with cybernetic animated **"Q"**, and quick facts.
   - `Problem`: Interactive Failure Autopsy that shows side-by-side comparisons of Retriever failures, Generator hallucinations, and pipeline breakdown.
   - `Loop`: 4-step cyclical workflow (Ingest & Chunk $\to$ Test 3 Modes $\to$ Diagnose $\to$ Recommend & Verify).
   - `Showcase`: Interactive dashboard preview with fixed height and zoom preview.
   - `Features`: 8 key feature cards with generated futuristic artwork and GSAP tilt physics.
   - `Diagnosis`: Visual matrix showing the 7 explainable outcomes.
   - `Pipeline`: 12-step engineering roadmap detailing every stage from document loading to report export.
   - `TechStack`: Interactive bouncy cards with authentic technology logos (Python, Streamlit, FastAPI, ChromaDB, etc.).
   - `CallToAction & Footer`: Final launch actions and copyright details.

2. **Dashboard (`frontend/src/dashboard/`)**:
   - `Overview`: High-level summary of the latest baseline vs candidate runs, pass rates, and key metrics.
   - `Documents`: File index, parsed sections, and chunk lists.
   - `Evaluations`: Question-by-question view with exact evidence highlight drawer.
   - `Analytics`: Interactive charts (metric distributions, rank vs recall, radar charts).
   - `Reports`: Comparative before-and-after tables, export to CSV/JSON, and regression warnings.

---

## 3. Communication Bridge (`frontend/src/bridge/` & `backend/ui_bridge.py`)

A key innovation of SynaptiQ is **host transparency**:
- When running inside **Streamlit**, the frontend communicates with Python using the Streamlit Custom Component protocol (`window.parent.postMessage`).
- When running inside **FastAPI**, the frontend sends standard HTTP POST/GET requests to `/api/v1/ui/*`.
- Both transport pathways route directly into `backend/ui_bridge.py`, meaning the frontend never needs two different codebases.

---

## 4. Backend Core Modules (`backend/`)

| Module | What It Does (Plain English) |
|---|---|
| **`document_loader.py`** | Reads PDF (PyMuPDF), DOCX (python-docx), and TXT files. Extracts clean text and remembers page numbers and character boundaries. |
| **`chunking.py`** | Cuts long text into smaller pieces (chunks) without breaking sentences. Assigns a unique, stable ID to every chunk. |
| **`embeddings.py`** | Converts text into mathematical vectors using Sentence Transformers (`all-MiniLM-L6-v2`). Falls back to deterministic hash vectors if offline. |
| **`vector_store.py`** | Manages local ChromaDB vector storage. Stores chunk vectors and metadata, and finds top matching chunks using cosine similarity. |
| **`retriever.py`** | Executes the search for relevant chunks given a user's question. |
| **`generator.py`** | Produces answers. Runs in **offline extractive mode** by default (finding answers directly in context), or calls Anthropic Claude if configured. |
| **`metrics.py`** | Scores answers: Hit@k, Context Recall, Context Precision, Answer Correctness, Faithfulness, and Abstention. |
| **`ragas_adapter.py`** | Connects to the Ragas evaluation library to calculate non-LLM sentence-level string similarity and context recall. |
| **`evaluator.py`** | Runs the 3 independent evaluation modes: Retriever-only, Generator-only, and End-to-end. |
| **`root_cause.py`** | Analyzes the results of the 3 modes to determine exactly why a question failed (Retrieval failure, Generation failure, etc.). |
| **`recommendations.py`** | Looks at failure evidence and generates exactly one targeted setting adjustment to test. |
| **`experiments.py`** | Compares a Baseline run with a Candidate run to detect improvements and regressions. |
| **`storage.py`** | SQLite relational database manager for documents, questions, runs, and results. |
| **`process_lock.py`** | Prevents data corruption by ensuring only one process accesses the database files at a time. |

---

## 5. End-to-End Data Flow

Here is how data flows from document upload to final report:

```
[User Uploads PDF]
       |
       v
[document_loader.py] ------> Extracts raw text, preserves page numbers
       |
       v
[chunking.py] -------------> Creates overlapping sentence chunks (e.g., 700 chars / 100 overlap)
       |
       v
[embeddings.py] -----------> Converts each chunk to a dense 384-dimensional vector
       |
       v
[vector_store.py] ---------> Stores chunks & vectors into ChromaDB
       |
       v
[synthetic_qa.py] ---------> Generates verified test questions with exact evidence quotes
       |
       v
[evaluator.py] ------------> Tests all 3 modes (Retriever, Generator, End-to-End)
       |
       v
[metrics.py] --------------> Computes transparent scores (Hit@k, Recall, Faithfulness, Correctness)
       |
       v
[root_cause.py] -----------> Diagnoses failures into 1 of 7 clear, explainable outcomes
       |
       v
[recommendations.py] ------> Suggests 1 parameter fix (e.g., "Increase top-k from 1 to 2")
       |
       v
[experiments.py] ----------> Runs candidate test and compares against baseline
       |
       v
[Dashboard UI] ------------> Displays interactive metrics, charts, and downloadable reports
```
