# grounded-rag-assistant

A production-minded pet project: a Retrieval-Augmented Generation (RAG) system that searches a user's documents and answers strictly from retrieved context.

## Why this project

This repository is built to demonstrate practical AI engineering skills:

- document ingestion
- chunking and metadata preservation
- embeddings and vector search
- grounded answer generation
- evaluation and testing
- agent-friendly repository design for Codex

## Product goal

Upload documents, index them, ask a question, get an answer with sources.

## MVP scope

- ingest `.txt`, `.md`, `.pdf`
- create chunks with overlap
- generate embeddings
- store vectors in a local FAISS index
- retrieve top-k relevant chunks
- answer only from retrieved context
- show citations/sources in the response
- cover the core flow with tests

## Planned stack

- Python 3.12+
- FastAPI for API
- sentence-transformers for embeddings
- FAISS for local vector search
- PyMuPDF for PDF parsing
- pytest for tests
- Ruff for linting

## Repository map

- `AGENTS.md` — instructions for Codex and other coding agents
- `.codex/config.toml` — project-scoped Codex defaults
- `docs/PROJECT_BRIEF.md` — concise product and technical scope
- `docs/ROADMAP.md` — phased roadmap with acceptance criteria
- `docs/AI_WORKFLOW.md` — best practices for coding with AI agents
- `docs/NEXT_STEP.md` — the next small implementation step to execute
- `backend/` — application code and tests

## Working principle

Every task should be:

1. small
2. testable
3. reviewable
4. documented if behavior changed

## First build target

Implement a CLI-only vertical slice:

- index local documents from a folder
- ask a question from the command line
- print answer + sources

After the CLI slice is stable, expose the same flow through FastAPI.

## Local verification

Run the narrowest unit checks from WSL:

```bash
cd /home/art/project/grounded-rag-assistant
python3 -m unittest backend.tests.test_chunking -v
python3 -m unittest backend.tests.test_models -v
```
