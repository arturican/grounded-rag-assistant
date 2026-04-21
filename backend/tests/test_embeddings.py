"""Unit tests for embedding providers."""

import unittest

from backend.app.embeddings import FakeEmbeddingProvider


class FakeEmbeddingProviderTests(unittest.TestCase):
    def test_embed_texts_returns_one_vector_per_input(self) -> None:
        provider = FakeEmbeddingProvider(dimensions=3)

        embeddings = provider.embed_texts(["alpha", "beta"])

        self.assertEqual(len(embeddings), 2)
        self.assertEqual(len(embeddings[0]), 3)
        self.assertEqual(len(embeddings[1]), 3)

    def test_embed_texts_is_deterministic_for_same_input(self) -> None:
        provider = FakeEmbeddingProvider(dimensions=4)

        first = provider.embed_texts(["alpha", "alpha"])
        second = provider.embed_texts(["alpha", "alpha"])

        self.assertEqual(first, second)
        self.assertEqual(first[0], first[1])

    def test_embed_texts_uses_distinct_vectors_for_distinct_inputs(self) -> None:
        provider = FakeEmbeddingProvider(dimensions=4)

        embeddings = provider.embed_texts(["alpha", "beta"])

        self.assertNotEqual(embeddings[0], embeddings[1])

    def test_embed_texts_rejects_non_positive_dimensions(self) -> None:
        provider = FakeEmbeddingProvider(dimensions=0)

        with self.assertRaisesRegex(ValueError, "dimensions must be > 0"):
            provider.embed_texts(["alpha"])
