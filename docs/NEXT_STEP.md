# Next Step

## Current milestone

Phase 1 — Core domain model

## Task

Create the first minimal domain models for the retrieval pipeline.

## Files to add

- `backend/app/models.py`
- `backend/tests/test_models.py`

## Required models

### DocumentChunk
Fields:
- `chunk_id: str`
- `source: str`
- `page: int | None`
- `chunk_index: int`
- `text: str`

### RetrievedChunk
Fields:
- all `DocumentChunk` fields
- `score: float`

## Constraints

- use dataclasses or Pydantic, but keep it simple
- text must not be empty or whitespace-only
- `chunk_index` must be >= 0
- `page` must be `None` or >= 1
- add tests for valid and invalid creation

## Done when

- the models exist
- invariants are enforced
- tests pass
- README or docs do not need updating unless the model shape changes

## Prompt to give Codex

```text
Read AGENTS.md and docs/NEXT_STEP.md.
Implement only the current step.
Add or update tests for the changed behavior.
Do not modify unrelated files.
At the end, summarize what changed and how to run the tests.
```
