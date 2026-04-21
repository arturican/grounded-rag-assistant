"""End-to-end tests for the local CLI slice."""

import io
import json
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

    def test_run_cli_hides_sources_for_unrelated_query(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir)
            docs_dir = workspace / "docs"
            docs_dir.mkdir()
            (docs_dir / "alpha.txt").write_text("Alpha facts live here.", encoding="utf-8")
            index_path = workspace / "index.json"

            index_output = io.StringIO()
            ask_output = io.StringIO()

            index_exit_code = run_cli(["index", str(docs_dir), str(index_path)], stdout=index_output)
            ask_exit_code = run_cli(
                ["ask", str(index_path), "cat"],
                stdout=ask_output,
            )

            rendered_output = ask_output.getvalue()

            self.assertEqual(index_exit_code, 0)
            self.assertEqual(ask_exit_code, 0)
            self.assertIn(
                "Answer: I could not answer from the retrieved context.",
                rendered_output,
            )
            self.assertNotIn("Sources:", rendered_output)

    def test_run_cli_renders_page_numbers_in_sources_block(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir)
            docs_dir = workspace / "docs"
            docs_dir.mkdir()
            (docs_dir / "alpha.txt").write_text("Alpha facts live here.", encoding="utf-8")
            source_path = docs_dir / "paged.pdf"
            index_path = workspace / "index.json"

            index_directory(docs_dir, index_path)

            saved_index = json.loads(index_path.read_text(encoding="utf-8"))
            paged_chunk = saved_index["indexed_chunks"][0]["chunk"]
            paged_chunk["source"] = str(source_path)
            paged_chunk["page"] = 7
            paged_chunk["chunk_id"] = f"{source_path}::page-7::chunk-0"
            index_path.write_text(
                json.dumps(saved_index, indent=2) + "\n",
                encoding="utf-8",
            )

            ask_output = io.StringIO()
            exit_code = run_cli(["ask", str(index_path), "Alpha facts"], stdout=ask_output)
            rendered_lines = ask_output.getvalue().splitlines()
            expected_source_line = f"- {source_path} page 7 ({source_path}::page-7::chunk-0)"

            self.assertEqual(exit_code, 0)
            self.assertIn("Sources:", rendered_lines)
            self.assertIn(expected_source_line, rendered_lines)

    def test_run_cli_renders_non_paged_sources_without_page_suffix_regression(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir)
            docs_dir = workspace / "docs"
            docs_dir.mkdir()
            (docs_dir / "alpha.txt").write_text("Alpha facts live here.", encoding="utf-8")
            source_path = docs_dir / "alpha.txt"
            index_path = workspace / "index.json"

            index_directory(docs_dir, index_path)

            ask_output = io.StringIO()
            exit_code = run_cli(["ask", str(index_path), "Alpha facts"], stdout=ask_output)
            rendered_lines = ask_output.getvalue().splitlines()

            # For non-paged sources (txt), format_sources returns "{source} ({chunk_id})"
            # and cli.py adds the "- " prefix for each line in the Sources: block.
            expected_source_line = f"- {source_path} ({source_path}::page-none::chunk-0)"

            self.assertEqual(exit_code, 0)
            self.assertIn("Sources:", rendered_lines)
            self.assertIn(expected_source_line, rendered_lines)
            self.assertFalse(any("page None" in line for line in rendered_lines))

    def test_run_cli_returns_tied_sources_in_stable_order_regression(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir)
            docs_dir = workspace / "docs"
            docs_dir.mkdir()
            shared_text = "Shared tie facts live here."
            first_source = docs_dir / "alpha.txt"
            second_source = docs_dir / "beta.txt"
            first_source.write_text(shared_text, encoding="utf-8")
            second_source.write_text(shared_text, encoding="utf-8")
            index_path = workspace / "index.json"

            index_directory(docs_dir, index_path)

            ask_output = io.StringIO()
            exit_code = run_cli(["ask", str(index_path), shared_text], stdout=ask_output)
            rendered_lines = ask_output.getvalue().splitlines()
            first_source_line = f"- {first_source} ({first_source}::page-none::chunk-0)"
            second_source_line = f"- {second_source} ({second_source}::page-none::chunk-0)"

            self.assertEqual(exit_code, 0)
            self.assertIn("Sources:", rendered_lines)
            self.assertIn(first_source_line, rendered_lines)
            self.assertIn(second_source_line, rendered_lines)
            self.assertLess(
                rendered_lines.index(first_source_line),
                rendered_lines.index(second_source_line),
            )
