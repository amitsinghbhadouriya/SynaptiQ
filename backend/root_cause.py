"""Transparent, rule-based root-cause diagnosis.

Inputs are three-state (True = pass, False = fail, None = not measured). Missing
measurements are never treated as failures; when evidence is insufficient the
diagnosis is UNCERTAIN_REQUIRES_REVIEW. A diagnosis is a likely cause backed by
evidence, not proof of causality.
"""

from __future__ import annotations

from dataclasses import dataclass, field

LABELS = {
    "PASS": "Pass",
    "LIKELY_RETRIEVAL_FAILURE": "Retrieval failure",
    "LIKELY_GENERATION_FAILURE": "Generation failure",
    "LIKELY_COMBINED_FAILURE": "Combined failure",
    "PIPELINE_INTERACTION_FAILURE": "Pipeline interaction",
    "CORRECT_BUT_UNGROUNDED": "Correct but ungrounded",
    "UNCERTAIN_REQUIRES_REVIEW": "Needs review",
}

NEXT_ACTIONS = {
    "PASS": "No action needed.",
    "LIKELY_RETRIEVAL_FAILURE": "Inspect chunking, the embedding model, top-k and ranking.",
    "LIKELY_GENERATION_FAILURE": "Inspect the prompt, the model and how the context is used.",
    "LIKELY_COMBINED_FAILURE": "Fix retrieval first, then repeat the generation and end-to-end tests.",
    "PIPELINE_INTERACTION_FAILURE": "Inspect prompt construction, context ordering and context length.",
    "CORRECT_BUT_UNGROUNDED": "Do not treat the answer as evidence-grounded; inspect retrieval.",
    "UNCERTAIN_REQUIRES_REVIEW": "Inspect the source passage and the test question manually.",
}


@dataclass
class Diagnosis:
    code: str
    reason: str
    evidence: list[str] = field(default_factory=list)

    @property
    def label(self) -> str:
        return LABELS[self.code]

    @property
    def next_action(self) -> str:
        return NEXT_ACTIONS[self.code]


def diagnose(
    retrieval_supported: bool | None,
    generator_passed: bool | None,
    end_to_end_passed: bool | None,
    *,
    answerable: bool = True,
    end_to_end_correct: bool | None = None,
    notes: list[str] | None = None,
) -> Diagnosis:
    """Combine the three independent test results into a likely diagnosis."""
    notes = list(notes or [])

    if not answerable:
        # Unanswerable questions: the right behaviour is to abstain.
        if end_to_end_passed is True and generator_passed is not False:
            return Diagnosis("PASS", "The system correctly declined a question the document cannot answer.", notes)
        if end_to_end_passed is False or generator_passed is False:
            return Diagnosis(
                "LIKELY_GENERATION_FAILURE",
                "The question is unanswerable from the document, but the generator produced an answer instead of "
                "declining — a hallucination risk.",
                notes,
            )
        return Diagnosis("UNCERTAIN_REQUIRES_REVIEW", "Not enough measurements to judge abstention.", notes)

    if retrieval_supported is False and end_to_end_correct is True:
        return Diagnosis(
            "CORRECT_BUT_UNGROUNDED",
            "The final answer matches the reference, but the retrieved chunks do not contain the reference "
            "evidence, so the answer is not grounded in the right source.",
            notes,
        )
    if retrieval_supported is False and generator_passed is True:
        return Diagnosis(
            "LIKELY_RETRIEVAL_FAILURE",
            "The generator answers correctly when given the reference evidence directly, but the retriever did "
            "not return that evidence in the top-k results.",
            notes,
        )
    if retrieval_supported is True and generator_passed is False:
        return Diagnosis(
            "LIKELY_GENERATION_FAILURE",
            "The supporting evidence was retrieved, and even with the reference evidence supplied directly the "
            "generator's answer was incorrect or unsupported.",
            notes,
        )
    if retrieval_supported is False and end_to_end_passed is False:
        return Diagnosis(
            "LIKELY_COMBINED_FAILURE",
            "The retriever missed the reference evidence and the end-to-end answer failed"
            + (" — the generator also failed with the evidence supplied." if generator_passed is False else "."),
            notes,
        )
    if retrieval_supported is True and generator_passed is True:
        if end_to_end_passed is False:
            return Diagnosis(
                "PIPELINE_INTERACTION_FAILURE",
                "Retrieval found the evidence and the generator succeeds with clean evidence, yet the combined "
                "pipeline failed — extra retrieved context or prompt assembly likely interfered.",
                notes,
            )
        if end_to_end_passed is True:
            return Diagnosis("PASS", "Retrieval, generation and the end-to-end answer all passed.", notes)
    return Diagnosis(
        "UNCERTAIN_REQUIRES_REVIEW",
        "The measurements conflict or are incomplete; the reference answer or evidence may be ambiguous.",
        notes,
    )

def compute_claim_attribution_summary(claims: list) -> dict:
    """Helper summarizing proposition support for diagnostic reports."""
    supported = sum(1 for c in claims if getattr(c, 'is_supported', False))
    return {"total": len(claims), "supported": supported, "unsupported": len(claims) - supported}
