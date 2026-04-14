"""Regression checks for the sample evaluation dataset."""

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from backend.app.cli import ask_index, index_directory


REPO_ROOT = Path(__file__).resolve().parents[2]
SAMPLE_DOCS_ROOT = REPO_ROOT / "sample_docs"
TEXT_ONLY_ROOT = SAMPLE_DOCS_ROOT / "text_only"
EVALUATION_DOC = REPO_ROOT / "docs" / "EVALUATION_DATASET.md"


class EvaluationDatasetTests(unittest.TestCase):
    """Ensure the evaluation dataset remains present and usable."""

    def test_sample_corpus_contains_expected_formats(self) -> None:
        sample_files = sorted(path.relative_to(SAMPLE_DOCS_ROOT) for path in SAMPLE_DOCS_ROOT.rglob("*") if path.is_file())

        self.assertEqual(
            sample_files,
            [
                Path("reference/facility_guide.pdf"),
                Path("text_only/operations_handbook.txt"),
                Path("text_only/release_plan.md"),
                Path("text_only/support_playbook.txt"),
            ],
        )

    def test_dataset_document_lists_all_questions(self) -> None:
        contents = EVALUATION_DOC.read_text(encoding="utf-8")

        for question_number in range(1, 11):
            self.assertIn(f"### Q{question_number}.", contents)

    def test_text_only_subset_is_usable_with_current_cli(self) -> None:
        with TemporaryDirectory() as temp_dir:
            index_path = Path(temp_dir) / "sample-index.json"

            indexed_chunk_ids = index_directory(TEXT_ONLY_ROOT, index_path)
            answer_lines = ask_index(index_path, "Where should billing questions be routed?")

        self.assertGreater(len(indexed_chunk_ids), 0)
        self.assertTrue(any("finance-ops@lighthouse.example" in line for line in answer_lines))
        self.assertTrue(any("support_playbook.txt" in line for line in answer_lines))

    def test_unrelated_question_fails_honestly_for_dataset_q10(self) -> None:
        with TemporaryDirectory() as temp_dir:
            index_path = Path(temp_dir) / "sample-index.json"

            index_directory(TEXT_ONLY_ROOT, index_path)
            answer_lines = ask_index(index_path, "What is the company travel reimbursement limit?")

        self.assertTrue(
            any("I could not answer from the retrieved context" in line for line in answer_lines)
        )
        self.assertFalse(any(line.startswith("- ") for line in answer_lines))
