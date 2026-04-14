"""Unit tests for grounded answer assembly."""

import unittest

from backend.app.answering import build_grounded_answer, format_sources
from backend.app.models import RetrievedChunk


class BuildGroundedAnswerTests(unittest.TestCase):
    def test_build_grounded_answer_regression_uses_only_top_ranked_context(self) -> None:
        chunks = [
            RetrievedChunk(
                chunk_id="chunk-1",
                source="policies.md",
                page=None,
                chunk_index=0,
                text="The support window is 30 days from purchase.",
                score=0.96,
            ),
            RetrievedChunk(
                chunk_id="chunk-2",
                source="faq.md",
                page=None,
                chunk_index=1,
                text="Refund requests must include the original order number.",
                score=0.88,
            ),
            RetrievedChunk(
                chunk_id="chunk-3",
                source="shipping.md",
                page=None,
                chunk_index=2,
                text="Standard shipping takes 5 business days.",
                score=0.73,
            ),
        ]

        answer = build_grounded_answer(chunks, min_score=0.1, max_chunks=2)

        self.assertTrue(answer.used_context)
        self.assertEqual(
            answer.answer,
            (
                "The support window is 30 days from purchase.\n\n"
                "Refund requests must include the original order number."
            ),
        )
        self.assertNotIn("Standard shipping takes 5 business days.", answer.answer)
        self.assertEqual(
            [source.chunk_id for source in answer.sources],
            ["chunk-1", "chunk-2"],
        )

    def test_build_grounded_answer_regression_limits_answer_to_top_chunk_when_max_chunks_is_one(self) -> None:
        chunks = [
            RetrievedChunk(
                chunk_id="chunk-top",
                source="policies.md",
                page=2,
                chunk_index=0,
                text="The refund window is 30 days from purchase.",
                score=0.97,
            ),
            RetrievedChunk(
                chunk_id="chunk-lower",
                source="faq.md",
                page=None,
                chunk_index=1,
                text="Refunds require the original receipt number.",
                score=0.91,
            ),
        ]

        answer = build_grounded_answer(chunks, min_score=0.1, max_chunks=1)

        self.assertTrue(answer.used_context)
        self.assertEqual(answer.answer, "The refund window is 30 days from purchase.")
        self.assertNotIn("Refunds require the original receipt number.", answer.answer)
        self.assertEqual(len(answer.sources), 1)
        self.assertEqual(answer.sources[0].chunk_id, "chunk-top")
        self.assertEqual(answer.sources[0].source, "policies.md")
        self.assertEqual(answer.sources[0].page, 2)

    def test_build_grounded_answer_joins_top_chunks_when_context_is_sufficient(self) -> None:
        chunks = [
            RetrievedChunk(
                chunk_id="chunk-1",
                source="notes.txt",
                page=None,
                chunk_index=0,
                text="First supporting paragraph.",
                score=0.91,
            ),
            RetrievedChunk(
                chunk_id="chunk-2",
                source="notes.txt",
                page=None,
                chunk_index=1,
                text="Second supporting paragraph.",
                score=0.82,
            ),
        ]

        answer = build_grounded_answer(chunks, min_score=0.1, max_chunks=2)

        self.assertTrue(answer.used_context)
        self.assertEqual(answer.answer, "First supporting paragraph.\n\nSecond supporting paragraph.")
        self.assertEqual([source.chunk_id for source in answer.sources], ["chunk-1", "chunk-2"])

    def test_build_grounded_answer_returns_honest_failure_when_context_is_insufficient(self) -> None:
        chunks = [
            RetrievedChunk(
                chunk_id="chunk-1",
                source="notes.txt",
                page=None,
                chunk_index=0,
                text="Weakly related text.",
                score=0.01,
            )
        ]

        answer = build_grounded_answer(chunks, min_score=0.1)

        self.assertFalse(answer.used_context)
        self.assertIn("could not answer from the retrieved context", answer.answer)
        self.assertEqual(answer.sources, [])

    def test_build_grounded_answer_rejects_non_positive_max_chunks(self) -> None:
        with self.assertRaisesRegex(ValueError, "max_chunks must be > 0"):
            build_grounded_answer([], max_chunks=0)


class FormatSourcesTests(unittest.TestCase):
    def test_format_sources_includes_page_when_available(self) -> None:
        lines = format_sources(
            [
                build_grounded_answer(
                    [
                        RetrievedChunk(
                            chunk_id="chunk-1",
                            source="docs/report.pdf",
                            page=4,
                            chunk_index=0,
                            text="Context",
                            score=0.9,
                        )
                    ]
                ).sources[0]
            ]
        )

        self.assertEqual(lines, ["docs/report.pdf page 4 (chunk-1)"])

    def test_format_sources_omits_page_for_non_paged_sources(self) -> None:
        lines = format_sources(
            [
                build_grounded_answer(
                    [
                        RetrievedChunk(
                            chunk_id="chunk-2",
                            source="notes.txt",
                            page=None,
                            chunk_index=0,
                            text="Context",
                            score=0.9,
                        )
                    ]
                ).sources[0]
            ]
        )

        self.assertEqual(lines, ["notes.txt (chunk-2)"])
