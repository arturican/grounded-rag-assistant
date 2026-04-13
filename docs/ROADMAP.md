# Roadmap

## Development strategy

Build the project in tiny, test-first or test-near steps. Each milestone must end in a runnable artifact.

---

## Phase 0 — Repository foundation

### Goal
Create a repo that Codex and humans can safely extend.

### Deliverables
- repo structure
- `AGENTS.md`
- Codex config
- project brief
- roadmap
- next-step file

### Exit criteria
- repository purpose is documented
- Codex has project instructions
- the next implementation step is unambiguous

---

## Phase 1 — Core domain model

### Goal
Define the data contracts used across ingestion and retrieval.

### Tasks
- create `DocumentChunk` model
- create `RetrievedChunk` model
- define metadata fields: source path, page, chunk index, text
- add unit tests for model invariants

### Exit criteria
- chunk metadata shape is stable
- tests pass

---

## Phase 2 — Text chunking

### Goal
Implement chunk splitting for plain text.

### Tasks
- normalize whitespace
- split by paragraphs first
- add sliding window fallback for long paragraphs
- cover edge cases with tests

### Exit criteria
- chunker handles short, long, and mixed input
- overlap behavior is tested

---

## Phase 3 — Document loaders

### Goal
Load text from supported file types.

### Tasks
- add TXT loader
- add MD loader
- add PDF loader
- preserve page numbers for PDF
- add tests for extraction behavior

### Exit criteria
- supported files can be read into normalized text units
- PDF pages are tracked

---

## Phase 4 — Embeddings service

### Goal
Add an interface for generating embeddings.

### Tasks
- create embedding provider abstraction
- implement local sentence-transformers provider
- add tests with a fake provider where possible

### Exit criteria
- app code depends on the interface, not raw library calls everywhere

---

## Phase 5 — Vector storage and retrieval

### Goal
Store chunk embeddings and retrieve the best matches.

### Tasks
- create FAISS-backed repository
- store metadata separately
- implement `top_k` retrieval
- test that relevant chunks are returned in ranked order

### Exit criteria
- retrieval works on a small local corpus

---

## Phase 6 — Grounded answer generation

### Goal
Build prompt assembly and answering logic.

### Tasks
- create prompt builder from query + retrieved chunks
- require “answer only from context” behavior
- include sources in the output
- handle insufficient-context cases
- add tests for prompt generation logic

### Exit criteria
- answer layer is deterministic where possible
- source formatting is consistent

---

## Phase 7 — CLI vertical slice

### Goal
Run the full RAG flow locally from terminal.

### Tasks
- add `index` command
- add `ask` command
- print answer and sources
- document local run commands

### Exit criteria
- end-to-end CLI demo works on sample data

---

## Phase 8 — FastAPI layer

### Goal
Expose the RAG pipeline through HTTP.

### Tasks
- create `/health`
- create `/index`
- create `/ask`
- validate request/response schemas
- add API tests

### Exit criteria
- API can index docs and answer questions locally

---

## Phase 9 — Evaluation and quality

### Goal
Measure whether retrieval and answers are actually useful.

### Tasks
- add a small evaluation dataset
- create retrieval checks
- create answer-quality checks
- define regression commands

### Exit criteria
- project has repeatable quality checks

---

## Phase 10 — UI and packaging

### Goal
Turn the prototype into a strong portfolio project.

### Tasks
- add minimal frontend or simple upload UI
- add Docker support
- improve README with screenshots and demo flow

### Exit criteria
- repo is easy to run and easy to understand

---

## Working rule

Never jump to the next phase before the current phase has a runnable result and a documented verification path.
