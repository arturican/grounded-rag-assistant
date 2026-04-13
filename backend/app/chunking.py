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
