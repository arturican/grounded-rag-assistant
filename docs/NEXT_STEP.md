# Next Step

## Current milestone

Phase 10 - UI and packaging

## Task

Add Docker support to the project to simplify local development and deployment of the full RAG stack (backend + frontend).

## Files to update

- `Dockerfile.backend`
- `Dockerfile.frontend`
- `docker-compose.yaml`
- `README.md` to include Docker run instructions

## Required behavior

- a single `docker-compose up` should start both the FastAPI backend and the Vite frontend
- backend should be accessible on port 8000
- frontend should be accessible on port 5173 and correctly point to the backend service
- indexing and asking should work end-to-end within the containers

## Constraints

- use lightweight base images (e.g., python:3.12-slim, node:20-slim)
- ensure volumes are used for the local index and sample documents if necessary
- do not change application logic

## Done when

- `docker-compose build && docker-compose up` finishes without errors
- the application is reachable and functional through the Docker-exposed ports
- README.md is updated with the new commands

## Prompt to give Codex

```text
Read AGENTS.md and docs/NEXT_STEP.md.
Create Dockerfiles for both backend and frontend.
Set up a docker-compose.yaml to orchestrate the services.
Update README.md with Docker usage instructions.
Ensure the frontend correctly connects to the backend within the Docker network.
```
