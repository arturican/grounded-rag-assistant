"""Deterministic grounded answer assembly."""

from dataclasses import dataclass

from backend.app.models import RetrievedChunk

_INSUFFICIENT_CONTEXT_MESSAGE = (
    "I could not answer from the retrieved context. Please index more relevant documents or refine the query."
)


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
    min_score: float = 0.05,
    max_chunks: int = 3,
) -> GroundedAnswer:
    """Build a deterministic grounded answer from retrieved context only."""

    if max_chunks <= 0:
        raise ValueError("max_chunks must be > 0")
    if not retrieved_chunks or retrieved_chunks[0].score < min_score:
        return GroundedAnswer(answer=_INSUFFICIENT_CONTEXT_MESSAGE, sources=[], used_context=False)

    selected_chunks = retrieved_chunks[:max_chunks]
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
