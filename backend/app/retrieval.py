"""In-memory retrieval over chunk embeddings."""

from dataclasses import dataclass
from math import sqrt

from backend.app.embeddings import EmbeddingProvider
from backend.app.models import DocumentChunk, RetrievedChunk


@dataclass(slots=True, frozen=True)
class IndexedChunk:
    """Stored chunk plus its embedding vector."""

    chunk: DocumentChunk
    embedding: list[float]


class InMemoryRetrievalStore:
    """Simple retrieval store for deterministic local tests and CLI wiring."""

    def __init__(self, embedding_provider: EmbeddingProvider) -> None:
        self._embedding_provider = embedding_provider
        self._indexed_chunks: list[IndexedChunk] = []

    def add_chunks(self, chunks: list[DocumentChunk]) -> None:
        """Embed and index new chunks in the current store."""

        if not chunks:
            return

        embeddings = self._embedding_provider.embed_texts([chunk.text for chunk in chunks])
        for chunk, embedding in zip(chunks, embeddings, strict=True):
            self._indexed_chunks.append(IndexedChunk(chunk=chunk, embedding=embedding))

    def load_indexed_chunks(self, indexed_chunks: list[IndexedChunk]) -> None:
        """Load precomputed indexed chunks into the store."""

        self._indexed_chunks.extend(indexed_chunks)

    def export_indexed_chunks(self) -> list[IndexedChunk]:
        """Return a snapshot of the indexed chunks."""

        return list(self._indexed_chunks)

    def search(self, query: str, *, top_k: int = 3) -> list[RetrievedChunk]:
        """Return the most relevant chunks for a query."""

        if top_k <= 0:
            raise ValueError("top_k must be > 0")
        if not self._indexed_chunks:
            return []

        query_embedding = self._embedding_provider.embed_texts([query])[0]
        ranked = sorted(
            (
                RetrievedChunk(
                    chunk_id=indexed.chunk.chunk_id,
                    source=indexed.chunk.source,
                    page=indexed.chunk.page,
                    chunk_index=indexed.chunk.chunk_index,
                    text=indexed.chunk.text,
                    score=_cosine_similarity(query_embedding, indexed.embedding),
                )
                for indexed in self._indexed_chunks
            ),
            key=lambda chunk: (-chunk.score, chunk.chunk_index, chunk.chunk_id),
        )
        return ranked[:top_k]


def _cosine_similarity(left: list[float], right: list[float]) -> float:
    """Return cosine similarity for two equal-length vectors."""

    if len(left) != len(right):
        raise ValueError("embedding dimensions must match")

    left_norm = sqrt(sum(value * value for value in left))
    right_norm = sqrt(sum(value * value for value in right))
    if left_norm == 0.0 or right_norm == 0.0:
        return 0.0

    dot_product = sum(left_value * right_value for left_value, right_value in zip(left, right, strict=True))
    return dot_product / (left_norm * right_norm)
