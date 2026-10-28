# 🔍 SynaptiQ Hybrid Retrieval Architecture

SynaptiQ fuses dense semantic embeddings with BM25 lexical keyword matching using **Reciprocal Rank Fusion (RRF)**.

## Fusion Formula
$$\text{RRF Score}(d) = \sum_{m \in \{dense, sparse\}} w_m \cdot \frac{1}{k + r_m(d)}$$

- Default constant $k = 60$
- Dense weight: $0.6$
- Lexical sparse weight: $0.4$
