# Next Step

## Current milestone

Phase 9 - Evaluation and quality

## Task

Add one retrieval-level regression test for deterministic ordering when similarity scores are equal.

## Files to update

- `backend/tests/test_retrieval.py`
- `README.md` only if the verification command changes

## Required behavior

- build the regression around `FixedEvaluationEmbeddingProvider` or another existing deterministic test helper
- create at least two chunks whose similarity to the query is exactly the same
- assert that `InMemoryRetrievalStore.search()` keeps the existing stable tie-break order:
  - higher score first
  - for equal scores, lower `chunk_index` first
  - if needed, `chunk_id` remains the final deterministic fallback
- keep the check independent from external models and filesystem state

## Constraints

- do not change retrieval behavior unless the new test reveals a real bug
- do not add a new evaluation framework
- prefer one focused regression test over broader retrieval refactors
- reuse existing test patterns already present in `backend/tests/test_retrieval.py`

## Done when

- retrieval has an explicit regression-style check for deterministic ordering on score ties
- the narrow verification command is still accurate in the docs

## Prompt to give Codex

```text
Read AGENTS.md and docs/NEXT_STEP.md.
Implement only the current step.
Add or update tests for the changed behavior.
Do not modify unrelated files.
At the end, summarize what changed and how to run the tests.
```
