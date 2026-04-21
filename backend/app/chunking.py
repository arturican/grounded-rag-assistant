"""Text normalization helpers for chunking."""

import re

_MULTI_BLANK_LINES_PATTERN = re.compile(r"\n[ \t]*(?:\n[ \t]*)+")
_PARAGRAPH_SEPARATOR = "\n\n"


def normalize_whitespace(text: str) -> str:
    """Normalize line endings and paragraph spacing for plain-text chunking."""

    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    stripped_lines = [line.strip() for line in normalized.split("\n")]
    collapsed_lines = "\n".join(stripped_lines)
    collapsed_paragraphs = _MULTI_BLANK_LINES_PATTERN.sub("\n\n", collapsed_lines)
    return collapsed_paragraphs.strip()


def split_into_paragraphs(text: str) -> list[str]:
    """Split plain text into ordered paragraph strings."""

    normalized = normalize_whitespace(text)
    if not normalized:
        return []

    return [paragraph for paragraph in normalized.split(_PARAGRAPH_SEPARATOR) if paragraph]


def split_into_chunks(
    text: str,
    *,
    chunk_size: int = 500,
    overlap: int = 50,
) -> list[str]:
    """Split text into ordered chunks, falling back to overlapping slices for long paragraphs."""

    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")
    if overlap < 0:
        raise ValueError("overlap must be >= 0")
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks: list[str] = []
    for paragraph in split_into_paragraphs(text):
        if len(paragraph) <= chunk_size:
            chunks.append(paragraph)
            continue

        chunks.extend(_split_long_paragraph(paragraph, chunk_size=chunk_size, overlap=overlap))

    return chunks


def _split_long_paragraph(paragraph: str, *, chunk_size: int, overlap: int) -> list[str]:
    """Split one long paragraph into overlapping character windows."""

    step = chunk_size - overlap
    chunks: list[str] = []

    for start in range(0, len(paragraph), step):
        chunk = paragraph[start : start + chunk_size]
        if not chunk:
            continue

        chunks.append(chunk)
        if start + chunk_size >= len(paragraph):
            break

    return chunks
