"""Core domain models for the retrieval pipeline."""

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class DocumentChunk:
    """A chunk of source text preserved with retrieval metadata."""

    chunk_id: str
    source: str
    page: int | None
    chunk_index: int
    text: str

    def __post_init__(self) -> None:
        if not self.text.strip():
            raise ValueError("text must not be empty or whitespace-only")
        if self.chunk_index < 0:
            raise ValueError("chunk_index must be >= 0")
        if self.page is not None and self.page < 1:
            raise ValueError("page must be None or >= 1")


@dataclass(slots=True, frozen=True)
class RetrievedChunk(DocumentChunk):
    """A retrieved chunk with its relevance score."""

    score: float
