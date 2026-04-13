# Next Step

## Current milestone

Phase 3 - Document loaders

## Task

Add a markdown `.md` loader.

## Files to update

- `backend/app/loaders.py`
- `backend/tests/test_loaders.py`

## Required behavior

- load UTF-8 markdown files from local storage
- return normalized text ready for chunking
- preserve the source path in returned metadata
- fail with a clear error for missing files

## Constraints

- keep the API pure and deterministic
- build on top of the existing plain-text loader pattern
- support only `.md` in this step
- do not add PDF parsing yet
- do not add embedding or retrieval logic
- add tests for successful load and missing-file behavior

## Done when

- an MD loader exists
- loader behavior is covered by tests
- the loaded text is normalized consistently for downstream chunking

## Prompt to give Codex

```text
Read AGENTS.md and docs/NEXT_STEP.md.
Implement only the current step.
Add or update tests for the changed behavior.
Do not modify unrelated files.
At the end, summarize what changed and how to run the tests.
```
