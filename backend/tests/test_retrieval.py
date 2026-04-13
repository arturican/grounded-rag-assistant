"""Unit tests for retrieval storage."""

import unittest

from backend.app.embeddings import FakeEmbeddingProvider
from backend.app.models import DocumentChunk
from backend.app.retrieval import InMemoryRetrievalStore


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
