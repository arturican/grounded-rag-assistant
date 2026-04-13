# Next Step

## Current milestone

Phase 5 - Chunk preparation

## Task

Build `DocumentChunk` objects from loaded documents.

## Files to update

- `backend/app/ingestion.py`
- `backend/tests/test_ingestion.py`

## Required behavior

- split normalized loaded documents into `DocumentChunk` records
- preserve source path, page number, and chunk order
- support plain text documents and page-aware PDF documents
- produce stable chunk ids

## Constraints

- keep the API pure and deterministic
- build on top of existing loader and chunking layers
- do not add retrieval or answer generation yet
- keep tests focused on chunk metadata and ordering

## Done when

- chunk-building functions exist
- source attribution is preserved in tests
- retrieval storage can consume the resulting chunks directly

## Prompt to give Codex

```text
Read AGENTS.md and docs/NEXT_STEP.md.
Implement only the current step.
Add or update tests for the changed behavior.
Do not modify unrelated files.
At the end, summarize what changed and how to run the tests.
```
