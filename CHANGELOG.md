# Changelog

All notable changes to SynaptiQ are documented here.

## [1.1.0] - 2026-10-28
### Added
- Sliding-window rate limiting with 30 req/min default (`backend/rate_limiter.py`).
- Token revocation blacklist and PBKDF2 password hashing (`backend/auth.py`).
- Hybrid dense + sparse retrieval with Reciprocal Rank Fusion (`backend/hybrid_retriever.py`).
- Fine-grained claim extraction and citation attribution (`backend/claim_extractor.py`).
- Telemetry, W3C tracecontext, and Prometheus metrics exporter (`backend/metrics_collector.py`).
- CLI tooling: `doctor`, `evaluate_batch`, `benchmark_retrieval`, `generate_report`.
- Architecture Decision Records (ADRs 0001 - 0005).

### Fixed
- Intercepted and silenced Windows asyncio `WinError 10054` Proactor socket shutdown errors.
