---
sidebar_position: 7
title: Risk Register
---

# Risk Register -- AI Support Copilot

**Engagement**: AI Support Copilot Pilot
**Owner**: Shivani (PM), with risk owners per item
**Version**: 1.0
**Date**: 2026-05-01
**Framework ref**: Doc 03, Section 6

> This is a **living document**. Updated weekly by the PM, reviewed in every sprint demo, and visible to the client. Any POD member can raise a new risk at any time -- no prior approval needed.

---

## Scoring Guide

| Level | Likelihood | Impact |
|---|---|---|
| **High** | > 60% chance of occurring | Blocks milestone or delivery; requires scope change |
| **Medium** | 30-60% chance | Delays timeline or degrades quality; recoverable with effort |
| **Low** | < 30% chance | Minor inconvenience; handled within normal sprint work |

**Risk Score** = Likelihood x Impact. High/High = Critical. Any Critical risk requires a mitigation plan with specific actions and dates.

---

## Active Risks

### Technical Risks

| ID | Risk | L | I | Score | Early Signal | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|---|---|
| R-01 | **Gemini accuracy does not reach 85% on all metrics** | M | H | High | Eval results plateau below target after 2 prompt iterations | LLM Gateway enables zero-code swap to GPT-4o or Claude; rapid prompt iteration in Sprint 1; per-step model selection (different model per pipeline step if needed) | Atharva + Amit | Open |
| R-02 | **End-to-end latency exceeds 15s hard limit** | M | M | Medium | Walking skeleton p95 > 10s | Parallelize classify + retrieve steps; implement streaming for draft step; consider smaller model for classification; add response caching for repeated tickets | Atharva | Open |
| R-03 | **Elasticsearch hybrid search (vector + BM25) underperforms on small KB** | M | M | Medium | Retrieval accuracy < 75% on golden set despite correct KB articles existing | Tune RRF parameters; adjust BM25 boost weights; increase embedding chunk overlap; consider adding keyword-based fallback | Atharva + Nancy | Open |
| R-04 | **LangChain.js introduces abstraction overhead or breaking changes** | L | M | Medium | Unexpected behavior in structured output parsing or provider switching | Pin exact versions in package.json; write integration tests for each pipeline step; have fallback to direct Vertex AI SDK calls | Amit | Open |

### Data Risks

| ID | Risk | L | I | Score | Early Signal | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|---|---|
| R-05 | **Low dataset diversity (11 unique scenarios from 36 tickets) limits model generalization** | H | H | Critical | Classification accuracy varies wildly across categories; overfits to seen patterns | Generate 30-40 diverse golden set cases by May 5; generate 1,000 synthetic eval set by May 14; flag limitation to client explicitly | Nishka + Atharva | Open |
| R-06 | **Reporting category has zero training data but is in eval set** | M | M | Medium | Reporting tickets consistently misclassified | Nancy adds 2-3 synthetic Reporting tickets to dataset; accept cold-start performance and document as known limitation | Nancy | Open |
| R-07 | **KB articles lack sufficient depth for grounded responses** | M | H | High | Response faithfulness < 80%; draft responses are generic despite correct retrieval | Review KB content with Prasanna; identify gaps; supplement with additional KB content or adjust expectations for thin categories | Amit + Nancy | Open |
| R-08 | **Excel-to-production data shape mismatch** | L | M | Medium | Fields in Excel don't map cleanly to Freshdesk API schema | Design data ingestion with abstraction layer; document mapping assumptions; validate schema with Prasanna during Sprint 1 | Nancy | Open |

### Timeline & Organisational Risks

| ID | Risk | L | I | Score | Early Signal | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|---|---|
| R-09 | **Tight timeline (16 days) with hard deadlines leaves no buffer** | H | H | Critical | Any task taking longer than estimated by Day 3 | Ruthless prioritization: cut polish, not core capabilities; daily standup catches blockers within 24 hours; pre-define scope cuts if needed (see Contingency section below) | Shivani + Amit | Open |
| R-10 | **Team members pulled to competing priorities** | M | H | High | Team member misses standup or deliverable date | Confirm dedicated allocation with all team members at sprint kickoff; escalate to Gyde leadership immediately if competing work appears | Shivani | Open |
| R-11 | **Client decision turnaround exceeds 1 business day** | L | M | Medium | Prasanna unavailable for > 24 hours during a decision-dependent task | Batch decisions into weekly call agenda; identify backup decision-maker; keep parallel work available when blocked | Shivani | Open |
| R-12 | **Knowledge transfer package is deprioritized under time pressure** | M | M | Medium | Documentation tasks consistently deferred to "later" | Documentation is a sprint deliverable, not a post-sprint activity; assign specific doc tasks per sprint; Amit owns architecture doc, Shivani owns engagement docs | Amit + Shivani | Open |

### Security & Governance Risks

| ID | Risk | L | I | Score | Early Signal | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|---|---|
| R-13 | **On-prem handover requirements surface late constraints** | L | M | Medium | Client's infra team flags incompatible components post-pilot | Document all dependencies and infrastructure requirements early; use only self-hostable components (no managed-only services); share infra requirements doc with Prasanna by Sprint 1 demo | Amit | Open |
| R-14 | **GCP Service Account permissions insufficient or misconfigured** | L | H | Medium | Vertex AI API calls fail during initial setup | Document exact IAM roles needed; test Service Account permissions before Sprint 1 code starts; have fallback API key auth for dev environment | Amit | Open |
| R-15 | **Guardrails fail to catch adversarial inputs** | M | M | Medium | Adversarial eval set reveals bypasses in profanity/PII/injection checks | Build adversarial test cases early (by May 10); layer multiple guardrail checks; human review remains mandatory for all responses | Shubham + Nishka | Open |

### Commercial Risks

| ID | Risk | L | I | Score | Early Signal | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|---|---|
| R-16 | **Cost per ticket exceeds client expectations** | M | M | Medium | Token usage from M1 estimates projects > $0.50/ticket at production volume | Model tiering (smaller model for classification, larger for drafting); prompt compression; response caching for recurring ticket patterns | Atharva + Amit | Open |
| R-17 | **Pilot success creates unrealistic production expectations** | L | M | Medium | Client assumes pilot accuracy will hold at 10x volume with real data | Set expectations in every demo: pilot uses curated data; production accuracy depends on KB quality and data diversity; document gaps explicitly in handover package | Shivani + Amit | Open |

---

## Risk Contingency Plan

If R-09 (timeline) materializes, the following scope cuts are pre-approved at POD level (no client approval needed for these specific cuts):

| Priority | What Gets Cut | Impact | When to Cut |
|---|---|---|---|
| 1 (first cut) | UI polish and visual refinements | Functional but less polished interface | If behind by Day 5 |
| 2 | Synthetic 1,000-question eval (reduce to 500) | Slightly less eval coverage; still statistically meaningful | If behind by Day 8 |
| 3 | Feedback loop (save corrections) | Agents can still use copilot; corrections not stored for learning | If behind by Day 10 |
| 4 | Confidence scoring granularity (binary instead of percentage) | Less nuanced confidence display; still shows high/low | If behind by Day 10 |

**Scope cuts that require client approval** (per POD Charter, Section 5):
- Reducing eval thresholds below minimum
- Dropping guardrails
- Removing any pipeline step (classify, retrieve, reason, draft)
- Changing delivery dates

---

## Assumptions Register

Each assumption is a belief the plan rests on. If an assumption proves wrong, it becomes a risk.

| ID | Assumption | Impact if Wrong | Validation Method | Validated? |
|---|---|---|---|---|
| A-01 | Excel dataset is representative of production ticket patterns | Pilot accuracy won't predict production accuracy | Compare Excel categories against Freshdesk category distribution (ask Prasanna) | No |
| A-02 | Prasanna is available for decisions within 1 business day | Sprint velocity drops; scope may slip | Confirmed in discovery call; monitor weekly | Yes |
| A-03 | GCP Vertex AI APIs are stable and available throughout the pilot | Need to switch LLM provider mid-sprint | Test API availability during setup; LLM Gateway provides fallback | No |
| A-04 | 85% accuracy is achievable with the provided KB content | May need to renegotiate thresholds or expand KB | Baseline metrics from M2 eval harness will validate | No |
| A-05 | Team members are dedicated to this engagement (no competing priorities) | Deliverables at risk; may miss hard deadlines | Confirm with each team member at sprint kickoff | No |
| A-06 | 12 KB articles cover the primary resolution paths for common ticket types | Retrieval step will have coverage gaps | Map KB articles to ticket categories; identify unmapped categories | No |
| A-07 | Gemini via Vertex AI produces reliable structured JSON output | Pipeline steps fail to parse LLM output | Validate during walking skeleton (M1); LangChain.js structured output parsing | No |
| A-08 | MongoDB and Elasticsearch can run on existing GCP VM without performance issues | Need separate infrastructure or managed services | Load test during Sprint 1 with full pipeline | No |

---

## Dependencies Register

| ID | Dependency | Provider | Needed By | Status |
|---|---|---|---|---|
| D-01 | GCP Service Account with Vertex AI permissions | Amit (setup) | May 2 (Sprint 1 Day 2) | Pending |
| D-02 | GCP VM access for MongoDB + Elasticsearch | Amit (existing infra) | May 2 | Pending |
| D-03 | Dataset (Excel file with tickets, KB, escalation rules, eval cases) | Prasanna (provided) | Available now | Done |
| D-04 | Client review of expanded golden dataset (30-40 cases) | Prasanna or support team lead | May 5 | Pending |
| D-05 | Client review of 1,000 synthetic eval results | Prasanna's support team lead | May 15 | Pending |
| D-06 | Decision on target cost-per-ticket for production | Prasanna | Next weekly call | Pending |

---

## Review Cadence

| Activity | Frequency | Participants |
|---|---|---|
| PM reviews and updates register | Weekly (minimum) | Shivani |
| Top-5 risks reviewed in POD standup | Weekly | Full POD |
| Risk summary in client status email | Weekly | Prasanna, Shivani |
| Risk discussion in sprint demo | Per sprint | Prasanna, full POD |
| New risk raised by any team member | Continuous | Anyone |

---

## Change Log

| Date | Change | By |
|---|---|---|
| 2026-05-01 | Initial risk register created with 17 risks, 8 assumptions, 6 dependencies | Shivani + Amit |

---

*Risk register is a living document. "Risks tracked but never mitigated" is an anti-pattern (Doc 03, Section 9). Every risk with a mitigation plan must have specific actions, not just words.*
