"""Ingestion helpers that turn loaded documents into chunk records."""

from backend.app.chunking import split_into_chunks
from backend.app.loaders import LoadedPage, LoadedTextDocument
from backend.app.models import DocumentChunk


def build_document_chunks(
    document: LoadedTextDocument,
    *,
    chunk_size: int = 500,
    overlap: int = 50,
) -> list[DocumentChunk]:
    """Split a loaded document into ordered chunks with source attribution."""

    if document.pages is not None:
        return _build_page_aware_chunks(document, chunk_size=chunk_size, overlap=overlap)

    chunks = split_into_chunks(document.text, chunk_size=chunk_size, overlap=overlap)
    return [
        DocumentChunk(
            chunk_id=_build_chunk_id(document.source_path, None, chunk_index),
            source=document.source_path,
            page=None,
            chunk_index=chunk_index,
            text=text,
        )
        for chunk_index, text in enumerate(chunks)
    ]


def _build_page_aware_chunks(
    document: LoadedTextDocument,
    *,
    chunk_size: int,
    overlap: int,
) -> list[DocumentChunk]:
    """Build chunks for documents that preserve page metadata."""

    chunks: list[DocumentChunk] = []
    chunk_index = 0
    for page in document.pages or ():
        page_chunks = split_into_chunks(page.text, chunk_size=chunk_size, overlap=overlap)
        for text in page_chunks:
            chunks.append(
                DocumentChunk(
                    chunk_id=_build_chunk_id(document.source_path, page.page_number, chunk_index),
                    source=document.source_path,
                    page=page.page_number,
                    chunk_index=chunk_index,
                    text=text,
                )
            )
            chunk_index += 1

    return chunks


def _build_chunk_id(source_path: str, page: int | None, chunk_index: int) -> str:
    """Return a stable chunk identifier from source metadata."""

    page_part = "page-none" if page is None else f"page-{page}"
    return f"{source_path}::{page_part}::chunk-{chunk_index}"
