---
sidebar_position: 1
title: Product Overview & Technical Primer
---

# AI Support Copilot -- Product Overview & Technical Primer

**Engagement**: AI Support Copilot Pilot
**Prepared by**: Amit (POD Lead)
**Date**: 2026-04-29
**Audience**: Engineering team (Atharva, Nancy, Nishka, Shubham)
**Purpose**: Understand what we're building, why it matters, and how the pieces fit together

---

## 1. The Problem We're Solving

### What support agents do today

When a support ticket arrives (e.g., "OTP code not arriving for login"), an agent has to:

1. **Read and classify** -- is this Authentication? Billing? Integrations? How urgent is it?
2. **Search the knowledge base** -- open the KB, try different keywords, read through articles to find the right one
3. **Decide what to do** -- should I reply with a fix? Ask the customer for more info? Escalate to engineering?
4. **Check escalation rules** -- if escalating, which team? What context do I need to include?
5. **Write a response** -- draft a reply that's accurate, cites the right KB article, and matches the right tone for the customer's mood
6. **Repeat** -- 30-50 times a day

Every step is manual cognitive work: reading, searching, reasoning, writing.

### Why this hurts

| Problem | Impact |
|---|---|
| **Slow** | Searching KB and writing responses from scratch takes time. Handle time is high |
| **Inconsistent** | Agent A escalates a ticket that Agent B would resolve. Different agents interpret KB differently |
| **Error-prone** | Agents miss relevant KB articles, apply wrong escalation rules, forget required context |
| **Knowledge is trapped** | Senior agents know which KB articles apply and when to escalate. New agents don't have this judgment |
| **Doesn't scale** | More tickets = more agents = linear cost growth |

### The core insight

The work agents do is **knowledge retrieval + judgment + writing** -- the exact combination where LLMs add value. The answers already exist (in KB articles, escalation rules, past tickets). The problem is finding and applying them consistently, every time, at speed.

---

## 2. What We're Building

An **AI copilot** that sits alongside the support agent and does the cognitive heavy-lifting before the agent acts.

### What the copilot does for every ticket

| Step | Copilot does | Agent used to do |
|---|---|---|
| **Classify** | Reads ticket, assigns category + priority | Mentally categorize |
| **Retrieve** | Finds most relevant KB article(s) with citations | Manually search KB |
| **Recommend action** | Suggests: Reply / Ask for more info / Escalate -- with reasoning | Mentally check escalation rules |
| **Draft response** | Writes grounded response citing KB, right tone | Write from scratch |
| **Show traceability** | Shows which KB used, what rule triggered, confidence level | Reasoning stays in agent's head |

### What the copilot does NOT do

- It does **not** auto-send responses. Human-in-the-loop only.
- It does **not** replace the agent. Agent reviews, edits, and decides.
- It does **not** handle cases outside the support domain.
- It does **not** make autonomous decisions with legal or financial consequences.

---

## 3. Why AI (Not Traditional Software)

This is worth understanding because it shapes every technical decision we make.

### Could we solve this without AI?

Partially. You could build:
- A decision tree for classification
- Keyword search for KB matching
- Response templates per category

But this breaks quickly because:

**Natural language is the input.** "OTP code not arriving", "MFA not working on my phone", and "can't log in, no SMS received" are the same issue. Keyword matching breaks on this variation. An LLM understands that these are semantically the same.

**The KB-to-ticket mapping is fuzzy.** KB-002 covers MFA issues. But does it apply when 3 users from the same tenant report it for 20 minutes? Yes, AND now it's also an escalation case (ER-005: route to Platform Ops). This **multi-factor reasoning** -- combining ticket content + KB articles + escalation rules + context -- is what LLMs handle well and rule engines handle poorly.

**Response generation isn't templatable.** A billing dispute response differs from an integration failure response. Tone shifts with customer sentiment (frustrated vs. calm). Required info changes per escalation rule (ER-003 needs invoice_id, billed amount, screenshots). Too many combinations for templates.

**The system improves with data.** As KB articles are added or tickets reveal new patterns, the copilot adapts without code changes. A rule-based system would need manual updates for every new edge case.

---

## 4. The Dataset We're Working With

Prasanna has shared a starter dataset (`ai_support_copilot_poc_dataset.xlsx`) with 5 sheets:

### Tickets_Historical (36 tickets)

These represent past resolved tickets. We use these for building and testing the pipeline.

| Field | Example | Purpose |
|---|---|---|
| `ticket_id` | TKT-1001 | Unique identifier |
| `subject` | "Imported 500 rows but only 420 visible" | What the customer reported |
| `description` | "Customer reports missing records after successful import job" | Full ticket text |
| `category` | Data Import | Ground truth classification |
| `priority` | Medium | Ground truth priority |
| `sentiment` | Frustrated | Customer tone |
| `channel` | Email / Chat / Portal | How it arrived |
| `source_kb_id` | KB-006 | Which KB article was actually used |
| `expected_next_best_action` | Escalate / Reply / Ask for more info | What the right action was |
| `resolution_summary` | "Escalated per KB-006 after unexplained skipped rows exceeded threshold" | How it was resolved |
| `target_sla_hours` | 48 | SLA target |

**Distribution:**
- 7 categories: Authentication, Billing, Data Import, Integrations, Access Control, Compliance, Known Issue
- 4 priority levels: Critical, High, Medium, Low
- 3 channels: Email, Chat, Portal
- 3 sentiments: Frustrated, Neutral, Calm
- 3 actions: Reply, Ask for more info, Escalate
- 8 customer companies
- 5 support agents

### KB_Articles (12 articles)

The knowledge base the copilot retrieves from.

| Field | Purpose |
|---|---|
| `kb_id` | Identifier (KB-001 through KB-012) |
| `title` | Article title |
| `category` | Authentication, Billing, Data Import, Integrations, Access Control, Compliance, Reporting, Known Issue |
| `content` | Full article text with resolution steps |
| `keywords` | Search keywords |
| `agent_note` | Internal guidance for agents (e.g., "Escalate only if admin panel action fails twice") |

The `agent_note` field is important -- it contains the kind of tacit knowledge that senior agents have and juniors don't. The copilot should use these notes in its reasoning.

### Escalation_Rules (5 rules)

Rules that determine when and how to escalate.

| Rule | Routes to | Triggers when |
|---|---|---|
| ER-001 | Engineering | No KB match + blocks workflow for multiple users |
| ER-002 | Integrations Engineering | Token reconnect succeeds but sync still fails, or webhook/SSL failure |
| ER-003 | Finance Operations | Duplicate charge, tax anomaly, enterprise pricing dispute |
| ER-004 | Compliance | PII export, legal hold, regulator, subpoena, data deletion request |
| ER-005 | Platform Operations | OTP/MFA delivery issue >15 min for multiple users |

Each rule specifies `minimum_context_required` -- the information the agent must include when escalating (e.g., tenant_id, screenshots, timestamps). The copilot should surface these requirements.

### Evaluation_Set (12 held-out cases)

**Do not use these for building or tuning the system.** These are the blind test cases.

Each case has:
- `ticket_text` -- the input
- `expected_category` -- ground truth classification
- `expected_priority` -- ground truth priority
- `expected_primary_kb` -- which KB article should be retrieved
- `expected_next_best_action` -- Reply / Ask for more info / Escalate
- `expected_reasoning_hint` -- why that action is correct

Covers all 8 categories and all 3 action types. Nishka will own evaluation execution against this set.

---

## 5. How the AI Pipeline Works

This is the technical flow. Every component is testable and measurable independently.

```
TICKET ARRIVES (text from Freshdesk or mock source)
       |
       v
+------------------+
|  1. CLASSIFY     |  LLM reads ticket text
|                  |  Outputs: category, priority, sentiment
+------------------+
       |
       v
+------------------+
|  2. RETRIEVE     |  Embed ticket text -> vector search against KB index
|                  |  Also: keyword/BM25 search (hybrid retrieval)
|                  |  Returns: top-K relevant KB articles with scores
+------------------+
       |
       v
+------------------+
|  3. REASON       |  LLM receives: ticket + retrieved KB articles + escalation rules
|                  |  Decides: Reply / Ask for more info / Escalate
|                  |  If escalate: which team + required context per rule
+------------------+
       |
       v
+------------------+
|  4. DRAFT        |  LLM generates response grounded in KB content
|                  |  Includes: citations, appropriate tone, required info
|                  |  Attaches: confidence score
+------------------+
       |
       v
+------------------+
|  5. PRESENT      |  Shows agent: draft response, sources, action,
|                  |  confidence, reasoning
|                  |  Agent: reviews, edits, sends (or overrides)
+------------------+
```

### What each team member touches

| Pipeline step | Primary owner | Also involved |
|---|---|---|
| **Data ingestion** (tickets + KB into the system) | **Nancy** | Amit (schema design) |
| **Embedding + indexing** (KB articles into vector store) | **Nancy** | Atharva (embedding model choice) |
| **Retrieval pipeline** (vector search + keyword search + merge) | **Atharva** | Nancy (index structure), Amit (architecture) |
| **Classification + reasoning + drafting** (LLM prompts) | **Atharva** | Amit (prompt design, model selection) |
| **Confidence gating** (when to show answer vs. disclaimer) | **Amit** | Atharva (implementation) |
| **Evaluation harness** (scoring pipeline outputs against golden set) | **Nishka** | Amit (metrics definition), Nancy (test data) |
| **Threat model + security review** | **Shubham** | Amit (architecture review) |
| **API/UI surface** (how agents interact with it) | **Atharva** | Amit (architecture) |

### Key technical decisions (to be made during/after Discovery)

These are the choices we'll need to make. Not yet decided -- depends on client answers:

| Decision | Options | Depends on |
|---|---|---|
| **LLM provider** | AWS Bedrock / OpenAI / GCP Vertex / Open-source | Client preference, cost, data residency |
| **Embedding model** | OpenAI ada / Gemini embedding / Cohere / open-source | Provider choice, cost, dimension size |
| **Vector store** | Elasticsearch / Pinecone / pgvector / Qdrant / ChromaDB | Scale needs, existing infra, operational complexity |
| **Retrieval approach** | Pure vector / Pure BM25 / Hybrid (vector + BM25) | KB size, query patterns. Hybrid is likely best |
| **Pipeline orchestration** | Single LLM call / Chained calls / Agent framework (LangChain, etc.) | Latency budget, complexity needs |
| **Deployment surface** | Standalone web app / Freshdesk sidebar app / API-only | Client preference, pilot scope |
| **Confidence gating** | Binary (confident/not) / Three-tier (confident/low-confidence/fallback) | Accuracy targets, UX expectations |

---

## 6. How We Measure Success

The eval set gives us 5 measurable dimensions per ticket:

| Dimension | What we measure | How |
|---|---|---|
| **Classification accuracy** | Did the copilot assign the right category and priority? | Exact match against `expected_category` and `expected_priority` |
| **Retrieval accuracy** | Did the copilot find the right KB article? | Check if `expected_primary_kb` is in the retrieved set |
| **Action accuracy** | Did the copilot recommend the right next action? | Exact match against `expected_next_best_action` |
| **Response quality** | Is the draft response accurate, grounded, and usable? | Human review: accept as-is / minor edit / rewrite needed |
| **Traceability** | Can we trace every output back to its sources? | Every response cites KB articles and shows reasoning |

We'll also measure:
- **Latency** -- time from ticket input to copilot output
- **Cost** -- LLM API cost per ticket
- **Confidence calibration** -- when the copilot says "high confidence," is it actually right?

---

## 7. Phase 1 Scope Boundaries

| In scope | Out of scope |
|---|---|
| One support queue | Multiple queues or multi-tenant |
| One knowledge source (12 KB articles) | Multiple knowledge sources |
| One escalation mechanism | Complex routing across teams |
| Human-in-the-loop only | Auto-send or autonomous resolution |
| Mock/sandbox integrations | Production Freshdesk integration |
| English only | Multi-language |
| Agent-facing copilot | Customer-facing bot |
| Classification + retrieval + drafting + action recommendation | Ticket auto-creation or workflow automation |

---

## 8. What Each Role Should Be Thinking About

### Atharva (AI Engineer)
- How to structure the LLM prompts for classification, reasoning, and drafting
- Retrieval pipeline design: embedding choice, search strategy, reranking
- Model abstraction: build a provider-agnostic LLM gateway so we can switch models without code changes (per Doc 08)
- Streaming vs. batch response generation
- How to pass escalation rules to the LLM context efficiently

### Nancy (Data Engineer)
- Ingestion pipeline: how do tickets and KB articles get into our system?
- Chunking strategy for KB articles (these are short -- probably single-chunk per article, but verify)
- Embedding generation and index management
- Data quality: are there KB articles with missing content? Tickets with ambiguous categories?
- Schema design for the ticket and KB stores
- Freshness: how will updated KB articles be re-indexed?

### Nishka (QA)
- Eval harness: a script/tool that runs the 12 eval cases through the pipeline and scores each dimension
- Golden set expansion: 12 cases may not be enough. Plan to add edge cases discovered during testing
- Adversarial cases: what happens with prompt injection? Out-of-scope tickets? Tickets in languages other than English?
- Regression testing: if we change the prompt or model, do scores go up or down?
- End-to-end smoke tests: does the full pipeline return a valid response for every ticket type?

### Shubham (Governance Engineer)
- Threat model: prompt injection (user crafts ticket text to manipulate the LLM), PII leakage (ticket contains customer data that ends up in the response), output exfiltration
- Data classification: what sensitivity level is ticket data? KB data?
- Responsible AI: the copilot must always disclose it's AI-generated. What disclaimers are needed?
- Secrets management: LLM API keys, database credentials -- none in code
- Pre-release security review checklist

---

## 9. Questions Still Open

These will be answered in the Discovery call with Prasanna today:

- Freshdesk access: real instance or mock?
- LLM provider preference
- Deployment surface (web app vs. Freshdesk sidebar vs. API)
- PII handling requirements
- Success criteria thresholds
- Cost and latency constraints
- Phase 2 vision

We'll update this document after Discovery with confirmed answers.

---

*This document will be updated as decisions are made. Refer to `01_Discovery_Call_Questions.md` for the full question list and answers from the Discovery call.*
