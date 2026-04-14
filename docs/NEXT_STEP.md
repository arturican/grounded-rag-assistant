# Next Step

## Current milestone

Phase 9 - Evaluation and quality

## Task

Add one answering-level regression test that proves `max_chunks=1` keeps only the top retrieved chunk in the final answer and sources.

## Files to update

- `backend/tests/test_answering.py`
- `README.md` only if the verification command changes

## Required behavior

- create a deterministic `RetrievedChunk` list with more than one relevant chunk
- call `build_grounded_answer(..., max_chunks=1)`
- assert that:
  - only the highest-ranked chunk text appears in the answer
  - lower-ranked chunk text is not included
  - returned `sources` contains exactly one source for the top chunk
- keep the test fully local and deterministic

## Constraints

- do not change answer assembly behavior unless the new test reveals a real bug
- do not add a new evaluation framework
- prefer one focused regression test over broader answer-layer changes
- reuse existing test patterns already present in `backend/tests/test_answering.py`

## Done when

- answer assembly has an explicit regression-style check for the `max_chunks=1` contract
- the narrow verification command is still accurate in the docs

## Prompt to give Codex

```text
Read AGENTS.md and docs/NEXT_STEP.md.
Implement only the current step.
Add or update tests for the changed behavior.
Do not modify unrelated files.
At the end, summarize what changed and how to run the tests.
```
