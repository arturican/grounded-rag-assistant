"""Unit tests for retrieval storage."""

import unittest

from backend.app.embeddings import EmbeddingProvider, FakeEmbeddingProvider
from backend.app.models import DocumentChunk
from backend.app.retrieval import InMemoryRetrievalStore


class FixedEvaluationEmbeddingProvider(EmbeddingProvider):
    """Deterministic embedding map for retrieval regression checks."""

    def __init__(self, embeddings_by_text: dict[str, list[float]]) -> None:
        self._embeddings_by_text = embeddings_by_text

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        return [list(self._embeddings_by_text[text]) for text in texts]


class InMemoryRetrievalStoreTests(unittest.TestCase):
    def test_search_returns_chunks_ranked_by_similarity(self) -> None:
        store = InMemoryRetrievalStore(FakeEmbeddingProvider(dimensions=5))
        store.add_chunks(
            [
                DocumentChunk(
                    chunk_id="chunk-1",
                    source="notes.txt",
                    page=None,
                    chunk_index=0,
                    text="alpha alpha alpha",
                ),
                DocumentChunk(
                    chunk_id="chunk-2",
                    source="notes.txt",
                    page=None,
                    chunk_index=1,
                    text="beta beta beta",
                ),
            ]
        )

        results = store.search("alpha", top_k=2)

        self.assertEqual([result.chunk_id for result in results], ["chunk-1", "chunk-2"])
        self.assertGreaterEqual(results[0].score, results[1].score)

    def test_search_preserves_chunk_metadata_in_results(self) -> None:
        store = InMemoryRetrievalStore(FakeEmbeddingProvider(dimensions=5))
        store.add_chunks(
            [
                DocumentChunk(
                    chunk_id="chunk-10",
                    source="docs/report.pdf",
                    page=3,
                    chunk_index=7,
                    text="retrieved context",
                )
            ]
        )

        result = store.search("retrieved", top_k=1)[0]

        self.assertEqual(result.chunk_id, "chunk-10")
        self.assertEqual(result.source, "docs/report.pdf")
        self.assertEqual(result.page, 3)
        self.assertEqual(result.chunk_index, 7)
        self.assertEqual(result.text, "retrieved context")

    def test_search_returns_empty_list_for_empty_store(self) -> None:
        store = InMemoryRetrievalStore(FakeEmbeddingProvider(dimensions=3))

        self.assertEqual(store.search("alpha", top_k=2), [])

    def test_search_rejects_non_positive_top_k(self) -> None:
        store = InMemoryRetrievalStore(FakeEmbeddingProvider(dimensions=3))

        with self.assertRaisesRegex(ValueError, "top_k must be > 0"):
            store.search("alpha", top_k=0)

    def test_retrieval_regression_returns_expected_source_for_fixed_query(self) -> None:
        query = "which document explains grounded answers"
        fixed_embeddings = {
            query: [1.0, 0.0, 0.0],
            "Grounded answers must cite retrieved chunks and preserve source metadata.": [0.99, 0.05, 0.0],
            "Frontend polish and packaging tasks stay in a later phase.": [0.15, 0.95, 0.0],
            "Team lunch notes mention tea, bread, and apples.": [0.05, 0.1, 0.99],
        }
        store = InMemoryRetrievalStore(FixedEvaluationEmbeddingProvider(fixed_embeddings))
        store.add_chunks(
            [
                DocumentChunk(
                    chunk_id="chunk-architecture",
                    source="architecture.md",
                    page=None,
                    chunk_index=0,
                    text="Grounded answers must cite retrieved chunks and preserve source metadata.",
                ),
                DocumentChunk(
                    chunk_id="chunk-roadmap",
                    source="roadmap.md",
                    page=None,
                    chunk_index=1,
                    text="Frontend polish and packaging tasks stay in a later phase.",
                ),
                DocumentChunk(
                    chunk_id="chunk-notes",
                    source="notes.txt",
                    page=None,
                    chunk_index=2,
                    text="Team lunch notes mention tea, bread, and apples.",
                ),
            ]
        )

        results = store.search(query, top_k=2)

        self.assertEqual([result.source for result in results], ["architecture.md", "roadmap.md"])
        self.assertEqual(results[0].chunk_id, "chunk-architecture")
        self.assertGreater(results[0].score, results[1].score)
