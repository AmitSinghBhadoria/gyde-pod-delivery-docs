---
sidebar_position: 4
title: Discovery Call Script
---

# Discovery Call Script

**Date**: 2026-04-29, 3:00 PM IST
**Duration**: 60 minutes
**Participants**: Amit (POD Lead), Shivani (Implementation Manager), Prasanna (Client)
**Format**: Video call
**Note-taker**: Shivani (or record the call)

---

## What We Need to Extract

By the end of this call, we need enough information to produce the **Discovery Output Pack** (Doc 03, Section 3.4):

| Artifact | Needs from this call |
|---|---|
| **Use Case Canvas** | Mission, users, volumes, inputs/outputs, success metrics, hard limits, data sources, out-of-scope |
| **Data Feasibility Report** | Source systems, access, quality assessment, sensitivity, gaps |
| **Architecture Sketch** | Deployment surface, infra preferences, integration points, constraints |
| **Evaluation Plan** | Target metrics, thresholds, test case sources, measurement approach |
| **Initial Risk Register** | Client-side risks, dependencies, blockers |
| **Engagement Plan** | Timeline, milestones, team, commercial shape |
| **POD Charter (draft)** | Mission, success criteria, scope, cadence, decision rights, escalation |

---

## Call Flow (60 minutes)

| Section | Lead | Time | What you extract |
|---|---|---|---|
| **Opening** | Shivani | 3 min | Set agenda, ask for Prasanna's additions |
| **1. The Problem** | Amit | 10 min | Current workflow, pain points, handle time, escalation rate |
| **2. Platform & Integrations** | Amit | 10 min | Freshdesk access, KB source, escalation channel, LLM provider, cloud, deployment surface |
| **3. Success Criteria** | Shivani (Amit supports) | 10 min | Measurable targets, quality thresholds, who evaluates, go-live decision |
| **4. Scope & Boundaries** | Shivani | 5 min | In/out of scope, Phase 2 vision |
| **5. Data & Privacy** | Amit | 5 min | PII, classification, retention, refresh strategy |
| **6. Delivery & Cadence** | Shivani | 7 min | Comms channel, cadence agreement, turnaround time, timeline flexibility |
| **7. Deliverables & Cost** | Shivani | 5 min | Deliverable priorities, budget constraints, cloud account |
| **8. Governance** | Amit | 3 min | HITL confirmation, failure mode, compliance needs |
| **Closing** | Shivani | 2 min | Summarize next steps, confirm charter delivery timeline |

> **Key ground rules**: Listen more than talk, don't commit to architecture on the spot, write down every threshold Prasanna mentions, and if you run short on time, sections 1-3 and 6 are non-negotiable.

---

## Call Script

### OPENING (Shivani leads -- 3 minutes)

**Shivani**:

> Prasanna, thank you for the brief and the starter dataset. We've reviewed both in detail -- the team has a good understanding of what you're looking for.
>
> The goal of this call is to align on a few things so we can draft the engagement charter and architecture sketch by end of this week. We have about 60 minutes. I'll manage time and make sure we cover everything.
>
> We'd like to walk through: first, understanding the current support workflow and where the pain is; then the technical setup and constraints; then success criteria and scope; and finally the operating cadence for the next 4 weeks.
>
> Amit will lead the technical discussion, I'll cover the delivery and engagement side. If we run short on time, we'll flag what needs a follow-up.
>
> Before we start -- are there any topics you specifically want to cover today that I should make sure we get to?

*[Let Prasanna respond. Note any additional topics.]*

---

### SECTION 1: THE PROBLEM (Amit leads -- 10 minutes)

**Purpose**: Understand the current workflow and pain points. This shapes everything -- the architecture, the eval metrics, the success criteria.

**Amit**:

> Before we get into the solution, I want to make sure we deeply understand the problem. Can you walk us through what happens today when a support ticket comes in?

*[Let Prasanna describe the workflow. Listen for:]*
- *How agents currently find answers (manual KB search? Ask colleagues? Memory?)*
- *What takes the most time*
- *Where mistakes happen*
- *How escalation decisions are made today*

**Follow-up questions (use as needed, don't read them all mechanically):**

> - What's the average handle time per ticket right now?
> - What percentage of tickets get escalated today? Is that too high, too low, or about right?
> - What are the biggest pain points for your agents -- is it slow KB search, inconsistent responses, not knowing when to escalate, something else?
> - The data shows SLA targets from 12 to 72 hours. Are those actively tracked? Are you hitting them?
> - Are there specific ticket types that cause the most trouble?

**What to listen for**: The business pain. This becomes the "mission statement" in the charter and helps us prioritize what the copilot should nail first.

**Transition (Amit)**:

> That's really helpful. Now I have a clear picture of the workflow. Let me ask about the technical setup.

---

### SECTION 2: PLATFORM & INTEGRATIONS (Amit leads -- 10 minutes)

**Purpose**: Determine what's real vs. mock, what we integrate with, what we build standalone.

**Amit**:

> You mentioned Freshdesk in the brief. A few questions on that --

> - Will we get access to a Freshdesk instance, even a sandbox, for the pilot? Or should we treat the Excel dataset as our source and mock the Freshdesk integration?

*[Listen for the answer. This determines whether Nancy needs to build a Freshdesk connector or an Excel/CSV ingestion pipeline.]*

> - The dataset has 12 KB articles. In production, where do these live -- Freshdesk KB, Confluence, or somewhere else? And for the pilot, should we use the Excel data or connect to a live source?

> - For escalation -- the brief says "one escalation mechanism." What channel do escalations go through today? Freshdesk reassignment, Slack, email to a team lead?

> - For the pilot, is a mock escalation -- say, logging the escalation with the right team and required context, plus a notification -- acceptable? Or do you want it wired into a real channel?

**Infra & LLM (Amit continues)**:

> Now on the infrastructure side --

> - Do you have a preferred LLM provider? AWS Bedrock, OpenAI, Google Vertex, or are you open?
> - What cloud is your current stack on?
> - Any hard constraints on where data can be processed or stored -- data residency, compliance requirements?
> - Any database preferences, or should we pick what fits the use case best?

**Deployment surface (Amit)**:

> Your brief mentioned three deployment options -- helpdesk side-panel, lightweight workspace, or API-first with a review UI. Do you have a leaning?

> For the pilot specifically -- is a standalone web app acceptable where agents can paste or see tickets and get copilot recommendations? Or does it need to live inside Freshdesk from day one?

**What to capture**: Write down exact answers. These become architecture decisions and will be recorded in ADRs.

---

### SECTION 3: SUCCESS CRITERIA (Shivani leads, Amit supports -- 10 minutes)

**Purpose**: Define what "good" looks like. The charter needs 3-5 measurable criteria including at least one AI quality metric and one business metric.

**Shivani**:

> Let's talk about what success looks like for this pilot. If we're sitting here in 4 weeks reviewing the results, what would make you say "this is ready to go live"?

*[Let Prasanna answer in his own words first. Then drill into specifics:]*

> - The copilot will classify tickets, retrieve KB articles, recommend actions, and draft responses. Which of those is the most important to get right?

> - On a metric level -- for example, the SimpliContract engagement used faithfulness above 0.85 and citation accuracy above 0.90. Do you have similar thresholds in mind, or should we propose targets?

> - What's the business metric you care about? For example: reduction in handle time, percentage of drafts agents accept without major rewriting, agent satisfaction?

> - Is there a threshold below which you'd say "this isn't good enough"? Like, if the copilot suggests the wrong KB article more than X% of the time?

**Amit (supporting)**:

> The eval set you shared has 12 held-out cases. That's a good start for scoring. Should we expand that during the pilot -- we were thinking 30-40 cases to get statistical coverage across all categories -- or is 12 sufficient for Phase 1?

> Who evaluates the sample outputs? Will you review them personally, or should we plan for the named agents (Asha, Kiran, etc.) to score response quality?

**What to capture**: Exact thresholds. These go directly into the charter and the evaluation plan. If Prasanna doesn't give numbers, propose them and get agreement.

---

### SECTION 4: SCOPE & BOUNDARIES (Shivani leads -- 5 minutes)

**Purpose**: Nail down what's in and what's explicitly out. Prevents scope creep later.

**Shivani**:

> Let me confirm the scope boundaries so we can document them clearly in the charter.

> - "One support queue" -- is there a specific queue or product area, or is it the general inbox?
> - Multi-language -- is English-only acceptable for Phase 1?
> - Are there any features you explicitly do NOT want us to build in Phase 1? Sometimes it helps to name what's out of scope so expectations are clear.

> And looking ahead -- you mentioned this is Phase 1. If it goes well, what does Phase 2 look like in your mind? More queues? More knowledge sources? Auto-triage? Customer-facing AI?

*[We ask about Phase 2 lightly -- just enough to architect for extensibility without over-building.]*

---

### SECTION 5: DATA & PRIVACY (Amit leads -- 5 minutes)

**Purpose**: Data classification and PII handling. Framework non-negotiable.

**Amit**:

> A few questions on the data side -- this is something our framework requires us to clarify before we start building.

> - The dataset has customer company names and agent names. In production, will tickets contain PII -- customer emails, phone numbers, account numbers?
> - What's the data classification for support ticket data? Our framework needs this to set the right security controls.
> - Any data retention requirements -- how long can we store ticket data in our system?
> - When the KB gets updated or new articles are added, how should the copilot pick those up? Manual trigger, nightly refresh, or real-time?

**What to capture**: Classification level, PII presence, retention policy. Shubham needs these for the threat model.

---

### SECTION 6: DELIVERY & CADENCE (Shivani leads -- 7 minutes)

**Purpose**: Agree how we'll work together for 4 weeks.

**Shivani**:

> Let me propose a working cadence and you can tell me if it works for you.

> - **Daily**: We'll post standup notes in a shared channel. You can read them async -- you don't need to attend.
> - **Weekly**: I'll send you a one-page written status every Friday -- overall RAG status, sprint progress, top risks, any decisions we need from you.
> - **Every 2 weeks**: A live sprint demo where we show working software. 30 minutes. We only demo what actually works, not mockups.
> - **As needed**: If something is at risk or blocked, we'll flag it immediately. Same day, not at the next weekly update.

> Does that cadence work for you?

*[Get agreement or adjust.]*

> A few more things:

> - What's your preferred communication channel -- Slack, Teams, email, WhatsApp?
> - Since you're our single point of contact for business, technical, and product decisions, how quickly can you typically turn around a question? Same day?
> - Is there anyone else on your side who needs to be in the loop or whose approval we need?
> - Are you comfortable with us recording the sprint demos for async review?

**Timeline (Shivani)**:

> On timeline -- you've said 4 weeks. Is that a hard deadline, or is there flexibility if we need an extra few days for hardening?

> Is there a specific event or decision point this pilot needs to be ready for?

---

### SECTION 7: DELIVERABLES & COST (Shivani leads -- 5 minutes)

**Purpose**: Confirm what Prasanna expects to receive and any budget constraints.

**Shivani**:

> Your brief lists five deliverables: working pilot, architecture note, eval results, sample outputs, and a productionization note. Let me confirm:

> - Is the working pilot the primary deliverable, or are the docs equally important?
> - For sample outputs -- we're thinking one per ticket category plus a few edge cases, roughly 10-12 examples. Does that work?
> - The productionization note -- is a high-level roadmap sufficient (1-2 pages covering deployment, security, monitoring), or do you want a detailed production plan?
> - At engagement close, do you want a formal walkthrough session, or is the documentation sufficient?

> And on the cost side:

> - Any budget constraints for LLM API costs during the pilot?
> - Should we use your cloud account, or provision our own for the pilot?
> - Is there a target cost-per-ticket you'd want to see in production?

---

### SECTION 8: GOVERNANCE (Amit leads -- 3 minutes)

**Purpose**: Quick confirmation on security and responsible AI requirements.

**Amit**:

> Two quick governance questions -- our framework requires these before we start building.

> - Human-in-the-loop -- just confirming: the copilot suggests, the agent always decides, no auto-send. Correct?
> - If the copilot gets something wrong -- bad KB match, wrong escalation recommendation -- how should it fail? We're thinking a confidence indicator where low-confidence answers get a disclaimer. Does that align with your expectations?
> - Is there any compliance or security review the pilot needs to pass before going live?

---

### CLOSING (Shivani leads -- 2 minutes)

**Shivani**:

> This has been really helpful. Let me summarize what we'll produce from this conversation:

> 1. **POD Charter** -- we'll have a draft to you by [tomorrow/end of this week] for sign-off
> 2. **Architecture sketch** -- Amit will draft the system design based on what we discussed today
> 3. **Evaluation plan** -- target metrics and thresholds based on what you've told us
> 4. **Sprint plan** -- two sprints mapped to the scope we agreed
> 5. **Risk register** -- initial risks identified today plus anything the team adds

> We'll share all of these in our shared docs space. Once you sign off on the charter and eval plan, we'll start Sprint 1.

> Any final questions or things we missed?

*[Let Prasanna respond.]*

> Thank you, Prasanna. We'll be in touch [tomorrow/day after] with the charter draft.

---

## Post-Call Checklist

Immediately after the call, Amit and Shivani should:

| # | Task | Owner | Deadline |
|---|---|---|---|
| 1 | Update `01_Discovery_Call_Questions.md` with answers | Amit | Same day |
| 2 | Update `04_Shivani_Discovery_Call_Questions.md` with answers | Shivani | Same day |
| 3 | Draft POD Charter | Shivani + Amit | Next day |
| 4 | Draft Architecture Sketch | Amit | Next day |
| 5 | Draft Evaluation Plan | Amit + Nishka | Next day |
| 6 | Draft Risk Register | Shivani | Next day |
| 7 | Brief the full team on Discovery outcomes | Amit + Shivani | Next day standup |
| 8 | Share all drafts with Prasanna for sign-off | Shivani | Day after drafts |
| 9 | Assign Nancy to start Data Feasibility Report | Amit | Same day |
| 10 | Assign Shubham to start Threat Model | Amit | Same day |

---

## Conversation Ground Rules

- **Listen more than you talk.** Prasanna is the domain expert. Let him describe the problem in his words before proposing solutions.
- **Don't solutioneer during the call.** Capture requirements, don't commit to architecture decisions on the spot. Say "we'll evaluate options and come back with a recommendation."
- **Name the uncertainties.** If something isn't clear, say so. "We'll need to investigate that" is better than guessing.
- **Write it down.** If Prasanna says a threshold, a constraint, or a preference, repeat it back and confirm. "Just to confirm -- you're saying classification accuracy above 85% would be the target?"
- **Respect the time.** If a section is running long, Shivani should steer: "Let's capture that and move to the next topic so we cover everything. We can do a follow-up on this specific area."
- **Don't oversell.** This is Discovery, not a sales pitch. Be honest about what 4 weeks can deliver.

---

## Fallback: If We Run Short on Time

If we hit 50 minutes and haven't covered everything, prioritize:

**Must cover (non-negotiable)**:
- Current workflow and pain points (Section 1)
- Platform setup and LLM preferences (Section 2)
- Success criteria with at least one number (Section 3)

**Can follow up async**:
- Scope boundaries (Section 4) -- Shivani can confirm via email
- Data & privacy (Section 5) -- Amit can follow up with Shubham and Prasanna
- Cost constraints (Section 7) -- Shivani can email
- Governance (Section 8) -- Shubham can schedule a 15-min follow-up

**Cannot skip**:
- Communication cadence (Section 6) -- must be agreed before Sprint 1 starts
