# ADR 0001: Hybrid Dense and Sparse Retrieval Architecture

## Status
Accepted

## Context
Dense vector embeddings miss exact keyword queries (acronyms, model codes), while sparse BM25 misses semantic paraphrases.

## Decision
Adopt weighted Reciprocal Rank Fusion (RRF) combining dense cosine similarity with BM25 lexical scores ($k=60$).
