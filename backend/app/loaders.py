"""Document loading helpers for local files."""

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from backend.app.chunking import normalize_whitespace


@dataclass(slots=True, frozen=True)
class LoadedPage:
    """Normalized text for one page of a paged document."""

    page_number: int
    text: str


@dataclass(slots=True, frozen=True)
class LoadedTextDocument:
    """Loaded plain-text content with its source path."""

    source_path: str
    text: str
    pages: tuple[LoadedPage, ...] | None = None


def load_document(path: str | Path) -> LoadedTextDocument:
    """Load a supported local document into the common normalized shape."""

    source_path = Path(path)
    suffix = source_path.suffix.lower()

    if suffix == ".txt":
        return load_text_file(source_path)
    if suffix == ".md":
        return load_markdown_file(source_path)
    if suffix == ".pdf":
        return load_pdf_file(source_path)

    raise ValueError(f"unsupported file type: {suffix or '<none>'}")


def load_text_file(path: str | Path) -> LoadedTextDocument:
    """Load and normalize a UTF-8 plain-text file from local storage."""

    return _load_utf8_document(path, expected_suffix=".txt", missing_label="text file")


def load_markdown_file(path: str | Path) -> LoadedTextDocument:
    """Load and normalize a UTF-8 markdown file from local storage."""

    return _load_utf8_document(path, expected_suffix=".md", missing_label="markdown file")


def load_pdf_file(
    path: str | Path,
    *,
    extractor: Callable[[Path], list[str]] | None = None,
) -> LoadedTextDocument:
    """Load PDF text through an injected page extractor."""

    source_path = Path(path)
    if source_path.suffix.lower() != ".pdf":
        raise ValueError("only .pdf files are supported")
    if not source_path.exists():
        raise FileNotFoundError(f"pdf file not found: {source_path}")
    if extractor is None:
        raise RuntimeError(f"pdf backend is unavailable: no extractor configured for file {source_path}")

    raw_pages = extractor(source_path)
    pages = tuple(
        LoadedPage(page_number=index + 1, text=normalize_whitespace(page_text))
        for index, page_text in enumerate(raw_pages)
    )
    combined_text = "\n\n".join(page.text for page in pages if page.text)
    return LoadedTextDocument(source_path=str(source_path), text=combined_text, pages=pages)


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
