---
name: ship-small-step
description: Implement only the smallest next step from docs/NEXT_STEP.md with tests and no unrelated changes.
---

# ship-small-step

## When to use

Use this skill when the task is to continue the roadmap safely in small steps.

## Instructions

1. Read `AGENTS.md`, `docs/PROJECT_BRIEF.md`, and `docs/NEXT_STEP.md`.
2. Restate the exact scope in 3-5 lines.
3. List the files to modify before changing code.
4. Implement only the smallest useful step.
5. Add or update tests for the changed behavior.
6. Run the narrowest relevant verification.
7. Summarize:
   - files changed
   - tests run
   - result
   - recommended next small step

## Guardrails

- No unrelated refactors.
- No dependency changes unless required by the current step.
- Do not silently expand scope.
