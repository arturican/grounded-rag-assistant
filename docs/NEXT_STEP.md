# Next Step

## Current milestone

Phase 2 - Text chunking

## Task

Add a sliding-window fallback for long paragraphs.

## Files to update

- `backend/app/chunking.py`
- `backend/tests/test_chunking.py`

## Required behavior

- build on top of `split_into_paragraphs`
- keep short paragraphs unchanged
- split long paragraphs into smaller text chunks
- preserve original order
- support configurable chunk size and overlap

## Constraints

- keep the API pure and deterministic
- do not create `DocumentChunk` objects yet
- do not add file loaders or embedding logic
- add tests for short input, long input, and overlap behavior

## Done when

- a long-paragraph splitter exists
- overlap behavior is covered by tests
- current normalization and paragraph-splitting tests still pass

## Prompt to give Codex

```text
Read AGENTS.md and docs/NEXT_STEP.md.
Implement only the current step.
Add or update tests for the changed behavior.
Do not modify unrelated files.
At the end, summarize what changed and how to run the tests.
```
