# Next Step

## Current milestone

Phase 5 - Vector storage and retrieval

## Task

Add an in-memory retrieval store over embeddings.

## Files to update

- `backend/app/retrieval.py`
- `backend/tests/test_retrieval.py`

## Required behavior

- store chunk embeddings with metadata
- retrieve top-k relevant chunks for a query embedding
- return `RetrievedChunk` records ranked by score
- keep ranking deterministic for tests

## Constraints

- keep the API pure and deterministic
- build on top of `DocumentChunk` and `EmbeddingProvider`
- use an in-memory implementation before adding FAISS
- do not add answer generation yet
- keep tests focused on ranking and metadata preservation

## Done when

- a retrieval store exists
- ranked retrieval is covered by tests
- the answer layer can consume retrieved chunks directly

## Prompt to give Codex

```text
Read AGENTS.md and docs/NEXT_STEP.md.
Implement only the current step.
Add or update tests for the changed behavior.
Do not modify unrelated files.
At the end, summarize what changed and how to run the tests.
```
