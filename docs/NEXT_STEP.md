# Next Step

## Current milestone

Phase 8 - FastAPI layer

## Task

Expose the current RAG slice through a small HTTP API.

## Files to update

- `backend/app/api.py`
- `backend/tests/test_api.py`
- `pyproject.toml` if an API dependency needs to be declared

## Required behavior

- expose `/health`
- expose `/index`
- expose `/ask`
- reuse the existing local RAG pipeline behind HTTP handlers

## Constraints

- keep the API pure and deterministic
- build on top of the existing CLI-capable pipeline
- keep request and response shapes explicit
- add only the minimal dependency required for the API layer
- keep tests focused on endpoint behavior

## Done when

- the HTTP layer can index docs and answer questions locally
- API behavior is covered by tests
- README documents how to run the API locally

## Prompt to give Codex

```text
Read AGENTS.md and docs/NEXT_STEP.md.
Implement only the current step.
Add or update tests for the changed behavior.
Do not modify unrelated files.
At the end, summarize what changed and how to run the tests.
```
