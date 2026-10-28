# ⚡ Performance Tuning Playbook

- **Embedding Caching**: Enable `RetrievalLRUCache` to eliminate redundant embedding lookups.
- **Batch Processing**: Use `ThreadPoolExecutor` in `evaluate_batch.py` for concurrent evaluations.
- **Top-K Selection**: Apply dynamic top-k thresholding to minimize token consumption.
