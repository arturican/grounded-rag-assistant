# Next Step

## Current milestone

Phase 9 - Evaluation and quality

## Task

Create a small sample corpus and a set of evaluation questions for manual/automated verification.

## Files to update

- `sample_docs/` (new directory)
- `docs/EVALUATION_DATASET.md` (new file)

## Required behavior

- provide 3-5 sample documents (.txt, .md, .pdf) with overlapping facts
- define 5-10 evaluation questions with expected grounded answers and source references
- this dataset will be used to verify retrieval recall and answer precision in future steps

## Constraints

- keep sample documents small to ensure fast test runs
- ensure documents are realistic for the RAG use case
- PDF should be included to test page-aware retrieval

## Done when

- `sample_docs/` directory contains verification files
- `docs/EVALUATION_DATASET.md` documents the expected behavior for each question

## Prompt to give Codex

```text
Read AGENTS.md and docs/NEXT_STEP.md.
Create the sample document corpus in sample_docs/.
Document the evaluation questions and expected outcomes in docs/EVALUATION_DATASET.md.
Do not modify the application code.
Summarize the dataset and how it improves evaluation.
```
