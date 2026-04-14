# Evaluation Dataset

## Purpose

This dataset provides a small, realistic corpus for manual and automated checks during Phase 9.
It is intentionally compact so retrieval and answer checks stay fast.

## Corpus layout

- `sample_docs/text_only/operations_handbook.txt`
- `sample_docs/text_only/release_plan.md`
- `sample_docs/text_only/support_playbook.txt`
- `sample_docs/reference/facility_guide.pdf`

The text files are safe to use with the current CLI flow.
The PDF file is included for future page-aware retrieval checks once the runtime PDF backend is wired into the end-to-end path.

## Shared facts and overlap

The corpus includes overlapping facts on purpose:

- `08:00-18:00 UTC` support and launch coverage appears in both the handbook and release plan
- `infra-oncall@lighthouse.example` appears in both the handbook and support playbook
- `Wednesday at 18:30 UTC` appears in the handbook, support playbook, and the PDF guide
- visitor access rules appear in the handbook, support playbook, and the PDF guide
- `Mira Chen` appears in the release plan and support playbook

This overlap makes it useful for checking both retrieval recall and source precision.

## Evaluation questions

### Q1. When does the Atlas pilot launch?

- Expected grounded answer: mention that the pilot launch begins on `2026-05-20`
- Expected sources: `sample_docs/text_only/release_plan.md`
- Notes: a correct answer should stay anchored to the release plan and not invent a time of day

### Q2. Who owns rollback decisions for the Atlas pilot?

- Expected grounded answer: mention `Mira Chen`
- Expected sources: `sample_docs/text_only/release_plan.md`
- Notes: the answer may also retrieve the support playbook because it repeats the same person for outage notification

### Q3. What coverage hours are planned for Atlas launch support?

- Expected grounded answer: mention `08:00 to 18:00 UTC` on weekdays
- Expected sources: `sample_docs/text_only/release_plan.md`, optionally `sample_docs/text_only/operations_handbook.txt`
- Notes: this checks whether the system can use overlapping schedule facts without drifting beyond the corpus

### Q4. Where should urgent infrastructure incidents be escalated?

- Expected grounded answer: mention `infra-oncall@lighthouse.example`
- Expected sources: `sample_docs/text_only/operations_handbook.txt`, optionally `sample_docs/text_only/support_playbook.txt`
- Notes: this is a good retrieval-recall check because the same address appears in multiple files

### Q5. Where should billing questions be routed?

- Expected grounded answer: mention `finance-ops@lighthouse.example`
- Expected sources: `sample_docs/text_only/support_playbook.txt`
- Notes: this should be a straightforward single-source answer

### Q6. What happens every Wednesday at 18:30 UTC?

- Expected grounded answer: mention backup verification or the backup review window
- Expected sources: `sample_docs/text_only/operations_handbook.txt`, `sample_docs/text_only/support_playbook.txt`
- Notes: future PDF-aware retrieval may also surface the facility guide because page 2 mentions the same time slot

### Q7. Until what time can visitors sign in at reception?

- Expected grounded answer: mention `17:00`
- Expected sources: `sample_docs/reference/facility_guide.pdf` page 1, optionally `sample_docs/text_only/operations_handbook.txt`
- Notes: this question is designed for page-aware source checks once PDF extraction is enabled end to end

### Q8. How many people fit in the training room?

- Expected grounded answer: mention `12`
- Expected sources: `sample_docs/reference/facility_guide.pdf` page 1
- Notes: this is a PDF-only fact and should help catch cases where page metadata is lost

### Q9. What is the P1 incident response target?

- Expected grounded answer: mention `15 minutes`
- Expected sources: `sample_docs/text_only/support_playbook.txt`
- Notes: this checks a concise operational fact with a single clear source

### Q10. What is the company travel reimbursement limit?

- Expected grounded answer: report insufficient context or explicitly state that the answer is not present in the indexed documents
- Expected sources: none
- Notes: this question exists to verify grounded refusal behavior

## Suggested local verification

Use the text-only subset with the current CLI flow:

```bash
cd /home/artur/project/grounded-rag-assistant
python3 -m backend.app.cli index ./sample_docs/text_only ./local_index.json
python3 -m backend.app.cli ask ./local_index.json "Where should billing questions be routed?"
python3 -m backend.app.cli ask ./local_index.json "Who owns rollback decisions for the Atlas pilot?"
python3 -m backend.app.cli ask ./local_index.json "What is the company travel reimbursement limit?"
```

Use the dataset file itself during manual review to check:

- whether the answer includes only facts present in retrieved chunks
- whether the cited source files match the expected source set
- whether unsupported questions fail honestly
