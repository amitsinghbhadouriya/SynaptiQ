# Agents & Root-Cause Intelligence

This document explains the agentic architecture inside **SynaptiQ**. 

---

## 1. The Agent Philosophy

In SynaptiQ, an **agent** is an intelligent, specialized component designed to perform one critical diagnostic task autonomously. 

Unlike systems that rely on an unpredictable LLM to guess why something failed, SynaptiQ combines **evidence-grounded reasoning**, **deterministic evaluation rules**, and **transparent heuristics**. This means:
- You always know **why** a diagnosis was made.
- You receive **verifiable facts** instead of AI hallucinations.
- Diagnoses are reproducible every single time.

---

## 2. The Three Core Agents

```
+-------------------------------------------------------------------------+
|                    1. SYNTHETIC QA GENERATION AGENT                     |
|           Extracts candidate questions, verifies verbatim quotes        |
+------------------------------------+------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                    2. ROOT-CAUSE DIAGNOSTIC AGENT                       |
|           Combines 3 modes into 1 of 7 explainable outcomes             |
+------------------------------------+------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                   3. TARGETED RECOMMENDATION AGENT                      |
|           Converts failure evidence into 1 testable parameter fix       |
+------------------------------------+------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                  4. EXPERIMENT VERIFICATION AGENT                       |
|           Executes candidate run and measures fixed vs regressed        |
+-------------------------------------------------------------------------+
```

---

## 3. Agent 1: Synthetic QA Generation Agent (`synthetic_qa.py`)

Generating a good test dataset is usually the most painful part of building a RAG application. The Synthetic QA Agent solves this:

1. **Scans Document Sections**: Identifies dense, information-rich passages across the document.
2. **Generates 4 Distinct Question Types**:
   - **Factual**: Direct facts (e.g. *"What is the standard vacation allowance?"*).
   - **Numerical**: Numbers, dates, or measurements (e.g. *"What is the maximum reimbursement cap?"*).
   - **Multi-hop**: Questions requiring information from two separate paragraphs or sections.
   - **Unanswerable**: Plausible-sounding questions that the document does **not** answer (e.g. *"What is the pet policy?"* when no pets section exists).
3. **Verbatim Evidence Verification**: Every generated question must include an exact, character-for-character quote from the source document. If a quote cannot be found verbatim in the document, it is immediately discarded.
4. **Human-in-the-Loop Review**: Questions enter a `review_required` queue where engineers can approve, edit, or reject them before benchmarking.

---

## 4. Agent 2: Root-Cause Diagnostic Agent (`root_cause.py`)

When an answer fails in production, is the retriever at fault, or did the generator make a mistake?

The Diagnostic Agent tests the system across **3 independent test modes**:
1. **Retriever-only**: Was the correct evidence present in the top-k chunks?
2. **Generator-only**: Did the generator produce a correct, faithful answer when given the known-correct evidence directly (bypassing the retriever)?
3. **End-to-end**: Did the complete pipeline produce a correct answer using what was retrieved?

The agent evaluates these 3 inputs using a three-state model (`Pass`, `Fail`, or `Not Measured`) and maps them into **7 Explainable Outcomes**:

| Outcome Code | Meaning | Plain English Diagnosis | Next Recommended Action |
|---|---|---|---|
| **`PASS`** | Success | All active test modes passed. | No action needed. System is healthy. |
| **`LIKELY_RETRIEVAL_FAILURE`** | Retrieval Miss | The generator answers correctly when given the evidence directly, but the retriever failed to find that evidence in the top-k results. | Inspect chunk size, chunk overlap, top-k, and vector embeddings. |
| **`LIKELY_GENERATION_FAILURE`** | Generator Mistake | The correct evidence was retrieved, but the generator hallucinated, contradicted the facts, or failed to answer. | Inspect the prompt instructions, LLM model choice, or temperature. |
| **`LIKELY_COMBINED_FAILURE`** | Both Failed | The retriever missed the evidence, and the generator failed the end-to-end test. | Fix retrieval first! You cannot evaluate generation without evidence. |
| **`PIPELINE_INTERACTION_FAILURE`** | Integration Issue | Both retriever and generator pass when tested in isolation, but the end-to-end pipeline fails when combined. | Inspect prompt assembly, context truncation, or the ordering of chunks. |
| **`CORRECT_BUT_UNGROUNDED`** | Lucky Guess | The final answer happened to match the reference answer, but the retrieved chunks did not actually contain the evidence. | Do not trust this answer as grounded; fix retrieval. |
| **`UNCERTAIN_REQUIRES_REVIEW`** | Insufficient Data | Conflicting metrics or missing measurements make a confident verdict impossible. | Manually review the question and source document. |

---

## 5. Agent 3: Targeted Recommendation Agent (`recommendations.py`)

Most evaluation tools show a dashboard of declining numbers and leave you guessing what to do next. The Recommendation Agent inspects the specific failure evidence of your run and produces **one single, high-probability fix**:

### Examples of Automated Reasoning:
- **Missing Top-k Rank**: If the required evidence chunk was found at rank #3, but your system was only retrieving top-1, the agent recommends:
  > *"Increase top-k from 1 to 3. The supporting chunk was ranked #3, just outside the top-1 window."*
- **Split Evidence**: If context recall is only 35% because an essential sentence was cut in half by a chunk boundary, the agent recommends:
  > *"Use larger, overlapping chunks (e.g. 1100 chars with 180 overlap). The evidence is split across boundaries."*
- **Vocabulary Mismatch**: If the retriever completely missed keywords, the agent recommends:
  > *"Try a stronger embedding model (e.g. `all-mpnet-base-v2`). The current model failed to link these semantic terms."*
- **Hallucinations on Unanswerable Queries**: If the system answered a question it should have declined, the agent recommends:
  > *"Increase abstention threshold or activate the strict grounded prompt."*

---

## 6. Agent 4: Experiment Verification Agent (`experiments.py`)

A recommendation is only a hypothesis until proven. 

The Verification Agent takes the proposed configuration change and automatically runs a **Candidate Evaluation**:
- **Identical Benchmark**: Evaluates the candidate against the exact same test questions.
- **Delta Scoring**: Measures the change in pass rate (e.g. `71% → 86%`).
- **Regression Detection**: Explicitly counts:
  - **Fixed Questions**: Questions that previously failed and now pass.
  - **Regressed Questions**: Questions that previously passed and now fail!
- **Small-Sample Warning**: Alerts you if the test set is too small to declare statistical confidence.
