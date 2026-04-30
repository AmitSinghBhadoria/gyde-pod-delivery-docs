---
sidebar_position: 5
title: Discovery Call Answers
---

# Discovery Call Answers

**Date**: 2026-04-29, 3:00 PM IST
**Duration**: 60 minutes
**Participants**: Amit (POD Lead), Shivani (Implementation Manager), Prasanna (Client)
**Format**: Google Meet

---

## Section 1: The Problem -- Current Workflow & Pain Points

### Current Workflow
- Support ticket gets raised in Freshdesk
- A human agent picks it up manually
- Agent does their own research -- searching KB manually, asking colleagues, relying on memory
- Agent sends the resolution

### Pain Points
- Resolution time ranges from **2 hours to 2 days** -- highly variable
- No standardization -- each agent researches and responds differently
- Knowledge trapped in individual agents' heads
- High human cost for repetitive, well-documented issues

### Volume
- **~100 tickets/month** currently

### Pilot Goal
- **30% of recurring tickets** (those with defined resolutions, e.g., common Authentication issues) to be answered autonomously by the copilot
- Human agent remains the final layer of approval (human-in-the-loop)
- Standardize responses across agents
- Reduce resolution time significantly
- Save on human cost

---

## Section 2: Platform & Integrations

### Source System
- **Freshworks suite** is the single source of truth -- KB, tickets, everything
- Entire sales and support infrastructure lives in Freshworks

### Pilot Approach
- **Excel dataset for the pilot** -- no Freshdesk integration needed yet
- Architect for Freshworks API integration post-pilot
- No KB refresh feature needed for pilot, but design for it (production will need it)

### LLM & Infrastructure
- **LLM**: Open to any provider for the pilot; wants flexibility and LLM-agnostic architecture; open to our recommendation for this use case
- **Cloud**: GCP for the pilot (our own GCP account)
- **Post-pilot**: Full on-premises handover -- code, models, data, everything goes to the client's premises
- **Implication**: Keep the stack portable, avoid vendor lock-in

### Deployment Surface
- Prasanna leans toward a **sidebar widget** on Freshdesk
- **Our recommendation (agreed)**: Chrome extension / sidebar overlay -- fastest to demo, doesn't require Freshdesk marketplace integration, shows real value in context

### Database
- Our call for the pilot

---

## Section 3: Success Criteria

### What Success Looks Like
1. The pilot answers queries **autonomously without handholding**
2. **Accuracy is good** -- target **85%** for the pilot, improve from there

### Go-Live Validation
- Run the agent against **1000 synthetic questions** before going live
- We generate the synthetic questions from existing data
- **Support team lead** reviews and evaluates the outputs
- Adjustments can be made based on evaluation results

### Specific Thresholds
- 85% accuracy target for pilot (we will propose detailed per-metric thresholds in the Evaluation Plan)
- 30% of recurring tickets auto-answered (with human approval)

---

## Section 4: Scope & Boundaries

### In Scope
- **General inbox** -- not a single narrow queue
- Scope defined by what the KB covers (7 categories from dataset: Authentication, Billing, Data Import, Integrations, Access Control, Compliance, Known Issue)
- **English only** for the pilot
- Human-in-the-loop always

### Out of Scope
- Multi-language support
- Live Freshdesk integration (pilot uses Excel)
- Customer-facing AI (agent-facing only)
- Auto-send (copilot suggests, agent decides)

### Phase 2
- Not defined yet -- to be discussed after pilot results

---

## Section 5: Data & Privacy

- **No PII concerns** for the pilot -- using Excel with simulated data, no real customer data
- No data classification or retention requirements for the simulation
- **No KB refresh feature** needed for pilot
- **For production**: architect for data refresh (Freshworks API integration), PII handling, and classification -- Shubham should document what production would require

---

## Section 6: Delivery & Cadence

### Communication Cadence (Agreed)
- **One weekly email** status update
- **One weekly call** (Google Meet)
- Total: 2 touchpoints per week

### Channels
- **Email** for written updates
- **Google Meet** for calls

### Decision Turnaround
- **2 hours to 1 day** -- Prasanna is responsive
- All team members on his side available for support

### Timeline (Hard Deadlines)
| Milestone | Date | Days from now |
|---|---|---|
| **Sprint 1 Demo** | May 10, 2026 | 11 days |
| **Final Delivery** | May 16, 2026 | 17 days |

- These are **hard deadlines**, not flexible

---

## Section 7: Deliverables & Cost

### Deliverables
- **Working pilot AND documentation are equally important**
- Knowledge transfer and docs are priority from day one
- Everything we build should be documented and transferable
- Post-pilot, the client takes forward the code and knowledge independently

### Expected Deliverables
1. Working pilot (Chrome extension / sidebar)
2. Architecture document
3. Evaluation results (including 1000-question run)
4. Sample outputs across categories
5. Productionization note
6. Complete codebase for handover

### Cost
- **No budget constraints** for the pilot (LLM API costs, infrastructure)
- **Our own GCP account** for the pilot
- **Target cost-per-ticket**: Not discussed yet -- **ACTION: Ask Prasanna in next communication**

---

## Section 8: Governance

### Confirmed
- **Human-in-the-loop**: Copilot suggests, agent decides, no auto-send

### Feedback Loop (New Requirement)
- Agent can rate response ("was it helpful")
- Agent can **edit the response**
- Edited version saved as a correct response
- System **learns from feedback** over time -- golden evaluations from real usage
- This creates a positive feedback loop for continuous improvement

### Guardrails (New Requirement)
- **Profanity check** on all outputs
- Handle negative/adversarial scenarios gracefully
- **Prevent misuse** of the system
- Graceful failure for edge cases

### Not Yet Confirmed
- Compliance/security review requirements (not applicable for simulation)
- Confidence indicator approach (to be proposed by us)

---

## Key Decisions Summary

| Decision | Answer |
|---|---|
| Data source for pilot | Excel dataset |
| Data source for production | Freshworks APIs |
| Cloud platform | GCP (our account) |
| Post-pilot deployment | On-premises handover |
| LLM provider | Our recommendation, keep LLM-agnostic |
| Deployment surface | Chrome extension / sidebar widget |
| Accuracy target | 85% for pilot |
| Auto-answer target | 30% of recurring tickets |
| Go-live validation | 1000 synthetic questions |
| Evaluator | Support team lead |
| Sprint 1 demo | May 10 (hard) |
| Final delivery | May 16 (hard) |
| Communication | 1 email + 1 call per week |
| Channel | Email + Google Meet |
| Decision turnaround | 2 hours to 1 day |
| Docs priority | Equal to working code |
| Feedback loop | Agent rates + edits, system learns |
| Guardrails | Profanity, misuse prevention |

---

## Open Items / Follow-ups

| # | Item | Owner | Status |
|---|---|---|---|
| 1 | Target cost-per-ticket for production | Shivani (ask Prasanna) | Pending |
| 2 | Confidence indicator design (propose to Prasanna) | Amit | Pending |
| 3 | Document production-grade PII handling requirements | Shubham | Pending |
| 4 | Document production-grade data classification | Shubham | Pending |
| 5 | Phase 2 scope discussion | Shivani + Prasanna | Post-pilot |

---

## Next Steps

| # | Task | Owner | Deadline |
|---|---|---|---|
| 1 | Draft Use Case Canvas | Amit + Shivani | Apr 30 |
| 2 | Draft POD Charter | Shivani + Amit | Apr 30 |
| 3 | Draft Architecture Sketch | Amit | May 1 |
| 4 | Draft Evaluation Plan | Amit + Nishka | May 1 |
| 5 | Draft Risk Register | Shivani | May 1 |
| 6 | Draft Sprint Plan | Shivani + Amit | May 1 |
| 7 | Start Data Feasibility Report | Nancy | May 1 |
| 8 | Start Threat Model | Shubham | May 1 |
| 9 | Brief full team on Discovery outcomes | Amit + Shivani | Apr 30 standup |
| 10 | Share drafts with Prasanna for sign-off | Shivani | May 2 |
