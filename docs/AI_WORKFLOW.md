# AI Workflow

## Goal

Use Codex as a disciplined coding agent, not as a random code generator.

## Best practices

### 1. Work in thin vertical slices

Good:
- add text chunking function + tests
- add PDF loader + tests
- add FAISS repository + tests

Bad:
- “build the entire RAG platform” in one step

### 2. Ask for a plan before large changes

For tasks touching multiple files or architecture, require a plan first.

Suggested prompt:

> Read `AGENTS.md`, `docs/PROJECT_BRIEF.md`, `docs/ROADMAP.md`, and `docs/NEXT_STEP.md`. Propose a small implementation plan, list files to change, then implement only Step 1.

### 3. Always bind coding to tests

Suggested prompt:

> Implement the scoped change and add/update tests for the changed behavior. Do not touch unrelated files.

### 4. Keep source of truth in files, not chat history

Important decisions must be written into:
- `docs/PROJECT_BRIEF.md`
- `docs/ROADMAP.md`
- `docs/NEXT_STEP.md`

### 5. Prefer reversible changes

Ask for additive changes first. Delay deep refactors until behavior is proven.

### 6. Force grounded outputs

Any answering module must:
- use retrieved context
- report sources
- state when context is insufficient

### 7. Review diffs, not promises

Judge work by:
- changed files
- tests
- commands run
- results observed

### 8. Close every step with verification

End each task with:
- what changed
- how to run it
- what passed
- what remains next

## Recommended task template

```text
Read AGENTS.md and docs/*.md relevant to the task.
Implement only the smallest next step from docs/NEXT_STEP.md.
Before coding, list the files you will modify and why.
After coding, run the narrowest relevant tests.
Summarize what changed, what passed, and what the next small step should be.
```

## Anti-patterns

- giant one-shot prompts
- refactoring unrelated code
- changing dependencies without explanation
- skipping tests “for now” on core logic
- storing important decisions only in chat
