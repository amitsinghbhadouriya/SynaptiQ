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

