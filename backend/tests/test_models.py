"""Unit tests for core domain models."""

import unittest

from backend.app.models import DocumentChunk, RetrievedChunk


class DocumentChunkTests(unittest.TestCase):
    def test_document_chunk_accepts_valid_data(self) -> None:
        chunk = DocumentChunk(
            chunk_id="chunk-1",
            source="notes/example.txt",
            page=1,
            chunk_index=0,
            text="Grounded answers start with grounded chunks.",
        )

        self.assertEqual(chunk.chunk_id, "chunk-1")
        self.assertEqual(chunk.source, "notes/example.txt")
        self.assertEqual(chunk.page, 1)
        self.assertEqual(chunk.chunk_index, 0)
        self.assertEqual(chunk.text, "Grounded answers start with grounded chunks.")

    def test_document_chunk_rejects_empty_text(self) -> None:
        with self.assertRaisesRegex(ValueError, "text must not be empty or whitespace-only"):
            DocumentChunk(
                chunk_id="chunk-invalid",
                source="notes/example.txt",
                page=None,
                chunk_index=0,
                text="",
            )

    def test_document_chunk_rejects_whitespace_only_text(self) -> None:
        with self.assertRaisesRegex(ValueError, "text must not be empty or whitespace-only"):
            DocumentChunk(
                chunk_id="chunk-invalid",
                source="notes/example.txt",
                page=None,
                chunk_index=0,
                text="   \n\t",
            )

    def test_document_chunk_rejects_negative_chunk_index(self) -> None:
        with self.assertRaisesRegex(ValueError, "chunk_index must be >= 0"):
            DocumentChunk(
                chunk_id="chunk-invalid",
                source="notes/example.txt",
                page=None,
                chunk_index=-1,
                text="Valid text",
            )

    def test_document_chunk_rejects_invalid_page(self) -> None:
        with self.assertRaisesRegex(ValueError, "page must be None or >= 1"):
            DocumentChunk(
                chunk_id="chunk-invalid",
                source="notes/example.txt",
                page=0,
                chunk_index=0,
                text="Valid text",
            )


class RetrievedChunkTests(unittest.TestCase):
    def test_retrieved_chunk_includes_score(self) -> None:
        chunk = RetrievedChunk(
            chunk_id="chunk-2",
            source="notes/example.txt",
            page=None,
            chunk_index=2,
            text="Relevant context",
            score=0.87,
        )

        self.assertEqual(chunk.chunk_id, "chunk-2")
        self.assertIsNone(chunk.page)
        self.assertEqual(chunk.score, 0.87)
