---
sidebar_position: 2
title: Discovery Call Questions (PM)
---

# Shivani's Discovery Call Questions for Prasanna

**Role**: Implementation (Project) Manager
**Call**: Discovery Call with Prasanna (Client CIO / Business Lead / Product Owner)
**Date**: 2026-04-29, 3:00 PM IST
**Purpose**: Get the delivery, commercial, and operational answers needed to draft the POD Charter and Engagement Plan

---

> **Note for Shivani**: Amit will lead the technical questions (architecture, LLM, data pipeline). Your job is to nail down everything around delivery shape, success criteria, client expectations, communication, risks, and scope boundaries. These are the questions that let you write the charter and engagement plan after the call.

---

## 1. Engagement Shape & Timeline

These answers go directly into the Engagement Plan (Doc 03, Section 7).

- You've said 4 weeks and Phase 1 scope. Is that a hard deadline or is there flexibility if we need an extra week for hardening?
- Is there a specific event or decision point this pilot needs to be ready for? (e.g., board review, budget cycle, vendor decision)
- Do you expect a formal Discovery phase (week 0), or should we absorb discovery into Sprint 1?
- After Phase 1, what's the decision process for go-live? Who approves it, and what do they need to see?

---

## 2. Success Criteria

Per the framework (Doc 01), the charter needs 3-5 measurable success criteria including at least one AI quality metric and one business metric.

- If you had to pick the single most important thing this pilot proves, what is it?
- What's the business metric you care about? For example:
  - Reduction in average handle time per ticket?
  - Percentage of tickets where the draft is usable without major rewrite?
  - Agent satisfaction / willingness to continue using the tool?
- Are there quality thresholds that would make you say "this is not good enough"? (e.g., if classification accuracy is below X%, or if the copilot hallucinates on more than Y% of tickets)
- Who evaluates whether the pilot succeeded -- you personally, the support team leads, or both?

---

## 3. Scope & Boundaries

The charter (Doc 01, Section 6) requires an explicit in-scope and out-of-scope list. Prasanna's brief is good but some boundaries need confirming.

- You mentioned "one support queue" -- which queue? Is it a specific product area, or the general support inbox?
- "One knowledge source" -- confirming this is the 12 KB articles in the dataset, or is there a live KB we should connect to?
- "One escalation mechanism" -- what's your preferred channel? (Slack notification, email to a team lead, Freshdesk reassignment, or something else?)
- Are there any features you explicitly do NOT want in Phase 1 that we should document as out-of-scope? (This prevents scope creep later)
- Is multi-language support needed, or is English-only acceptable for Phase 1?

---

## 4. Stakeholders & Decision Rights

Per Doc 05, every POD role needs a named client counterpart. Since Prasanna is wearing three hats, this needs to be explicit.

- You'll be our primary contact for business decisions, technical direction, and product feedback. Is that sustainable for 4 weeks, or should we plan for someone else as day-to-day contact?
- Who are the support agents who will test the pilot? Can we get their names?
- If a scope question comes up mid-sprint, can you turn it around same-day, or do we need to plan for a 2-3 day decision cycle?
- Is there anyone else on your side who needs to be informed or whose approval is needed? (IT, InfoSec, legal, support team manager?)
- Who signs off on the final pilot evaluation -- you alone, or a group?

---

## 5. Communication & Cadence

Per Doc 05, Shivani owns the communication cadence. Need to agree it with Prasanna now.

- What's your preferred communication channel for day-to-day? (Slack, Teams, email, WhatsApp?)
- Are you comfortable with the following cadence, or do you want to adjust?
  - **Daily**: Standup notes posted in shared channel (async, you read when convenient)
  - **Weekly**: Written status update from me (one page, 5-min read) + optional 30-min sync
  - **Per sprint (every 2 weeks)**: Live demo of working system (30 min) + sprint output pack
- How do you prefer to receive bad news? (Our policy is same-day transparency -- if something is at risk, you'll hear it immediately, not at the weekly update)
- Do you want access to our backlog/sprint board, decision log, and eval results in real-time, or are the weekly summaries sufficient?
- Are demos recorded? Any objection to recording for async stakeholders?

---

## 6. Risk & Dependencies

Per Doc 03 Section 6, the risk register needs the top 5 risks with owner and mitigation. These questions help populate it.

- What's the biggest risk you see in this pilot from your side?
- Are there any dependencies on your side that could block us? (e.g., data access approvals, security reviews, infrastructure provisioning)
- If the starter dataset turns out to be insufficient (too few tickets, missing categories), can you provide additional data quickly?
- Is there a risk that priorities change mid-pilot? (e.g., a production incident pulls your attention away for a week)
- What happens if the pilot results are mixed -- say 3 out of 5 metrics pass but 2 don't? Is that enough to proceed to Phase 2, or does everything need to pass?

---

## 7. Deliverables & Handover

Prasanna's brief lists specific deliverables. Confirm expectations.

- You asked for: working pilot, architecture note, eval results, sample outputs, and productionization note. Are those weighted equally, or is the working pilot the primary deliverable?
- For the "sample outputs across representative tickets" -- how many do you want to see? (We're thinking one per category = ~8, plus 2-3 edge cases)
- The productionization note -- is this a high-level roadmap (1-2 pages) or a detailed production plan?
- At engagement close, do you want a formal handover session (walkthrough of the system, docs, runbooks), or is the documentation sufficient?
- Do you expect a knowledge transfer to your team, or is this purely a Gyde-delivered pilot?

---

## 8. Commercial & Resource

These may or may not apply in the simulation, but per the framework, Shivani should ask them.

- Are there budget constraints for cloud infrastructure and LLM API costs during the pilot?
- Do we need to use your cloud account, or can we provision our own for the pilot?
- Any procurement or vendor approval needed for LLM providers (e.g., OpenAI terms of service, AWS Bedrock access)?
- Is there a target cost-per-ticket you'd want to see in production? (This shapes model selection)

---

## 9. Governance & Compliance

Shubham will go deeper on security, but Shivani should confirm the governance surface.

- Is there an internal security or compliance review the pilot needs to pass before going live?
- Any data residency requirements? (Where ticket data can be stored and processed)
- Does your support platform handle any regulated data (financial, healthcare, legal)?
- Do we need to sign an NDA or data processing agreement for the pilot?

---

## 10. Phase 2 Vision (Light touch)

Don't go deep here -- just enough to architect for the future without over-building.

- If this pilot works, what does Phase 2 look like in your mind?
  - More queues?
  - More knowledge sources?
  - Auto-triage (automated ticket routing without human approval)?
  - Customer-facing AI (not just agent-facing)?
- Rough timeline for Phase 2 decision?

---

## Post-Call: What Shivani Produces

After this call, Shivani should be able to draft:

| Document | Framework reference | Target completion |
|---|---|---|
| **POD Charter (draft)** | Doc 01, Section 6 | End of day today |
| **Engagement Plan (draft)** | Doc 03, Section 7 | Tomorrow |
| **Risk Register (initial)** | Doc 03, Section 6 | Tomorrow |
| **Communication Protocol** | Doc 05, Section 3 | End of day today |
| **Milestone Schedule** | Doc 03, Section 5 | Tomorrow (with Amit) |

---

## Answer Capture Template

> Fill during the call

### Engagement Shape
- Hard deadline: _[pending]_
- Decision point trigger: _[pending]_
- Discovery week: _[pending]_
- Go-live decision process: _[pending]_

### Success Criteria
- Primary success signal: _[pending]_
- Business metric: _[pending]_
- Failure threshold: _[pending]_
- Evaluator: _[pending]_

### Scope
- Queue: _[pending]_
- KB source: _[pending]_
- Escalation channel: _[pending]_
- Explicit out-of-scope: _[pending]_
- Language: _[pending]_

### Stakeholders
- Day-to-day contact: _[pending]_
- Pilot test agents: _[pending]_
- Decision turnaround: _[pending]_
- Other approvers: _[pending]_

### Communication
- Channel: _[pending]_
- Cadence agreed: _[pending]_
- Board access: _[pending]_
- Demo recording: _[pending]_

### Risk & Dependencies
- Client's top risk: _[pending]_
- Blocking dependencies: _[pending]_
- Data availability: _[pending]_
- Priority change risk: _[pending]_
- Mixed results threshold: _[pending]_

### Deliverables
- Primary deliverable: _[pending]_
- Sample output count: _[pending]_
- Prod note depth: _[pending]_
- Handover format: _[pending]_
- Knowledge transfer: _[pending]_

### Commercial
- Budget constraints: _[pending]_
- Cloud account: _[pending]_
- Vendor approvals needed: _[pending]_
- Target cost per ticket: _[pending]_

### Governance
- Security review required: _[pending]_
- Data residency: _[pending]_
- Regulated data: _[pending]_
- NDA/DPA needed: _[pending]_

### Phase 2
- Vision: _[pending]_
- Timeline: _[pending]_
