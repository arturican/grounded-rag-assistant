# Next Step

## Current milestone

Phase 9 - Evaluation and quality

## Task

Verify that retrieval score ties are handled deterministically at the CLI level.

## Files to update

- `backend/tests/test_cli.py`

## Required behavior

- setup a small index where two chunks have identical text (thus identical embeddings and scores)
- ensure they come from different sources
- verify that `run_cli(["ask", ...])` always returns them in a stable order (e.g. by chunk_id or source path)
- this avoids flaky CLI tests when scores are equal

## Constraints

- use `index_directory` and a temporary setup to reach the deterministic retrieval logic
- keep the test narrow and focused on CLI-visible stability

## Done when

- CLI has a regression test for retrieval tie-breaking
- all CLI tests pass

## Prompt to give Codex

```text
Read AGENTS.md and docs/NEXT_STEP.md.
Implement only the current step.
Add or update tests for the changed behavior.
Do not modify unrelated files.
At the end, summarize what changed and how to run the tests.
```
