# Next Step

## Current milestone

Phase 9 - Evaluation and quality

## Task

Add a tiny retrieval-quality regression check for ranked results on fixed indexed chunks.

## Files to update

- `backend/tests/test_retrieval.py`
- `docs/ROADMAP.md` only if the evaluation shape needs clarification
- `README.md` if a new local verification command is added

## Required behavior

- define a fixed indexed-chunk set directly in tests
- assert that the most relevant chunk ranks ahead of distractors for a stable query
- assert that retrieval still preserves source metadata in returned results
- keep the check deterministic and independent from external models

## Constraints

- stay within the current in-memory retrieval implementation
- do not add a new evaluation framework yet
- prefer one focused regression test over a broad harness
- keep the sample data small and readable

## Done when

- retrieval quality is checked by at least one deterministic regression-style test
- the verification command is documented if it changed

## Prompt to give Codex

```text
Read AGENTS.md and docs/NEXT_STEP.md.
Implement only the current step.
Add or update tests for the changed behavior.
Do not modify unrelated files.
At the end, summarize what changed and how to run the tests.
```
