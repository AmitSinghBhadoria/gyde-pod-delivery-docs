# CLAUDE.md -- AI Support Copilot POD Engagement Context

> This file provides full context for Claude Code sessions working on this project.

## Project Overview

Gyde is an AI consultancy pivoting to offer **AI POD services** -- small cross-functional teams that build production AI systems for enterprise clients. The company has created a 21-document framework (the "Gyde POD Operation Framework") that governs how every POD operates.

This repo is the **documentation hub** for a simulation engagement where:
- The CEO (Prasanna) plays a realistic enterprise client
- A team of 6 runs the POD framework for real
- The goal is to build a working product AND validate the framework in 4 weeks

## The Product: AI Support Copilot

### Problem
Support agents manually classify tickets, search knowledge bases, decide on actions (reply/escalate/ask for info), and write responses from scratch -- 30-50 times a day. This is slow, inconsistent, error-prone, and knowledge stays trapped in senior agents' heads.

### Solution
An AI copilot that sits alongside agents and for every incoming ticket:
1. **Classifies** -- assigns category (Authentication, Billing, etc.) and priority
2. **Retrieves** -- finds relevant KB articles via hybrid search (vector + BM25)
3. **Reasons** -- recommends action (Reply / Ask for more info / Escalate) using escalation rules
4. **Drafts** -- generates a grounded response with KB citations
5. **Presents** -- shows the agent: draft, sources, action, confidence, reasoning

Human-in-the-loop only. The copilot suggests, the agent decides.

### Phase 1 Scope
- One support queue
- One knowledge source (12 KB articles)
- One escalation mechanism (5 rules)
- Mock/sandbox integrations acceptable
- English only
- Agent-facing only (not customer-facing)

### Dataset
Located at: `../Gyde AI POD Framework/Simulation Docs/ai_support_copilot_poc_dataset.xlsx`

| Sheet | Records | Purpose |
|---|---|---|
| Tickets_Historical | 36 | Past resolved tickets for building/testing. 7 categories, 4 priorities, 3 channels, 3 sentiments |
| KB_Articles | 12 | Knowledge base articles with content, keywords, agent notes |
| Escalation_Rules | 5 | Rules mapping conditions to teams (Engineering, Integrations, Finance, Compliance, Platform Ops) |
| Evaluation_Set | 12 | **Held-out blind test set** -- do NOT use for building or tuning |

Categories: Authentication, Billing, Data Import, Integrations, Access Control, Compliance, Known Issue
Actions: Reply, Ask for more info, Escalate
Channels: Email, Chat, Portal

## Team Composition

| Role | Person | Primary Responsibilities |
|---|---|---|
| **POD Lead** | Amit | Architecture, agent design, model selection, eval strategy, code review final say on AI components, technical demos |
| **AI Engineer** | Atharva | Prompts, chains, retrieval pipeline, model integration, LLM gateway, agent tooling |
| **Data Engineer** | Nancy | Ingestion pipelines, chunking, embeddings, vector store, data quality, lineage |
| **QA** | Nishka | Test strategy, golden set curation, eval harness, adversarial testing, UAT |
| **Governance Engineer** | Shubham | Threat model, security, responsible AI, compliance, pre-release sign-off. Also 2nd-level escalation SPOC |
| **Implementation Manager** | Shivani | POD charter, delivery, client comms, sprint cadence, scope, risk register, milestone tracking |

**Client side**: Prasanna (CEO playing CIO + Business Lead + Product Owner)

## Framework Essentials

The full framework is at: `../Gyde AI POD Framework/` (21 PDFs across 7 modules)

### 8 Guiding Principles
1. Production from day one
2. Evaluation precedes optimization
3. Security is a feature, not a phase
4. Data is a first-class deliverable
5. Small, reversible changes
6. Observable by default
7. Human-in-the-loop where it matters
8. Transparency with the client

### 5 Non-Negotiables (never tailored away)
1. Threat modeling and secrets management
2. Evaluation before production
3. Versioned data and prompts
4. Audit trail for AI decisions
5. Incident response readiness

### RACI Summary (who does what)
- **POD Lead (Amit)**: Accountable for architecture, agent/chain implementation, prompt/eval creation, code review, pre-release quality gate
- **AI Engineer (Atharva)**: Responsible for implementation under POD Lead's direction
- **Data Engineer (Nancy)**: Accountable for data pipelines, vector store, data quality
- **QA (Nishka)**: Responsible for test strategy and eval harness execution
- **Governance (Shubham)**: Accountable for security review, compliance gate
- **PM (Shivani)**: Accountable for charter, delivery, client comms, risk register

### Milestone Shape (from Doc 03)
| # | Milestone | What it means |
|---|---|---|
| M0 | Charter & Eval Plan signed | Signed charter, eval plan, environments provisioned |
| M1 | Walking skeleton | End-to-end thin slice: one input, one retrieval, one output |
| M2 | Eval harness operational | Golden set committed, automated scoring, baseline metrics |
| M3 | MVP feature-complete | All MVP scope built, eval gates passing, security reviewed |
| M4 | Production deployment | Live in production, on-call active, runbooks ready |
| M5 | Stable operation | Two weeks stable against quality/reliability targets |
| M6 | Engagement close | Knowledge transfer complete, framework feedback delivered |

### Communication Cadence (from Doc 05)
- **Daily**: Standup notes in shared channel (15 min, async OK)
- **Weekly**: Written status update from PM (one page, RAG status, risks, decisions needed)
- **Per sprint**: Live demo (30 min, working software only) + sprint output pack
- **Decision log**: Any decision above POD-internal level recorded within 24 hours

### Effort Buckets (from Doc 03)
| Bucket | Typical share |
|---|---|
| Data work | 20-40% |
| AI engineering | 20-35% |
| Application engineering | 15-25% |
| Governance & security | 10-15% |
| Quality, ops, & release | 10-15% |

## Current Status

**Phase**: Discovery
**Discovery call**: Scheduled with Prasanna
**Key decisions pending**: LLM provider, deployment surface, vector store, success criteria thresholds

## Repo Structure

This is a Docusaurus docs site. Key paths:

```
docs/                           # All documentation (markdown with frontmatter)
├── index.md                    # Landing page
├── discovery/                  # Discovery phase artifacts
├── team/                       # Team reference docs
└── engagement/                 # Engagement artifacts (charter, arch, eval, sprint plan)
docusaurus.config.ts            # Site config (GitHub Pages deployment)
sidebars.ts                     # Sidebar navigation (auto-generated from folder structure)
.github/workflows/deploy.yml   # Auto-deploy to GitHub Pages on push to main
```

## Docs in Simulation Docs folder

The original working docs are also at: `../Gyde AI POD Framework/Simulation Docs/`

| File | Content |
|---|---|
| `ai_support_copilot_poc_dataset.xlsx` | Prasanna's starter dataset |
| `01_Discovery_Call_Questions.md` | Technical questions for Discovery call |
| `02_Discovery_Call_Invite_Email.md` | Email template for Shivani to send |
| `03_Product_Overview_and_Technical_Primer.md` | Full product + technical briefing for the team |
| `04_Shivani_Discovery_Call_Questions.md` | PM-specific questions for Discovery call |

## Technical Decisions (Pending Discovery)

These need to be decided after the Discovery call with Prasanna:

| Decision | Options being considered |
|---|---|
| LLM provider | AWS Bedrock / OpenAI / GCP Vertex AI / Open-source |
| Embedding model | OpenAI ada / Gemini embedding / Cohere / open-source |
| Vector store | Elasticsearch / Pinecone / pgvector / Qdrant / ChromaDB |
| Retrieval approach | Pure vector / Pure BM25 / Hybrid (likely hybrid) |
| Pipeline orchestration | Single LLM call / Chained calls / Agent framework |
| Deployment surface | Standalone web app / Freshdesk sidebar / API-first |
| Confidence gating | Binary / Three-tier (confident / low-confidence / fallback) |

## AI Pipeline Architecture (Proposed)

```
Ticket arrives
    → Classify (LLM: category + priority + sentiment)
    → Retrieve (embed ticket → hybrid search KB index)
    → Reason (LLM: ticket + KB articles + escalation rules → action recommendation)
    → Draft (LLM: generate grounded response with citations)
    → Present to agent (with confidence, sources, action, reasoning)
    → Agent reviews, edits, sends (or overrides)
```

## Evaluation Dimensions

| Dimension | How measured |
|---|---|
| Classification accuracy | Exact match on category and priority |
| Retrieval accuracy | Expected KB article in retrieved set |
| Action accuracy | Exact match on next-best-action |
| Response quality | Human review: accept as-is / minor edit / rewrite |
| Traceability | Every response cites KB sources and shows reasoning |
| Latency | Time from input to copilot output |
| Cost | LLM API cost per ticket |

## Key Anti-Patterns to Avoid (from framework)

- **Hero engineer**: Don't let one person be the only one who understands a component
- **Demoware drift**: Only demo what works in the real environment, fully evaluated
- **Governance as final gate**: Shubham is involved from Sprint 0, not pulled in at the end
- **Silent handoffs**: Use decision log and explicit handover notes
- **PM as messenger**: Shivani owns scope, risk, and decisions -- not just passing notes

## Working Conventions

- All substantial outputs saved as `.md` files in `docs/` and committed
- Documents numbered sequentially within each section
- Every doc gets Docusaurus frontmatter (sidebar_position, title)
- Commit and push after creating/updating docs -- site auto-deploys
- Framework PDFs are reference-only, stored separately (not in this repo)

## Commands

```bash
# Local dev
npm start

# Build
npm run build

# The site deploys automatically on push to main via GitHub Actions
```
