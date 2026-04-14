# Next Step

## Current milestone

Phase 10 - UI and packaging

## Task

Add a focused failure-mode check for PDF ingestion without a configured extractor, so the current API/CLI path fails explicitly instead of surfacing an opaque runtime error.

## Files to update

- `backend/app/loaders.py`
- `backend/tests/test_loaders.py`
- `README.md` only if user-facing runtime behavior needs clarification

## Required behavior

- when a `.pdf` file is encountered without a configured extractor, the failure should be explicit and readable
- keep current text and markdown ingestion behavior unchanged
- add one narrow regression test for the no-extractor PDF case

## Constraints

- do not add new dependencies
- keep the change minimal and limited to PDF loader failure handling
- do not wire in a real PDF backend yet

## Done when

- PDF ingestion fails with a deterministic, readable error when no extractor is configured
- loader tests include focused coverage for that scenario
- the next step remains small and directly runnable

## Prompt to give Codex

```text
Read AGENTS.md and docs/NEXT_STEP.md.
Implement only a small PDF-loader failure-mode improvement for the no-extractor case.
Add one focused regression test for that behavior.
Keep TXT and Markdown loading unchanged.
Do not wire in a real PDF parser yet.
```
