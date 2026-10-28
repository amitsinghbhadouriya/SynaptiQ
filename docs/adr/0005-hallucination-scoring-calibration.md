# ADR 0005: Multi-Metric Hallucination Scoring Calibration

## Status
Accepted

## Context
Single-metric faithfulness scores fail on subtle contradictions or over-generalized statements.

## Decision
Combine atomic claim decomposition, NLI premise support checks, and citation span overlap into a composite index.
