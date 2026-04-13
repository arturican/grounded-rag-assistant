# Next Step

## Current milestone

Phase 3 - Document loaders

## Task

Add a dispatch function for supported local text formats.

## Files to update

- `backend/app/loaders.py`
- `backend/tests/test_loaders.py`

## Required behavior

- route supported source files to the correct loader
- support `.txt` and `.md`
- return the same normalized loaded-document shape
- fail clearly for unsupported file types

## Constraints

- keep the API pure and deterministic
- build on top of the existing loader functions
- do not add PDF parsing yet
- do not add embedding or retrieval logic
- add tests for `.txt`, `.md`, and unsupported-extension behavior

## Done when

- a `load_document` entry point exists
- dispatch behavior is covered by tests
- supported formats share one stable return shape

## Prompt to give Codex

```text
Read AGENTS.md and docs/NEXT_STEP.md.
Implement only the current step.
Add or update tests for the changed behavior.
Do not modify unrelated files.
At the end, summarize what changed and how to run the tests.
```
