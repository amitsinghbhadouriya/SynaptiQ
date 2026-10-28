# ADR 0004: In-Memory vs Persistent Vector Index Tradeoffs

## Status
Accepted

## Context
Evaluation workloads require both rapid in-memory ephemeral test runs and persistent workspace vector indices.

## Decision
Support dual storage engines: in-memory FAISS/Numpy for CI tests, and local disk ChromaDB for production workspaces.
