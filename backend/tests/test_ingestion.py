"""Unit tests for ingestion helpers."""

import unittest

from backend.app.ingestion import build_document_chunks
from backend.app.loaders import LoadedPage, LoadedTextDocument


class BuildDocumentChunksTests(unittest.TestCase):
    def test_build_document_chunks_preserves_source_and_order_for_plain_text(self) -> None:
        document = LoadedTextDocument(source_path="notes/example.txt", text="Alpha\n\nBeta")

        chunks = build_document_chunks(document, chunk_size=50, overlap=10)

        self.assertEqual(len(chunks), 2)
        self.assertEqual(chunks[0].source, "notes/example.txt")
        self.assertIsNone(chunks[0].page)
        self.assertEqual(chunks[0].chunk_index, 0)
        self.assertEqual(chunks[0].text, "Alpha")
        self.assertEqual(chunks[0].chunk_id, "notes/example.txt::page-none::chunk-0")
        self.assertEqual(chunks[1].chunk_index, 1)
        self.assertEqual(chunks[1].text, "Beta")

    def test_build_document_chunks_preserves_page_numbers_for_paged_documents(self) -> None:
        document = LoadedTextDocument(
            source_path="docs/report.pdf",
            text="First page\n\nSecond page",
            pages=(
                LoadedPage(page_number=1, text="First page"),
                LoadedPage(page_number=2, text="Second page"),
            ),
        )

        chunks = build_document_chunks(document, chunk_size=50, overlap=10)

        self.assertEqual(len(chunks), 2)
        self.assertEqual(chunks[0].page, 1)
        self.assertEqual(chunks[0].chunk_index, 0)
        self.assertEqual(chunks[0].chunk_id, "docs/report.pdf::page-1::chunk-0")
        self.assertEqual(chunks[1].page, 2)
        self.assertEqual(chunks[1].chunk_index, 1)
        self.assertEqual(chunks[1].chunk_id, "docs/report.pdf::page-2::chunk-1")

    def test_build_document_chunks_splits_long_pages_with_stable_chunk_ids(self) -> None:
        document = LoadedTextDocument(
            source_path="docs/report.pdf",
            text="ABCDEFGHIJ",
            pages=(LoadedPage(page_number=3, text="ABCDEFGHIJ"),),
        )

        chunks = build_document_chunks(document, chunk_size=4, overlap=1)

        self.assertEqual([chunk.text for chunk in chunks], ["ABCD", "DEFG", "GHIJ"])
        self.assertEqual(
            [chunk.chunk_id for chunk in chunks],
            [
                "docs/report.pdf::page-3::chunk-0",
                "docs/report.pdf::page-3::chunk-1",
                "docs/report.pdf::page-3::chunk-2",
            ],
        )
