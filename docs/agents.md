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
