"""Local persistence for indexed chunks."""

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from backend.app.models import DocumentChunk
from backend.app.retrieval import IndexedChunk


@dataclass(slots=True, frozen=True)
class SavedIndex:
    """Serialized retrieval payload stored on disk."""

    indexed_chunks: list[IndexedChunk]


def save_index(path: str | Path, indexed_chunks: list[IndexedChunk]) -> None:
    """Persist indexed chunks to a local JSON file."""

    target_path = Path(path)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "indexed_chunks": [
            {
                "chunk": asdict(indexed.chunk),
                "embedding": indexed.embedding,
            }
            for indexed in indexed_chunks
        ]
    }
    target_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def load_index(path: str | Path) -> SavedIndex:
    """Load indexed chunks from a local JSON file."""

    source_path = Path(path)
    if not source_path.exists():
        raise FileNotFoundError(f"index file not found: {source_path}")

    payload = json.loads(source_path.read_text(encoding="utf-8"))
    indexed_chunks = [
        IndexedChunk(
            chunk=DocumentChunk(**item["chunk"]),
            embedding=[float(value) for value in item["embedding"]],
        )
        for item in payload["indexed_chunks"]
    ]
    return SavedIndex(indexed_chunks=indexed_chunks)
