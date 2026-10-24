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
