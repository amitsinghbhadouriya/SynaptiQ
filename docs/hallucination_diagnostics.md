# 🔬 Hallucination Diagnostics & Attribution Methodology

SynaptiQ identifies hallucinations by decomposing generated RAG answers into atomic claims and checking premise support.

## Pipeline Steps
1. **Proposition Split**: Decomposes text into discrete atomic claims (`backend/claim_extractor.py`).
2. **Entailment Verification**: Matches claims with retrieved context chunks using lexical entailment heuristics (`backend/entailment_checker.py`).
3. **Severity Calculation**: Computes the Hallucination Index ($H = \frac{\text{unsupported}}{\text{total}}$).
4. **Attribution Heatmap**: Maps token-level citation weights for UI visualization.
