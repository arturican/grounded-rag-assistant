"""Document loading helpers for local files."""

from dataclasses import dataclass
from pathlib import Path

from backend.app.chunking import normalize_whitespace


@dataclass(slots=True, frozen=True)
class LoadedTextDocument:
    """Loaded plain-text content with its source path."""

    source_path: str
    text: str


def load_text_file(path: str | Path) -> LoadedTextDocument:
    """Load and normalize a UTF-8 plain-text file from local storage."""

    source_path = Path(path)
    if source_path.suffix.lower() != ".txt":
        raise ValueError("only .txt files are supported")
    if not source_path.exists():
        raise FileNotFoundError(f"text file not found: {source_path}")

    text = source_path.read_text(encoding="utf-8")
    return LoadedTextDocument(
        source_path=str(source_path),
        text=normalize_whitespace(text),
    )
