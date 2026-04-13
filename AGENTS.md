# AGENTS.md

## Repository purpose

Build a clean, testable RAG system that searches user documents and answers only from retrieved context.

## How to work in this repo

- Make small, focused changes.
- Prefer one task per commit.
- Read `docs/PROJECT_BRIEF.md`, `docs/ROADMAP.md`, and `docs/NEXT_STEP.md` before coding.
- Keep `AGENTS.md` short; detailed project truth lives in `docs/`.
- Update docs when behavior, architecture, or workflow changes.

## Coding rules

- Write simple, explicit Python.
- Add type hints for public functions.
- Avoid hidden magic and premature abstractions.
- Do not introduce new dependencies unless they are justified in the task.
- Do not refactor unrelated code while implementing a scoped task.
- Preserve source attribution metadata throughout the retrieval pipeline.
- Answers must be grounded in retrieved chunks. Do not implement “helpful” hallucination behavior.

## Testing rules

- Add or update tests for any behavior change.
- Start with unit tests for pure logic.
- Add integration tests only for completed vertical slices.
- If a task is not testable yet, leave a TODO note in the relevant doc and keep the change minimal.

## File placement

- Core app code goes in `backend/app/`.
- Tests go in `backend/tests/`.
- New architectural decisions go in `docs/`.
- Temporary experiments should be isolated and easy to delete.

## Definition of done

A task is done only when all of the following are true:

1. code is implemented
2. tests for the changed behavior exist
3. local commands for verification are documented
4. docs are updated if the design changed

## Execution style

- For complex tasks, plan first.
- Show the intended file changes before broad refactors.
- Prefer additive changes over risky rewrites.
- When blocked, write down the blocker and the smallest safe next move.
