"""Unit tests for local document loaders."""

import tempfile
import unittest
from pathlib import Path

from backend.app.loaders import load_document, load_markdown_file, load_text_file


class LoadTextFileTests(unittest.TestCase):
    def test_load_text_file_returns_normalized_text_and_source_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source_path = Path(temp_dir) / "notes.txt"
            source_path.write_text("  First line \r\n\r\n Second line  \r\n", encoding="utf-8")

            loaded = load_text_file(source_path)

            self.assertEqual(loaded.source_path, str(source_path))
            self.assertEqual(loaded.text, "First line\n\nSecond line")

    def test_load_text_file_raises_clear_error_for_missing_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            missing_path = Path(temp_dir) / "missing.txt"

            with self.assertRaisesRegex(FileNotFoundError, "text file not found"):
                load_text_file(missing_path)

    def test_load_text_file_rejects_non_txt_extensions(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source_path = Path(temp_dir) / "notes.md"
            source_path.write_text("markdown", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "only .txt files are supported"):
                load_text_file(source_path)


class LoadMarkdownFileTests(unittest.TestCase):
    def test_load_markdown_file_returns_normalized_text_and_source_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source_path = Path(temp_dir) / "notes.md"
            source_path.write_text("  # Title \r\n\r\n Body line  \r\n", encoding="utf-8")

            loaded = load_markdown_file(source_path)

            self.assertEqual(loaded.source_path, str(source_path))
            self.assertEqual(loaded.text, "# Title\n\nBody line")

    def test_load_markdown_file_raises_clear_error_for_missing_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            missing_path = Path(temp_dir) / "missing.md"

            with self.assertRaisesRegex(FileNotFoundError, "markdown file not found"):
                load_markdown_file(missing_path)

    def test_load_markdown_file_rejects_non_md_extensions(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source_path = Path(temp_dir) / "notes.txt"
            source_path.write_text("plain text", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, r"only \.md files are supported"):
                load_markdown_file(source_path)


class LoadDocumentTests(unittest.TestCase):
    def test_load_document_dispatches_txt_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source_path = Path(temp_dir) / "notes.txt"
            source_path.write_text("Alpha\r\n\r\nBeta", encoding="utf-8")

            loaded = load_document(source_path)

            self.assertEqual(loaded.source_path, str(source_path))
            self.assertEqual(loaded.text, "Alpha\n\nBeta")

    def test_load_document_dispatches_md_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source_path = Path(temp_dir) / "notes.md"
            source_path.write_text("# Title\r\n\r\nBody", encoding="utf-8")

            loaded = load_document(source_path)

            self.assertEqual(loaded.source_path, str(source_path))
            self.assertEqual(loaded.text, "# Title\n\nBody")

    def test_load_document_rejects_unsupported_extensions(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source_path = Path(temp_dir) / "notes.pdf"
            source_path.write_text("not really a pdf", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, r"unsupported file type: \.pdf"):
                load_document(source_path)
