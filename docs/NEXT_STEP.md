# Next Step

## Current milestone

Phase 7 - CLI vertical slice

## Task

Build CLI index/ask commands with local JSON persistence.

## Files to update

- `backend/app/cli.py`
- `backend/app/index_store.py`
- `backend/tests/test_cli.py`

## Required behavior

- index supported local documents from a folder into a local file
- load the saved index and answer a user query from retrieved context
- print answer text and sources in a readable CLI format
- keep the vertical slice runnable without external services

## Constraints

- keep the API pure and deterministic
- build on top of the existing loader, ingestion, retrieval, and answering layers
- use simple local persistence before adding FastAPI
- keep tests focused on CLI behavior and saved-index loading

## Done when

- `index` and `ask` commands exist
- a local end-to-end CLI path is covered by tests
- README documents the local commands

## Prompt to give Codex

```text
Read AGENTS.md and docs/NEXT_STEP.md.
Implement only the current step.
Add or update tests for the changed behavior.
Do not modify unrelated files.
At the end, summarize what changed and how to run the tests.
```
