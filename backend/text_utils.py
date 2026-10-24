"""Small, dependency-free text helpers shared by chunking, metrics and generation."""

from __future__ import annotations

import re
from dataclasses import dataclass

STOPWORDS = frozenset(
    """
    a about above after again against all am an and any are as at be because been before being below between both
    but by can could did do does doing down during each few for from further had has have having he her here hers
    herself him himself his how i if in into is it its itself just me more most my myself no nor not now of off on
    once only or other our ours ourselves out over own same she should so some such than that the their theirs them
    themselves then there these they this those through to too under until up very was we were what when where which
    while who whom why will with would you your yours yourself yourselves also may must shall per via within without
    according document documents say says said tell does give given gives provide provided provides state states
    stated describe described mention mentioned many much one two us get got
    """.split()
)

_WORD_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9.%$'-]*")
_NUMBER_RE = re.compile(r"(?<![A-Za-z])\$?\d[\d,]*(?:\.\d+)?%?")
_SENTENCE_RE = re.compile(r"[^.!?\n]+(?:[.!?]+[\"')\]]*|\n|$)")
_ABSTAIN_RE = re.compile(
    r"(cannot|can't|could not|couldn't|unable to) (find|locate|answer|determine)|"
    r"not (mentioned|stated|specified|covered|included|available|found|provided) in|"
    r"no (information|evidence|mention|details?) (about|on|regarding|in)|"
    r"(do|does) not (contain|mention|say|specify|include)|insufficient (evidence|information)|"
    r"i don't know|not enough (information|evidence)",
    re.IGNORECASE,
)

ABSTAIN_ANSWER = "I cannot find this in the provided documents."


@dataclass(frozen=True)
class Sentence:
    text: str
    start: int
    end: int


def normalize_whitespace(text: str) -> str:
