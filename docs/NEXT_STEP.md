# Next Step

## Current milestone

Phase 9 - Evaluation and quality

## Task

Add a small regression script or test module that exercises the evaluation corpus through the current text-only CLI path.

## Files to update

- `backend/tests/` (new or updated test)
- `docs/EVALUATION_DATASET.md`
- `README.md` if verification commands change

## Required behavior

- verify the text-only subset of `sample_docs/` can still be indexed with the current CLI
- verify at least one grounded question returns the expected fact from the sample corpus
- keep the check fast enough for routine local runs

## Constraints

- do not add new dependencies
- do not expand into a full evaluation framework yet
- keep the test aligned with the current deterministic answering behavior

## Done when

- a narrow automated check covers the evaluation corpus smoke path
- docs explain how to run that check locally
- the next step remains small and directly runnable

## Prompt to give Codex

```text
Read AGENTS.md and docs/NEXT_STEP.md.
Add a narrow automated regression check for the sample evaluation corpus using the current text-only CLI flow.
Update documentation with the exact local verification command.
Keep the change small and do not introduce a full evaluation framework yet.
Summarize the test coverage and the next recommended step.
```
