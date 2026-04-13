# Next Step

## Current milestone

Phase 4 - Embeddings service

## Task

Add an embeddings provider interface with a fake test implementation.

## Files to update

- `backend/app/embeddings.py`
- `backend/tests/test_embeddings.py`

## Required behavior

- define an interface for generating embeddings from text inputs
- keep app code depending on the interface, not a concrete library
- include a fake provider for tests
- return deterministic vectors in tests

## Constraints

- keep the API pure and deterministic
- do not wire in sentence-transformers yet
- do not add embedding or retrieval logic
- keep tests focused on interface behavior and simple invariants

## Done when

- an embeddings provider contract exists
- fake-provider behavior is covered by tests
- the next storage step can consume the interface directly

## Prompt to give Codex

```text
Read AGENTS.md and docs/NEXT_STEP.md.
Implement only the current step.
Add or update tests for the changed behavior.
Do not modify unrelated files.
At the end, summarize what changed and how to run the tests.
```
