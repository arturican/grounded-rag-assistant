"""Unit tests for text chunking helpers."""

import unittest

from backend.app.chunking import normalize_whitespace, split_into_chunks, split_into_paragraphs


class NormalizeWhitespaceTests(unittest.TestCase):
    def test_normalize_whitespace_normalizes_line_endings_and_trims_lines(self) -> None:
        text = "\r\n  First line  \r\nSecond line\t \r\n\r\n   Third line  \r"

        normalized = normalize_whitespace(text)

        self.assertEqual(normalized, "First line\nSecond line\n\nThird line")

    def test_normalize_whitespace_collapses_multiple_blank_lines(self) -> None:
        text = "Alpha\n\n \n\t\nBeta"

        normalized = normalize_whitespace(text)

        self.assertEqual(normalized, "Alpha\n\nBeta")

    def test_normalize_whitespace_returns_empty_string_for_whitespace_only_input(self) -> None:
        normalized = normalize_whitespace(" \n\t\r\n ")

        self.assertEqual(normalized, "")

    def test_normalize_whitespace_preserves_single_newlines(self) -> None:
        text = "Alpha\nBeta\nGamma"

        normalized = normalize_whitespace(text)

        self.assertEqual(normalized, "Alpha\nBeta\nGamma")


class SplitIntoParagraphsTests(unittest.TestCase):
    def test_split_into_paragraphs_returns_empty_list_for_empty_input(self) -> None:
        paragraphs = split_into_paragraphs(" \n\t\r\n ")

        self.assertEqual(paragraphs, [])

    def test_split_into_paragraphs_returns_single_paragraph(self) -> None:
        paragraphs = split_into_paragraphs("  Alpha line  \nBeta line  ")

        self.assertEqual(paragraphs, ["Alpha line\nBeta line"])

    def test_split_into_paragraphs_returns_multiple_paragraphs_in_order(self) -> None:
        text = " First paragraph \r\n\r\n Second paragraph \n\n\n Third paragraph "

        paragraphs = split_into_paragraphs(text)

        self.assertEqual(
            paragraphs,
            ["First paragraph", "Second paragraph", "Third paragraph"],
        )


class SplitIntoChunksTests(unittest.TestCase):
    def test_split_into_chunks_keeps_short_paragraphs_unchanged(self) -> None:
        text = "Alpha paragraph.\n\nBeta paragraph."

        chunks = split_into_chunks(text, chunk_size=50, overlap=10)

        self.assertEqual(chunks, ["Alpha paragraph.", "Beta paragraph."])

    def test_split_into_chunks_splits_long_paragraph_with_overlap(self) -> None:
        text = "ABCDEFGHIJ"

        chunks = split_into_chunks(text, chunk_size=4, overlap=1)

        self.assertEqual(chunks, ["ABCD", "DEFG", "GHIJ"])

    def test_split_into_chunks_preserves_paragraph_order_when_only_some_are_split(self) -> None:
        text = "Hey\n\nABCDEFGHIJ"

        chunks = split_into_chunks(text, chunk_size=4, overlap=1)

        self.assertEqual(chunks, ["Hey", "ABCD", "DEFG", "GHIJ"])

    def test_split_into_chunks_rejects_overlap_equal_to_chunk_size(self) -> None:
        with self.assertRaisesRegex(ValueError, "overlap must be smaller than chunk_size"):
            split_into_chunks("Alpha", chunk_size=5, overlap=5)
