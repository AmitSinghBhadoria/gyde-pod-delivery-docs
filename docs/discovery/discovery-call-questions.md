---
sidebar_position: 1
title: Discovery Call Questions (Technical)
---

# Discovery Call Questions for Client (Prasanna)

**Engagement**: AI Support Copilot Pilot
**Prepared by**: Amit (POD Lead)
**Date**: 2026-04-29
**Status**: Pre-Discovery

---

## 1. Platform & Integrations

### Freshdesk
- Will we get access to a real Freshdesk instance (sandbox or production), or should we treat the Excel dataset as the source and mock the Freshdesk API?
- If Freshdesk is available: which queue are we targeting? What's the ticket volume per day/week?
- Is the Excel data representative of real ticket patterns, or is production data shaped differently?

### Knowledge Source
- The dataset has 12 KB articles. In production, where do these live? (Freshdesk KB, Confluence, Notion, a CMS, static docs?)
- How often do KB articles change? Weekly? Monthly?
- Are there other knowledge sources beyond articles -- e.g., internal wikis, Slack threads, runbooks, past ticket resolutions?

### Action/Escalation Integration
- The brief says "one escalation mechanism." In production, where do escalations go? (Freshdesk assignment, Slack channel, PagerDuty, Jira ticket?)
- For the pilot, is a mock escalation (log + notification) acceptable, or do you want it wired into a real channel?

---

## 2. LLM & Infrastructure Preferences

- Do you have a preferred LLM provider? (AWS Bedrock, OpenAI, GCP Vertex AI, Azure OpenAI, open-source?)
- Are there any provider constraints -- e.g., data residency requirements, existing cloud contracts, budget caps on API spend?
- What cloud is the current stack on? (AWS, GCP, Azure, on-prem?)
- Any database preferences? (We'll need a vector store for embeddings and a document store for sessions/prompts)
- Any hard constraints on where data can be processed or stored?

---

## 3. Deployment & Distribution

- The brief mentions three options: helpdesk side-panel, lightweight workspace, or API-first with review UI. Do you have a leaning?
- For the pilot specifically, is a standalone web app acceptable? Or does it need to sit inside Freshdesk (which means building a Freshdesk app/extension)?
- Who are the pilot users? How many support agents will use it? (5 agents are named in the data -- is that the target group?)
- Will agents use this alongside Freshdesk, or as a replacement interface?

---

## 4. Data & Privacy

> Framework non-negotiable (Doc 16) -- must be clarified before Sprint 1

- The ticket data contains customer names (ZenShop, Acme Capital, etc.) and agent names. Is this real or synthetic?
- In production, will tickets contain PII (customer emails, phone numbers, account numbers)?
- What's the data classification? (The framework requires this before Sprint 1)
- Any data retention requirements? How long can we store ticket data in our system?
- Who are the authorized data contacts on your side for access approvals?

---

## 5. Current Support Workflow

> Understanding the problem before designing the solution

- Walk us through what happens today when a ticket arrives. Agent opens Freshdesk, reads ticket, searches KB manually, types response?
- What's the average handle time per ticket currently?
- What percentage of tickets get escalated today?
- What are the biggest pain points for agents right now? (Slow KB search? Inconsistent responses? Missing context?)
- Are there SLA targets we should know about? (The data has `target_sla_hours` ranging from 12-72 hours)

---

## 6. Success Criteria & Evaluation

> Framework non-negotiable (Doc 01) -- charter requires 3-5 measurable outcomes

- What does success look like to you specifically?
  - Ticket classification accuracy target?
  - KB retrieval accuracy target?
  - Draft response quality bar? (Agent accepts as-is, agent edits slightly, agent rewrites?)
  - Next-best-action accuracy target?
- The eval set has 12 cases. Should we expand it during the pilot, or is 12 sufficient for Phase 1?
- Who reviews the sample outputs -- you, or the named agents (Asha, Kiran, etc.)?
- Is there a specific metric that would make you say "yes, take this to production"?

---

## 7. Output Format & UX Expectations

- What should the copilot's output look like for each ticket? For example:
  - Ticket summary/classification
  - Suggested KB articles (with citations)
  - Draft response
  - Recommended action (Reply / Ask for more info / Escalate)
  - Confidence indicator
- Should the agent be able to edit the draft and send from the copilot, or copy-paste into Freshdesk?
- Should the copilot show its reasoning/sources (traceability), or just the answer?
- Any tone/style requirements for draft responses?

---

## 8. Human-in-the-Loop & Governance

> Framework non-negotiable (Docs 14, 15)

- "Human-in-the-loop only" -- confirm: the copilot suggests, the agent always decides, no auto-send?
- Should there be a supervisor/manager review step, or is the agent's judgment sufficient?
- If the copilot gets a ticket wrong (bad KB match, wrong escalation), how should it fail? (Disclaimer? Fallback to "I don't know"? Flag for human review?)
- Any compliance requirements for the support domain? (Regulated industry, audit trail needs?)

---

## 9. Cost & Timeline Constraints

- Budget constraints for LLM API costs during the pilot?
- Latency expectation: how fast should the copilot respond after a ticket comes in? (Real-time? Under 5 seconds? Under 30 seconds?)
- The brief says "Phase 1" -- what's your rough vision for Phase 2? (This helps us architect for extensibility without over-building)
- Any hard deadlines beyond the 4-week window?

---

## 10. Observability & Production Path

> Framework non-negotiable (Doc 12)

- What monitoring do you expect in the pilot? (Cost tracking, latency, accuracy drift, usage patterns?)
- Do you want a dashboard, or are logs/reports sufficient for Phase 1?
- For the production path: who operates the system after handover? Your support ops team? Engineering?
- Is there an existing observability stack we should integrate with? (Datadog, CloudWatch, Grafana?)

---

## 11. New Data Ingestion

- When new KB articles are written or updated, how should the copilot pick them up? (Manual trigger? Nightly refresh? Real-time?)
- When new ticket types emerge (categories not in the current 7), how should the system handle them?
- Who is responsible for keeping the KB up to date on your side?

---

## Already Answered by Dataset (Do Not Re-Ask)

| Area | What we know |
|---|---|
| Ticket schema | 15 columns: ticket_id, created_at, customer_name, channel, subject, description, category, priority, sentiment, assigned_agent, status, source_kb_id, expected_next_best_action, resolution_summary, target_sla_hours |
| Ticket volume | 36 historical tickets (synthetic) |
| Categories | Authentication, Billing, Data Import, Integrations, Access Control, Compliance, Known Issue |
| Priorities | Critical, High, Medium, Low |
| Channels | Email, Chat, Portal |
| Sentiments | Frustrated, Neutral, Calm |
| KB articles | 12 articles with content, keywords, agent notes |
| Escalation rules | 5 rules: Engineering, Integrations Eng, Finance Ops, Compliance, Platform Ops |
| Eval set | 12 held-out cases covering all categories and actions |
| Eval dimensions | category, priority, KB retrieval, next-best-action, reasoning |
| Actions | Reply, Ask for more info, Escalate |

---

## Suggested Call Flow

1. **Current workflow** (#5) -- understand the problem first
2. **Platform & integrations** (#1) -- what's real vs. mock
3. **Success criteria** (#6) -- what "good" looks like
4. **Deployment & UX** (#3, #7) -- how agents will use it
5. **Infrastructure preferences** (#2) -- technical constraints
6. **Data & privacy** (#4) -- classification and PII
7. **Cost & timeline** (#9) -- constraints
8. **Governance, observability, ops** (#8, #10, #11) -- if time permits, else follow up async

---

## Answers (To be filled during/after call)

> Fill this section during the Discovery call

### Platform & Integrations
- Freshdesk: _[pending]_
- KB source: _[pending]_
- Escalation target: _[pending]_

### LLM & Infrastructure
- LLM provider: _[pending]_
- Cloud: _[pending]_
- Database: _[pending]_

### Deployment
- Surface: _[pending]_
- Pilot users: _[pending]_

### Data & Privacy
- PII present: _[pending]_
- Classification: _[pending]_
- Retention: _[pending]_

### Success Criteria
- Classification accuracy: _[pending]_
- Retrieval accuracy: _[pending]_
- Draft quality: _[pending]_
- Go-live threshold: _[pending]_

### Cost & Timeline
- API budget: _[pending]_
- Latency target: _[pending]_
- Phase 2 vision: _[pending]_

### Observability
- Monitoring: _[pending]_
- Dashboard: _[pending]_

### Governance
- HITL confirmed: _[pending]_
- Compliance: _[pending]_
