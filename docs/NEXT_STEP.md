# Next Step

## Current milestone

Phase 9 - Evaluation and quality

## Task

Add one CLI-level regression test that verifies source rendering without page metadata keeps the non-paged format.

## Files to update

- `backend/tests/test_cli.py`
- `README.md` only if the verification command changes

## Required behavior

- build a tiny local index fixture or another narrow CLI-facing setup that reaches the rendered `Sources:` output
- use a chunk or saved index entry whose source metadata keeps `page=None`
- assert that the CLI output includes:
  - the `Sources:` block
  - the source path
  - the non-paged `(<chunk_id>)` formatting from `format_sources(...)`
  - no unexpected `page N` suffix for that source line
- keep the test deterministic and local, without adding PDF parser dependencies

## Constraints

- do not change CLI behavior unless the new test reveals a real bug
- do not add a new evaluation framework
- prefer one focused regression test over broader CLI coverage changes
- reuse existing test patterns already present in `backend/tests/test_cli.py`

## Done when

- CLI has an explicit regression-style check for non-paged source rendering
- the narrow verification command is still accurate in the docs

## Prompt to give Codex

```text
Read AGENTS.md and docs/NEXT_STEP.md.
Implement only the current step.
Add or update tests for the changed behavior.
Do not modify unrelated files.
At the end, summarize what changed and how to run the tests.
```
