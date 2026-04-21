# Next Step

## Current milestone

Phase 10 - UI and packaging

## Task

Add a minimal multi-service local demo stack so the existing backend container and frontend app can be started together without introducing production deployment complexity.

## Files to update

- `docker-compose.yml` for a local backend + frontend demo stack
- `README.md` to include exact `docker compose up` / verification commands

## Required behavior

- `docker compose up --build` should start:
  - backend API on port 8000
  - frontend demo on port 5173 or another explicit local port
- frontend container should point to the backend container with the correct API base URL
- `/health` should respond successfully from the backend container
- frontend root page should load successfully from the compose stack
- no application-logic changes should be required

## Constraints

- keep the scope local-demo only; do not add production orchestration
- reuse the existing `Dockerfile.backend` instead of redesigning backend packaging
- do not change application logic

## Done when

- local compose stack starts without manual per-service setup
- backend `/health` works through the containerized stack
- frontend page loads against the containerized backend
- README.md documents the exact local compose verification commands

## Prompt to give Codex

```text
Read AGENTS.md and docs/NEXT_STEP.md.
Add a minimal local docker compose stack for the existing backend container and frontend demo.
Reuse Dockerfile.backend for the API.
Do not introduce production deployment features.
Update README.md with exact docker compose build/run/verification commands.
Keep the change limited to local packaging and startup flow.
```
