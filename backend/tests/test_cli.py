"""End-to-end tests for the local CLI slice."""

import io
import tempfile
import unittest
from pathlib import Path

from backend.app.cli import ask_index, index_directory, run_cli


class CliVerticalSliceTests(unittest.TestCase):
    def test_index_directory_builds_local_index_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir)
            docs_dir = workspace / "docs"
            docs_dir.mkdir()
            (docs_dir / "alpha.txt").write_text("Alpha facts live here.", encoding="utf-8")
            index_path = workspace / "index.json"

            chunk_ids = index_directory(docs_dir, index_path)

            self.assertTrue(index_path.exists())
            self.assertGreaterEqual(len(chunk_ids), 1)

    def test_ask_index_returns_grounded_answer_and_sources(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir)
            docs_dir = workspace / "docs"
            docs_dir.mkdir()
            (docs_dir / "alpha.txt").write_text("Alpha facts live here.", encoding="utf-8")
            (docs_dir / "beta.md").write_text("Beta notes stay over here.", encoding="utf-8")
            index_path = workspace / "index.json"

            index_directory(docs_dir, index_path)
            lines = ask_index(index_path, "Alpha facts")

            self.assertIn("Answer: ", lines[0])
            self.assertIn("Alpha facts live here.", lines[0])
            self.assertIn("Sources:", lines[1])
            self.assertTrue(any("alpha.txt" in line for line in lines[2:]))

    def test_run_cli_executes_index_and_ask_commands(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir)
            docs_dir = workspace / "docs"
            docs_dir.mkdir()
            (docs_dir / "alpha.txt").write_text("Alpha facts live here.", encoding="utf-8")
            index_path = workspace / "index.json"

            index_output = io.StringIO()
            ask_output = io.StringIO()

            index_exit_code = run_cli(["index", str(docs_dir), str(index_path)], stdout=index_output)
            ask_exit_code = run_cli(["ask", str(index_path), "Alpha facts"], stdout=ask_output)

            self.assertEqual(index_exit_code, 0)
            self.assertEqual(ask_exit_code, 0)
            self.assertIn("Indexed", index_output.getvalue())
            self.assertIn("Answer: Alpha facts live here.", ask_output.getvalue())
