# Next Step

## Current milestone

Phase 10 - UI and packaging

## Task

Make frontend `/index` error rendering as informative as `/ask`, so failed indexing requests show backend status and detail instead of a generic raw error string.

## Files to update

- `frontend/src/App.tsx`
- `frontend/src/api.ts` only if the existing `ApiError` contract needs a small adjustment
- `README.md` only if local demo behavior needs clarification

## Required behavior

- when `/index` fails, the UI should show a readable backend error block with status and detail
- keep `/ask` error rendering unchanged
- keep the change minimal and local to the current demo frontend

## Constraints

- do not add new dependencies
- do not redesign the page
- do not change backend API semantics in the same step

## Done when

- failed `/index` requests render a more helpful client-facing error message
- `/ask` behavior stays as-is
- the next step remains small and directly runnable

## Prompt to give Codex

```text
Read AGENTS.md and docs/NEXT_STEP.md.
Implement only a small frontend `/index` error-rendering improvement.
Reuse the existing backend error detail when possible.
Keep `/ask` behavior unchanged.
Do not expand into broader frontend refactors.
```
