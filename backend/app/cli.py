"""CLI entry point for indexing and asking grounded questions."""

import argparse
from pathlib import Path
from typing import Sequence, TextIO

from backend.app.answering import build_grounded_answer, format_sources
from backend.app.embeddings import FakeEmbeddingProvider
from backend.app.index_store import load_index, save_index
from backend.app.ingestion import build_document_chunks
from backend.app.loaders import load_document
from backend.app.retrieval import InMemoryRetrievalStore

_SUPPORTED_EXTENSIONS = {".txt", ".md", ".pdf"}


def run_cli(argv: Sequence[str], *, stdout: TextIO) -> int:
    """Run the local grounded-rag CLI."""

    parser = _build_parser()
    args = parser.parse_args(list(argv))

    if args.command == "index":
        indexed_chunks = index_directory(args.input_dir, args.index_path)
        print(
            f"Indexed {len(indexed_chunks)} chunks into {args.index_path}",
            file=stdout,
        )
        return 0

    if args.command == "ask":
        answer_lines = ask_index(args.index_path, args.query)
        print("\n".join(answer_lines), file=stdout)
        return 0

    raise ValueError(f"unsupported command: {args.command}")


def index_directory(input_dir: str | Path, index_path: str | Path) -> list[str]:
    """Index all supported files in a directory into a local JSON index."""

    source_dir = Path(input_dir)
    documents = [path for path in sorted(source_dir.rglob("*")) if path.suffix.lower() in _SUPPORTED_EXTENSIONS]
    provider = FakeEmbeddingProvider()
    store = InMemoryRetrievalStore(provider)

    for document_path in documents:
        loaded = load_document(document_path)
        store.add_chunks(build_document_chunks(loaded))

    indexed_chunks = store.export_indexed_chunks()
    save_index(index_path, indexed_chunks)
    return [indexed.chunk.chunk_id for indexed in indexed_chunks]


def ask_index(index_path: str | Path, query: str) -> list[str]:
    """Answer a query from a saved local index."""

    saved_index = load_index(index_path)
    store = InMemoryRetrievalStore(FakeEmbeddingProvider())
    store.load_indexed_chunks(saved_index.indexed_chunks)
    results = store.search(query, top_k=3)
    answer = build_grounded_answer(results)

    lines = [f"Answer: {answer.answer}"]
    if answer.sources:
        lines.append("Sources:")
        lines.extend(f"- {line}" for line in format_sources(answer.sources))

    return lines


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="grounded-rag-assistant")
    subparsers = parser.add_subparsers(dest="command", required=True)

    index_parser = subparsers.add_parser("index")
    index_parser.add_argument("input_dir")
    index_parser.add_argument("index_path")

    ask_parser = subparsers.add_parser("ask")
    ask_parser.add_argument("index_path")
    ask_parser.add_argument("query")

    return parser


def main() -> int:
    """Run the CLI using standard output."""

    import sys

    return run_cli(sys.argv[1:], stdout=sys.stdout)


if __name__ == "__main__":
    raise SystemExit(main())
