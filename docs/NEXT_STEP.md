# Next Step

## Current milestone

Phase 9 - Evaluation and quality

## Task

Add one CLI-level regression test for the honest insufficient-context path on an unrelated query.

## Files to update

- `backend/tests/test_cli.py`
- `README.md` only if the verification command changes

## Required behavior

- build a tiny local index inside the test using the existing CLI indexing path
- call the CLI `ask` flow with an unrelated query against that saved index
- assert that the rendered output keeps the honest-failure contract:
  - the answer line contains the existing insufficient-context message
  - no `Sources:` block is printed
- keep the check deterministic and independent from external models

## Constraints

- reuse the current FakeEmbeddingProvider-based flow
- do not add a new evaluation framework
- prefer one focused regression test over broader CLI coverage changes
- do not modify application behavior unless the test reveals a real bug

## Done when

- the CLI has a regression-style check for the insufficient-context branch
- the narrow verification command is still accurate in the docs

## Prompt to give Codex

```text
Read AGENTS.md and docs/NEXT_STEP.md.
Implement only the current step.
Add or update tests for the changed behavior.
Do not modify unrelated files.
At the end, summarize what changed and how to run the tests.
```
