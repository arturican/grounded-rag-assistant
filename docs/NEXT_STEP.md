# Next Step

## Current milestone

Phase 3 - Document loaders

## Task

Add a PDF loader interface and document the dependency choice.

## Files to update

- `backend/app/loaders.py`
- `backend/tests/test_loaders.py`
- `docs/ROADMAP.md` or `README.md` if the PDF parsing approach needs clarification

## Required behavior

- load text from PDF files through a dedicated loader function
- preserve page numbers in the returned structure
- keep the return shape compatible with the existing loader layer
- fail clearly when the PDF backend is unavailable

## Constraints

- keep the API pure and deterministic
- make the dependency choice explicit before broadening scope
- do not add embedding or retrieval logic
- keep tests focused on the loader contract, using fakes or fixtures if needed

## Done when

- a PDF loader entry point exists
- page-aware return data is covered by tests
- the dependency and verification path are documented

## Prompt to give Codex

```text
Read AGENTS.md and docs/NEXT_STEP.md.
Implement only the current step.
Add or update tests for the changed behavior.
Do not modify unrelated files.
At the end, summarize what changed and how to run the tests.
```
