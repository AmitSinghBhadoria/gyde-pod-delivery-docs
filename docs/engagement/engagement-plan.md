---
sidebar_position: 8
title: Engagement Plan
---

# Engagement Plan -- AI Support Copilot

**Engagement**: AI Support Copilot Pilot
**Owner**: Shivani (PM)
**Version**: 1.0
**Date**: 2026-05-01
**Framework ref**: Doc 03, Section 7

---

## 1. Executive Summary

Gyde AI POD will deliver a working AI Support Copilot that enables support agents to resolve tickets faster and more consistently. The copilot automates classification, knowledge retrieval, action recommendation, and response drafting -- with human approval on every response.

**Mission**: Achieve 85% accuracy across classification, retrieval, and action recommendation, with 30% of recurring tickets handled autonomously (human-approved), within a 16-day pilot using curated data.

**Key success metrics**:
- Classification accuracy >= 85%
- Retrieval accuracy >= 85%
- Action accuracy >= 85%
- Response acceptance rate >= 70%
- Auto-answer coverage >= 30%

**Duration**: 16 days (May 1 -- May 16, 2026)
**Milestones**: M0 (Charter signed) → M1 (Walking skeleton) → M2 (Eval harness) → M3 (MVP feature-complete)
**Team**: 6-person POD (POD Lead, AI Engineer, Data Engineer, QA, Governance, PM)
**Top risks**: Dataset diversity (Critical), tight timeline (Critical), LLM accuracy uncertainty (High)

---

## 2. Scope

### In Scope (Phase 1 Pilot)

| # | Capability | Description |
|---|---|---|
| 1 | Ticket classification | Category, priority, sentiment, confidence via LLM |
| 2 | KB retrieval | Hybrid search (vector + BM25) over Elasticsearch |
| 3 | Action recommendation | Reply / Ask for more info / Escalate with reasoning |
| 4 | Response drafting | Grounded response with KB citations |
| 5 | Confidence scoring | Per-step confidence indicators |
| 6 | Feedback loop | Agent rates/edits responses; corrections stored |
| 7 | Guardrails | Profanity filter, PII check, misuse prevention, confidence gating |
| 8 | Web application | Three-panel dashboard (ticket queue, detail, copilot sidebar) |
| 9 | Evaluation harness | Automated scoring against golden dataset |
| 10 | Synthetic evaluation | 1,000-question eval run reviewed by client's support lead |
| 11 | Documentation | Architecture docs, model card, knowledge transfer package |

### Out of Scope (Phase 1)

| # | Exclusion | Rationale |
|---|---|---|
| 1 | Freshdesk API integration | Architecture designed for it; not built in pilot (uses Excel data) |
| 2 | Multi-language support | English only for pilot |
| 3 | Customer-facing AI | Agent-facing only; no direct customer interaction |
| 4 | Auto-send without approval | Human always approves before sending |
| 5 | Live KB refresh | Static dataset; real-time refresh is production scope |
| 6 | Production deployment | Pilot validates feasibility; production is a separate engagement |
| 7 | Load testing / scaling | Not needed for pilot; noted in productionization doc |
| 8 | Phase 2 features | Not yet defined by client |

---

## 3. Milestone Schedule

### Timeline Overview

```
May 1                May 5          May 10              May 14    May 16
  |-------- Sprint 1 --------|----------- Sprint 2 ------------|
  M0                  mid         M1+M2                  mid       M3
  Charter            Golden       Skeleton               Synth    MVP
  signed             set          + Harness              eval     delivery
```

### Milestone Details

| # | Milestone | Target Date | Exit Criteria |
|---|---|---|---|
| M0 | Charter & Eval Plan signed | May 1 | POD Charter signed; Evaluation Plan agreed; GCP environment provisioned; threat model in flight |
| M1 | Walking skeleton | May 10 | One ticket → classify → retrieve → reason → draft → UI display, working end-to-end in dev |
| M2 | Eval harness operational | May 10 | Golden dataset committed (30-40 cases); automated scoring running; baseline metrics published |
| M3 | MVP feature-complete | May 16 | All scope items built; eval metrics at target for 2 consecutive runs; security review passed; documentation delivered |

**Note**: M1 and M2 are targeted for the same Sprint 1 demo (May 10). This is intentional -- the walking skeleton produces the outputs the harness needs to score. M4-M6 (production deployment, stable operation, engagement close) are out of scope for this pilot.

---

## 4. Estimation Summary

### Effort by Bucket

| Bucket | Scope | Share | Notes |
|---|---|---|---|
| **Data work** | Excel ingestion, KB indexing, embeddings, data quality, synthetic data generation | ~25% | Lower than typical (20-40%) because pilot uses curated Excel, not messy production data |
| **AI engineering** | Prompts, pipeline (classify/retrieve/reason/draft), retrieval tuning, confidence scoring, feedback loop | ~30% | Core of the engagement; highest uncertainty |
| **Application engineering** | Express API, React UI (three-panel), LLM Gateway, MongoDB integration, ES integration | ~25% | Higher than typical (15-25%) because of standalone web app requirement |
| **Governance & security** | Threat model, guardrails (profanity, PII, injection), security review | ~10% | At framework minimum; pilot is internal-facing |
| **Quality, ops, & release** | Eval harness, golden dataset, adversarial cases, synthetic eval, CI integration, documentation | ~10% | At framework minimum; eval harness is critical path |

### Estimation Method

**Primary method**: Time-boxed (Doc 03, Section 4.2). Duration is fixed at 16 days; scope is shaped to fit. The contingency plan in the Risk Register defines pre-approved scope cuts.

**Estimation modifiers applied**:
- Data quality: +0% (curated Excel dataset, clean)
- Novel use case: +0% (RAG over KB is a known pattern with Gyde reference architecture)
- Internal-facing only: -10% (no customer-facing surface risk)
- Tight timeline: +15% (compressed from typical 6-week build into 16 days)
- **Net modifier**: +5%

### Confidence Level

Given the fixed timeline and hard deadlines, confidence in delivering all scope items is **Medium**. The contingency plan mitigates this -- core capabilities (pipeline + eval) are protected; polish and expansion features are the flex.

---

## 5. Team & Engagement Model

### POD Composition

| Role | Name | Allocation | Key Deliverables |
|---|---|---|---|
| POD Lead | Amit | Full-time | Architecture, UI, code review, demos, tech decisions |
| AI Engineer | Atharva | Full-time | Pipeline (classify, retrieve, reason, draft), prompts, confidence scoring, feedback loop |
| Data Engineer | Nancy | Full-time | Data ingestion, KB indexing, embeddings, vector store, data quality |
| QA | Nishka | Full-time | Eval harness, golden dataset, adversarial cases, synthetic eval |
| Governance Engineer | Shubham | Part-time | Threat model, guardrails, security review |
| Implementation Manager | Shivani | Part-time | Charter, sprint planning, status reports, risk register, client comms |

### Client Counterparts

| Client Role | Name | Responsibilities |
|---|---|---|
| Client Sponsor (CIO + Business Lead + Product Owner) | Prasanna | Decisions, sign-offs, success criteria, domain expertise |
| Support Team Lead | TBD (via Prasanna) | Reviews synthetic eval results, validates accuracy |

### Engagement Model

- POD operates as a self-contained delivery unit
- All team members report to POD Lead (Amit) for technical decisions
- PM (Shivani) manages client communication and engagement logistics
- Client has a single point of contact (Shivani for process, Amit for technical)

---

## 6. Risk Register Summary

Top 5 risks (full register in separate document):

| # | Risk | Score | Owner |
|---|---|---|---|
| R-05 | Low dataset diversity (11 unique scenarios) | Critical | Nishka + Atharva |
| R-09 | Tight timeline (16 days) with hard deadlines | Critical | Shivani + Amit |
| R-01 | Gemini accuracy may not reach 85% | High | Atharva + Amit |
| R-07 | KB articles lack sufficient depth | High | Amit + Nancy |
| R-10 | Team members pulled to competing priorities | High | Shivani |

See [Risk Register](./risk-register.md) for full details including mitigation plans, assumptions, dependencies, and contingency plan.

---

## 7. Assumptions & Dependencies

### Key Assumptions

| # | Assumption | Validated? |
|---|---|---|
| A-01 | Excel dataset is representative of production ticket patterns | No |
| A-02 | Prasanna available for decisions within 1 business day | Yes |
| A-03 | GCP Vertex AI APIs stable throughout pilot | No |
| A-04 | 85% accuracy achievable with provided KB content | No |
| A-05 | Team members dedicated (no competing priorities) | No |

### Key Dependencies

| # | Dependency | Provider | Needed By | Status |
|---|---|---|---|---|
| D-01 | GCP Service Account with Vertex AI permissions | Amit | May 2 | Pending |
| D-02 | GCP VM for MongoDB + Elasticsearch | Amit | May 2 | Pending |
| D-03 | Dataset (Excel) | Prasanna | Now | Done |
| D-04 | Client review of expanded golden set | Prasanna | May 5 | Pending |
| D-05 | Client review of 1,000 synthetic eval results | Support lead | May 15 | Pending |
| D-06 | Decision on target cost-per-ticket | Prasanna | Next weekly call | Pending |

---

## 8. Commercial Summary

| Item | Detail |
|---|---|
| **Engagement type** | Pilot / Proof of Concept |
| **Duration** | 16 days (May 1 -- May 16, 2026) |
| **Team size** | 6 (4 full-time, 2 part-time) |
| **Infrastructure** | Gyde's GCP account for pilot; client bears no infra cost during pilot |
| **LLM costs** | Borne by Gyde during pilot (Vertex AI / Gemini API costs) |
| **Budget constraints** | None specified by client for pilot phase |
| **Post-pilot** | Full codebase and knowledge transfer to client; client deploys on own infrastructure |
| **Change request process** | Per Doc 03, Section 8 -- any scope/schedule/cost change logged, impact-assessed within 3 days, decided by client sponsor + Gyde |

---

## 9. Governance & Reporting

### Communication Cadence

| Activity | Frequency | Channel | Participants |
|---|---|---|---|
| POD standup | Daily | Internal (Slack/Meet) | Full POD |
| Weekly status email | Weekly | Email | Prasanna, POD |
| Weekly sync call | Weekly | Google Meet (30 min) | Prasanna, Amit, Shivani |
| Sprint demo | Per sprint (May 10, May 16) | Google Meet | Prasanna, full POD |
| Sprint retro | Per sprint | Internal | Full POD |

### Status Report Format

Weekly status email includes:
- Sprint progress (stories completed / in progress / blocked)
- Eval metrics delta (if harness is operational)
- Top 3 risks with status changes
- Blockers requiring client action
- Next week's plan

### Decision Escalation

| Tier | Authority | Examples |
|---|---|---|
| POD-Internal | POD Lead + owning role | Library choice, prompt structure, code style |
| POD Lead | Amit | Architecture patterns, model selection, release readiness |
| Client Approval | Prasanna via Shivani | Scope changes, milestone shifts, success criteria changes |
| Gyde Leadership | Engineering Director | Framework non-negotiable deviations |

---

## 10. Non-Negotiable Compliance

Per Doc 01, Section 5.1, this engagement adheres to all five framework non-negotiables:

| # | Non-Negotiable | Fulfillment |
|---|---|---|
| 1 | Threat modeling and secrets management | Shubham delivers threat model; secrets via GCP Secret Manager or env vars |
| 2 | Evaluation before production | Eval harness gates every release; 1,000-question run before delivery |
| 3 | Versioned data and prompts | All prompts, datasets, configs in Git |
| 4 | Audit trail for AI decisions | Every copilot decision logged with full pipeline output |
| 5 | Incident response readiness | Runbooks in knowledge transfer package |

---

## Change Log

| Date | Change | By |
|---|---|---|
| 2026-05-01 | Initial engagement plan created | Shivani + Amit |

---

*This plan is the definitive reference for the engagement. Any changes to scope, milestones, or commercial terms follow the Change Request process (Doc 03, Section 8). The plan is signed off by the client sponsor and triggers Sprint 1.*
