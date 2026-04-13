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

    return _load_utf8_document(path, expected_suffix=".txt", missing_label="text file")


def load_markdown_file(path: str | Path) -> LoadedTextDocument:
    """Load and normalize a UTF-8 markdown file from local storage."""

    return _load_utf8_document(path, expected_suffix=".md", missing_label="markdown file")


def _load_utf8_document(
    path: str | Path,
    *,
    expected_suffix: str,
    missing_label: str,
) -> LoadedTextDocument:
    """Load and normalize a UTF-8 file with a specific extension."""

    source_path = Path(path)
    if source_path.suffix.lower() != expected_suffix:
        raise ValueError(f"only {expected_suffix} files are supported")
    if not source_path.exists():
        raise FileNotFoundError(f"{missing_label} not found: {source_path}")

    text = source_path.read_text(encoding="utf-8")
    return LoadedTextDocument(source_path=str(source_path), text=normalize_whitespace(text))
