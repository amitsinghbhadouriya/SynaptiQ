# SynaptiQ Documentation

Welcome to the **SynaptiQ** documentation library! This folder contains complete, beginner-friendly guides to help you understand, run, develop, test, and debug the SynaptiQ system.

---

## What is SynaptiQ?

**SynaptiQ** is an intelligent tool designed to test and improve **Retrieval-Augmented Generation (RAG)** systems. 

Normally, when an AI answers questions from your documents, it does two steps:
1. **The Retriever**: Searches your documents to find the most relevant pieces of information (called chunks).
2. **The Generator**: Reads those pieces of information and writes a clear, helpful answer to the user.

When the final answer is wrong, most developers do not know who made the mistake. Did the retriever fail to find the right information, or did the generator hallucinate even though the information was right in front of it?

**SynaptiQ solves this problem.** It tests both parts separately, explains the exact reason why an answer failed using real document evidence, suggests a single targeted setting to fix it, and immediately verifies if that fix improved your system.

---

## Documentation Index

Explore the documentation guides below:

| Document | Description |
|---|---|
| [**Architecture**](architecture.md) | High-level system design, frontend and backend layers, and how data moves through the app. |
| [**Design System**](design.md) | The visual look, colors, dark mode, typography, 3D hero animation, and UI components. |
| [**Database & Storage**](database.md) | How documents, text chunks, vector embeddings (ChromaDB), and run histories (SQLite) are stored. |
| [**API Reference**](api.md) | Complete guide to all REST API endpoints, request and response examples, and status codes. |
| [**Agents & Diagnostics**](agents.md) | How the automated root-cause engine, recommendation generator, and question generator work. |
| [**Project Implementation**](project_implementation.md) | Step-by-step breakdown of the complete 12-stage pipeline from document upload to report generation. |
| [**Setup & Installation**](setup.md) | Simple, step-by-step instructions to install, configure, and launch SynaptiQ on Windows, Mac, or Linux. |
| [**Feature Development**](feature_development.md) | Developer guide on how to add new metrics, new file formats, custom chunking algorithms, or UI widgets. |
| [**Authentication & Security**](authentication_and_security.md) | Privacy-first principles, local offline execution, zero data leaks, and production security tips. |
| [**Integrations**](integration.md) | How to connect SynaptiQ with Claude, OpenAI, Ollama, Hugging Face, or your own custom RAG app. |
| [**Testing & QA**](testing_and_qa.md) | Guide to the 61 automated tests, running pytest, validating benchmarks, and quality assurance. |
| [**Debugging & Troubleshooting**](debugging.md) | Solutions to common errors, port issues, Python version gotchas, and database locks. |

---

## Quick Architecture Summary

```
+-----------------------------------------------------------------------+
|                         USER INTERFACE (FRONTEND)                     |
|   React 19 + Vite   *   Tailored Dark Theme   *   3D Three.js Hero   |
|   Landing Page      *   Evaluation Dashboard  *   Streamlit Workbench |
+-----------------------------------+-----------------------------------+
                                    |
          (Streamlit Component Bridge OR FastAPI REST Calls)
                                    |
+-----------------------------------v-----------------------------------+
|                        SYNAPTIQ BACKEND CORE (PYTHON)                 |
|                                                                       |
|  [Document Loader]  -->  [Chunking Engine]  -->  [Embedding Model]   |
|    (PDF, DOCX, TXT)        (Offsets & IDs)         (SentenceTransf.)  |
|                                                                       |
|  [Retriever Engine] -->  [Generator Engine] -->  [Metrics Scorer]     |
|    (Top-k Search)          (Offline/Claude)        (Ragas + Custom)   |
|                                                                       |
|  [Root-Cause Engine] ->  [Recommendations]  -->  [Experiment Runner]  |
|    (7 Failure Modes)       (1 Targeted Fix)        (Before vs After)  |
+-----------------------------------+-----------------------------------+
                                    |
            +-----------------------+-----------------------+
            |                                               |
+-----------v-----------+                       +-----------v-----------+
|   CHROMADB VECTOR DB  |                       |   SQLITE RELATIONAL   |
|   Document Chunks     |                       |   Documents & Tests   |
|   Dense Embeddings    |                       |   Run History & Diffs |
+-----------------------+                       +-----------------------+
```

---

## Core Philosophy

1. **Evidence-Grounded**: Every evaluation is tied to exact character offsets in your source files, not vague summaries.
2. **Local-First & Offline**: Runs 100% locally on your computer with zero external API calls by default.
3. **Deterministic Diagnostics**: Uses clear, explainable logic rules rather than asking another black-box LLM to guess what went wrong.
4. **Fair Benchmarks**: Tests baseline and candidate configurations against the exact same questions and evidence spans.
