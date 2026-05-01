---
sidebar_position: 9
title: Sprint Plan
---

# Sprint Plan -- AI Support Copilot

**Engagement**: AI Support Copilot Pilot
**Owner**: Shivani (PM) + Amit (POD Lead)
**Version**: 1.0
**Date**: 2026-05-01
**Framework ref**: Doc 04 (Agile Delivery Framework)

---

## Engagement Shape

| Attribute | Value |
|---|---|
| Total duration | 16 calendar days (May 1 -- May 16) |
| Sprint count | 2 |
| Sprint 1 | May 1 -- May 10 (10 days) |
| Sprint 2 | May 11 -- May 16 (6 days) |
| Team size | 6 (4 full-time, 2 part-time) |
| Net build capacity (Sprint 1) | ~30 person-days (6 members x ~5 build days each) |
| Net build capacity (Sprint 2) | ~18 person-days (6 members x ~3 build days each) |

**Tailoring note**: Sprint 2 is 6 days, not the standard 10. This is justified by the hard delivery deadline of May 16. Ceremonies are compressed accordingly (see Section 4).

---

## Sprint 1: Walking Skeleton + Eval Harness

**Dates**: May 1 -- May 10
**Sprint goal**: Deliver end-to-end pipeline (one ticket in, full copilot output displayed) with operational eval harness showing baseline metrics.
**Milestones**: M1 (Walking Skeleton) + M2 (Eval Harness Operational)
**Demo**: May 10

### Sprint 1 Stories

#### S1-01: Set up project repo, dev environment, and infrastructure

| Field | Value |
|---|---|
| **Owner** | Amit |
| **QA Buddy** | Nancy |
| **Estimate** | 2 days |
| **Days** | May 1-2 |
| **Bucket** | Application engineering |

**Acceptance criteria**:
- [ ] Monorepo initialized with `client/` (React) and `server/` (Express) directories
- [ ] `docker-compose.yml` provisions MongoDB + Elasticsearch locally
- [ ] GCP Service Account created with `roles/aiplatform.user` and `roles/serviceusage.serviceUsageConsumer`
- [ ] Vertex AI API (`aiplatform.googleapis.com`) enabled
- [ ] `.env.example` documents all required env vars (no secrets in code)
- [ ] CI pipeline runs lint + tests on PR
- [ ] README with setup instructions; team can clone and run locally

---

#### S1-02: Ingest Excel data into MongoDB and Elasticsearch

| Field | Value |
|---|---|
| **Owner** | Nancy |
| **QA Buddy** | Atharva |
| **Estimate** | 3 days |
| **Days** | May 1-3 |
| **Bucket** | Data work |

**Acceptance criteria**:
- [ ] Ingestion script reads all 4 sheets from `ai_support_copilot_poc_dataset.xlsx`
- [ ] 36 tickets inserted into MongoDB `tickets` collection with all fields mapped
- [ ] 12 KB articles inserted into MongoDB and indexed in Elasticsearch (`kb_articles` index)
- [ ] KB articles embedded using Vertex AI text-embedding-005 (768 dims) and stored in `kb_vectors` index
- [ ] Elasticsearch HNSW index configured for cosine similarity
- [ ] 5 escalation rules loaded as JSON config
- [ ] Ingestion script is idempotent (can re-run without duplicates)
- [ ] Data quality report: null fields flagged, schema documented

---

#### S1-03: Build classification pipeline step

| Field | Value |
|---|---|
| **Owner** | Atharva |
| **QA Buddy** | Amit |
| **Estimate** | 3 days |
| **Days** | May 2-4 |
| **Bucket** | AI engineering |
| **Depends on** | S1-01 (GCP Service Account) |

**Acceptance criteria**:
- [ ] Classify function accepts ticket text, returns structured JSON: `{ category, priority, sentiment, confidence }`
- [ ] Uses Gemini via Vertex AI with structured output (JSON schema enforcement)
- [ ] Prompt template is a versioned file in `prompts/classify.txt`
- [ ] Category values match dataset categories (Authentication, Billing, Feature Request, Bug Report, General Inquiry, Integration, Reporting)
- [ ] Priority values: Low, Medium, High, Critical
- [ ] Confidence is a float 0.0-1.0
- [ ] Unit test with 3 sample tickets passes
- [ ] Works through LLM Gateway abstraction (not direct Vertex AI SDK call)

---

#### S1-04: Build LLM Gateway (provider-agnostic abstraction)

| Field | Value |
|---|---|
| **Owner** | Amit |
| **QA Buddy** | Atharva |
| **Estimate** | 2 days |
| **Days** | May 2-3 |
| **Bucket** | Application engineering |

**Acceptance criteria**:
- [ ] `LLMProvider` interface with `generateStructured()`, `generateText()`, `embed()` methods
- [ ] `VertexAIProvider` implementation (default)
- [ ] Provider selected via `LLM_PROVIDER` env var
- [ ] Factory function `createProvider(providerName)` returns correct implementation
- [ ] Integration test: call Gemini via Gateway, get structured response
- [ ] Placeholder implementations for OpenAI and Anthropic providers (interface only, not tested)

---

#### S1-05: Build retrieval pipeline step (hybrid search)

| Field | Value |
|---|---|
| **Owner** | Nancy + Atharva |
| **QA Buddy** | Nishka |
| **Estimate** | 3 days |
| **Days** | May 3-5 |
| **Bucket** | Data work + AI engineering |
| **Depends on** | S1-02 (KB indexed), S1-04 (LLM Gateway for embeddings) |

**Acceptance criteria**:
- [ ] Retrieve function accepts ticket text, returns top-K KB articles with relevance scores
- [ ] Query embedding generated via Vertex AI text-embedding-005
- [ ] Elasticsearch query combines kNN vector search + BM25 keyword match
- [ ] Results merged via Reciprocal Rank Fusion (RRF)
- [ ] Default K=3 (configurable)
- [ ] Each result includes: kb_id, title, content, relevance_score
- [ ] Unit test: known ticket retrieves expected KB article in top-3

---

#### S1-06: Build reason pipeline step

| Field | Value |
|---|---|
| **Owner** | Atharva |
| **QA Buddy** | Amit |
| **Estimate** | 2 days |
| **Days** | May 5-6 |
| **Bucket** | AI engineering |
| **Depends on** | S1-03 (classify), S1-05 (retrieve) |

**Acceptance criteria**:
- [ ] Reason function accepts ticket + retrieved KB articles + escalation rules
- [ ] Returns structured JSON: `{ action, reasoning, escalation_team?, required_context?, confidence }`
- [ ] Action is one of: Reply, Ask, Escalate
- [ ] Uses chain-of-thought prompting via versioned prompt template (`prompts/reason.txt`)
- [ ] If escalation rule matches, sets action=Escalate with correct team and context
- [ ] If KB match has resolution, sets action=Reply
- [ ] If insufficient info, sets action=Ask
- [ ] Unit test with 3 scenarios (Reply, Ask, Escalate) passes

---

#### S1-07: Build draft pipeline step

| Field | Value |
|---|---|
| **Owner** | Atharva |
| **QA Buddy** | Nishka |
| **Estimate** | 2 days |
| **Days** | May 6-7 |
| **Bucket** | AI engineering |
| **Depends on** | S1-06 (reason) |

**Acceptance criteria**:
- [ ] Draft function accepts ticket + KB articles + action + reasoning
- [ ] Returns: `{ draft_response, cited_kb_ids, tone }`
- [ ] Every claim in the draft response cites a KB article ID
- [ ] Response tone matches recommended action (helpful for Reply, clarifying for Ask, formal for Escalate)
- [ ] Prompt template versioned at `prompts/draft.txt`
- [ ] Unit test: given a Reply action with KB context, draft contains citation references

---

#### S1-08: Build pipeline orchestrator (LangChain.js)

| Field | Value |
|---|---|
| **Owner** | Atharva |
| **QA Buddy** | Amit |
| **Estimate** | 2 days |
| **Days** | May 7-8 |
| **Bucket** | AI engineering |
| **Depends on** | S1-03, S1-05, S1-06, S1-07 |

**Acceptance criteria**:
- [ ] Sequential chain: Classify → Retrieve → Reason → Draft → (Guardrails placeholder)
- [ ] Single entry point: `procesTicket(ticketText)` returns full pipeline output
- [ ] Each step's output is passed as input to the next
- [ ] Full pipeline output includes all intermediate results (classification, retrieval, reasoning, draft)
- [ ] Latency tracked end-to-end (start to finish timer)
- [ ] Pipeline output logged to MongoDB `audit_log` collection
- [ ] Integration test: one ticket through full pipeline produces valid output

---

#### S1-09: Build Express API endpoints

| Field | Value |
|---|---|
| **Owner** | Amit |
| **QA Buddy** | Nancy |
| **Estimate** | 2 days |
| **Days** | May 7-8 |
| **Bucket** | Application engineering |
| **Depends on** | S1-08 (pipeline orchestrator) |

**Acceptance criteria**:
- [ ] `POST /api/copilot/process` -- accepts ticket_id, runs pipeline, returns full output
- [ ] `GET /api/tickets` -- returns paginated list of tickets from MongoDB
- [ ] `GET /api/tickets/:id` -- returns single ticket with full details
- [ ] `POST /api/feedback` -- accepts feedback payload (ticket_id, helpful, edited_draft)
- [ ] Error handling middleware returns consistent error format
- [ ] Request logging middleware
- [ ] CORS configured for local React dev server

---

#### S1-10: Build React frontend (three-panel dashboard)

| Field | Value |
|---|---|
| **Owner** | Amit |
| **QA Buddy** | Shivani |
| **Estimate** | 4 days |
| **Days** | May 5-8 |
| **Bucket** | Application engineering |

**Acceptance criteria**:
- [ ] Three-panel layout: TicketQueue (left), TicketDetail (center), CopilotSidebar (right)
- [ ] TicketQueue: lists tickets from API, filterable by category/priority/status
- [ ] TicketDetail: shows full ticket text, metadata, SLA info
- [ ] CopilotSidebar: shows classification, KB matches, recommended action, draft response, confidence
- [ ] "Run Copilot" button triggers pipeline for selected ticket
- [ ] Loading state while pipeline runs
- [ ] FeedbackWidget: "Was this helpful?" + edit capability
- [ ] State management via React Context or Zustand
- [ ] Responsive enough to demo (not pixel-perfect)

---

#### S1-11: Build eval harness with golden dataset

| Field | Value |
|---|---|
| **Owner** | Nishka |
| **QA Buddy** | Atharva |
| **Estimate** | 4 days |
| **Days** | May 3-8 |
| **Bucket** | Quality, ops, & release |

**Acceptance criteria**:
- [ ] Golden dataset: 30-40 test cases in JSON format (per Evaluation Plan structure)
- [ ] Includes all 12 provided eval cases + 18-28 new cases curated by Nishka + Amit
- [ ] Scorers implemented: classification accuracy, retrieval accuracy, action accuracy
- [ ] `run-eval.js` CLI runs all scorers against the golden set
- [ ] Produces markdown report with per-metric scores
- [ ] Report includes per-category breakdown
- [ ] Failed cases listed with expected vs. actual
- [ ] CI integration: eval runs on every PR touching pipeline code
- [ ] Baseline metrics published and compared against Evaluation Plan thresholds

---

#### S1-12: Initial threat model

| Field | Value |
|---|---|
| **Owner** | Shubham |
| **QA Buddy** | Amit |
| **Estimate** | 3 days |
| **Days** | May 1-5 |
| **Bucket** | Governance & security |

**Acceptance criteria**:
- [ ] Threat surface identified: data flow diagram showing all entry/exit points
- [ ] STRIDE analysis for each component (Frontend, API, Pipeline, MongoDB, ES, Vertex AI)
- [ ] Top 5 threats ranked by severity
- [ ] Mitigation plan for each threat
- [ ] Secrets management approach documented (GCP Service Account, env vars)
- [ ] Reviewed by POD Lead

---

#### S1-13: Sprint 1 status report and demo preparation

| Field | Value |
|---|---|
| **Owner** | Shivani |
| **QA Buddy** | Amit |
| **Estimate** | 1 day |
| **Days** | May 9-10 |
| **Bucket** | Process |

**Acceptance criteria**:
- [ ] Weekly status email sent (May 5 or 6)
- [ ] Sprint 1 demo agenda prepared
- [ ] Demo rehearsal completed with Amit
- [ ] Risk register updated with any new risks from Sprint 1
- [ ] Backlog state documented (committed vs. completed vs. carry-over)

---

### Sprint 1 Day-by-Day View

| Day | Date | Amit | Atharva | Nancy | Nishka | Shubham | Shivani |
|---|---|---|---|---|---|---|---|
| 1 | May 1 (Thu) | S1-01: Repo + infra | -- (blocked on S1-01) | S1-02: Data ingestion | S1-11: Golden set curation | S1-12: Threat model | Sprint planning |
| 2 | May 2 (Fri) | S1-01 + S1-04: LLM Gateway | S1-03: Classify step | S1-02: Data ingestion | S1-11: Golden set curation | S1-12: Threat model | Weekly email draft |
| 3 | May 3 (Sat) | S1-04: LLM Gateway | S1-03: Classify step | S1-02 + S1-05: Retrieve | S1-11: Eval harness | S1-12: Threat model | -- |
| 4 | May 4 (Sun) | Code review | S1-03: Classify step | S1-05: Retrieve | S1-11: Eval harness | -- | -- |
| 5 | May 5 (Mon) | S1-10: React UI | S1-05 + S1-06: Reason | S1-05: Retrieve | S1-11: Eval harness | S1-12: Finalize | Mid-sprint check-in |
| 6 | May 6 (Tue) | S1-10: React UI | S1-06 + S1-07: Draft | Code review + data fixes | S1-11: Scorers | -- | Weekly status email |
| 7 | May 7 (Wed) | S1-09: API + S1-10: UI | S1-07 + S1-08: Orchestrator | QA buddy duties | S1-11: CI integration | -- | -- |
| 8 | May 8 (Thu) | S1-09 + S1-10: Integration | S1-08: Orchestrator | QA buddy duties | S1-11: Baseline run | -- | -- |
| 9 | May 9 (Fri) | Integration + bug fixes | Integration + bug fixes | Integration support | Eval run + report | Review + fixes | S1-13: Demo prep |
| 10 | May 10 (Sat) | Pre-demo + Demo | Demo support | -- | Eval results presented | -- | S1-13: Demo |

**Notes**:
- Weekend days (May 3-4, May 10) are included given the compressed timeline. Adjust based on team availability.
- "Code review" and "QA buddy duties" are tracked as overhead, not separate stories.
- Mid-sprint check-in with Prasanna on May 5.

### Sprint 1 Exit Criteria

**M1 -- Walking Skeleton**:
- [ ] One ticket → classify → retrieve → reason → draft → UI display, working end-to-end
- [ ] Pipeline runs through LLM Gateway (provider-agnostic)
- [ ] Output logged to audit trail

**M2 -- Eval Harness Operational**:
- [ ] Golden dataset committed (30-40 cases minimum)
- [ ] Automated scoring running (classification, retrieval, action accuracy)
- [ ] Baseline metrics published against Evaluation Plan thresholds
- [ ] CI integration: eval runs on PR

---

## Sprint 2: MVP + Hardening + Handover

**Dates**: May 11 -- May 16
**Sprint goal**: Feature-complete MVP with all eval gates passing, guardrails active, documentation delivered, and knowledge transfer ready.
**Milestone**: M3 (MVP Feature-Complete)
**Demo**: May 16 (final delivery)

### Sprint 2 Stories

#### S2-01: Build guardrails layer

| Field | Value |
|---|---|
| **Owner** | Shubham + Atharva |
| **QA Buddy** | Nishka |
| **Estimate** | 3 days |
| **Days** | May 11-13 |
| **Bucket** | Governance & security |

**Acceptance criteria**:
- [ ] Profanity filter: catches profanity in draft response output; flags but does not suppress
- [ ] PII check: detects customer PII in draft response; flags if PII is echoed unnecessarily
- [ ] Confidence gating: if any step confidence < threshold, adds warning to output
- [ ] Prompt injection detection: basic pattern matching for common injection attempts
- [ ] Hallucination check: verifies all claims in draft trace to cited KB articles
- [ ] Guardrail status included in pipeline output: `{ passed: bool, warnings: [] }`
- [ ] Guardrails run as Step 5 in the pipeline (post-processing)

---

#### S2-02: Build feedback loop

| Field | Value |
|---|---|
| **Owner** | Atharva |
| **QA Buddy** | Nancy |
| **Estimate** | 2 days |
| **Days** | May 11-12 |
| **Bucket** | AI engineering |

**Acceptance criteria**:
- [ ] `POST /api/feedback` stores: ticket_id, helpful (bool), original_draft, edited_draft, action_override, timestamp
- [ ] Feedback stored in MongoDB `feedback` collection
- [ ] UI FeedbackWidget sends feedback on "Accept" / "Edit & Accept" / "Reject"
- [ ] Feedback data accessible via `GET /api/feedback` (for future analysis)
- [ ] Agent can edit draft response before accepting

---

#### S2-03: Adversarial test cases

| Field | Value |
|---|---|
| **Owner** | Nishka + Shubham |
| **QA Buddy** | Atharva |
| **Estimate** | 2 days |
| **Days** | May 11-12 |
| **Bucket** | Quality, ops, & release |

**Acceptance criteria**:
- [ ] 15-20 adversarial test cases covering all 8 categories from Evaluation Plan Section 6
- [ ] At least: 2 out-of-scope, 2 prompt injection, 2 PII, 2 ambiguous, 2 multi-issue, 2 profane, 2 empty/gibberish, 2 non-English
- [ ] Expected behavior documented for each case
- [ ] Adversarial scorer integrated into eval harness
- [ ] Eval run with adversarial set produces separate report section
- [ ] Results reviewed and any guardrail gaps documented as bugs

---

#### S2-04: Prompt iteration and accuracy improvement

| Field | Value |
|---|---|
| **Owner** | Atharva |
| **QA Buddy** | Amit |
| **Estimate** | 3 days |
| **Days** | May 12-14 |
| **Bucket** | AI engineering |
| **Type** | Experiment story |

**Hypothesis**: Iterating prompts based on baseline eval results can bring all metrics from baseline to target (>= 85%).

**Success metric**: Classification, retrieval, and action accuracy all >= 85% on golden set.

**Time-box**: 3 days. Results reviewed on May 14 regardless of outcome.

**Acceptance criteria**:
- [ ] Review baseline eval results from Sprint 1
- [ ] Identify categories/scenarios with lowest accuracy
- [ ] Iterate classify prompt (at least 2 versions, eval each)
- [ ] Iterate reason prompt (at least 2 versions, eval each)
- [ ] Iterate draft prompt for faithfulness improvement
- [ ] Each iteration: PR with prompt change + eval results before/after
- [ ] Final eval results documented with delta from baseline

---

#### S2-05: Synthetic eval set (1,000 questions)

| Field | Value |
|---|---|
| **Owner** | Nishka + Atharva |
| **QA Buddy** | Amit |
| **Estimate** | 2 days |
| **Days** | May 13-14 |
| **Bucket** | Quality, ops, & release |

**Acceptance criteria**:
- [ ] 1,000 synthetic test questions generated across all 7 ticket categories
- [ ] Distribution weighted by production traffic estimates (not uniform)
- [ ] Mix of easy (40%), medium (40%), hard (20%)
- [ ] Reviewed by Nishka before use (not used blindly)
- [ ] Full eval run completed against synthetic set
- [ ] Results report generated with per-category breakdown
- [ ] Results shared with Prasanna's support team lead for review

---

#### S2-06: UI polish and confidence indicators

| Field | Value |
|---|---|
| **Owner** | Amit |
| **QA Buddy** | Shivani |
| **Estimate** | 2 days |
| **Days** | May 11-12 |
| **Bucket** | Application engineering |

**Acceptance criteria**:
- [ ] Confidence score displayed per pipeline step (color-coded: green/yellow/red)
- [ ] KB citations in draft response are clickable (show KB article content)
- [ ] Guardrail warnings displayed as banners in CopilotSidebar
- [ ] Escalation output shows team name and required context
- [ ] Loading states and error states polished
- [ ] Responsive layout works at common screen sizes

---

#### S2-07: Response faithfulness scorer (LLM-judge)

| Field | Value |
|---|---|
| **Owner** | Nishka |
| **QA Buddy** | Atharva |
| **Estimate** | 2 days |
| **Days** | May 12-13 |
| **Bucket** | Quality, ops, & release |

**Acceptance criteria**:
- [ ] LLM-judge scorer: sends draft response + cited KB articles to Gemini, asks if all claims are grounded
- [ ] Returns faithfulness score (0.0-1.0) per test case
- [ ] Integrated into eval harness as `faithfulness.js` scorer
- [ ] Runs as part of nightly eval (not on every PR -- too expensive)
- [ ] Results included in eval report

---

#### S2-08: Architecture document (final) + Model card

| Field | Value |
|---|---|
| **Owner** | Amit |
| **QA Buddy** | Shubham |
| **Estimate** | 2 days |
| **Days** | May 14-15 |
| **Bucket** | Documentation |

**Acceptance criteria**:
- [ ] Architecture document updated from sketch to final: includes actual implementation details, not just design
- [ ] ADRs documented for key decisions made during build
- [ ] Model card created: model used, task, metrics, limitations, ethical considerations
- [ ] Productionization note: what needs to change for Freshdesk integration, scaling, monitoring
- [ ] All docs committed to repo

---

#### S2-09: Knowledge transfer package

| Field | Value |
|---|---|
| **Owner** | Amit + Shivani |
| **QA Buddy** | Prasanna (client review) |
| **Estimate** | 2 days |
| **Days** | May 15-16 |
| **Bucket** | Documentation |

**Acceptance criteria**:
- [ ] Setup guide: step-by-step instructions to run the system from scratch
- [ ] Environment requirements: GCP permissions, Node.js version, MongoDB/ES versions
- [ ] Runbooks for top failure modes (API down, ES connection lost, Vertex AI rate limit)
- [ ] Prompt tuning guide: how to modify prompts and re-run eval
- [ ] Data refresh guide: how to add new KB articles and re-index
- [ ] Architecture diagram (final) included
- [ ] All eval results and reports included
- [ ] Codebase documentation (README files per directory)

---

#### S2-10: Security review sign-off

| Field | Value |
|---|---|
| **Owner** | Shubham |
| **QA Buddy** | Amit |
| **Estimate** | 2 days |
| **Days** | May 14-15 |
| **Bucket** | Governance & security |

**Acceptance criteria**:
- [ ] Code review for security: no hardcoded secrets, no SQL/NoSQL injection vectors, no XSS in frontend
- [ ] Guardrails tested against adversarial set -- no critical bypasses
- [ ] PII handling reviewed: draft responses do not echo unnecessary PII
- [ ] Dependency audit: no known critical CVEs in npm packages
- [ ] Security review document signed off
- [ ] Any blocking findings fixed before final demo

---

#### S2-11: Sprint 2 status report, final demo, and engagement summary

| Field | Value |
|---|---|
| **Owner** | Shivani + Amit |
| **QA Buddy** | -- |
| **Estimate** | 2 days |
| **Days** | May 15-16 |
| **Bucket** | Process |

**Acceptance criteria**:
- [ ] Sprint 2 status report delivered
- [ ] Final demo agenda prepared and rehearsed
- [ ] Engagement summary document: what was built, what was achieved, what comes next
- [ ] All eval metrics at target for 2 consecutive runs documented
- [ ] Sample outputs (10-12 across categories) prepared for demo
- [ ] Final demo delivered to Prasanna on May 16

---

### Sprint 2 Day-by-Day View

| Day | Date | Amit | Atharva | Nancy | Nishka | Shubham | Shivani |
|---|---|---|---|---|---|---|---|
| 11 | May 11 (Sun) | S2-06: UI polish | S2-02: Feedback loop | QA buddy | S2-03: Adversarial cases | S2-01: Guardrails | Sprint 2 planning |
| 12 | May 12 (Mon) | S2-06: UI polish | S2-02 + S2-04: Prompt iteration | QA buddy | S2-03 + S2-07: Faithfulness scorer | S2-01: Guardrails | Weekly status email |
| 13 | May 13 (Tue) | Code review + integration | S2-04: Prompt iteration | QA buddy | S2-05 + S2-07: Synthetic eval | S2-01: Guardrails | Weekly call prep |
| 14 | May 14 (Wed) | S2-08: Arch doc + model card | S2-04: Prompt iteration | -- | S2-05: Synthetic eval run | S2-10: Security review | -- |
| 15 | May 15 (Thu) | S2-08 + S2-09: KT package | Integration + bug fixes | -- | Final eval run | S2-10: Security sign-off | S2-11: Engagement summary |
| 16 | May 16 (Fri) | S2-09: KT + Final demo | Demo support | -- | Eval results presented | -- | S2-11: Final demo |

### Sprint 2 Exit Criteria

**M3 -- MVP Feature-Complete**:
- [ ] All in-scope capabilities (1-11 from Engagement Plan) implemented
- [ ] All AI quality metrics (classification, retrieval, action, faithfulness) at target for 2 consecutive nightly runs
- [ ] Adversarial eval cases run -- no critical failures
- [ ] Security review completed -- no blocking findings
- [ ] 1,000-question synthetic eval completed and shared with client
- [ ] All documentation delivered (architecture, model card, productionization note, KT package)

**Delivery Gate**:
- [ ] Knowledge transfer package complete
- [ ] Final demo and client walkthrough conducted
- [ ] Codebase ready for handover (clean, documented, no secrets)
- [ ] Engagement summary delivered

---

## Ceremony Schedule

### Sprint 1 (May 1-10)

| Ceremony | Date | Time | Duration | Attendees |
|---|---|---|---|---|
| Sprint 1 Planning | May 1 (Thu) AM | -- | 90 min | Full POD |
| Daily Standup | Daily | 09:30 | 15 min | Full POD |
| Mid-sprint Check-in | May 5 (Mon) PM | -- | 30 min | Amit + Shivani + Prasanna |
| Weekly Sync Call | May 6 (Tue) | -- | 30 min | Amit + Shivani + Prasanna |
| Pre-demo Verification | May 9 (Fri) AM | -- | 60 min | Amit + Nishka |
| Sprint 1 Demo | May 10 (Sat) AM | -- | 30 min | Full POD + Prasanna |
| Sprint 1 Retro | May 10 (Sat) PM | -- | 45 min | POD only |

### Sprint 2 (May 11-16)

| Ceremony | Date | Time | Duration | Attendees |
|---|---|---|---|---|
| Sprint 2 Planning | May 11 (Sun) AM | -- | 60 min | Full POD |
| Daily Standup | Daily | 09:30 | 15 min | Full POD |
| Mid-sprint Check-in | May 13 (Tue) PM | -- | 30 min | Amit + Shivani + Prasanna |
| Weekly Sync Call | May 13 (Tue) | -- | 30 min | Amit + Shivani + Prasanna |
| Pre-demo Verification | May 15 (Thu) AM | -- | 60 min | Amit + Nishka |
| Final Demo | May 16 (Fri) | -- | 45 min | Full POD + Prasanna |
| Final Retro | May 16 (Fri) PM | -- | 45 min | POD only |

---

## Definition of Done (All Stories)

Per Doc 04, Section 4.4:

- [ ] Code reviewed and merged to main; no open PRs against the story
- [ ] Automated tests cover new behavior; tests pass in CI
- [ ] QA buddy has verified acceptance criteria in a clean environment
- [ ] If the change touches AI behavior: eval harness run, thresholds met or deviation documented
- [ ] If the change introduces data flow: lineage and PII handling documented
- [ ] If the change has security impact: Governance Engineer signed off
- [ ] Documentation updated (README, ADR, or runbook as appropriate)
- [ ] Story works in dev environment and is deployable to staging

**Author cannot mark their own story Done** -- QA buddy moves it to Done.

---

## Story Dependency Graph

```
S1-01 (Repo + infra)
  ├─► S1-04 (LLM Gateway)
  │     └─► S1-03 (Classify) ──┐
  │                             ├─► S1-08 (Orchestrator) ─► S1-09 (API) ─┐
  │     S1-02 (Data ingestion) ─┤                                         │
  │           └─► S1-05 (Retrieve) ─► S1-06 (Reason) ─► S1-07 (Draft) ──┘
  │                                                                       │
  │                                                            S1-10 (UI) ◄┘
  │
  S1-11 (Eval harness) ──── runs independently, needs pipeline by Day 8
  S1-12 (Threat model) ──── runs independently
  S1-13 (Status/demo) ──── final 2 days

Sprint 2 stories depend on Sprint 1 completion:
  S2-01 (Guardrails) ─► plugs into S1-08 pipeline
  S2-02 (Feedback) ─► uses S1-09 API
  S2-03 (Adversarial) ─► extends S1-11 eval harness
  S2-04 (Prompt iteration) ─► uses S1-11 eval results
  S2-05 (Synthetic eval) ─► extends S1-11 eval harness
  S2-06 (UI polish) ─► extends S1-10 UI
  S2-07 (Faithfulness) ─► extends S1-11 eval harness
```

---

## Carry-Over Policy

If a Sprint 1 story is not completed:
1. **Critical path** (S1-03 through S1-08, S1-10): carries over as top priority in Sprint 2; scope from Sprint 2 is cut per Risk Register contingency plan
2. **Non-critical path** (S1-11, S1-12, S1-13): carries over but does not block Sprint 2 feature work
3. Any carry-over is explicitly stated in the Sprint 1 demo -- no hidden debt

---

## Change Log

| Date | Change | By |
|---|---|---|
| 2026-05-01 | Initial sprint plan created with 24 stories across 2 sprints | Shivani + Amit |

---

*Sprint plan is a commitment to scope, not a contract on dates. If scope needs to flex, the Risk Register contingency plan defines pre-approved cuts. The PM updates this plan via the Change Request process (Doc 03, Section 8).*
