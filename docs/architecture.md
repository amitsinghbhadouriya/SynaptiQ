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
