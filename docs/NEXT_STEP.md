# Next Step

## Current milestone

Phase 6 - Grounded answer generation

## Task

Build deterministic grounded answer assembly from retrieved chunks.

## Files to update

- `backend/app/answering.py`
- `backend/tests/test_answering.py`

## Required behavior

- answer only from retrieved chunk text
- return source references with file and page metadata when available
- handle insufficient-context cases honestly
- keep output deterministic for tests

## Constraints

- keep the API pure and deterministic
- build on top of `RetrievedChunk`
- do not call external LLMs yet
- keep tests focused on answer selection and source formatting

## Done when

- an answer assembly layer exists
- insufficient-context behavior is covered by tests
- CLI can print answers and sources directly from this layer

## Prompt to give Codex

```text
Read AGENTS.md and docs/NEXT_STEP.md.
Implement only the current step.
Add or update tests for the changed behavior.
Do not modify unrelated files.
At the end, summarize what changed and how to run the tests.
```
