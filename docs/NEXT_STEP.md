# Next Step

## Current milestone

Phase 9 - Evaluation and quality

## Task

Verify that the API `ask` response preserves page metadata in returned sources.

## Files to update

- `backend/tests/test_api.py`

## Required behavior

- build or patch a tiny saved index entry whose source metadata includes a concrete page number
- call the `/ask` endpoint and inspect the structured JSON response
- verify that the first returned source keeps both `page` and `chunk_id`
- keep the test narrow and focused on API-visible source metadata, not formatting strings

## Constraints

- reuse the existing FastAPI test patterns in `backend/tests/test_api.py`
- do not change API behavior unless the regression test reveals a real bug
- avoid adding new dependencies or broader API fixtures

## Done when

- API has a regression test for page-aware source metadata
- the narrow API test passes in the project test environment

## Prompt to give Codex

```text
Read AGENTS.md and docs/NEXT_STEP.md.
Implement only the current step.
Add or update tests for the changed behavior.
Do not modify unrelated files.
At the end, summarize what changed and how to run the tests.
```
