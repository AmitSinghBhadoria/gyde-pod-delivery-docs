---
sidebar_position: 2
title: Use Case Canvas
---

# Use Case Canvas -- AI Support Copilot

**Engagement**: AI Support Copilot Pilot
**Client**: Prasanna
**Version**: 1.0
**Date**: 2026-04-30
**Authors**: Amit (POD Lead), Shivani (PM)
**Framework ref**: Doc 03, Section 3.2

> Single-page canvas. If this cannot be completed, the engagement is not ready to estimate.

---

## Mission Statement

Enable support agents to resolve tickets faster and more consistently by providing an AI copilot that classifies incoming tickets, retrieves relevant KB articles, recommends the next-best-action, and drafts grounded responses -- reducing resolution time from hours/days to minutes while maintaining human approval on every response.

---

## Users & Volumes

| Dimension | Detail |
|---|---|
| **Primary users** | Support agents (Freshdesk users) |
| **Secondary users** | Support team lead (reviews outputs, evaluates quality) |
| **Ticket volume** | ~1000 tickets/month |
| **Auto-answer target** | 30% of recurring tickets (~300/month) answered autonomously with human approval |
| **Peak load** | Not specified; estimate ~50 tickets/day on average, peak likely 2-3x |
| **Usage pattern** | Agent processes ticket → copilot provides recommendation → agent reviews, edits, sends |

---

## Inputs & Outputs

### Inputs

| Input | Source | Example |
|---|---|---|
| Support ticket | Freshdesk (Excel for pilot) | `Subject: "SSO login fails after password reset"` `Description: "User changed password yesterday, now SSO throws 403 error. Tried clearing cache, still failing. Need urgent fix."` `Channel: Email` `Customer: Acme Corp` |
| KB articles | Freshdesk KB (Excel for pilot) | 12 articles covering Authentication, Billing, Data Import, Integrations, Access Control, Compliance, Known Issues |
| Escalation rules | Configured rules (Excel for pilot) | 5 rules mapping conditions → teams (Engineering, Integrations, Finance, Compliance, Platform Ops) |

### Outputs

| Output | Description | Example |
|---|---|---|
| **Classification** | Category + Priority + Sentiment | `Category: Authentication` `Priority: High` `Sentiment: Frustrated` |
| **Retrieved KB articles** | Top-k relevant articles with relevance scores | `1. KB-AUTH-001: SSO Configuration Guide (0.92)` `2. KB-AUTH-003: Password Reset Procedures (0.87)` |
| **Action recommendation** | Reply / Ask for more info / Escalate | `Recommended action: Reply` `Confidence: 0.91` |
| **Draft response** | Grounded response with KB citations | `"Thank you for reporting this. Based on our SSO Configuration Guide [KB-AUTH-001], this typically occurs when... Steps to resolve: 1) ... 2) ... 3) ..."` |
| **Confidence score** | Per-output confidence indicator | `Overall confidence: High (0.91)` |
| **Reasoning trace** | Why the copilot made this recommendation | `"Matched to Authentication category based on 'SSO' and '403 error'. KB-AUTH-001 covers SSO configuration issues. No escalation rule triggered -- standard resolution path available."` |

---

## Success Metrics

| # | Metric | Type | Target | Measurement |
|---|---|---|---|---|
| 1 | Classification accuracy | AI quality | >= 85% | Exact match on category and priority against golden set |
| 2 | Retrieval accuracy | AI quality | >= 85% | Expected KB article appears in top-k retrieved set |
| 3 | Action accuracy | AI quality | >= 85% | Exact match on next-best-action (Reply / Ask / Escalate) |
| 4 | Response acceptance rate | Business | >= 70% | % of drafts agents accept without major rewriting |
| 5 | Auto-answer coverage | Business | 30% of recurring tickets | % of well-defined tickets the copilot can handle |
| 6 | Autonomous operation | Business | No handholding | System answers queries without manual intervention |

**Go-live validation**: Run against 1000 synthetic questions, reviewed by support team lead.

---

## Hard Limits

| Constraint | Limit | Rationale |
|---|---|---|
| **Human-in-the-loop** | Always -- no auto-send | Agent must review and approve every response |
| **Profanity / misuse** | Zero tolerance | All outputs must be checked; adversarial inputs handled gracefully |
| **LLM vendor lock-in** | Must be LLM-agnostic | Architecture must support swapping LLM providers |
| **Portability** | Full on-premises handover post-pilot | Code, models, data -- everything transferable to client premises |
| **Timeline** | Demo by May 10, final delivery May 16 | Hard deadlines, not flexible |
| **Hallucination** | Responses must be grounded in KB | No fabricated information; cite sources or flag "no match" |

---

## Data Sources

| Source | Records | Access (Pilot) | Access (Production) | Sensitivity |
|---|---|---|---|---|
| Historical tickets | 36 | Excel dataset | Freshworks API | Low (simulated data for pilot) |
| KB articles | 12 | Excel dataset | Freshworks KB API | Low |
| Escalation rules | 5 | Excel dataset | Freshworks / config | Low |
| Evaluation set | 12 (held out) | Excel dataset | Expanded to 1000 synthetic | Low |

**KB refresh**: Not needed for pilot. Production will require automated refresh via Freshworks APIs.
**PII**: No PII in pilot data. Production will require PII handling policy (Shubham to document).

---

## Out of Scope (Phase 1)

| Item | Reason |
|---|---|
| Freshdesk API integration | Pilot uses Excel; architect for it but don't build yet |
| Multi-language support | English only for pilot |
| Customer-facing AI | Agent-facing only; customers never interact with the copilot |
| Auto-send / auto-reply | Human always in the loop |
| Live KB refresh | Not needed with static Excel data |
| Production deployment | Pilot is standalone; productionization note covers the path forward |
| Phase 2 scope | Not defined; to be discussed after pilot results |
| Load testing / scaling | Not applicable for pilot with demo + eval run |

---

## Open Questions

| # | Question | Owner | Status |
|---|---|---|---|
| 1 | Target cost-per-ticket for production? | Shivani → Prasanna | Pending -- ask in next communication |
| 2 | Confidence indicator design -- binary or three-tier? | Amit → propose to Prasanna | Pending |
| 3 | Which LLM to recommend for this use case? | Amit | To be decided in Architecture Sketch |
| 4 | Vector store selection (pgvector / Qdrant / ChromaDB / Elasticsearch)? | Amit | To be decided in Architecture Sketch |
| 5 | How many synthetic questions to generate per category? | Nishka + Amit | To be decided in Evaluation Plan |
| 6 | Feedback loop storage -- where do agent edits persist? | Amit + Nancy | To be decided in Architecture Sketch |
