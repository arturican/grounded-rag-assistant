# Next Step

## Current milestone

Phase 2 - Text chunking

## Task

Split normalized plain text into paragraph units.

## Files to update

- `backend/app/chunking.py`
- `backend/tests/test_chunking.py`

## Required behavior

- build on top of `normalize_whitespace`
- split text on blank-line paragraph boundaries
- discard empty paragraphs
- preserve paragraph order
- return plain strings for now

## Constraints

- keep the API simple and pure
- do not implement sliding-window chunking yet
- do not create `DocumentChunk` objects yet
- add tests for empty input, single paragraph, and multiple paragraphs

## Done when

- a paragraph splitter exists
- paragraph order is preserved
- tests pass
- current normalization tests still pass

## Prompt to give Codex

```text
Read AGENTS.md and docs/NEXT_STEP.md.
Implement only the current step.
Add or update tests for the changed behavior.
Do not modify unrelated files.
At the end, summarize what changed and how to run the tests.
```
