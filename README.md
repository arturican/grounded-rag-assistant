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

PDF loading is currently designed behind an injectable backend in the loader layer, so the parser choice stays isolated from ingestion logic.

## Repository map

- `AGENTS.md` — instructions for Codex and other coding agents
- `.codex/config.toml` — project-scoped Codex defaults
- `docs/PROJECT_BRIEF.md` — concise product and technical scope
- `docs/ROADMAP.md` — phased roadmap with acceptance criteria
- `docs/AI_WORKFLOW.md` — best practices for coding with AI agents
- `docs/NEXT_STEP.md` — the next small implementation step to execute
- `docs/ARCHITECTURE_RU.md` — Russian walkthrough of the current project architecture
- `docs/commit-notes/` — Russian-language study notes for key commits
- `backend/` — application code and tests

## Commit notes for study

If you want to understand the project commit by commit, start with:

- `docs/commit-notes/README.md`

That directory contains Russian-language notes for the main project commits and the key documentation commits that explain them:

- what was added in the commit
- how the new code works
- why that step matters in the overall RAG pipeline

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

## Local setup

Create a local virtual environment and install the project in editable mode:

```bash
cd /home/artur/project/grounded-rag-assistant
python3 -m venv .venv
.venv/bin/python -m pip install -e .
```

If your system Python does not provide `venv`, create the same environment with `virtualenv` instead:

```bash
cd /home/artur/project/grounded-rag-assistant
python3 -m virtualenv .venv
.venv/bin/python -m pip install -e .
```

## Local verification

Run the narrowest unit checks from WSL:

```bash
cd /home/artur/project/grounded-rag-assistant
.venv/bin/python -m unittest backend.tests.test_evaluation_dataset -v
.venv/bin/python -m unittest backend.tests.test_loaders -v
.venv/bin/python -m unittest backend.tests.test_chunking -v
.venv/bin/python -m unittest backend.tests.test_models -v
.venv/bin/python -m unittest backend.tests.test_embeddings -v
.venv/bin/python -m unittest backend.tests.test_ingestion -v
.venv/bin/python -m unittest backend.tests.test_retrieval -v
.venv/bin/python -m unittest backend.tests.test_answering -v
.venv/bin/python -m unittest backend.tests.test_cli -v
.venv/bin/python -m unittest backend.tests.test_api -v
```

Run the current CLI slice:

```bash
cd /home/artur/project/grounded-rag-assistant
.venv/bin/python -m backend.app.cli index ./sample_docs/text_only ./local_index.json
.venv/bin/python -m backend.app.cli ask ./local_index.json "Your question here"
```

The repository also contains `sample_docs/reference/facility_guide.pdf` for future page-aware evaluation work.
Until the runtime PDF backend is wired into the full CLI flow, use `sample_docs/text_only/` for the local end-to-end demo.

Run the API locally:

```bash
cd /home/artur/project/grounded-rag-assistant
.venv/bin/python -m uvicorn backend.app.api:app --reload
```

Verify the API endpoints:

```bash
cd /home/artur/project/grounded-rag-assistant
.venv/bin/python -m unittest backend.tests.test_api -v
curl http://127.0.0.1:8000/health
curl -X POST http://127.0.0.1:8000/index \
  -H "Content-Type: application/json" \
  -d '{"input_dir":"./sample_docs","index_path":"./local_index.json"}'
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"index_path":"./local_index.json","query":"Your question here"}'
```
