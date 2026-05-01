---
sidebar_position: 12
title: Sprint 1 Role Assignments
---

# Sprint 1 Role Assignments

**Engagement**: AI Support Copilot Pilot
**Sprint**: 1 of 2
**Dates**: May 1 -- May 10, 2026
**Prepared by**: Amit (POD Lead)
**Purpose**: Each team member should read their section and know exactly what they own, when it is due, who they depend on, and who depends on them.

---

## Sprint 1 Goal

Deliver an end-to-end AI copilot pipeline (walking skeleton) where a single support ticket enters the system, passes through classification, KB retrieval, reasoning, and draft generation, and the full output is displayed in a three-panel React dashboard. In parallel, build an operational eval harness with a golden dataset of 30-40 test cases and produce baseline metrics against the thresholds defined in the Evaluation Plan. By the May 10 demo, Prasanna should be able to select a ticket, click "Run Copilot," and see the full pipeline output on screen, while we present baseline accuracy numbers alongside it.

---

## Ceremony Schedule

| Ceremony | Date | Time | Duration | Attendees |
|---|---|---|---|---|
| Sprint 1 Planning | May 1 (Thu) AM | -- | 90 min | Full POD |
| Daily Standup | Daily | 09:30 | 15 min | Full POD |
| Mid-sprint Check-in | May 5 (Mon) PM | -- | 30 min | Amit + Shivani + Prasanna |
| Pre-demo Verification | May 9 (Fri) AM | -- | 60 min | Amit + Nishka |
| Sprint 1 Demo | May 10 (Sat) AM | -- | 30 min | Full POD + Prasanna |
| Sprint 1 Retro | May 10 (Sat) PM | -- | 45 min | POD only |

**Standup format**: What I did yesterday, what I am doing today, any blockers. Keep it under 15 minutes. If a discussion runs long, take it offline with the relevant people.

---

## Amit -- POD Lead

### Stories

| Story | Description | Days | Estimate |
|---|---|---|---|
| S1-01 | Set up project repo, dev environment, and infrastructure | May 1-2 | 2 days |
| S1-04 | Build LLM Gateway (provider-agnostic abstraction) | May 2-3 | 2 days |
| S1-09 | Build Express API endpoints | May 7-8 | 2 days |
| S1-10 | Build React frontend (three-panel dashboard) | May 5-8 | 4 days |

### Day-by-Day

| Day | Date | Focus |
|---|---|---|
| 1 | May 1 (Thu) | S1-01: Initialize monorepo, docker-compose for MongoDB + ES, GCP Service Account, CI pipeline, README |
| 2 | May 2 (Fri) | S1-01: Finalize infra, verify team can clone and run. Start S1-04: LLMProvider interface + VertexAIProvider |
| 3 | May 3 (Sat) | S1-04: Complete LLM Gateway, integration test with Gemini, placeholder providers |
| 4 | May 4 (Sun) | Code review: review PRs from Nancy (S1-02), Atharva (S1-03). Unblock any issues |
| 5 | May 5 (Mon) | S1-10: Start React UI -- three-panel layout, TicketQueue component, state management |
| 6 | May 6 (Tue) | S1-10: TicketDetail + CopilotSidebar components, "Run Copilot" button, loading states |
| 7 | May 7 (Wed) | S1-09: Express API endpoints (process, tickets, feedback). S1-10: Wire UI to API |
| 8 | May 8 (Thu) | S1-09: Finish API integration. S1-10: FeedbackWidget, end-to-end integration testing |
| 9 | May 9 (Fri) | Integration bug fixes, pre-demo verification with Nishka, final code reviews |
| 10 | May 10 (Sat) | Pre-demo rehearsal with Shivani, Sprint 1 Demo to Prasanna, Retro |

### Dependencies

| I need | From whom | By when |
|---|---|---|
| Data ingested and queryable (S1-02) | Nancy | End of Day 3 |
| Pipeline orchestrator working (S1-08) | Atharva | End of Day 8 |
| Eval baseline results for demo (S1-11) | Nishka | Day 9 |
| Demo agenda and prep (S1-13) | Shivani | Day 9 |

| Others need from me | Who | By when |
|---|---|---|
| Repo + infra ready (S1-01) | Atharva, Nancy | End of Day 2 |
| LLM Gateway ready (S1-04) | Atharva (S1-03, S1-05, S1-06, S1-07) | End of Day 3 |
| API endpoints ready (S1-09) | Frontend integration | End of Day 8 |
| Code reviews on PRs | Everyone | Within 24 hours of PR submission |

### Definition of Done Reminders

- S1-01: Team can clone, run `docker-compose up`, and hit a health endpoint. CI runs lint + tests on PR.
- S1-04: Integration test proves structured output and embedding calls work through the Gateway.
- S1-09: All four endpoints return correct responses; error handling middleware tested.
- S1-10: Three-panel layout renders, ticket selection triggers pipeline, output displays in CopilotSidebar. Responsive enough to demo.
- All PRs reviewed by QA buddy before merge.

### QA Buddy Assignments

| Role | Story |
|---|---|
| **Amit reviews** | Nancy's S1-02, Atharva's S1-03, S1-06, S1-08, Shubham's S1-12 |
| **Amit is reviewed by** | Nancy (S1-01, S1-09), Shivani (S1-10), Atharva (S1-04) |

---

## Atharva -- AI Engineer

### Stories

| Story | Description | Days | Estimate | Depends on |
|---|---|---|---|---|
| S1-03 | Build classification pipeline step | May 2-4 | 3 days | S1-01, S1-04 |
| S1-05 | Build retrieval step (hybrid search) -- with Nancy | May 3-5 | 3 days | S1-02, S1-04 |
| S1-06 | Build reason pipeline step | May 5-6 | 2 days | S1-03, S1-05 |
| S1-07 | Build draft pipeline step | May 6-7 | 2 days | S1-06 |
| S1-08 | Build pipeline orchestrator (LangChain.js) | May 7-8 | 2 days | S1-03, S1-05, S1-06, S1-07 |

### Day-by-Day

| Day | Date | Focus |
|---|---|---|
| 1 | May 1 (Thu) | Blocked on S1-01. Use this day to: draft classify prompt (`prompts/classify.txt`), review dataset categories, study Vertex AI structured output docs |
| 2 | May 2 (Fri) | S1-03: Implement classify function using LLM Gateway. Structured JSON output with category, priority, sentiment, confidence |
| 3 | May 3 (Sat) | S1-03: Unit tests (3 sample tickets). Start S1-05 with Nancy: define retrieval interface, query embedding via LLM Gateway |
| 4 | May 4 (Sun) | S1-03: Finalize and PR. S1-05: Implement hybrid search (kNN + BM25 + RRF), unit test with known ticket |
| 5 | May 5 (Mon) | S1-05: Complete retrieval step, PR. S1-06: Start reason step -- chain-of-thought prompting, `prompts/reason.txt` |
| 6 | May 6 (Tue) | S1-06: Finish reason step (Reply/Ask/Escalate logic), unit tests (3 scenarios). S1-07: Start draft step |
| 7 | May 7 (Wed) | S1-07: Complete draft step with citation logic, `prompts/draft.txt`, unit test. S1-08: Start orchestrator |
| 8 | May 8 (Thu) | S1-08: Complete sequential chain (Classify -> Retrieve -> Reason -> Draft -> Guardrails placeholder), integration test, latency tracking, audit logging |
| 9 | May 9 (Fri) | Integration bug fixes, support Amit on end-to-end testing, support Nishka on baseline eval run |
| 10 | May 10 (Sat) | Demo support, fix any last-minute pipeline issues |

### Dependencies

| I need | From whom | By when |
|---|---|---|
| Repo + GCP Service Account ready (S1-01) | Amit | End of Day 2 |
| LLM Gateway ready (S1-04) | Amit | End of Day 3 |
| Data ingested, KB indexed + embedded (S1-02) | Nancy | End of Day 3 |
| Elasticsearch HNSW index configured (S1-02) | Nancy | End of Day 3 |

| Others need from me | Who | By when |
|---|---|---|
| Classify step working (S1-03) | Self (S1-06), Nishka (eval harness) | End of Day 4 |
| Retrieval step working (S1-05) | Self (S1-06), Nishka (eval harness) | End of Day 5 |
| Full pipeline via orchestrator (S1-08) | Amit (S1-09 API), Nishka (baseline eval) | End of Day 8 |

### Definition of Done Reminders

- Every prompt template is a versioned file in `prompts/` directory, not hardcoded in source.
- All LLM calls go through the LLM Gateway -- no direct Vertex AI SDK calls.
- Each step returns structured JSON matching the defined schema.
- Unit tests cover at least 3 representative scenarios per step.
- Pipeline output includes all intermediate results (classification, retrieval, reasoning, draft).
- Pipeline execution is logged to MongoDB `audit_log` collection.

### QA Buddy Assignments

| Role | Story |
|---|---|
| **Atharva reviews** | Nancy's S1-02, Nishka's S1-11 |
| **Atharva is reviewed by** | Amit (S1-03, S1-06, S1-08), Nishka (S1-07) |

---

## Nancy -- Data Engineer

### Stories

| Story | Description | Days | Estimate |
|---|---|---|---|
| S1-02 | Ingest Excel data into MongoDB and Elasticsearch | May 1-3 | 3 days |
| S1-05 | Build retrieval step (hybrid search) -- with Atharva | May 3-5 | 3 days |

### Day-by-Day

| Day | Date | Focus |
|---|---|---|
| 1 | May 1 (Thu) | S1-02: Parse all 4 sheets from `ai_support_copilot_poc_dataset.xlsx`. Insert 36 tickets into MongoDB `tickets` collection. Load 5 escalation rules as JSON config |
| 2 | May 2 (Fri) | S1-02: Insert 12 KB articles into MongoDB. Configure Elasticsearch `kb_articles` index. Set up HNSW index for cosine similarity |
| 3 | May 3 (Sat) | S1-02: Embed KB articles using Vertex AI text-embedding-005 (768 dims) via LLM Gateway. Store in `kb_vectors` index. Idempotency + data quality report. PR for S1-02. Start S1-05 with Atharva |
| 4 | May 4 (Sun) | S1-05: Elasticsearch hybrid query (kNN vector search + BM25 keyword match), Reciprocal Rank Fusion merging |
| 5 | May 5 (Mon) | S1-05: Complete retrieval step, test with Atharva, verify top-K results for known tickets. PR |
| 6 | May 6 (Tue) | Code review and data fixes. QA buddy duty for Amit's S1-01 and S1-09 |
| 7 | May 7 (Wed) | QA buddy duties: verify S1-09 API endpoints in clean environment |
| 8 | May 8 (Thu) | QA buddy duties: verify S1-09 acceptance criteria |
| 9 | May 9 (Fri) | Integration support -- help debug any data-related issues |
| 10 | May 10 (Sat) | -- |

### Dependencies

| I need | From whom | By when |
|---|---|---|
| Repo + docker-compose with MongoDB + ES (S1-01) | Amit | End of Day 2 (can start MongoDB script Day 1 locally, but need docker-compose for ES) |
| LLM Gateway for embedding calls (S1-04) | Amit | End of Day 3 (needed for KB embedding step) |

| Others need from me | Who | By when |
|---|---|---|
| Tickets in MongoDB (S1-02) | Amit (S1-10 UI), Nishka (eval harness) | End of Day 2 |
| KB articles indexed + embedded in ES (S1-02) | Atharva (S1-05 retrieval) | End of Day 3 |
| Retrieval step working (S1-05) | Atharva (S1-06 reason step) | End of Day 5 |

### Definition of Done Reminders

- Ingestion script is idempotent -- can re-run without creating duplicates.
- Data quality report flags any null fields and documents the schema.
- Elasticsearch HNSW index uses cosine similarity with 768-dimension vectors.
- All field mappings from Excel to MongoDB are documented.
- KB embedding uses Vertex AI text-embedding-005 via the LLM Gateway, not a direct SDK call.

### QA Buddy Assignments

| Role | Story |
|---|---|
| **Nancy reviews** | Amit's S1-01, Amit's S1-09 |
| **Nancy is reviewed by** | Atharva (S1-02) |

---

## Nishka -- QA Engineer

### Stories

| Story | Description | Days | Estimate |
|---|---|---|---|
| S1-11 | Build eval harness with golden dataset | May 3-8 | 4 days |

### Day-by-Day

| Day | Date | Focus |
|---|---|---|
| 1 | May 1 (Thu) | Review Evaluation Plan. Study the 12 provided eval cases in the dataset. Plan golden set structure (JSON format per Evaluation Plan) |
| 2 | May 2 (Fri) | Continue golden set planning. Review dataset categories and coverage gaps. Begin curating new test cases |
| 3 | May 3 (Sat) | **Golden set curation**: Take 12 provided eval cases, curate 18-28 new cases to reach 30-40 total. Ensure coverage across all 7 categories, all 3 actions (Reply/Ask/Escalate), and edge cases |
| 4 | May 4 (Sun) | **Golden set finalization**: Complete golden dataset JSON file. Get review from Amit on case quality and coverage. PR for golden set |
| 5 | May 5 (Mon) | **Scorers**: Build classification accuracy scorer (predicted category + priority vs. expected) |
| 6 | May 6 (Tue) | **Scorers**: Build retrieval accuracy scorer (expected KB article in top-K) and action accuracy scorer (predicted action vs. expected). `run-eval.js` CLI |
| 7 | May 7 (Wed) | **CI integration**: Integrate eval harness into CI pipeline -- runs on PRs touching pipeline code. Markdown report generation |
| 8 | May 8 (Thu) | **Baseline run**: Run full eval against working pipeline. Produce baseline metrics report. Compare against Evaluation Plan thresholds. Document per-category breakdown and failed cases |
| 9 | May 9 (Fri) | Eval run with latest pipeline. Final report for demo. QA buddy review of S1-05 and S1-07 |
| 10 | May 10 (Sat) | Present eval results at demo |

### Dependencies

| I need | From whom | By when |
|---|---|---|
| Dataset file accessible in repo | Amit (S1-01) | End of Day 2 |
| Review of golden set cases | Amit | Day 4-5 |
| Pipeline steps callable individually for scoring | Atharva (S1-03, S1-05, S1-06) | Day 7 (for individual scorer testing) |
| Full pipeline running end-to-end (S1-08) | Atharva | End of Day 8 (for baseline run) |

| Others need from me | Who | By when |
|---|---|---|
| Baseline eval results for demo | Amit, Shivani | Day 9 |
| QA buddy sign-off on S1-05, S1-07 | Atharva | Day 7-8 |

### Definition of Done Reminders

- Golden dataset contains 30-40 cases minimum, in the JSON format specified by the Evaluation Plan.
- All 12 provided eval cases are included; remaining cases are new and curated by Nishka + Amit.
- Scorers produce a markdown report with per-metric scores and per-category breakdown.
- Failed cases list expected vs. actual for easy debugging.
- CI integration: eval runs automatically on PRs that touch `server/` pipeline code.
- Baseline metrics are compared against Evaluation Plan thresholds and the comparison is documented.

### QA Buddy Assignments

| Role | Story |
|---|---|
| **Nishka reviews** | Atharva's S1-05 (retrieval), Atharva's S1-07 (draft) |
| **Nishka is reviewed by** | Atharva (S1-11) |

---

## Shubham -- Governance Engineer (Part-Time)

### Stories

| Story | Description | Days | Estimate |
|---|---|---|---|
| S1-12 | Initial threat model -- full STRIDE validation | May 1-5 | 3 days |

### Day-by-Day

| Day | Date | Focus |
|---|---|---|
| 1 | May 1 (Thu) | Review existing initial threat model. Begin data flow diagram showing all entry/exit points (Frontend, API, Pipeline, MongoDB, ES, Vertex AI) |
| 2 | May 2 (Fri) | STRIDE analysis for each component. Identify and rank threats by severity |
| 3 | May 3 (Sat) | Complete STRIDE analysis. Document top 5 threats with mitigation plans |
| 4 | May 4 (Sun) | -- |
| 5 | May 5 (Mon) | Finalize secrets management approach. Submit for POD Lead review. PR |
| 6-10 | May 6-10 | Available for questions. Prepare for Sprint 2 guardrails work (S2-01) |

### Dependencies

| I need | From whom | By when |
|---|---|---|
| Architecture sketch / system components list | Amit | Day 1 (already exists) |
| Review of threat model | Amit | Day 5-6 |

| Others need from me | Who | By when |
|---|---|---|
| Threat model document | Amit (for demo), Shivani (for status report) | End of Day 5 |
| Security guidance on secrets management | Nancy (data ingestion), Atharva (LLM calls) | Day 3 |

### Definition of Done Reminders

- Data flow diagram covers all entry/exit points in the system.
- STRIDE analysis completed for each of the 6 components (Frontend, API, Pipeline, MongoDB, ES, Vertex AI).
- Top 5 threats ranked by severity with mitigation plan for each.
- Secrets management approach documented (GCP Service Account key handling, env vars, no secrets in code).
- Reviewed and signed off by POD Lead (Amit).

### QA Buddy Assignments

| Role | Story |
|---|---|
| **Shubham reviews** | -- (no buddy assignments in Sprint 1) |
| **Shubham is reviewed by** | Amit (S1-12) |

---

## Shivani -- Implementation Manager / PM (Part-Time)

### Stories

| Story | Description | Days | Estimate |
|---|---|---|---|
| S1-13 | Sprint 1 status report and demo preparation | May 9-10 | 1 day |

### Day-by-Day

| Day | Date | Focus |
|---|---|---|
| 1 | May 1 (Thu) | Facilitate Sprint 1 Planning session (90 min). Ensure all stories are understood and assigned |
| 2 | May 2 (Fri) | Begin drafting weekly status email |
| 3-4 | May 3-4 | -- |
| 5 | May 5 (Mon) | Coordinate and attend mid-sprint check-in with Prasanna. Capture any feedback or scope changes |
| 6 | May 6 (Tue) | Send weekly status email to Prasanna. Update risk register with any new risks |
| 7-8 | May 7-8 | QA buddy review of S1-10 (React frontend). Monitor sprint progress |
| 9 | May 9 (Fri) | S1-13: Prepare demo agenda. Rehearse demo with Amit. Update backlog state (committed vs. completed vs. carry-over) |
| 10 | May 10 (Sat) | S1-13: Final demo to Prasanna. Facilitate Sprint 1 Retro |

### Dependencies

| I need | From whom | By when |
|---|---|---|
| Sprint progress updates | Everyone (via standups) | Daily |
| Eval baseline results for status report | Nishka | Day 9 |
| Working demo environment | Amit | Day 9 |
| Threat model status | Shubham | Day 5 |

| Others need from me | Who | By when |
|---|---|---|
| Sprint planning facilitation | Full POD | Day 1 |
| Mid-sprint check-in coordination | Amit | Day 5 |
| Weekly status email sent | Prasanna | Day 5 or 6 |
| Demo agenda and rehearsal | Amit | Day 9 |

### Definition of Done Reminders

- Weekly status email sent to Prasanna on May 5 or 6.
- Demo agenda is written, shared with Amit, and rehearsed.
- Risk register updated with any new risks identified during Sprint 1.
- Backlog state documented: which stories are committed, completed, or carrying over.
- QA buddy sign-off on S1-10 requires verifying the UI in a clean browser session.

### QA Buddy Assignments

| Role | Story |
|---|---|
| **Shivani reviews** | Amit's S1-10 (React frontend) |
| **Shivani is reviewed by** | Amit (S1-13) |

---

## Key Dependencies

This section maps the critical handoffs that can block others. If you are on the "provides" side of a dependency, treat the deadline as a hard commitment. If you are going to miss it, raise it immediately -- do not wait for standup.

### Critical Path Dependencies

```
S1-01 (Amit: Repo + infra, May 1-2)
  ├── blocks S1-03 (Atharva: Classify, needs GCP Service Account)
  ├── blocks S1-02 (Nancy: embedding step needs docker-compose ES)
  └── blocks S1-04 (Amit: LLM Gateway, needs GCP setup)

S1-04 (Amit: LLM Gateway, May 2-3)
  ├── blocks S1-03 (Atharva: Classify, all LLM calls go through Gateway)
  ├── blocks S1-05 (Nancy + Atharva: Retrieval, needs embed() for query)
  ├── blocks S1-06 (Atharva: Reason, needs generateStructured())
  └── blocks S1-07 (Atharva: Draft, needs generateText())

S1-02 (Nancy: Data ingestion, May 1-3)
  └── blocks S1-05 (Nancy + Atharva: Retrieval, needs KB indexed + embedded)

S1-03 → S1-05 → S1-06 → S1-07 → S1-08 (Sequential pipeline chain)
  Pipeline steps must be completed in order.
  Atharva is the sole owner of S1-03, S1-06, S1-07, S1-08.
  S1-05 is shared between Nancy and Atharva.

S1-08 (Atharva: Orchestrator, May 7-8)
  ├── blocks S1-09 (Amit: API endpoints need pipeline to call)
  └── blocks S1-11 baseline run (Nishka: needs full pipeline for baseline eval)

S1-11 (Nishka: Eval harness, May 3-8)
  └── needs pipeline running by Day 8 for baseline metrics
```

### Dependency Timeline Summary

| By end of | What must be done | Who delivers | Who is unblocked |
|---|---|---|---|
| Day 2 (May 2) | Repo + infra + docker-compose ready (S1-01) | Amit | Atharva, Nancy (ES step) |
| Day 3 (May 3) | LLM Gateway ready (S1-04) | Amit | Atharva (all pipeline steps) |
| Day 3 (May 3) | Data ingested + KB embedded (S1-02) | Nancy | Atharva (S1-05 retrieval) |
| Day 4 (May 4) | Classification step done (S1-03) | Atharva | Self (S1-06) |
| Day 5 (May 5) | Retrieval step done (S1-05) | Nancy + Atharva | Atharva (S1-06), Nishka (scorer testing) |
| Day 5 (May 5) | Threat model submitted (S1-12) | Shubham | Amit (review) |
| Day 6 (May 6) | Reason step done (S1-06) | Atharva | Self (S1-07) |
| Day 7 (May 7) | Draft step done (S1-07) | Atharva | Self (S1-08) |
| Day 8 (May 8) | Orchestrator done (S1-08) | Atharva | Amit (S1-09), Nishka (baseline) |
| Day 8 (May 8) | API endpoints done (S1-09) | Amit | UI integration (S1-10) |
| Day 8 (May 8) | UI integrated (S1-10) | Amit | Shivani (QA buddy review) |
| Day 8 (May 8) | Baseline eval run (S1-11) | Nishka | Demo prep |
| Day 9 (May 9) | Demo prep done (S1-13) | Shivani | Demo |

---

## Communication

### Daily Standup

- **Time**: 09:30 every day
- **Format**: What I did yesterday. What I am doing today. Any blockers.
- **Duration**: 15 minutes maximum. Extended discussions go offline.

### Blockers

- **Raise blockers the same day they occur.** Post in the team channel immediately. Do not wait for the next standup.
- If a dependency is going to slip, the person delivering it must notify the blocked person directly, with the new expected date.

### Code Review

- **All PRs require code review** from the assigned QA buddy (or POD Lead) before merge.
- **Review turnaround**: within 24 hours of PR submission. If you are blocked on a review, ping the reviewer directly.
- **Pipeline changes require an eval harness run.** Any PR touching files in the pipeline (`server/pipeline/`, `prompts/`) must include eval results or trigger the CI eval job.

### Escalation

- **Technical blockers**: Raise to Amit (POD Lead) immediately.
- **Client-facing issues**: Raise to Shivani (PM) who coordinates with Prasanna.
- **Security concerns**: Raise to Shubham (Governance Engineer) and Amit.

### PR Naming Convention

Use the story ID in the PR title: `S1-XX: Brief description of change`. This makes it easy to trace PRs back to stories.

---

## Change Log

| Date | Change | By |
|---|---|---|
| 2026-05-01 | Initial Sprint 1 role assignments created | Amit |
