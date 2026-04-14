# Next Step

## Current milestone

Phase 10 - UI and packaging

## Task

Add a backend-only Docker image so the API can be started in a clean, repeatable container before wiring the full multi-service stack.

## Files to update

- `Dockerfile.backend`
- `README.md` to include exact backend container build/run commands

## Required behavior

- `docker build -f Dockerfile.backend .` should succeed
- `docker run` for the backend image should expose the FastAPI app on port 8000
- `/health` should respond successfully from the running container
- no frontend or application-logic changes should be required

## Constraints

- use a lightweight Python base image (for example `python:3.12-slim`)
- keep the step backend-only; do not add frontend Docker support or `docker-compose` yet
- do not change application logic

## Done when

- backend image builds without errors
- containerized backend answers `/health`
- README.md documents the exact local Docker verification commands

## Prompt to give Codex

```text
Read AGENTS.md and docs/NEXT_STEP.md.
Create Dockerfile.backend only.
Do not add docker-compose or frontend containerization yet.
Update README.md with exact docker build/run/health-check commands.
Keep the change limited to packaging for the backend service.
```
