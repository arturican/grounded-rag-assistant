"""Unit tests for local document loaders."""

import tempfile
import unittest
from pathlib import Path

from backend.app.loaders import load_text_file


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
