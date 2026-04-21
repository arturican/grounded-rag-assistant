"""Deterministic grounded answer assembly."""

import re
from dataclasses import dataclass

from backend.app.models import RetrievedChunk

_INSUFFICIENT_CONTEXT_MESSAGE = (
    "I could not answer from the retrieved context. Please index more relevant documents or refine the query."
)
_STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "at",
    "be",
    "by",
    "for",
    "from",
    "how",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "the",
    "to",
    "what",
    "when",
    "where",
    "who",
    "why",
    "with",
}


@dataclass(slots=True, frozen=True)
class AnswerSource:
    """Source reference attached to a grounded answer."""

    source: str
    page: int | None
    chunk_id: str


@dataclass(slots=True, frozen=True)
class GroundedAnswer:
    """Deterministic answer package for CLI and future API layers."""

    answer: str
    sources: list[AnswerSource]
    used_context: bool


def build_grounded_answer(
    retrieved_chunks: list[RetrievedChunk],
    *,
    min_score: float = 0.9,
    max_chunks: int = 3,
    query: str | None = None,
) -> GroundedAnswer:
    """Build a deterministic grounded answer from retrieved context only."""

    if max_chunks <= 0:
        raise ValueError("max_chunks must be > 0")
    if not retrieved_chunks or retrieved_chunks[0].score < min_score:
        return GroundedAnswer(answer=_INSUFFICIENT_CONTEXT_MESSAGE, sources=[], used_context=False)

    selected_chunks = retrieved_chunks[:max_chunks]
    if query and not _chunks_share_query_terms(query, selected_chunks):
        return GroundedAnswer(answer=_INSUFFICIENT_CONTEXT_MESSAGE, sources=[], used_context=False)

    answer_text = "\n\n".join(chunk.text for chunk in selected_chunks)
    sources = [
        AnswerSource(source=chunk.source, page=chunk.page, chunk_id=chunk.chunk_id)
        for chunk in selected_chunks
    ]
    return GroundedAnswer(answer=answer_text, sources=sources, used_context=True)


def format_sources(sources: list[AnswerSource]) -> list[str]:
    """Format grounded answer sources for CLI and test assertions."""

    formatted_sources: list[str] = []
    for source in sources:
        if source.page is None:
            formatted_sources.append(f"{source.source} ({source.chunk_id})")
            continue

        formatted_sources.append(f"{source.source} page {source.page} ({source.chunk_id})")

    return formatted_sources


def _chunks_share_query_terms(query: str, retrieved_chunks: list[RetrievedChunk]) -> bool:
    """Return whether retrieved context shares at least one meaningful term with the query."""

    query_terms = _extract_meaningful_terms(query)
    if not query_terms:
        return True

    chunk_terms = set().union(*(_extract_meaningful_terms(chunk.text) for chunk in retrieved_chunks))
    return bool(query_terms & chunk_terms)


def _extract_meaningful_terms(text: str) -> set[str]:
    """Extract lowercase query/content terms while dropping tiny tokens and common stopwords."""

    return {
        token
        for token in re.findall(r"[a-z0-9]+", text.lower())
        if len(token) >= 3 and token not in _STOPWORDS
    }
