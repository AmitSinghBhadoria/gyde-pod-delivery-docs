---
sidebar_position: 4
title: POD Charter
---

# POD Charter -- AI Support Copilot

**Engagement**: AI Support Copilot Pilot
**Version**: 1.0
**Date**: 2026-04-30
**Framework ref**: Doc 01, Section 6

**Signatories**:

| Role | Name | Signature | Date |
|---|---|---|---|
| POD Lead | Amit | __________ | __________ |
| Implementation Manager | Shivani | __________ | __________ |
| Client Sponsor | Prasanna | __________ | __________ |

---

## 1. Mission

Deliver a working AI copilot that enables support agents to resolve tickets faster and more consistently by automating classification, knowledge retrieval, action recommendation, and response drafting -- targeting 85% accuracy and autonomous handling of 30% of recurring tickets, while maintaining human approval on every response. The pilot will validate feasibility, establish baseline metrics, and produce a complete knowledge transfer package for production deployment.

---

## 2. Success Criteria

| # | Metric | Type | Target | Measurement Method |
|---|---|---|---|---|
| 1 | Classification accuracy | AI Quality | >= 85% | Exact match on category + priority against golden dataset |
| 2 | Retrieval accuracy | AI Quality | >= 85% | Expected KB article appears in top-K retrieved set |
| 3 | Action recommendation accuracy | AI Quality | >= 85% | Exact match on recommended action (Reply / Ask / Escalate) |
| 4 | Response acceptance rate | Business | >= 70% | % of drafts agents accept without major rewriting |
| 5 | Auto-answer coverage | Business | 30% | % of recurring tickets copilot handles autonomously (with human approval) |

**Go-live validation**: 1,000 synthetic questions evaluated by client's support team lead before production readiness sign-off.

---

## 3. Scope and Out-of-Scope

### In Scope (Phase 1 Pilot)

- Ticket classification (category, priority, sentiment)
- KB article retrieval via hybrid search (vector + BM25)
- Action recommendation (Reply / Ask for more info / Escalate) with reasoning
- Response drafting grounded in KB articles with citations
- Confidence scoring per output
- Feedback loop (agent rates/edits responses, system stores corrections)
- Guardrails (profanity filter, misuse prevention, graceful failure)
- Standalone web application (three-panel dashboard: ticket queue, detail, copilot sidebar)
- Evaluation harness with automated scoring
- 1,000-question synthetic evaluation run
- Complete documentation and knowledge transfer package

### Out of Scope (Phase 1)

- Freshdesk API integration (architecture designed for it, not built)
- Multi-language support (English only)
- Customer-facing AI (agent-facing only)
- Auto-send / autonomous resolution without human approval
- Live KB refresh (static dataset for pilot)
- Production deployment, scaling, load testing
- Phase 2 features (not yet defined)

---

## 4. Operating Cadence

| Ceremony | Frequency | Duration | Participants | Owner |
|---|---|---|---|---|
| Sprint | 2 sprints total | Sprint 1: May 1-10, Sprint 2: May 11-16 | Full POD | Shivani |
| Weekly status email | Weekly | Async (written) | Prasanna, POD | Shivani |
| Weekly sync call | Weekly | 30 min (Google Meet) | Prasanna, Amit, Shivani | Shivani |
| Sprint demo | Per sprint | 30-45 min | Prasanna, full POD | Amit |
| POD standup | Daily | 15 min (internal) | Full POD | Amit |
| Sprint retro | Per sprint | 30 min (internal) | Full POD | Amit |

**Channels**: Email for written updates, Google Meet for calls.

**Decision turnaround**: Client commits to 2 hours to 1 business day for all decisions.

---

## 5. Decision Rights

| Tier | Authority | Examples | Escalation needed? |
|---|---|---|---|
| **POD-Internal** | POD Lead + owning role | Library choice, prompt structure, code style, sprint task ordering | No |
| **POD Lead** | Amit, informed by POD | Architecture patterns, model selection, evaluation thresholds, release readiness, tech stack changes | No |
| **Client Approval** | Prasanna + Shivani | Scope changes, milestone shifts, data access changes, success criteria changes, production deployment decisions | Yes -- Shivani raises to Prasanna |
| **Gyde Leadership** | Engineering Director | Deviation from framework non-negotiables, commercial changes | Yes -- Amit raises to Gyde leadership |

---

## 6. Escalation Paths

| Escalation Type | Gyde Contact | Client Contact |
|---|---|---|
| **Technical** | Amit (POD Lead) | Prasanna |
| **Delivery / Commercial** | Shivani (PM) | Prasanna |
| **Governance / Security** | Shubham (Governance Eng) | Prasanna |
| **2nd Level (Gyde)** | Shubham (Escalation SPOC) | -- |

**Escalation protocol**: Same-day transparency. If any risk materializes, the client hears about it within the same business day via email, not deferred to the weekly update.

---

## 7. Definition of Done

An increment is releasable to the client environment when ALL of the following are met:

| # | Gate | Verified by |
|---|---|---|
| 1 | All acceptance criteria for committed stories are met | Nishka (QA) |
| 2 | Evaluation metrics are at or above target thresholds | Nishka + Amit |
| 3 | No critical or high-severity bugs open | Nishka |
| 4 | Code reviewed and merged to main branch | Amit |
| 5 | All prompts and data versioned in source control | Atharva + Nancy |
| 6 | Security review passed (no blocking findings) | Shubham |
| 7 | Documentation updated (architecture, ADRs, runbooks) | Amit |
| 8 | Demo-ready in staging environment | Amit |

---

## 8. Risks and Assumptions

### Top 5 Risks

| # | Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|---|
| 1 | Low dataset diversity (11 unique scenarios) limits model generalization | High | High | Generate diverse synthetic data early; flag limitation to client | Nishka + Atharva |
| 2 | Tight timeline (16 days) with hard deadlines leaves no buffer | High | High | Ruthless prioritization; cut polish, not core capabilities; daily standup to catch blockers early | Shivani + Amit |
| 3 | Gemini accuracy may not reach 85% on first pass for all metrics | Medium | High | Build LLM-agnostic architecture; have fallback to GPT-4o or Claude; iterate prompts rapidly | Atharva + Amit |
| 4 | Reporting category has zero training data but is in eval set | Medium | Medium | Add 2-3 synthetic Reporting tickets; accept cold-start performance and document | Nancy |
| 5 | On-prem handover requirements may surface late constraints | Low | Medium | Document all dependencies and infrastructure early; use only self-hostable components | Amit |

### Assumptions

| # | Assumption | Impact if wrong |
|---|---|---|
| 1 | Excel dataset is representative of production ticket patterns | Pilot accuracy won't predict production accuracy |
| 2 | Prasanna is available for decisions within 1 business day | Sprint velocity drops; scope may slip |
| 3 | GCP Vertex AI APIs are stable and available throughout the pilot | Need to switch LLM provider mid-sprint |
| 4 | 85% accuracy is achievable with the provided KB content | May need to renegotiate thresholds or expand KB |
| 5 | Team members are dedicated to this engagement (no competing priorities) | Deliverables at risk; may miss hard deadlines |

---

## Non-Negotiable Adherence

Per Doc 01, Section 5.1, this engagement adheres to all five framework non-negotiables:

| # | Non-Negotiable | How We Fulfill It |
|---|---|---|
| 1 | Threat modeling and secrets management | Shubham delivers threat model; all API keys via GCP Secret Manager or env vars, never in code |
| 2 | Evaluation before production | Eval harness gates every release; 1,000-question run before go-live |
| 3 | Versioned data and prompts | All prompts, datasets, and configs in Git; every change is a tracked commit |
| 4 | Audit trail for AI decisions | Every copilot decision logged with input, output, confidence, reasoning, and sources |
| 5 | Incident response readiness | Runbooks for top failure modes included in knowledge transfer package |

---

## POD Composition

| Role | Name | Key Responsibilities |
|---|---|---|
| POD Lead | Amit | Architecture, UI, code review, tech decisions, demos |
| AI Engineer | Atharva | LLM prompts, retrieval pipeline, confidence scoring, feedback loop |
| Data Engineer | Nancy | Data ingestion, KB indexing, embeddings, vector store, data quality |
| QA | Nishka | Eval harness, golden dataset, synthetic data, adversarial testing |
| Governance Engineer | Shubham | Threat model, guardrails, security review, compliance |
| Implementation Manager | Shivani | Charter, sprint planning, status reports, risk register, client comms |

---

*This charter is effective upon signature by all three signatories and remains in force for the duration of the engagement. Any material changes require written agreement from all parties.*
