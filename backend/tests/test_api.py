"""Endpoint tests for the FastAPI layer."""

import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from backend.app.api import app


class ApiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_health_returns_ok(self) -> None:
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_index_endpoint_builds_local_index(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir)
            docs_dir = workspace / "docs"
            docs_dir.mkdir()
            (docs_dir / "alpha.txt").write_text("Alpha facts live here.", encoding="utf-8")
            index_path = workspace / "index.json"

            response = self.client.post(
                "/index",
                json={"input_dir": str(docs_dir), "index_path": str(index_path)},
            )

            self.assertEqual(response.status_code, 200)
            payload = response.json()
            self.assertTrue(index_path.exists())
            self.assertEqual(payload["index_path"], str(index_path))
            self.assertGreaterEqual(payload["indexed_chunk_count"], 1)
            self.assertEqual(len(payload["indexed_chunk_ids"]), payload["indexed_chunk_count"])

    def test_index_endpoint_returns_404_for_missing_input_dir(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir)
            missing_docs_dir = workspace / "missing-docs"
            index_path = workspace / "index.json"

            response = self.client.post(
                "/index",
                json={"input_dir": str(missing_docs_dir), "index_path": str(index_path)},
            )

            self.assertEqual(response.status_code, 404)
            self.assertEqual(
                response.json()["detail"],
                f"input_dir does not exist: {missing_docs_dir}",
            )
            self.assertFalse(index_path.exists())

    def test_index_endpoint_returns_400_for_file_input_dir(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir)
            file_input_path = workspace / "not-a-directory.txt"
            file_input_path.write_text("Alpha facts live here.", encoding="utf-8")
            index_path = workspace / "index.json"

            response = self.client.post(
                "/index",
                json={"input_dir": str(file_input_path), "index_path": str(index_path)},
            )

            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                response.json()["detail"],
                f"input_dir is not a directory: {file_input_path}",
            )
            self.assertFalse(index_path.exists())

    def test_ask_endpoint_returns_grounded_answer_and_sources(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir)
            docs_dir = workspace / "docs"
            docs_dir.mkdir()
            (docs_dir / "alpha.txt").write_text("Alpha facts live here.", encoding="utf-8")
            index_path = workspace / "index.json"

            index_response = self.client.post(
                "/index",
                json={"input_dir": str(docs_dir), "index_path": str(index_path)},
            )
            self.assertEqual(index_response.status_code, 200)

            response = self.client.post(
                "/ask",
                json={"index_path": str(index_path), "query": "Alpha facts"},
            )

            self.assertEqual(response.status_code, 200)
            payload = response.json()
            self.assertIn("Alpha facts live here.", payload["answer"])
            self.assertTrue(payload["used_context"])
            self.assertTrue(any(source["source"].endswith("alpha.txt") for source in payload["sources"]))

    def test_ask_endpoint_returns_honest_failure_for_unrelated_query(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir)
            docs_dir = workspace / "docs"
            docs_dir.mkdir()
            (docs_dir / "alpha.txt").write_text("Alpha facts live here.", encoding="utf-8")
            index_path = workspace / "index.json"

            index_response = self.client.post(
                "/index",
                json={"input_dir": str(docs_dir), "index_path": str(index_path)},
            )
            self.assertEqual(index_response.status_code, 200)

            response = self.client.post(
                "/ask",
                json={"index_path": str(index_path), "query": "cat"},
            )

            self.assertEqual(response.status_code, 200)
            payload = response.json()
            self.assertFalse(payload["used_context"])
            self.assertEqual(payload["sources"], [])
            self.assertIn("could not answer from the retrieved context", payload["answer"])

    def test_ask_endpoint_validates_top_k(self) -> None:
        response = self.client.post(
            "/ask",
            json={"index_path": "index.json", "query": "Alpha facts", "top_k": 0},
        )

        self.assertEqual(response.status_code, 422)

    def test_ask_endpoint_returns_404_for_missing_index(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            missing_index_path = Path(temp_dir) / "missing-index.json"

            response = self.client.post(
                "/ask",
                json={"index_path": str(missing_index_path), "query": "Alpha facts"},
            )

            self.assertEqual(response.status_code, 404)
            self.assertEqual(
                response.json()["detail"],
                f"index_path does not exist: {missing_index_path}",
            )
