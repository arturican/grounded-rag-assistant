"""Unit tests for text chunking helpers."""

import unittest

from backend.app.chunking import normalize_whitespace


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
