# Project Brief

## One-line summary

A grounded RAG assistant that answers questions using only the user's indexed documents and returns sources.

## User value

The user uploads documents and gets fast, source-backed answers instead of manually searching through files.

## Target audience

- individual professionals
- students and researchers
- small teams with internal documents
- portfolio reviewers evaluating AI engineering skills

## Non-goals for MVP

- multi-tenant enterprise auth
- cloud-scale indexing
- advanced hybrid search
- OCR-heavy scanned PDF support
- polished production UI

## MVP requirements

1. load documents from local storage
2. extract text from supported formats
3. split text into chunks with overlap
4. generate embeddings
5. store vectors and metadata
6. retrieve relevant chunks by query
7. generate an answer only from retrieved context
8. return sources with file and page metadata when available
9. fail honestly when the answer is not present in context

## Success criteria

- a small sample corpus can be indexed end-to-end
- questions return grounded answers with sources
- missing-answer cases are handled explicitly
- core logic is covered by tests
- another developer or agent can continue work from repository docs alone

## Initial architecture

- ingestion layer
- parsing layer
- chunking layer
- embedding layer
- vector index layer
- retrieval layer
- answer generation layer
- API layer later

## Core principle

Grounding is more important than sounding smart.
