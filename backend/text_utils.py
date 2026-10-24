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
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", " ", text)
    text = re.sub(r"[ \t ]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _stem(token: str) -> str:
    """Very light stemmer: approve/approved/approves -> approv, policies -> policy."""
    if token.endswith("ies") and len(token) > 5:
        return token[:-3] + "y"
    for suffix in ("ing", "ed", "es", "s"):
        if len(token) > len(suffix) + 3 and token.endswith(suffix) and not token.endswith("ss"):
            token = token[: -len(suffix)]
            break
    if len(token) > 4 and token.endswith("e"):
        token = token[:-1]
    return token


def tokenize(text: str) -> list[str]:
    """Lowercased word tokens with trailing punctuation stripped."""
    tokens = []
    for match in _WORD_RE.finditer(text.lower()):
        token = match.group(0).strip(".'-")
        if token:
            tokens.append(token)
    return tokens


def content_tokens(text: str) -> list[str]:
    """Tokens without stopwords, lightly stemmed so 'policies' matches 'policy'."""
    return [_stem(t) for t in tokenize(text) if t not in STOPWORDS and len(t) > 1]


def numbers_in(text: str) -> set[str]:
    return {m.group(0).replace(",", "").rstrip(".") for m in _NUMBER_RE.finditer(text)}


def split_sentences(text: str, offset: int = 0) -> list[Sentence]:
    """Split text into sentences, keeping absolute character offsets."""
    sentences: list[Sentence] = []
    for match in _SENTENCE_RE.finditer(text):
